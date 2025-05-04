from glob import glob
from figure import Figure, Handles
from pathlib import Path
from euclid import Point2, Line2
from constants import ScreenConstants, EPS, N_STEPS
import math
import random
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
    

    def probe_layer(self, x, y):
        for figure in sorted(self.figures, key=lambda x: x.layer, reverse=True):
            if figure.can_grab(x, y):
                return figure.layer
        return 0

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
        self.kmeans()


    def kmeans(self, external_points=None):
        if external_points:
            points=external_points
        points = []
        for _,v in self.intersections.items():
            for p in v:
                points.append(p[0])
        N = len(points)
        # points_oz = np.log(points[points>0])
        # points_sz = np.log(-1*points[points<0])
        # points_log = np.concatenate([points_oz, points_sz])
        a,b = random.choices(points, k=2)
        cluster_ids = [0 for _ in range(N)]
        points_in_a = []
        points_in_b = []
        for _ in range(10):
            points_in_a = []
            points_in_b = []
            for i in range(N):
                dist_a = math.sqrt((points[i]-a)**2)
                dist_b = math.sqrt((points[i]-b)**2)
                if dist_a < dist_b:
                    cluster_ids[i] = 0
                    points_in_a.append(points[i])
                else:
                    cluster_ids[i] = 1
                    points_in_b.append(points[i])
            if points_in_a:
                a = sum(points_in_a)/len(points_in_a)
            else:
                a = random.choice(points)

            if points_in_b:
                b = sum(points_in_b)/len(points_in_b)
            else:
                b = random.choice(points)

        a_std = 0
        b_std = 0
        for p_a in points_in_a:
            a_std += (p_a - a)**2
        for p_b in points_in_b:
            b_std += (p_b - b)**2
        if a_std:
            a_std /= len(points_in_a)
        if b_std:
            b_std /= len(points_in_b)

        print(a_std, b_std)
        self.clusters = [0 if cluster_ids[i] else 1 for i in range(N)]



