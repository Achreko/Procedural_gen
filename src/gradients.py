import numpy as np
from PIL import Image, ImageDraw
import math
import random

def circular_gradient(shape: tuple, radius: int, cntr: float) -> np.ndarray:
    img = Image.new("L", shape)
    pix = img.load()
    center_x = shape[1]//cntr
    center_y = shape[0]//cntr
    for y in range(shape[0]):
        for x in range(shape[1]):
            dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            if dist < radius:
                ratio = dist / radius
                pix[y,x] = int(255 - 255*ratio)
    grad = np.array(img, dtype=np.uint8)
    return grad


def ridge_noise(noise: float) -> float:
    return 2 * (0.5 - abs(0.5-noise))


class Point:
    def __init__(self,x: int, y: int):
        self.x = x
        self.y = y

class Vector:
    def __init__(self, x: float,y: float):
        self.x = x
        self.y = y

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def normalized(self):
        length = self.length()
        if length == 0:
            return Vector(0.03, 0.03)
        return Vector(self.x / length, self.y / length)

    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def scale(self, f: float):
        return Vector(f * self.x, f * self.y)
    
class Path:
    def __init__(self, st):
        self.points = [st]
        self.finished = False

    def smooth(self):
        for i in range(1, len(self.points)):
            start = self.points[i-1]
            end = self.points[i]
        
            self.points[i].x = (start.x + end.x) // 2
            self.points[i].y = (start.y + end.y) // 2

    def flow_direction(self):
        size = len(self.points)
        if size < 2:
            return None
        start = self.points[size -2]
        end = self.points[size -1]
        return Vector(end.x - start.x, end.y - start.y).normalized()


def should_branch(gradient, height: float) -> bool:
    return gradient.length() < 0.013 and height < 0.4

def is_in_water(elev) -> bool:
    return elev < 0.15

def wiggle_vector(vector, strength: float) :
    return Vector(
        vector.x + random.uniform(-strength, strength),
        vector.y + random.uniform(-strength, strength)
    )

def follow_gradient(point, gradient):
    return Point(
        int(round(point.x + gradient.x)),
        int(round(point.y + gradient.y))
    )
 
def gradient_at(e_map: np.ndarray, point):
    return Vector(
    -height_at(e_map, Point(point.x+1, point.y)) + height_at(e_map, Point(point.x-1, point.y)),
    -height_at(e_map, Point(point.x, point.y +1)) + height_at(e_map, Point(point.x, point.y - 1))
    )

def height_at(e_map, point):
    shp = e_map.shape
    x = max(min(point.x, shp[0]),0)
    y = max(min(point.y, shp[1]),0)

    return e_map[x][y]/255


def gradient_descent(e_map: np.ndarray):
    shp = e_map.shape
    divergeFromRiverFlow = 0.3
    
    point = Point(
        random.randint(shp[0] //2 - shp[0] //10, shp[0] //2 + shp[0] //10),
         random.randint(shp[1] //2 - shp[1] //10, shp[1] //2 + shp[1] //10)
         )
    while height_at(e_map, point) < 0.7:
        point = Point(
        random.randint(shp[0] //2 - shp[0] //10, shp[0] //2 + shp[0] //10),
         random.randint(shp[1] //2 - shp[1] //10, shp[1] //2 + shp[1] //10)
         )
    paths = [Path(point)]

    for i in range(180):
        height = height_at(e_map, point)
        
        for path in filter(lambda xd: not xd.finished, paths):
                gradient = gradient_at(e_map, point)

                gradient = wiggle_vector(gradient, (1 / (gradient.length() + 0.1)) * 0.004)
                flow_direction = path.flow_direction()

                if flow_direction is not None:
                    combined_gradient_and_flow = gradient.normalized() \
                    .scale(divergeFromRiverFlow) \
                    .add(flow_direction.scale(1 - divergeFromRiverFlow)) \
                    .normalized().scale(gradient.length())

                    gradient = combined_gradient_and_flow

                next_point = follow_gradient(point, gradient.normalized().scale(80*gradient.length() + 0.1))

                point = next_point
                print(point.x, point.y)
                path.points.append(point)

                if len(paths) < 10 and should_branch(gradient, height):
                    path.finished = True

                    paths.append(Path(point))
                    paths.append(Path(point))
                elif is_in_water(height_at(e_map, point)):
                    path.finished = True
                    break

    img = Image.open("results/landmap.png")
    draw = ImageDraw.Draw(img)           

    for path in paths:
        draw.line([tuple([pt.x, pt.y]) for pt in path.points], fill=(0,0,240))
    
    img.save("results/lmap_rivers.png")
