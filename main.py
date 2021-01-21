import warnings
import shutil

from termcolor import colored

import inkml2img
from graph_representator_factory import GraphRepresentatorFactory
from graph_edit_distance_algorithm import GraphEditDistanceAlgorithm
from misc import *

inkml_path = 'trainData1/'
png_path = 'images/'
skeleton_path = 'skeletons/'
graph_grid_path = 'graphs-grid/'
graph_polygon_path = 'graphs-polygon/'
query_images_path = 'query-images/'
query_inkml_path = 'query-inkml/'
ged_results_path = 'ged-results/'
plots_path = 'plots/'

shutil.rmtree(png_path)
shutil.rmtree(skeleton_path)
shutil.rmtree(graph_grid_path)
shutil.rmtree(graph_polygon_path)
shutil.rmtree(query_images_path)
shutil.rmtree(query_inkml_path)
shutil.rmtree(ged_results_path)
# shutil.rmtree(plots_path)
os.mkdir(png_path)
os.mkdir(skeleton_path)
os.mkdir(graph_grid_path)
os.mkdir(graph_polygon_path)
os.mkdir(query_images_path)
os.mkdir(query_inkml_path)
os.mkdir(ged_results_path)
# os.mkdir(plots_path)

ns = {'InkML': 'http://www.w3.org/2003/InkML'}

extract_query(inkml_path, query_inkml_path)

grf = GraphRepresentatorFactory()
geda = GraphEditDistanceAlgorithm('DISTANCE')
# num_best = 8


num_expressions = len(list(os.scandir(inkml_path)))
num_queries = len(list(os.scandir(query_inkml_path)))
for i, inkml in enumerate(os.scandir(inkml_path)):
    warnings.filterwarnings('ignore')
    inkml2img.inkml2img(inkml.path,
                        png_path + os.path.splitext(inkml.name)[0] + '.png')
    print('Converting InkML expression to png:', i + 1, '/', num_expressions)
for i, inkml in enumerate(os.scandir(query_inkml_path)):
    warnings.filterwarnings('ignore')
    inkml2img.inkml2img(inkml.path,
                        query_images_path + os.path.splitext(inkml.name)[0] + '.png')
    print('Converting InkML query to png:', i + 1, '/', num_queries)

processed_expressions = 0
num_thresholds = 2 ** 8
total_recall = [0] * num_thresholds
total_precision = [0] * num_thresholds
total_weight = 0
for query_inkml in os.scandir(query_inkml_path):
    ged_dict = {}
    gt_dict = {}
    query_tree = ET.parse(query_inkml.path)
    annotation = query_tree.find('InkML:traceGroup/InkML:traceGroup/InkML:annotation', ns).text
    query = grf.build_graph(query_images_path, os.path.splitext(query_inkml.name)[0] + '.png')
    for inkml in os.scandir(inkml_path):
        print()
        print(colored(inkml.name, 'blue'))
        tree = ET.parse(inkml.path)
        symbols_list = [symbol.text for symbol in tree.findall('InkML:traceGroup/InkML:traceGroup/InkML:annotation', ns)]
        gt_dict[os.path.splitext(inkml.name)[0]] = annotation in symbols_list
        print(colored('Ground truth: ' + str(symbols_list), 'yellow'))

        image_name = os.path.splitext(inkml.name)[0] + '.png'
        grp = grf.build_graph(png_path, image_name, graph_polygon_path, skeleton_path, graph_grid_path)

        ged_dict[os.path.splitext(inkml.name)[0]] = geda.find(grp.graph, query.graph, image_name, ged_results_path)
        processed_expressions += 1
        print(colored('Checked expressions = ' + str(processed_expressions) + ' / ' + str(num_expressions), 'magenta'))

    for i, ged_threshold in enumerate(x / num_thresholds * 32 for x in range(num_thresholds)):
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

        weight = true_positives + false_negatives
        total_recall[i] += true_positives
        if true_positives + false_positives > 0:
            total_precision[i] += true_positives / (true_positives + false_positives) * weight
        else:
            total_precision[i] += weight
    total_weight += weight
    print(total_recall)
    print(total_precision)

recall = [tr / total_weight for tr in total_recall]
precision = [tp / total_weight for tp in total_precision]
print('recall =', recall)
print('precision =', precision)
plot_precision_recall(recall, precision, plots_path + 'plot.png')
print()
print(colored('Created precision-recall plot', 'green'))

# print()
# sorted_ged_dict = sorted(ged_dict.items(), key=lambda item: item[1])
# for i in range(num_best):
#     print(colored(str(i + 1) + '-th best match: ' + sorted_ged_dict[i][0] + ', with min GED: ' + str(sorted_ged_dict[i][1]), 'red'))
