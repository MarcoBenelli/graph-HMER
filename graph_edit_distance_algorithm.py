import networkx as nx
import numpy as np

from graph import Graph
from misc import *


class GraphEditDistanceAlgorithm:
    def __init__(self, threshold, mode):
        self.threshold = threshold
        self.mode = mode

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
        normalized_graph1 = graph1.normalize()
        normalized_graph2 = graph2.normalize()
        g1 = normalized_graph1.convert_networkx()
        g2 = normalized_graph2.convert_networkx()
        imsave('debug/' + name1,
               np.array(normalized_graph1.get_image(size=128) * 255, dtype=np.uint8))
        imsave('debug/' + name2,
               np.array(normalized_graph2.get_image(size=128) * 255, dtype=np.uint8))
        if self.mode == 'COSINE':
            ged = nx.algorithms.similarity.graph_edit_distance(g1, g2, timeout=1,
                                                               edge_del_cost=lambda e: e['length'],
                                                               edge_ins_cost=lambda e: e['length'],
                                                               edge_subst_cost=lambda e1, e2: abs(
                                                                   e1['length'] - e2['length']),
                                                               node_del_cost=lambda n: n['weight'],
                                                               node_ins_cost=lambda n: n['weight'],
                                                               node_subst_cost=lambda n1, n2: abs(
                                                                   n1['weight'] - n2['weight']))
        elif self.mode == 'DISTANCE':
            ged = nx.algorithms.similarity.graph_edit_distance(g1, g2, timeout=1,
                                                               edge_del_cost=lambda e: e['length'],
                                                               edge_ins_cost=lambda e: e['length'],
                                                               edge_subst_cost=lambda e1, e2: abs(
                                                                   e1['length'] - e2['length']),
                                                               node_del_cost=lambda n: 1,
                                                               node_ins_cost=lambda n: 1,
                                                               node_subst_cost=lambda n1, n2: euclidean_distance(
                                                                   n1['position'], n2['position']))
        else:
            raise RuntimeError('Invalide GED mode')
        print('calculated ged with ' + name1 + ' = ' + str(ged))
        return ged


if __name__ == '__main__':
    coords1 = [1, 1, 1]
    coords2 = [1, 1, (1, 4)]
    graph1 = Graph([coords1], (10, 10))
    graph2 = Graph([coords2], (10, 10))
    geda = GraphEditDistanceAlgorithm(20)
    print(geda.execute(graph1, graph2))
