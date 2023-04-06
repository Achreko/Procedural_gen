import random
import numpy as np
from scipy.spatial import Voronoi
from PIL import Image, ImageDraw

def river_generation(river_number: int, map: np.ndarray, shp: tuple, point_number: int) -> np.ndarray:
    points = [[random.randrange(shp[0]), random.randrange(shp[0])]
     for xd in range(point_number)]
    points.append((-shp[0]*3, -shp[1]*3))
    points.append((-shp[0]*3, shp[1]*4))
    points.append((shp[0]*4, -shp[1]*3))
    points.append((shp[0]*4, shp[1]*4))
    
    img = Image.new("L", shp, color=255)
    draw = ImageDraw.Draw(img)
    vor = Voronoi(points)
    vor_vertices = vor.vertices
    for region in vor.regions[1:]:
        if -1 not in region:
            polygon = [tuple(vor_vertices[p]) for p in region]
            draw.polygon(polygon, outline='black')
    img.save("results/vor.png")
    return map