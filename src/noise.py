from opensimplex import OpenSimplex
import numpy as np
from PIL import Image
from math import pow
import random

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
            elev =  e1 * abs(noise_gen_height.noise2(1*nx,1*ny)) + \
                    e2 * abs(noise_gen_height.noise2(2*nx,2*ny)) + \
                    e3 * abs(noise_gen_height.noise2(4*nx,4*ny)) + \
                    e4 * abs(noise_gen_height.noise2(8*nx,8*ny)) + \
                    e5 * abs(noise_gen_height.noise2(16*nx,16*ny)) + \
                    e6 * abs(noise_gen_height.noise2(32*nx,32*ny))
            elev = elev/sum((e1,e2,e3,e4,e5,e6))

            m1,m2,m3,m4,m5,m6 = 1, 0.5, 0.25, 0.12, 0.06, 0.03
            moist = m1 * abs(noise_gen_moist.noise2(1*nx,1*ny)) + \
                    m2 * abs(noise_gen_moist.noise2(2*nx,2*ny)) + \
                    m3 * abs(noise_gen_moist.noise2(4*nx,4*ny)) + \
                    m4 * abs(noise_gen_moist.noise2(8*nx,8*ny)) + \
                    m5 * abs(noise_gen_moist.noise2(16*nx,16*ny)) + \
                    m6 * abs(noise_gen_moist.noise2(32*nx,32*ny))
            heights[y][x] = pow(elev,exp)

    # Create an image from the heightmap array using the PIL library
    img = Image.fromarray(heights, 'I')
    img.save(f'results/heightmap{noise_gen_height.noise2(1/e1*nx,1/e1*ny)}.png')


    def biome(e,m):
        return 1

    # var m = (0.00 * noiseM( 1 * nx,  1 * ny)
    #        + 1.00 * noiseM( 2 * nx,  2 * ny)
    #        + 0.33 * noiseM( 4 * nx,  4 * ny)
    #        + 0.33 * noiseM( 8 * nx,  8 * ny)
    #        + 0.33 * noiseM(16 * nx, 16 * ny)
    #        + 0.50 * noiseM(32 * nx, 32 * ny));
    # m = m / (0.00 + 1.00 + 0.33 + 0.33 + 0.33 + 0.50);
if __name__ == "__main__":
    generate()