import numpy as np

def circular_gradient(shape: tuple, radius: int) -> np.ndarray:
    grad = np.zeros(shape = shape)
    center_x = shape[1]//2
    center_y = shape[0]//2
    for y in range(shape[0]):
        for x in range(shape[1]):
            dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            if dist < radius:
                ratio = dist / radius
                grad[y,x] = int(255 - 255*ratio)
    return grad
    