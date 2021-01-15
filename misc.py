from skimage import io


def imread(img_path):
    return io.imread(img_path, as_gray=True)


def imsave(image_path, image):
    io.imsave(image_path, image, check_contrast=False)


def make_interval(val, max_val, min_val=0):
    if val < min_val:
        return min_val
    elif val >= max_val:
        return max_val - 1
    else:
        return val


def draw_line(image, point1, point2):
    n = max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))
    for k in range(n):
        current_i = make_interval(point1[0] + k * (point2[0] - point1[0]) // n, image.shape[0])
        current_j = make_interval(point1[1] + k * (point2[1] - point1[1]) // n, image.shape[1])
        image[current_i, current_j] = 1


def draw_dot(image, point, radius):
    image[max(point[0] - radius, 0): min(point[0] + radius, image.shape[0]),
          max(point[1] - radius, 0): min(point[1] + radius, image.shape[1])] = 1


def multiply_coord(point, scalar):
    return tuple(int(coord * scalar) for coord in point)


def vect_norm(x):
    return sum(i ** 2 for i in x) ** (1 / 2)
