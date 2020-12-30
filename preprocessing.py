import numpy as np
import skimage
from skimage import morphology, transform


def resize(image, shape):
    return transform.resize(image, shape)


def binarize(image, threshold=0.5):
    return np.array(image > threshold, dtype=float)


def invert(image):
    return skimage.util.invert(image)


def skeletonize(image):
    return morphology.skeletonize(image)
