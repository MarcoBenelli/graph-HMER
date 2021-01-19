import numpy as np

import preprocessing
from graph_representator_grid import GraphRepresentatorGrid
from graph_representator_polygon import GraphRepresentatorPolygon
from misc import *


class GraphRepresentatorFactory:
    def __init__(self, image_height=512, threshold=0.25, polygon_tolerance=10, cell_length=32):
        self.polygon_tolerance = polygon_tolerance
        self.cell_length = cell_length
        self.image_height = image_height
        self.threshold = threshold

    def build_graph(self, images_path, image_name, graph_polygon_path=None, skeletons_path=None, graph_grid_path=None):
        image = imread(images_path + image_name)
        image_resized = preprocessing.resize(image,
                                             (self.image_height, image.shape[1] * self.image_height // image.shape[0]))
        image_binarized = preprocessing.binarize(image_resized, self.threshold)
        image_inverted = preprocessing.invert(image_binarized)
        image_skeletonized = preprocessing.skeletonize(image_inverted)
        if skeletons_path is not None:
            imsave(skeletons_path + image_name, np.array(image_skeletonized * 255, dtype=np.uint8))

        grp = GraphRepresentatorPolygon(image_inverted, self.polygon_tolerance, image_name)
        graph_image_polygon = grp.represent_graph()

        if graph_grid_path is not None:
            grg = GraphRepresentatorGrid(image_skeletonized, self.cell_length)
            graph_image_grid = grg.represent_graph()
            imsave(graph_grid_path + image_name,
                   np.array(graph_image_grid * 255, dtype=np.uint8))
        if graph_polygon_path is not None:
            imsave(graph_polygon_path + image_name,
                   np.array(graph_image_polygon * 255, dtype=np.uint8))

        return grp
