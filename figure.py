from dataclasses import dataclass
from PIL import Image
from constants import ScreenConstants
import pygame
from pathlib import Path
from typing import List, Tuple
import json
from euclid import Point2, Line2, LineSegment2



@dataclass
class Handles:
    lines: List[Line2]
    
    @classmethod
    def from_json(cls, json_location: Path, scaled=1.0):
        lines = []
        def to_line(x1y1, x2y2):
            a = Point2(scaled*x1y1[0], scaled*x1y1[1])
            b = Point2(scaled*x2y2[0], scaled*x2y2[1])
            return Line2(a,b)
        with open(json_location) as f:
            config = json.load(f)
            for shape in config["shapes"]:
            
                lines.append(to_line(*shape["points"]))

        return cls(lines=lines)
    

class Figure:
    def __init__(self, name: Path):
        self.image = Image.open(name).convert("RGBA")
        self.x = 0
        self.y = 0
        self.name = name.root
        self.layer = 0
        self.w, self.h = self.image.size
        self.scaled_w = int(self.w * ScreenConstants.SCALE)
        self.scaled_h = int(self.h * ScreenConstants.SCALE)
        self.scaled_image = self.image.resize(size=(self.scaled_w, self.scaled_h))
        self.scaled_sprite = pygame.image.frombytes(self.scaled_image.tobytes(), 
                                                    size=self.scaled_image.size, 
                                                    format="RGBA")
                                                    
        if self.scaled_h > ScreenConstants.THUMBNAIL_H:
            thumbnail_scale = self.scaled_h / ScreenConstants.THUMBNAIL_H
        else:
            raise AttributeError("Image is smaller than Thumbnail height")

        self.thumbnail_w = int(self.scaled_w / thumbnail_scale)
        self.thumbnail_h = ScreenConstants.THUMBNAIL_H
        self.thumbnail = self.image.resize(size=(self.thumbnail_w, self.thumbnail_h))
        self.thumbnail_sprite = pygame.image.frombytes(self.thumbnail.tobytes(), 
                                                    size=self.thumbnail.size, 
                                                    format="RGBA")
        self.z = 0
        self.in_ui = True
        self.is_grabbed = False

    def set_pos(self, pos_x: int, pos_y: int, centered=False):
        if centered:
            if self.in_ui:
                self.x = pos_x - self.thumbnail_w//2
                self.y = pos_y - self.thumbnail_h//2
            else:
                self.x = pos_x - self.scaled_w//2
                self.y = pos_y - self.scaled_h//2
        else:
            self.x = pos_x
            self.y = pos_y


    def can_grab(self, mouse_x, mouse_y):
        if self.in_ui:
            off_x, off_y = self.thumbnail_w, self.thumbnail_h
        else:
            off_x, off_y = self.scaled_w, self.scaled_h
        rule1 = (mouse_x > self.x) and (mouse_x < self.x + off_x)
        rule2 = (mouse_y > self.y) and (mouse_y < self.y + off_y)
        return rule1 and rule2

    def try_grab(self, mouse_x: int, mouse_y: int, layer=0) -> bool:
        if self.can_grab(mouse_x, mouse_y):
            if self.is_grabbed:
                self.x = mouse_x
                self.y = mouse_y
                self.layer = layer
            else:
                self.x = mouse_x
                self.y = mouse_y
                self.is_grabbed = True
                self.layer = layer
            return True
        return False

    def try_release(self, mouse_x, mouse_y, objects):
        if self.is_grabbed:
            # release back to UI
            if mouse_x > ScreenConstants.WIDTH-ScreenConstants.WIDTH//7:
                self.set_pos(
                    ScreenConstants.WIDTH-ScreenConstants.WIDTH//7,
                    ScreenConstants.THUMBNAIL_H*(len(objects) + 1)
                )
                self.in_ui = True
            # release to the screen
            else:
                self.set_pos(mouse_x, mouse_y, centered=True)
                self.in_ui = False
            self.is_grabbed = False
            return True
        return False

    def draw(self, context: pygame.Surface):
        if self.in_ui:
            context.blit(self.thumbnail_sprite, (self.x, self.y))
        else:
            context.blit(self.scaled_sprite, (self.x, self.y))
        
