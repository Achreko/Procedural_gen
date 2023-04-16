from PIL import Image
import numpy as np
from land_enum import Land

def save_img(array: np.ndarray, name: str, md: str) -> None:
    img = Image.fromarray(array, md)
    img.save(f'results/{name}.png')


def biome(e: float, m: float, t: float) -> tuple:
    if e > 1.0:
        e = 1.0
    if e<0.15: return (0,0,204+int(255 * e))
    if e<0.2: return Land.BEACH.value

    if e > 0.7:
      if m < 0.4 or t < 0.3: return Land.SNOW.value
      if m < 0.8 or t < 0.7: return Land.TUNDRA.value
      return Land.MOUNTAIN.value

    if e > 0.5:
      if m < 0.45: return Land.SHRUBLAND.value
      return Land.TAIGA.value

    if e <= 0.5:
      if m < 0.1 or t > 0.8: return Land.DESERT.value
      if m < 0.5 : return Land.GRASSLAND.value
      if m < 0.7: return Land.DECIDUOUS_FOREST.value
      return Land.RAIN_FOREST.value

    if m < 0.1: return Land.DESERT.value
    if m < 0.4: return Land.GRASSLAND.value
    return Land.VERDANT_RAIN_FOREST.value