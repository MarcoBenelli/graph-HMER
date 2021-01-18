import networkx as nx
import numpy as np

from graph import Graph
from misc import *


class GraphEditDistanceAlgorithm:
    def __init__(self, threshold, mode):
        self.threshold = threshold
        self.mode = mode

    # TODO
    def find(self, expression, query, expression_name, query_name):
        normalized_query = query.normalize()
        imsave('ged-results/' + 'query_' + query_name,
               np.array(normalized_query.get_image(size=128) * 255, dtype=np.uint8))
        for i, coords in enumerate(expression.coords_lists):
            symbol = Graph([coords], expression.shape)
            normalized_symbol = symbol.normalize()
            ged = self.execute(normalized_symbol, normalized_query)
            imsave('ged-results/' + str('%.3f' % ged) + '_' + expression_name,
                   np.array(normalized_symbol.get_image(size=128) * 255, dtype=np.uint8))
            print('calculated ged with ' + expression_name + ' = ' + str(ged))
            if ged is not None and ged <= self.threshold:
                print('MATCHED')
                return True
            print()

    def execute(self, graph1, graph2):
        nx_graph1 = graph1.convert_networkx()
        nx_graph2 = graph2.convert_networkx()
        if self.mode == 'COSINE':
            ged = nx.algorithms.similarity.graph_edit_distance(nx_graph1, nx_graph2, timeout=1,
                                                               edge_del_cost=lambda e: e['length'],
                                                               edge_ins_cost=lambda e: e['length'],
                                                               edge_subst_cost=lambda e1, e2: abs(
                                                                   e1['length'] - e2['length']),
                                                               node_del_cost=lambda n: n['weight'],
                                                               node_ins_cost=lambda n: n['weight'],
                                                               node_subst_cost=lambda n1, n2: abs(
                                                                   n1['weight'] - n2['weight']))
        elif self.mode == 'DISTANCE':
            ged = nx.algorithms.similarity.graph_edit_distance(nx_graph1, nx_graph2, timeout=1,
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
        return ged
