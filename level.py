import json
from glob import glob
from figure import Figure, Handles
from pathlib import Path
from utils import Linspace
from euclid import Point2, Line2
from constants import ScreenConstants, EPS, N_STEPS
import math
from copy import copy
from pygame import Surface

class Level:
    def __init__(self, n_level):
        self.dir = dir
        self.lines = [Handles.from_json(Path(path), scaled=ScreenConstants.SCALE) for path in sorted(glob(f"assets/level{n_level}/box*.json"))]
        self.figures = [Figure(Path(path)) for path in sorted(glob(f"assets/level{n_level}/box*.png"))]
        self.intersections = {}

    def try_grab(self, x, y, layer):
        for figure in self.figures:
            if figure.try_grab(x,y, layer):
                break

    def try_release(self, x, y):
        for figure in self.figures:
            figure.try_release(x, y, self.figures)
            self.intersections[figure.name] = []

    def update(self, x, y):
        for i, figure in enumerate(self.figures):
            if figure.is_grabbed:
                figure.set_pos(x, y, centered=True)
            elif figure.in_ui:
                figure.set_pos(
                        ScreenConstants.WIDTH - ScreenConstants.WIDTH//7, 
                        i*ScreenConstants.THUMBNAIL_H*2
                )
    def draw(self, surface: Surface):
        for figure in sorted(self.figures, key=lambda x: x.layer):
            figure.draw(surface)

    def check_perspective(self):
        horizon_left = Point2(0, ScreenConstants.HEIGHT//2)
        horizon_right = Point2(ScreenConstants.WIDTH, ScreenConstants.HEIGHT//2)
        horizon = Line2(horizon_left, horizon_right)
        for figure,handle in zip(self.figures, self.lines):
            if figure.in_ui:
                continue
            for line in handle.lines:
                new_line = copy(line)
                
                new_line.p = new_line.p + Point2(figure.x, figure.y)
                intersection = new_line.intersect(horizon)
                print(intersection, figure.x, figure.y)
                if intersection:
                    if figure.name not in self.intersections.keys():
                        self.intersections[figure.name] = [intersection]
                    else:
                        self.intersections[figure.name].append(intersection)


            


        


        
        

