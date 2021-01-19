from skimage import io
import matplotlib.pyplot as plt


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


def euclidean_distance(point1, point2):
    return sum((i1 - i2) ** 2 for i1, i2 in zip(point1, point2)) ** (1 / 2)


def interpolate_precision(recall, precision):
    interpolated_recall, interpolated_precision = [1], [0]
    max_precision = 0
    for i in range(1, len(recall)):
        if precision[i] > max_precision:
            interpolated_recall.append(recall[i])
            interpolated_precision.append(max_precision)
            max_precision = precision[i]
            interpolated_recall.append(recall[i])
            interpolated_precision.append(precision[i])
    interpolated_recall.append(0)
    interpolated_precision.append(1)
    return interpolated_recall, interpolated_precision


def plot_precision_recall(recall, precision, output_path):
    recall.reverse()
    precision.reverse()
    interpolated_recall, interpolated_precision = interpolate_precision(recall, precision)
    fig, ax = plt.subplots()
    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.plot(interpolated_recall, interpolated_precision)
    fig.savefig(output_path)
