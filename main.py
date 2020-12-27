import os

import skimage
from skimage import io, morphology, transform

import inkml2img
import preprocessing
from graph_image import GraphImage
from misc import *

# np.set_printoptions(threshold=np.inf)

inkml_path = 'trainData1/'
png_path = 'images/'
skeleton_path = 'skeletons/'
node_path = 'nodes/'
graph_path = 'graphs/'

# for inkml in os.scandir(inkml_path):
#     print(inkml.name)
#     inkml2img.inkml2img(inkml.path,
#                         png_path + os.path.splitext(inkml.name)[0] + '.png')

for file in os.scandir(png_path):
    image_name = file.name
    print(image_name)

    image = imread(png_path + image_name)
    image_resized = preprocessing.resize(image, (512, image.shape[1] * 512 // image.shape[0]))
    image_binarized = preprocessing.binarize(image_resized)
    image_inverted = preprocessing.invert(image_binarized)
    image_skeletonized = preprocessing.skeletonize(image_inverted)
    imsave(skeleton_path + image_name, np.array(image_skeletonized * 255, dtype=np.uint8))

    gi = GraphImage(image_skeletonized, 32)
    nodes_image = gi.represent_nodes()
    graph = gi.represent_graph_simple()

    imsave(node_path + image_name,
              np.array(nodes_image * 255, dtype=np.uint8))
    imsave(graph_path + image_name,
              np.array(graph * 255, dtype=np.uint8))
    # io.imsave(graph_path + 'grid-' + image_name,
    #           np.array(grid * 255, dtype=np.uint8),
    #           check_contrast=False)
