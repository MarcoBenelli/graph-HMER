import numpy as np

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