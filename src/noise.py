from opensimplex import OpenSimplex
import numpy as np
from PIL import Image
from math import pow
import random

def generate():
    noise_gen = OpenSimplex(seed=random.randint(0,10**6))

    width = 256
    height = 256
    heights = np.empty((width,height))

    for x in range(width):
        for y in range(height):
            nx = x/width - 0.5
            ny = y/height - 0.5
            e1,e2,e3,e4,e5,e6 = 1, 0.5, 0.25, 0.12, 0.06, 0.03
            exp = 1
            elev = abs(e1 * noise_gen.noise2(1/e1*nx,1/e1*ny)) + \
                    e2 * abs(noise_gen.noise2(1/e2*nx,1/e2*ny)) + \
                    e3 * abs(noise_gen.noise2(1/e3*nx,1/e3*ny)) + \
                    e4 * abs(noise_gen.noise2(1/e4*nx,1/e4*ny)) + \
                    e5 * abs(noise_gen.noise2(1/e5*nx,1/e5*ny)) + \
                    e6 * abs(noise_gen.noise2(1/e6*nx,1/e6*ny))
            elev = elev/sum((e1,e2,e3,e4,e5,e6))
            heights[y][x] = pow(elev,exp)

    # Create an image from the heightmap array using the PIL library
    img = Image.fromarray(heights, 'I')
    img.save(f'results/heightmap{noise_gen.noise2(1/e1*nx,1/e1*ny)}.png')


    def biome():
        pass


if __name__ == "__main__":
    generate()