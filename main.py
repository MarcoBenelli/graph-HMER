import os
import xml.etree.ElementTree as ET
import warnings

import numpy as np
from termcolor import colored

import inkml2img
from graph_representator_factory import GraphRepresentatorFactory
from graph_edit_distance_algorithm import GraphEditDistanceAlgorithm
from misc import *

# np.set_printoptions(threshold=np.inf)

inkml_path = 'trainData1/'
png_path = 'images/'
skeleton_path = 'skeletons/'
graph_grid_path = 'graphs-grid/'
graph_polygon_path = 'graphs-polygon/'
query_path = 'query-image/'
ged_results_path = 'ged-results/'
plots_path = 'plots/'

ns = {'InkML': 'http://www.w3.org/2003/InkML'}

grf = GraphRepresentatorFactory()
query_name = list(os.scandir(query_path))[0].name
query = grf.build_graph(query_path, query_name)
imsave(ged_results_path + 'query-' + query_name,
       np.array(query.graph.normalize().get_image(size=128) * 255, dtype=np.uint8))
geda = GraphEditDistanceAlgorithm('DISTANCE')
num_best = 8

ged_dict = {}
gt_dict = {}
recall = []
precision = []

num_expressions = len(list(os.scandir(inkml_path)))
processed_expressions = 0
for i, inkml in enumerate(os.scandir(inkml_path)):
    warnings.filterwarnings('ignore')
    inkml2img.inkml2img(inkml.path,
                        png_path + os.path.splitext(inkml.name)[0] + '.png')
    print('Converting InkML files to png:', i + 1, '/', num_expressions)
for inkml in os.scandir(inkml_path):
    print()
    print(colored(inkml.name, 'blue'))
    tree = ET.parse(inkml.path)
    symbols_list = [symbol.text for symbol in tree.findall('InkML:traceGroup/InkML:traceGroup/InkML:annotation', ns)]
    gt_dict[os.path.splitext(inkml.name)[0]] = '(' in symbols_list
    print(colored('Ground truth: ' + str(symbols_list), 'yellow'))

    image_name = os.path.splitext(inkml.name)[0] + '.png'
    grp = grf.build_graph(png_path, image_name, graph_polygon_path, skeleton_path, graph_grid_path)

    ged_dict[os.path.splitext(inkml.name)[0]] = geda.find(grp.graph, query.graph, image_name, ged_results_path)
    processed_expressions += 1
    print(colored('Checked expressions = ' + str(processed_expressions) + ' / ' + str(num_expressions), 'magenta'))

for ged_threshold in (x / 8 for x in range(2 ** 8)):
    true_positives = 0
    false_negatives = 0
    false_positives = 0
    for expression in ged_dict.keys():
        if ged_dict[expression] <= ged_threshold and gt_dict[expression]:
            true_positives += 1
        elif ged_dict[expression] <= ged_threshold and not gt_dict[expression]:
            false_positives += 1
        elif ged_dict[expression] > ged_threshold and gt_dict[expression]:
            false_negatives += 1

    recall.append(true_positives / (true_positives + false_negatives))
    if true_positives + false_positives > 0:
        precision.append(true_positives / (true_positives + false_positives))
    else:
        precision.append(1)
plot_precision_recall(recall, precision, plots_path + 'plot.png')
print()
print(colored('Created precision-recall plot', 'green'))

print()
sorted_ged_dict = sorted(ged_dict.items(), key=lambda item: item[1])
for i in range(num_best):
    print(colored(str(i + 1) + '-th best match: ' + sorted_ged_dict[i][0] + ', with min GED: ' + str(sorted_ged_dict[i][1]), 'red'))
