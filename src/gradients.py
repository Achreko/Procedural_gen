import numpy as np
import math

def circular_gradient(shape: tuple) -> np.ndarray:
    grad = np.zeros(shape)
    center_x = shape[1]//2
    center_y = shape[0]//2
    mx = center_x + center_y
    for y in range(shape[0]):
        for x in range(shape[1]):
            distx = abs(x - center_x)
            disty = abs(y - center_y)
            dist = math.sqrt(distx*distx + disty*disty)
            grad[y][x] = dist/mx
            print(grad[y][x])
    # for y in range(array.shape[0]):
    #     for x in range(array.shape[1]):
    #         if grad[y][x] >0:
    #             grad[y][x] *=20
    # max_grad = np.max(grad)
    # grad = grad / max_grad
    return grad
    