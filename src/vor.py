import random
import numpy as np
from scipy.spatial import Voronoi, Delaunay
from PIL import Image, ImageDraw
from image_functions import biome
from vorigon import Vorigon
from deriangle import Deriangle

def voron_gen( e_mp: np.ndarray, m_mp: np.ndarray, t_mp: np.ndarray, point_number: int) -> None:
    shp = e_mp.shape
    points = [[random.randrange(shp[0]), random.randrange(shp[0])]
     for xd in range(point_number)]
    points.append((-shp[0]*3, -shp[1]*3))
    points.append((-shp[0]*3, shp[1]*4))
    points.append((shp[0]*4, -shp[1]*3))
    points.append((shp[0]*4, shp[1]*4))
    
    vorigons, deriangles = [], []

    img = Image.new("RGB", shp, color=(0,0,220))
    draw = ImageDraw.Draw(img)
    vor = Voronoi(points)

    for i, region in enumerate(vor.regions, start=1):
        if -1 not in region:
            polygon = [tuple(vor.vertices[p]) for p in region]
            coordinates = []
            

            for el in polygon:
                if el[0] > 0 and el[1] > 0 and el[0] < shp[0] and el[1] < shp[1]:
                    coordinates.append(tuple([int(el[0]),int(el[1])]))
            if len(coordinates) >=3:
                st_x = min(coordinates[0][0],coordinates[-1][0])
                st_y= min(coordinates[0][1], coordinates[-1][1])
                fn_x = max(coordinates[0][0],coordinates[-1][0])
                fn_y= max(coordinates[0][1], coordinates[-1][1])
                if st_x == fn_x:
                    fn_x += 1
                if st_y == fn_y:
                    fn_y += 1
                elev = find_most_freq(e_mp[st_x:fn_x,st_y:fn_y])
                fl = biome(elev,
                 find_most_freq(m_mp[st_x:fn_x,st_y:fn_y]),
                 find_most_freq(t_mp[st_x:fn_x,st_y:fn_y]))
                
                
                center = np.where(vor.point_region == i)[0]
                if len(center) != 0:
                    for ind in center:
                        pnt = points[int(ind)]
                        if abs(pnt[0]) <= shp[0] and abs(pnt[1]) <= shp[1]:
                            vorigons.append(Vorigon(i, tuple(points[int(ind)]), polygon, elev))
                            draw.polygon(coordinates, fill=fl, outline="black")
            
    delan = Delaunay(points)
    delan_simp = delan.simplices

    
    for i, simp in enumerate(delan_simp):
        if not any(cord < 0 for cord in simp):
            deriangles.append(Deriangle(i, simp, delan.neighbors[i]))
    # for simp in delan_simp:
    #     if not any(cord < 0 for cord in simp):
    #         p1, p2, p3 = points[simp[0]],points[simp[1]], points[simp[2]]
    #         polygon = [tuple(p1),tuple(p2),tuple(p3)]
    #         draw.polygon(polygon, outline="red")


    vorigons.sort(reverse=True, key= lambda xd: xd.height)


    img.save("results/vor.png")



def find_most_freq(ar: np.ndarray) -> float:
    return (np.amax(ar) + np.amin(ar))/255



# def midpoint_displacement(cord: list, roughness: float) -> list:
#     new_points = [cord[0]]
#     for i in range(len(cord) - 1):
#         x1, y1 = cord[i]
#         x2, y2 = cord[i + 1]
#         mx = (x1 + x2) // 2
#         my = (y1 + y2) // 2
#         displacement = (random.random() - 0.5) * roughness * (x2 - x1 + y2 - y1)
#         height = int((y1 + y2) / 2 + displacement)
#         new_points.append((mx, height))
#     if len(new_points) > 2:
#         roughness /= 2
#         left_points = midpoint_displacement(new_points[:len(new_points) // 2 + 1], roughness)
#         right_points = midpoint_displacement(new_points[len(new_points) // 2:], roughness)
#         new_points = left_points[:-1] + right_points
#     return new_points