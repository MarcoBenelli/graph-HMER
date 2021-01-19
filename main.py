import os
import xml.etree.ElementTree as ET

import numpy as np

# import inkml2img
from graph import Graph
from graph_representator_factory import GraphRepresentatorFactory
from graph_edit_distance_algorithm import GraphEditDistanceAlgorithm
from misc import imsave

# np.set_printoptions(threshold=np.inf)

inkml_path = 'trainData1/'
png_path = 'images/'
skeleton_path = 'skeletons/'
graph_grid_path = 'graphs-grid/'
graph_polygon_path = 'graphs-polygon/'
query_path = 'query-image/'
ged_results_path = 'ged-results/'

ns = {'InkML': 'http://www.w3.org/2003/InkML'}

grf = GraphRepresentatorFactory()
query_name = list(os.scandir(query_path))[0].name
query = grf.build_graph(query_path, query_name)
imsave(ged_results_path + 'query-' + query_name,
       np.array(query.graph.normalize().get_image(size=128) * 255, dtype=np.uint8))

recall = []
precision = []

for ged_threshold in (x * 4 for x in range(0, 4)):
    geda = GraphEditDistanceAlgorithm(ged_threshold, 'DISTANCE')
    print('threshold =', ged_threshold)
    true_positives = 0
    false_negatives = 0
    false_positives = 0
    for inkml in os.scandir(inkml_path):
        print('   ', inkml.name)
        # inkml2img.inkml2img(inkml.path,
        #                     png_path + os.path.splitext(inkml.name)[0] + '.png')
        tree = ET.parse(inkml.path)
        symbols_list = [symbol.text for symbol in tree.findall('InkML:traceGroup/InkML:traceGroup/InkML:annotation', ns)]
        gt = '(' in symbols_list
        print('   ', symbols_list)

        image_name = os.path.splitext(inkml.name)[0] + '.png'
        grp = grf.build_graph(png_path, image_name, graph_polygon_path, skeleton_path, graph_grid_path)

        found = geda.find(grp.graph, query.graph, image_name, ged_results_path)
        if found and gt:
            true_positives += 1
        elif found and not gt:
            false_positives += 1
        elif not found and gt:
            false_negatives += 1

    recall.append(true_positives / (true_positives + false_negatives))
    if true_positives + false_positives > 0:
        precision.append(true_positives / (true_positives + false_positives))
    else:
        precision.append(1)

print(recall)
print(precision)
