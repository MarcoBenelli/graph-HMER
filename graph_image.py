import numpy as np

from misc import *


class GraphImage:
    def __init__(self, skeleton, cell_length):
        self.cell_length = cell_length
        self.skeleton = skeleton
        self.grid = np.zeros((skeleton.shape[0] // cell_length,
                              skeleton.shape[1] // cell_length))
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                self.grid[i, j] = np.any(skeleton[cell_length * i:cell_length * (i + 1),
                                                  cell_length * j:cell_length * (j + 1)])

    def represent_nodes(self):
        graph = np.zeros(self.skeleton.shape)
        self.baricenters = []
        for i in range(self.grid.shape[0]):
            self.baricenters.append([])
            for j in range(self.grid.shape[1]):
                baricenter_i = 0
                baricenter_j = 0
                num_points = 0
                for cell_i in range(self.cell_length):
                    for cell_j in range(self.cell_length):
                        if self.skeleton[self.cell_length * i + cell_i, self.cell_length * j + cell_j]:
                            baricenter_i += self.cell_length * i + cell_i
                            baricenter_j += self.cell_length * j + cell_j
                            num_points += 1
                if num_points > 0:
                    baricenter_i //= num_points
                    baricenter_j //= num_points
                    graph[baricenter_i, baricenter_j] = 1
                    self.baricenters[i].append((baricenter_i, baricenter_j))
                else:
                    self.baricenters[i].append(None)
        return graph

    def represent_graph_simple(self):
        graph = np.zeros(self.skeleton.shape)
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[make_interval(i, self.grid.shape[0] - 1),
                             make_interval(j, self.grid.shape[1] - 1)]:
                    for di in (-1, 0, 1):
                        for dj in (-1, 0, 1):
                            if self.grid[make_interval(i + di, self.grid.shape[0] - 1),
                                         make_interval(j + dj, self.grid.shape[1] - 1)]:
                                self.draw_line(graph,
                                               self.baricenters[i][j],
                                               self.baricenters[make_interval(i + di, self.grid.shape[0] - 1)]
                                                               [make_interval(j + dj, self.grid.shape[1] - 1)])
        return graph

    def draw_line(self, image, point1, point2):
        n = max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))
        for k in range(n):
            current_i = make_interval(point1[0] + k * (point2[0] - point1[0]) // n, image.shape[0] - 1, 0)
            current_j = make_interval(point1[1] + k * (point2[1] - point1[1]) // n, image.shape[1] - 1, 0)
            image[current_i, current_j] = 1

    # TODO
    def generate_graph(self):
        graph = np.zeros(self.skeleton.shape)
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                graph[self.cell_length * i + self.cell_length // 2,
                      self.cell_length * j + self.cell_length // 2] = self.grid[i, j]
                if self.grid[make_interval(i, self.grid.shape[0] - 1),
                        make_interval(j, self.grid.shape[1] - 1)]:
                    # cardinal directions
                    for di, dj in ((0, 1), (1, 0)):
                        found_connection = False
                        for k in range(self.cell_length):
                            if self.skeleton[self.cell_length * i + k * di, self.cell_length * j + k * dj]:
                                for dk in (-1, 0, 1):
                                    if self.skeleton[self.cell_length * (i + di) - k * di, self.cell_length * (j + dj) - k * dj]:
                                        found_connection = True
                        if found_connection:
                            self.draw_line(graph, self.cell_length * i + self.cell_length // 2,
                                           self.cell_length * j + self.cell_length // 2,
                                           di, dj, self.cell_length)
        return graph
