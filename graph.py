import numpy as np
import networkx as nx

from misc import *


class Graph:
    def __init__(self, coords_lists, shape):
        self.coords_lists = coords_lists
        self.shape = shape

    def get_image(self):
        image = np.zeros(self.shape)
        for coords in self.coords_lists:
            for i in range(len(coords) - 1):
                draw_line(image, coords[i], coords[i + 1])
                draw_dot(image, coords[i], 2)
            draw_line(image, coords[-1], coords[0])
            draw_dot(image, coords[-1], 2)
        return image

    def convert_networkx(self):
        assert len(self.coords_lists) == 1
        g = nx.Graph()
        g.add_node(0)
        for i, coord in enumerate(self.coords_lists[0][1:]):
            g.add_node(i + 1)
            g.add_edge(i, i + 1)
        g.add_edge(len(self.coords_lists[0]) - 1, 0)
        return g

    def normalize(self):
        min_i = np.inf
        min_j = np.inf
        max_i = 0
        max_j = 0
        for coords in self.coords_lists:
            min_i = min(min_i, min(coord[0] for coord in coords))
            min_j = min(min_j, min(coord[1] for coord in coords))
            max_i = max(max_i, max(coord[0] for coord in coords))
            max_j = max(max_j, max(coord[1] for coord in coords))
        di = max_i - min_i
        dj = max_j - min_j
        scale_factor = max(di, dj) / 100  # tmp
        if scale_factor == 0:
            return Graph([[(0, 0)]], (100, 100))
        coords_lists = []
        for coords in self.coords_lists:
            coords_lists.append([])
            for coord in coords:
                coords_lists[-1].append((int((coord[0] - min_i) // scale_factor),
                                         int((coord[1] - min_j) // scale_factor)))  # TODO remove /
        # print(coords_lists)
        return Graph(coords_lists, (100, 100))
