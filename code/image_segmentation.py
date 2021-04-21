import os
import argparse
import numpy as np
from skimage import io, img_as_ubyte
from sklearn.cluster import KMeans


def parse_args():
    """
    Allow user to specify image, k, and output
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', help='path to data file',
                        nargs='?', default='../data/irises.jpeg')
    parser.add_argument(
        '-k', help='number of image cluster from [4,7]', nargs='?', type=int, default=4)
    parser.add_argument('-o', help='output image file',
                        nargs='?', default='output.jpg')
    return parser.parse_args()


def image_difference(original, compressed):
    """
    Return the difference between the original image and compressed image
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


def assign_new_colors_by_luminance(centroids, new_colors):
    new_colors = np.divide(new_colors, 255)
    centroid_luminance = []
    new_luminance = []
    new_colors_sorted = np.zeros((new_colors.shape[0], new_colors.shape[1]))
    # calculate luminance
    for i in range(centroids.shape[0]):
        centroid_luminance.append(
            0.2126*centroids[i, 0] + 0.7152*centroids[i, 1] + 0.0722*centroids[i, 2])
        new_luminance.append(
            0.2126*new_colors[i, 0] + 0.7152*new_colors[i, 1] + 0.0722*new_colors[i, 2])
    centroid_indices = np.argsort(centroid_luminance)
    new_color_indices = np.argsort(new_luminance)
    # reassign indices of new_color to match centroids
    for index in new_color_indices:
        new_colors_sorted[centroid_indices[index],
                          :] = new_colors[new_color_indices[index], :]
    return new_colors_sorted

def naive_palette(centroids, new_color):
    new_color = np.divide(new_color, 255)
    index = 0
    new_colors = np.zeros((centroids.shape[0], centroids.shape[1]))
    # compare luminance to find where new_color should appear
    new_luminance = 0.2126*new_color[0] + 0.7152*new_color[1] + 0.0722*new_color[2]
    min_dist = 10000000000
    for i in range(centroids.shape[0]):
        centroid_luminance = 0.2126*centroids[i, 0] + 0.7152*centroids[i, 1] + 0.0722*centroids[i, 2]
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

def cluster(k, image):
    print("Clustering")

    X = image.reshape(image.shape[0]*image.shape[1], 3)
    K = k

    kmeans = KMeans(n_clusters=K, max_iter=20)
    kmeans.fit(X)
    centroids = kmeans.cluster_centers_
    print(centroids)

    return kmeans, centroids


def run_clustering(k, image):
    kmeans, centroids = cluster(k, image)
    idx = kmeans.labels_
    X_recovered = centroids[idx]
    X_recovered = np.reshape(X_recovered, (image.shape[0], image.shape[1], 3))

    print("Recoloring")
    # let user pick all colors
    # new_colors = [[186, 199, 219], [116, 96, 150],
    #               [209, 145, 82], [220, 232, 209]]
    # new_colors = assign_new_colors_by_luminance(centroids, new_colors)

    # naive palette picker given one color
    new_color = [247, 146, 242]
    new_colors = naive_palette(centroids, new_color)

    X_recovered = naive_recolor(image, X_recovered, idx, new_colors)
    X_recovered = np.clip(X_recovered, 0, 1)
    print("Output saved to output/" + "output.jpeg")
    io.imsave("output/" + "output.jpeg", img_as_ubyte(X_recovered))
    io.imsave("static/" + "output.jpeg", img_as_ubyte(X_recovered))
    print("DONE")
    return "static/output.jpeg"


def main():
    args = parse_args()

    image = io.imread(args.d)
    image = image/255
    run_clustering(args.k, image)

    io.imshow("output/output.jpeg")
    io.show()

    # webbrowser.open(
    #     'file://' + os.path.realpath('../frontend/index.html'), new=2)


if __name__ == '__main__':
    main()
