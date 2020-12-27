def draw_line(image, i, j, di, dj, cell_length):
    for k in range(cell_length):
        current_i = make_interval(i + k * di, image.shape[0] - 1, 0)
        current_j = make_interval(j + k * dj, image.shape[1] - 1, 0)
        image[current_i, current_j] = 1


def make_interval(val, max_val, min_val=0):
    if val < min_val:
        return min_val
    elif val > max_val:
        return max_val
    else:
        return val
