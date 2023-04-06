from PIL import Image
import numpy as np

def save_img(array: np.ndarray, name: str, md: str) -> None:
    img = Image.fromarray(array, md)
    img.save(f'results/{name}.png')