from PIL import Image
from numpy import ndarray

def save_img(array: ndarray, name: str, md: str) -> None:
    img = Image.fromarray(array, md)
    img.save(f'results/{name}.png')