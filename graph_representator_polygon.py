import numpy as np
from skimage import measure

from graph import Graph


class GraphRepresentatorPolygon:
    def __init__(self, binarized_image, tolerance, name):
        self.contours = measure.find_contours(binarized_image, 0.5)
        self.contours = [np.array(contour, dtype=int) for contour in self.contours]
        self.tolerance = tolerance
        self.name = name
        coords_lists = []
        for contour in self.contours:
            coords_lists.append(measure.approximate_polygon(contour, tolerance=self.tolerance))
        self.graph = Graph(coords_lists, binarized_image.shape)

    def represent_graph_normalized(self):
        return self.graph.get_image_normalized((64, 64))

    def represent_graph_full(self):
        return self.graph.get_image_full()
