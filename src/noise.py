from opensimplex import OpenSimplex
import numpy as np
from math import pow
import random
from land_enum import Land
from image_functions import save_img


def generate():
    seed_h = random.randint(0,10**6)
    seed_m = random.randint(-100000,0)
    seed_t = random.randint(10**6+2,10**7)
    noise_gen_height = OpenSimplex(seed=seed_h)
    noise_gen_moist = OpenSimplex(seed=seed_m)
    noise_gen_temperature = OpenSimplex(seed=seed_t)

    width = 256
    height = 256
    heights =  np.zeros((height,width,3), dtype=np.uint8) 

    for y in range(height):
        for x in range(width):
            nx = 2*x/width - 1
            ny = 2*y/height - 1

            # elevation
            e1,e2,e3,e4,e5,e6 = 1, 0.5, 0.25, 0.13, 0.06, 0.03
            exp = 2
            elev =  e1 * (noise_gen_height.noise2(1*nx,1*ny) /2.0 + 0.5) + \
                    e2 * (noise_gen_height.noise2(2*nx,2*ny) /2.0 + 0.5)+ \
                    e3 * (noise_gen_height.noise2(4*nx,4*ny) /2.0 + 0.5)+ \
                    e4 * (noise_gen_height.noise2(8*nx,8*ny) /2.0 + 0.5)+ \
                    e5 * (noise_gen_height.noise2(16*nx,16*ny) /2.0 + 0.5)+ \
                    e6 * (noise_gen_height.noise2(32*nx,32*ny)/2.0 + 0.5)

            #moisture
            m1,m2,m3,m4,m5,m6 = 1, 0.5, 0.25, 0.13, 0.06, 0.03
            moist = m1 * (noise_gen_moist.noise2(1*nx,1*ny) /2.0 + 0.5)+ \
                    m2 * (noise_gen_moist.noise2(2*nx,2*ny) /2.0 + 0.5)+ \
                    m3 * (noise_gen_moist.noise2(4*nx,4*ny) /2.0 + 0.5)+ \
                    m4 * (noise_gen_moist.noise2(8*nx,8*ny) /2.0 + 0.5)+ \
                    m5 * (noise_gen_moist.noise2(16*nx,16*ny) /2.0 + 0.5)+ \
                    m6 * (noise_gen_moist.noise2(32*nx,32*ny)/2.0 + 0.5)
            
            #temperature
            t1,t2,t3,t4,t5,t6 = 1, 0.5, 0.25, 0.13, 0.06, 0.03
            temperature = t1 * (noise_gen_temperature.noise2(1*nx,1*ny) /2.0 + 0.5)+ \
                    t2 * (noise_gen_temperature.noise2(2*nx,2*ny) /2.0 + 0.5)+ \
                    t3 * (noise_gen_temperature.noise2(4*nx,4*ny) /2.0 + 0.5)+ \
                    t4 * (noise_gen_temperature.noise2(8*nx,8*ny) /2.0 + 0.5)+ \
                    t5 * (noise_gen_temperature.noise2(16*nx,16*ny) /2.0 + 0.5)+ \
                    t6 * (noise_gen_temperature.noise2(32*nx,32*ny)/2.0 + 0.5)
            # square bump
            d = 1 - (1-nx**2) * (1-ny**2)
            elev = (elev + (1-d))/2
            fudge_factor = 1.15

            heights[y][x] = biome(pow(elev *fudge_factor,exp), moist)

            save_img(heights, "landmap", 'RGB')
            save_img(elev,"elev",'L')
            save_img(moist,"moist","L")
            save_img(temperature,"temperature","L")
    


def biome(e: np.ndarray, m: np.ndarray) -> tuple:
    if e<0.1: return Land.OCEAN.value
    if e<0.14: return Land.BEACH.value

    if e >0.9:
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