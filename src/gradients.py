import numpy as np
from PIL import Image

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
    