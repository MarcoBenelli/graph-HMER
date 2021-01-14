import networkx as nx
import numpy as np

from graph import Graph
from misc import *


class GraphEditDistanceAlgorithm:
    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, expression, query, expression_name, query_name):
        matches = []
        for i, coords in enumerate(expression.coords_lists):
            print(' finding symbol')
            symbol = Graph([coords], expression.shape)
            print(' created symbol graph')
            ged = self.execute(symbol, query, str(i) + expression_name, query_name)
            print(' executed')
            if ged is not None and ged <= self.threshold:
                matches.append(coords)
        print(len(matches))

    # TODO
    def execute(self, graph1, graph2, name1, name2):
        print('  starting execute')
        normalized_graph1 = graph1.normalize()
        normalized_graph2 = graph2.normalize()
        print('  normalized graphs')
        g1 = normalized_graph1.convert_networkx()
        g2 = normalized_graph2.convert_networkx()
        print('  converted graphs')
        imsave('debug/' + name1,
               np.array(normalized_graph1.get_image() * 255, dtype=np.uint8))
        imsave('debug/' + name2,
               np.array(normalized_graph2.get_image() * 255, dtype=np.uint8))
        print('  saved images')
        ged = nx.algorithms.similarity.graph_edit_distance(g1, g2, timeout=1)
        print('  calculated ged with ' + name1 + ' = ' + str(ged))
        return ged


if __name__ == '__main__':
    coords1 = [1, 1, 1]
    coords2 = [1, 1, (1, 4)]
    graph1 = Graph([coords1], (10, 10))
    graph2 = Graph([coords2], (10, 10))
    geda = GraphEditDistanceAlgorithm(20)
    print(geda.execute(graph1, graph2))
