import os

import numpy as np
import skimage
from skimage import io, morphology, transform

import inkml2img
from misc import *

# np.set_printoptions(threshold=np.inf)

inkml_path = 'trainData1/'
png_path = 'images/'
skeleton_path = 'skeletons/'
graph_path = 'graphs/'

# for inkml in os.scandir(inkml_path):
#     print(inkml.name)
#     inkml2img.inkml2img(inkml.path,
#                         png_path + os.path.splitext(inkml.name)[0] + '.png')

for file in os.scandir(png_path):
    image_name = file.name
    print(image_name)
    image = io.imread(png_path + image_name, as_gray=True)
    image_resized = transform.resize(image,
                                     (512,
                                      image.shape[1] * 512 // image.shape[0]))
    image_binarized = np.array(image_resized > 0.5, dtype=float)
    image_inverted = skimage.util.invert(image_binarized)
    skeleton = morphology.skeletonize(image_inverted)
    io.imsave(skeleton_path + image_name,
              np.array(skeleton * 255, dtype=np.uint8),
              check_contrast=False)
    cell_length = 24
    grid = np.zeros((skeleton.shape[0] // cell_length,
                     skeleton.shape[1] // cell_length))
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i, j] = np.any(skeleton[cell_length * i:cell_length * (i + 1),
                                cell_length * j:cell_length * (j + 1)])
    graph = np.zeros(skeleton.shape)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            graph[cell_length * i + cell_length // 2,
                  cell_length * j + cell_length // 2] = grid[i, j]
            if grid[make_interval(i, grid.shape[0] - 1),
                    make_interval(j, grid.shape[1] - 1)]:
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if grid[make_interval(i + di, grid.shape[0] - 1),
                                make_interval(j + dj, grid.shape[1] - 1)]:
                            draw_line(graph, cell_length * i + cell_length // 2,
                                      cell_length * j + cell_length // 2,
                                      di, dj, cell_length)
    io.imsave(graph_path + 'graph-' + image_name,
              np.array(graph * 255, dtype=np.uint8),
              check_contrast=False)
    io.imsave(graph_path + 'grid-' + image_name,
              np.array(grid * 255, dtype=np.uint8),
              check_contrast=False)
