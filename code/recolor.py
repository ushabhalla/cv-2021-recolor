import numpy as np

def image_difference(original, compressed):
    """
    Return the difference normalized between the original image and compressed image. This 
    """
    dist = original-compressed
    max_val = np.max(dist)
    return dist/max_val/2


def naive_recolor(image, clustered_image, indices, new_colors):
    """
    Recolor the image using specified new_colors
    """
    image = image_difference(image, clustered_image)
    indices = np.reshape(indices, (image.shape[0], image.shape[1]))
    for i in range(clustered_image.shape[0]):
        for j in range(clustered_image.shape[1]):
            image[i, j] += new_colors[indices[i, j]]
    return image

def sort_luminance(centroids, new_colors):
    centroid_luminance = []
    new_luminance = []
    # calculate luminance
    for i in range(centroids.shape[0]):
        centroid_luminance.append(
            0.2126*centroids[i, 0] + 0.7152*centroids[i, 1] + 0.0722*centroids[i, 2])
        new_luminance.append(
            0.2126*new_colors[i, 0] + 0.7152*new_colors[i, 1] + 0.0722*new_colors[i, 2])
    centroid_indices = np.argsort(centroid_luminance)
    new_color_indices = np.argsort(new_luminance)
    return centroid_indices, new_color_indices

def assign_new_colors_by_luminance(centroids, new_colors):
    new_colors = np.divide(new_colors, 255)
    new_colors_sorted = np.zeros((new_colors.shape[0], new_colors.shape[1]))
    centroid_indices, new_color_indices = sort_luminance(centroids, new_colors)
    # reassign indices of new_color to match centroids
    for index in new_color_indices:
        new_colors_sorted[centroid_indices[index],
                          :] = new_colors[new_color_indices[index], :]
    return new_colors_sorted

# def luminance_transfer(centroids, new_colors):
#     centroid_indices, new_color_indices = sort_luminance(centroids, new_colors)
#     for color in new_colors:

# def solve_weights(centroids):
#     all_dists = []
#     for i in range(centroids.shape[0]):
#         for j in range(i, centroids.shape[0]):
#             all_dists.append(centroids[i] - centroids[j])
#     sigma_r = np.mean(all_dists)

def naive_palette(centroids, new_color):
    """ Currently this just tints the image by whatever new_color is
    """
    new_color = np.divide(new_color, 255)
    index = 0
    new_colors = np.zeros((centroids.shape[0], centroids.shape[1]))
    # compare luminance to find where new_color should appear
    new_luminance = 0.2126*new_color[0] + \
        0.7152*new_color[1] + 0.0722*new_color[2]
    min_dist = 10000000000
    for i in range(centroids.shape[0]):
        centroid_luminance = 0.2126 * \
            centroids[i, 0] + 0.7152*centroids[i, 1] + 0.0722*centroids[i, 2]
        if min_dist > abs(new_luminance - centroid_luminance):
            min_dist = abs(new_luminance - centroid_luminance)
            index = i
    # select palette by subtracting same distance from each value
    diff = new_color - centroids[index]
    for i in range(centroids.shape[0]):
        if i == index:
            new_colors[i] = new_color
        else:
            # clip colors to remain in gamut
            new_colors[i] = np.clip(centroids[i] + diff, 0, 1)
    return new_colors

def single_recolor(centroids, new_color):
    """ Currently this just tints the image by whatever new_color is
    """
    new_color = np.divide(new_color, 255)
    index = 0
    new_colors = np.zeros((centroids.shape[0], centroids.shape[1]))

    # if only one color is given, expand the dims
    if new_color.ndim == 1:
        np.expand_dims(new_color, 0)

    new_luminance = []
    for i in range(new_color.shape[0]):
        new_luminance.append(0.2126*new_color[i, 0] + 0.7152*new_color[i, 1] + 0.0722*new_color[i, 2])

    # compare luminance to find where new_color should appear
    min_dist = 10000000000
    for i in range(centroids.shape[0]):
        centroid_luminance = 0.2126 * \
            centroids[i, 0] + 0.7152*centroids[i, 1] + 0.0722*centroids[i, 2]
        if min_dist > abs(new_luminance - centroid_luminance):
            min_dist = abs(new_luminance - centroid_luminance)
            index = i
    # only set one cluster to new_color
    for i in range(centroids.shape[0]):
        if i == index:
            new_colors[i] = new_color
        else:
            new_colors[i] = centroids[i]
    return new_colors