import random
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt


def river_generation(river_number: int, map: np.ndarray, point_number: int) -> np.ndarray:
    shp = map.shape
    points = [[random.randrange(shp[0]) - random.randrange(shp[0]), random.randrange(shp[0]) - random.randrange(shp[0])]
     for xd in range(point_number)]
    vor = Voronoi(points)
    fig = voronoi_plot_2d(vor)
    plt.show()
    return map