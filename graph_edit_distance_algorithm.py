import networkx as nx
import numpy as np

from graph import Graph
from misc import *


class GraphEditDistanceAlgorithm:
    def __init__(self, mode, timeout=0.1):
        self.mode = mode
        self.timeout = timeout

    def find(self, expression, query, expression_name, output_path):
        max_ged = 0
        for coords_list in query.coords_lists:
            query_component = Graph([coords_list])
            normalized_query = query_component.normalize()
            min_ged = np.inf
            for i, coords in enumerate(expression.coords_lists):
                symbol = Graph([coords], expression.shape)
                normalized_symbol = symbol.normalize()
                ged = self.execute(normalized_symbol, normalized_query)
                if ged is not None:
                    imsave(output_path + str('%.3f' % ged) + '_' + str(i) + '_' + expression_name,
                           np.array(normalized_symbol.get_image_normalized(size=128) * 255, dtype=np.uint8))
                print('    Calculated GED with ' + str(i + 1) + '-th symbol = ' + str(ged))
                if ged is not None and ged < min_ged:
                    min_ged = ged
            max_ged = max(max_ged, min_ged)
        return max_ged

    def execute(self, graph1, graph2):
        nx_graph1 = graph1.convert_networkx()
        nx_graph2 = graph2.convert_networkx()
        if self.mode == 'angle':
            ged = nx.algorithms.similarity.graph_edit_distance(nx_graph1, nx_graph2, timeout=self.timeout,
                                                               edge_del_cost=lambda e: e['length'],
                                                               edge_ins_cost=lambda e: e['length'],
                                                               edge_subst_cost=lambda e1, e2: abs(
                                                                   e1['length'] - e2['length']),
                                                               node_del_cost=lambda n: n['weight'],
                                                               node_ins_cost=lambda n: n['weight'],
                                                               node_subst_cost=lambda n1, n2: abs(
                                                                   n1['weight'] - n2['weight']))
        elif self.mode == 'position':
            ged = nx.algorithms.similarity.graph_edit_distance(nx_graph1, nx_graph2, timeout=self.timeout,
                                                               edge_del_cost=lambda e: e['length'],
                                                               edge_ins_cost=lambda e: e['length'],
                                                               edge_subst_cost=lambda e1, e2: abs(
                                                                   e1['length'] - e2['length']),
                                                               node_del_cost=lambda n: 1,
                                                               node_ins_cost=lambda n: 1,
                                                               node_subst_cost=lambda n1, n2: euclidean_distance(
                                                                   n1['position'], n2['position']))
        else:
            raise RuntimeError('Invalid GED mode')
        return ged
