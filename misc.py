import numpy as np
from skimage import io


def imread(img_path):
    return io.imread(img_path, as_gray=True)


def imsave(image_path, image):
    io.imsave(image_path, image, check_contrast=False)


def make_interval(val, max_val, min_val=0):
    if val < min_val:
        return min_val
    elif val >= max_val:
        return max_val-1
    else:
        return val