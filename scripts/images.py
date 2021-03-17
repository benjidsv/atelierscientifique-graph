import os
import numpy as np
from PIL import Image

image = Image.open('C:/Users/benja/Desktop/Python/atelierscientifique-graph-main/ressources/graph.jpg')
raster = np.array(image)
width, height, _ = raster.shape

mask = np.zeros(raster.shape, dtype=np.uint8)
mask[np.where(image == [0, 0, 0])] = [255, 255, 255]
if np.any(mask == [255, 255, 255]): print("yes")

trim = raster[0:100, 0:100]
Image.fromarray(mask).show()