import opensimplex
import numpy as np
from PIL import Image

def generate():
    # Create an instance of the OpenSimplex class
    noise_gen = opensimplex .OpenSimplex(seed=1234)

    # Set the dimensions of the height  map
    width = 512
    height = 512

    # Create an array to store the height values
    heights = np.empty((width, height))

    # Generate noise values for each coordinate in the heightmap
    for x in range(width):
        for y in range(height):
            # Generate a noise value using the noise2d method
            noise_val = noise_gen.noise2(x=x, y=y)
            # Scale and offset the noise value to fit the desired range of heights
            scaled_val = (noise_val + 1) * 64
            # Assign the height value to the appropriate element in the array
            heights[x][y] = scaled_val

    # Create an image from the heightmap array using the PIL library
    img = Image.fromarray(heights, 'I')
    img.save('results/heightmap.png')



if __name__ == "__main__":
    generate()