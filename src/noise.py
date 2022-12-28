from opensimplex import OpenSimplex
import numpy as np
from PIL import Image
from math import pow
import random
from land_enum import Land

def generate():
    noise_gen_height = OpenSimplex(seed=random.randint(0,10**6))
    noise_gen_moist = OpenSimplex(seed=random.randint(-100000,0))

    width = 256
    height = 256
    heights = np.empty((width,height))

    for x in range(width):
        for y in range(height):
            nx = x/width - 0.5
            ny = y/height - 0.5
            e1,e2,e3,e4,e5,e6 = 1, 0.5, 0.25, 0.12, 0.06, 0.03
            exp = 1
            elev =  e1 * noise_gen_height.noise2(1*nx,1*ny) /2.0 + 0.5 + \
                    e2 * noise_gen_height.noise2(2*nx,2*ny) /2.0 + 0.5+ \
                    e3 * noise_gen_height.noise2(4*nx,4*ny) /2.0 + 0.5+ \
                    e4 * noise_gen_height.noise2(8*nx,8*ny) /2.0 + 0.5+ \
                    e5 * noise_gen_height.noise2(16*nx,16*ny) /2.0 + 0.5+ \
                    e6 * noise_gen_height.noise2(32*nx,32*ny)/2.0 + 0.5
            elev = elev/sum((e1,e2,e3,e4,e5,e6))

            m1,m2,m3,m4,m5,m6 = 1, 0.5, 0.25, 0.12, 0.06, 0.03
            moist = m1 * noise_gen_moist.noise2(1*nx,1*ny) /2.0 + 0.5+ \
                    m2 * noise_gen_moist.noise2(2*nx,2*ny) /2.0 + 0.5+ \
                    m3 * noise_gen_moist.noise2(4*nx,4*ny) /2.0 + 0.5+ \
                    m4 * noise_gen_moist.noise2(8*nx,8*ny) /2.0 + 0.5+ \
                    m5 * noise_gen_moist.noise2(16*nx,16*ny) /2.0 + 0.5+ \
                    m6 * noise_gen_moist.noise2(32*nx,32*ny)/2.0 + 0.5
            heights[y][x] = biome(pow(elev,exp), moist)

    # Create an image from the heightmap array using the PIL library
    img = Image.fromarray(heights, 'I')

    img.save(f'results/heightmap{noise_gen_height.noise2(1/e1*nx,1/e1*ny)}.png')


def biome(e,m):
    if e<0.1: return Land.OCEAN.value
    if e<0.14: return Land.BEACH.value

    if e >0.8:
      if m< 0.1: return Land.SCORCHED.value
      if m< 0.2: return Land.TUNDRA.value
      return Land.SNOW.value

    if e > 0.7:
      if m < 0.45: return Land.SHRUBLAND.value
      return Land.TAIGA.value

    if e> 0.3:
      if m < 0.1: return Land.DESERT.value
      if m <0.5 : return Land.GRASSLAND.value
      if m < 0.7: return Land.DECIDUOUS_FOREST.value
      return Land.RAIN_FOREST.value

    if m < 0.1: return Land.DESERT.value
    if m < 0.4: return Land.GRASSLAND.value
    return Land.VERDANT_RAIN_FOREST.value

if __name__ == "__main__":
    generate()