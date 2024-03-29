from opensimplex import OpenSimplex
import numpy as np
from math import pow
import random
from image_functions import *
from gradients import circular_gradient, gradient_descent
from vor import *
from math import sqrt


def generate():
    seed_h = random.randint(0,10**6)
    seed_m = random.randint(-100000,0)
    seed_t = random.randint(10**6+2,10**7)
    noise_gen_height = OpenSimplex(seed=seed_h)
    noise_gen_moist = OpenSimplex(seed=seed_m)
    noise_gen_temperature = OpenSimplex(seed=seed_t)

    WIDTH = 256
    HEIGHT = 256
    FEATURE_SIZE = 24

    exp = 3
    heights =  np.empty((HEIGHT,WIDTH,3), dtype=np.uint8)
    # gradients = [circular_gradient((HEIGHT,WIDTH),50, 2),circular_gradient((HEIGHT,WIDTH),50, 2.5),circular_gradient((HEIGHT,WIDTH),50, 1.5)]
    # grad = circular_gradient((HEIGHT,WIDTH),150, 2)

    e_map, m_map, t_map = np.empty((HEIGHT,WIDTH), dtype=np.uint8), np.empty((HEIGHT,WIDTH), dtype=np.uint8), np.empty((HEIGHT,WIDTH), dtype=np.uint8)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            nx = x/WIDTH - 0.5
            ny = y/HEIGHT - 0.5

            # elevation
            e = [1, 0.5, 0.25, 0.13, 0.06, 0.03]
            # elev = (noise_gen_height.noise2(x / FEATURE_SIZE,y / FEATURE_SIZE) /2.0 + 0.5) #for archipelago
           
            # elev = (ridge_noise(noise_gen_height.noise2(x / FEATURE_SIZE,y / FEATURE_SIZE) /2.0 + 0.5)) + \
            elev =  e[0] * (noise_gen_height.noise2(x / FEATURE_SIZE,y / FEATURE_SIZE) /2.0 + 0.5) + \
                    e[1] * (noise_gen_height.noise2((2*x + 2.137) / FEATURE_SIZE,(2*y + 3.75) / FEATURE_SIZE) /2.0 + 0.5) + \
                    e[2] * (noise_gen_height.noise2((4*x + 690) / FEATURE_SIZE,(4*y + 690) / FEATURE_SIZE) /2.0 + 0.5) + \
                    e[3] * (noise_gen_height.noise2((8*x + 4200) / FEATURE_SIZE,(8*y +4200) / FEATURE_SIZE) /2.0 + 0.5)+ \
                    e[4] * (noise_gen_height.noise2((16*x + 1800) / FEATURE_SIZE,(16*y + 1800) / FEATURE_SIZE) /2.0 + 0.5)+ \
                    e[5] * (noise_gen_height.noise2((32*x + 2137) / FEATURE_SIZE,(32*y + 2137) / FEATURE_SIZE)/2.0 + 0.5)
            elev = elev/sum(e)
            #moisture
            m = [1, 0.5, 0.25, 0.13, 0.06, 0.03]
            moist = m[0] * (noise_gen_moist.noise2(x / FEATURE_SIZE,y / FEATURE_SIZE) /2.0 + 0.5) + \
                    m[1] * (noise_gen_moist.noise2((2*x + 2.137) / FEATURE_SIZE,(2*y + 3.75) / FEATURE_SIZE) /2.0 + 0.5) + \
                    m[2] * (noise_gen_moist.noise2((4*x + 690) / FEATURE_SIZE,(4*y + 690) / FEATURE_SIZE) /2.0 + 0.5) + \
                    m[3] * (noise_gen_moist.noise2((8*x + 4200) / FEATURE_SIZE,(8*y +4200) / FEATURE_SIZE) /2.0 + 0.5) + \
                    m[4] * (noise_gen_moist.noise2((16*x + 1800) / FEATURE_SIZE,(16*y + 1800) / FEATURE_SIZE) /2.0 + 0.5) +\
                    m[5] * (noise_gen_moist.noise2((32*x + 2137) / FEATURE_SIZE,(32*y + 2137) / FEATURE_SIZE)/2.0 + 0.5)        
            moist = moist/sum(m)
            m_map[y][x] = moist*255
            #temperature
            t = [1, 0.5, 0.25, 0.13, 0.06, 0.03]
            temperature = t[0] * (noise_gen_temperature.noise2(1*nx,1*ny) /2.0 + 0.5)+ \
                    t[1] * (noise_gen_temperature.noise2(2*nx + 2.137,2*ny + 3.75) /2.0 + 0.5)+ \
                    t[2] * (noise_gen_temperature.noise2(4*nx + 7.77,4*ny + 6.66) /2.0 + 0.5)+ \
                    t[3] * (noise_gen_temperature.noise2(8*nx +8.36 ,8*ny +17.3) /2.0 + 0.5)+ \
                    t[4] * (noise_gen_temperature.noise2(16*nx + 21.37,16*ny + 20) /2.0 + 0.5)+ \
                    t[5] * (noise_gen_temperature.noise2(32*nx + 37,32*ny + 28)/2.0 + 0.5)
            temperature = temperature/sum(t)
            t_map[y][x] = temperature*255

            # square bump/euclidean for island
            nx = 2*x/WIDTH - 1
            ny = 2*y/HEIGHT - 1
            d = min(1, (nx**2 + ny**2) / sqrt(2))
            # d = 1 - (1-nx**2) * (1-ny**2)
            elev = (elev + (1-d))/2
            # mountains


            
            fudge_factor = 1.15

            e_map[y][x] = pow(elev *fudge_factor,exp)*255


            heights[y][x] = biome(pow(elev *fudge_factor,exp), moist, temperature)
            # heights[y][x] = biome(pow(elev *fudge_factor * grad[y][x]/255,exp), moist, temperature) #for archipelago
            
    # save_img(grad, "grad", "L")
    save_img(heights, "landmap", 'RGB')
    save_img(e_map,"elev",'L')
    # save_img(m_map,"moist",'L')
    # save_img(t_map,"temperature",'L')
    # voron_gen(e_map, m_map,t_map,256)
    gradient_descent(e_map)
    


if __name__ == "__main__":
    generate()