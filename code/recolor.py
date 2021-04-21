import numpy as np

def image_difference(original, clustered):
    """
    Return the difference normalized between the original image and clustered image. This removes the original color from the image so that new color can be added. The normalization helps preserve some of the edges or outlines in the image that are not present in the clustering.

    :param original: the original image
    :param clustered: the clustered image
    :return: an array of image size
    """
    dist = original-clustered
    max_val = np.max(dist)
    return dist/max_val/2


def recolor_image(image, clustered_image, indices, new_colors):
    """
    Recolor the image using specified new_colors.

    :param image: the original image
    :param clustered_image: the clustered image
    :param indices: the labels of each pixel from clustering
    :param new_colors: [k x 3] array of the new colors for each segment
    :return: an array of size image recolored
    """
    # image = image_difference(image, clustered_image)
    # reshape indices to be same shape as image
    indices = np.reshape(indices, (image.shape[0], image.shape[1]))
    for i in range(clustered_image.shape[0]):
        for j in range(clustered_image.shape[1]):
            # add color of the correct label to the image
            image[i, j] += new_colors[indices[i, j]]
    return image


def sort_luminance(centroids, new_colors):
    """
    Sort the luminance of the centroids and the new_colors.

    :param centroids: [k x 3] array of centroid rgb values
    :param new_colors: [k x 3] array of new colors rgb values
    :return: indices of sorted centroids and new_colors arrays
    """
    centroid_luminance = []
    new_luminance = []
    # calculate luminance for each centroid and new color
    for i in range(centroids.shape[0]):
        centroid_luminance.append(
            0.2126*centroids[i, 0] + 0.7152*centroids[i, 1] + 0.0722*centroids[i, 2])
        new_luminance.append(
            0.2126*new_colors[i, 0] + 0.7152*new_colors[i, 1] + 0.0722*new_colors[i, 2])
    centroid_indices = np.argsort(centroid_luminance)
    new_color_indices = np.argsort(new_luminance)
    return centroid_indices, new_color_indices


def assign_new_colors_by_luminance(centroids, new_colors):
    """
    Sorts the new_colors such that the index of each new_color is most closely associated with the luminance of the centroid at that index.

    :param centroids: [k x 3] array of centroid rgb values
    :param new_colors: [k x 3] array of new colors rgb values
    :return: array of the new_colors rgb values sorted to match centroids
    """
    # normalize the new_colors
    new_colors = np.divide(new_colors, 255)
    new_colors_sorted = np.zeros((new_colors.shape[0], new_colors.shape[1]))
    # get the sorted indices based on luminance
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

def naive_tint_palette(centroids, new_color):
    """
    Recolor entire image given one new color. Essentially just tints the image to that color. This was an attempt at implementing the recoloring function from this paper: https://gfx.cs.princeton.edu/pubs/Chang_2015_PPR/chang2015-palette_small.pdf, but naively because the colors are clipped to the gamut. Also this recolors each centroid,not just one feature.

    :param centroids: [k x 3] array of centroid rgb values
    :param new_colors: [1 x 3] array of the new color rgb values
    :return: 2d array of the new_colors rgb values
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
    """ 
    Recolor one segment of the image to new_color. This is similar to naive_tint_palette, but rather than recoloring each segment, only one is recolored and the rest of the image remains the same.

    :param centroids: [k x 3] array of centroid rgb values
    :param new_colors: [1 x 3] array of the new color rgb values
    :return: 2d array of the new_colors rgb values
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
    # only set one cluster to new_color
    for i in range(centroids.shape[0]):
        if i == index:
            new_colors[i] = new_color
        else:
            new_colors[i] = centroids[i]
    return new_colors
