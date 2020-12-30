import os

import numpy as np

import inkml2img
import preprocessing
from graph_representator_grid import GraphRepresentatorGrid
from graph_representator_polygon import GraphRepresentatorPolygon
from misc import *

# np.set_printoptions(threshold=np.inf)

inkml_path = 'trainData/'
png_path = 'images/'
skeleton_path = 'skeletons/'
graph_grid_path = 'graphs-grid/'
graph_no_grid_connection_path = 'graphs-no-grid-connection/'
graph_polygon_path = 'graphs-polygon/'


for inkml in os.scandir(inkml_path):
    print(inkml.name)
    inkml2img.inkml2img(inkml.path,
                        png_path + os.path.splitext(inkml.name)[0] + '.png')

for file in os.scandir(png_path):
    image_name = file.name
    print(image_name)

    image = imread(png_path + image_name)
    image_resized = preprocessing.resize(image, (512, image.shape[1] * 512 // image.shape[0]))
    image_binarized = preprocessing.binarize(image_resized, 0.25)
    image_inverted = preprocessing.invert(image_binarized)
    image_skeletonized = preprocessing.skeletonize(image_inverted)
    imsave(skeleton_path + image_name, np.array(image_skeletonized * 255, dtype=np.uint8))

    gig = GraphRepresentatorGrid(image_skeletonized, 32)
    graph_simple = gig.represent_graph_no_grid_connection()
    graph = gig.represent_graph()

    gip = GraphRepresentatorPolygon(image_inverted, 10, image_name)
    graph_image_polygon = gip.represent_graph()

    imsave(graph_no_grid_connection_path + image_name,
           np.array(graph_simple * 255, dtype=np.uint8))
    imsave(graph_grid_path + image_name,
           np.array(graph * 255, dtype=np.uint8))
    imsave(graph_polygon_path + image_name,
           np.array(graph_image_polygon * 255, dtype=np.uint8))
