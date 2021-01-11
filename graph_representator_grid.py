import numpy as np

from misc import *


class GraphRepresentatorGrid:
    def __init__(self, skeleton, cell_length):
        self.cell_length = cell_length
        self.skeleton = skeleton
        self.grid = np.zeros((skeleton.shape[0] // cell_length,
                              skeleton.shape[1] // cell_length))
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                self.grid[i, j] = np.any(skeleton[cell_length * i:cell_length * (i + 1),
                                         cell_length * j:cell_length * (j + 1)])
        self.baricenters = []
        self.calculate_baricenters()

    def calculate_baricenters(self):
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
                    self.baricenters[i].append((baricenter_i, baricenter_j))
                else:
                    self.baricenters[i].append(None)

    def represent_graph_no_grid_connection(self):
        graph = np.zeros(self.skeleton.shape)
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[make_interval(i, self.grid.shape[0]),
                             make_interval(j, self.grid.shape[1])]:
                    for di in (-1, 0, 1):
                        for dj in (-1, 0, 1):
                            if self.grid[make_interval(i + di, self.grid.shape[0]),
                                         make_interval(j + dj, self.grid.shape[1])]:
                                draw_line(graph, self.baricenters[i][j],
                                          self.baricenters[make_interval(i + di, self.grid.shape[0])]
                                          [make_interval(j + dj, self.grid.shape[1])])
        self.draw_dots(graph, 2)
        return graph

    def represent_graph(self):
        graph = np.zeros(self.skeleton.shape)
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[make_interval(i, self.grid.shape[0]),
                             make_interval(j, self.grid.shape[1])]:
                    # cardinal directions
                    for di, dj in ((0, 1), (1, 0)):
                        if i - dj >= 0 and j - di >= 0:
                            found_connection = False
                            for k in range(self.cell_length):
                                if self.skeleton[self.cell_length * i + k * di, self.cell_length * j + k * dj]:
                                    for dk in (-1, 0, 1):
                                        if self.skeleton[self.cell_length * i
                                                         + make_interval(k + dk, self.cell_length) * di - dj,
                                                         self.cell_length * j
                                                         + make_interval(k + dk, self.cell_length) * dj - di]:
                                            found_connection = True
                            if found_connection:
                                draw_line(graph, self.baricenters[i][j], self.baricenters[i - dj][j - di])
                    # diagonal directions
                    if i > 0 and j > 0 and self.skeleton[self.cell_length * i - 1, self.cell_length * j - 1]:
                        draw_line(graph, self.baricenters[i][j], self.baricenters[i - 1][j - 1])
                    if i > 0 and j < len(self.baricenters[0]) - 1 \
                            and self.skeleton[self.cell_length * i - 1, self.cell_length * (j + 1)]:
                        draw_line(graph, self.baricenters[i][j], self.baricenters[i - 1][j + 1])
        self.draw_dots(graph, 2)
        return graph

    def draw_dots(self, graph, radius):
        for row in self.baricenters:
            for point in row:
                if point is not None:
                    draw_dot(graph, point, radius)
