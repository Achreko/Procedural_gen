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
    
    img = Image.fromarray(map, "RGB")
    draw = ImageDraw.Draw(img)
    vor = Voronoi(points)
    vor_vertices = vor.vertices
    for region in vor.regions[1:100]:
        if -1 not in region:
            polygon = [tuple(vor_vertices[p]) for p in region]
            draw.polygon(polygon, outline='black')

    # for i in range(river_number):
    #     strt = vor_vertices[random.randint(0, len(vor_vertices))]
    #     ending = vor_vertices[random.randint(0, len(vor_vertices))]
    #     while (strt[0] * strt[1]) < 0:
    #         strt = vor_vertices[random.randint(0, len(vor_vertices))]
    #     while (ending[0] * ending[1]) < 0:
    #         ending = vor_vertices[random.randint(0, len(vor_vertices))]
    #     draw.line([strt[0]//1, strt[1]//1, ending[0]//1, ending[1]//1],
    #     fill="blue",width=3)


    img.save("results/vor.png")
    return map