import numpy as np
import networkx as nx

from misc import *


class Graph:
    def __init__(self, coords_lists, shape=(1, 1)):
        self.coords_lists = coords_lists
        self.shape = shape

    def get_image_normalized(self, size):
        image = np.zeros((size, size), dtype=int)
        for coords in self.coords_lists:
            for i in range(len(coords) - 1):
                draw_line(image, multiply_coord(coords[i], size), multiply_coord(coords[i + 1], size))
                draw_dot(image, multiply_coord(coords[i], size), 2)
            draw_line(image, multiply_coord(coords[-1], size), multiply_coord(coords[0], size))
            draw_dot(image, multiply_coord(coords[-1], size), 2)
        return image

    def get_image_full(self):
        image = np.zeros(self.shape, dtype=int)
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
        g.add_node(0, position=self.coords_lists[0][0], weight=self.get_node_weight(0))
        for i, coord in enumerate(self.coords_lists[0][1:]):
            g.add_node(i + 1, position=self.coords_lists[0][i + 1], weight=self.get_node_weight(i + 1))
            g.add_edge(i, i + 1, length=self.get_edge_length(i))
        g.add_edge(len(self.coords_lists[0]) - 1, 0, length=self.get_edge_length(-1))
        return g

    def get_edge_length(self, i):
        return (self.coords_lists[0][i][0] - self.coords_lists[0][(i + 1) % len(self.coords_lists[0])][0]) ** 2 + (
                self.coords_lists[0][i][1] - self.coords_lists[0][(i + 1) % len(self.coords_lists[0])][1]) ** 2

    def get_node_weight(self, i):
        vect1x = self.coords_lists[0][(i + 1) % len(self.coords_lists[0])][0] - self.coords_lists[0][i][0]
        vect1y = self.coords_lists[0][(i + 1) % len(self.coords_lists[0])][1] - self.coords_lists[0][i][1]
        vect2x = self.coords_lists[0][i][0] - self.coords_lists[0][(i - 1) % len(self.coords_lists[0])][0]
        vect2y = self.coords_lists[0][i][1] - self.coords_lists[0][(i - 1) % len(self.coords_lists[0])][1]
        if vect_norm((vect1x, vect1y)) == 0 or vect_norm((vect2x, vect2y)) == 0:
            return 0
        cosine = ((vect1x * vect2x) + (vect1y * vect2y)) / (vect_norm((vect1x, vect1y)) * vect_norm((vect2x, vect2y)))
        return (1 - cosine) / 2

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
        scale_factor = max(di, dj)
        if scale_factor == 0:
            return Graph([[(0, 0)]])
        coords_lists = []
        for coords in self.coords_lists:
            coords_lists.append([])
            for coord in coords:
                coords_lists[-1].append(((coord[0] - min_i) / scale_factor,
                                         (coord[1] - min_j) / scale_factor))
        return Graph(coords_lists)
