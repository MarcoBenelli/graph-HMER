import os
import xml.etree.ElementTree as ET

import numpy as np

# import inkml2img
import preprocessing
from graph import Graph
from graph_representator_grid import GraphRepresentatorGrid
from graph_representator_polygon import GraphRepresentatorPolygon
from graph_edit_distance_algorithm import GraphEditDistanceAlgorithm
from misc import *

# np.set_printoptions(threshold=np.inf)

inkml_path = 'trainData1/'
png_path = 'images/'
skeleton_path = 'skeletons/'
graph_grid_path = 'graphs-grid/'
graph_no_grid_connection_path = 'graphs-no-grid-connection/'
graph_polygon_path = 'graphs-polygon/'

# TODO
for inkml in os.scandir(inkml_path):
    print()
    print(inkml.name)
    # inkml2img.inkml2img(inkml.path,
    #                     png_path + os.path.splitext(inkml.name)[0] + '.png')
    tree = ET.parse(inkml.path)
    root = tree.getroot()
    for child in root:
        if child.tag == '{http://www.w3.org/2003/InkML}traceGroup':
            for child1 in child:
                i = 0
                for child2 in child1:
                    if child2.tag == '{http://www.w3.org/2003/InkML}annotation':
                        i += 1
                        print(child2.text, i)

for file in os.scandir(png_path):
    image_name = file.name
    print(image_name)

    image = imread(png_path + image_name)
    image_resized = preprocessing.resize(image, (512, image.shape[1] * 512 // image.shape[0]))
    image_binarized = preprocessing.binarize(image_resized, 0.25)
    image_inverted = preprocessing.invert(image_binarized)
    image_skeletonized = preprocessing.skeletonize(image_inverted)
    imsave(skeleton_path + image_name, np.array(image_skeletonized * 255, dtype=np.uint8))

    grg = GraphRepresentatorGrid(image_skeletonized, 32)
    graph_simple = grg.represent_graph_no_grid_connection()
    graph = grg.represent_graph()

    grp = GraphRepresentatorPolygon(image_inverted, 10, image_name)
    graph_image_polygon = grp.represent_graph()

    imsave(graph_no_grid_connection_path + image_name,
           np.array(graph_simple * 255, dtype=np.uint8))
    imsave(graph_grid_path + image_name,
           np.array(graph * 255, dtype=np.uint8))
    imsave(graph_polygon_path + image_name,
           np.array(graph_image_polygon * 255, dtype=np.uint8))

    geda = GraphEditDistanceAlgorithm(4, 'DISTANCE')
    char_index = 1
    query = Graph(grp.graph.coords_lists[char_index:char_index + 1], grp.graph.shape)
    found = geda.find(grp.graph, query, image_name, 'query-' + image_name)

    break
