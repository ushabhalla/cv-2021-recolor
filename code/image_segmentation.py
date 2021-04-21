import os
from skimage import io, img_as_ubyte
import numpy as np
from sklearn.cluster import KMeans
import argparse
import random
import webbrowser


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', help='path to data file', nargs='?',
                        default='../data/lotus.jpeg')
    parser.add_argument(
        '-o', help='path to output directory', nargs='?', default='output')
    parser.add_argument(
        'k', help='number of k means clusters', nargs='?', default=4)
    parser.add_argument(
        '--gui', help='GUI', nargs='?', default='False')
    return parser.parse_args()


def image_distance(original, compressed):
    """
    Calculates the pixel element-wise (pixel-by-pixel) difference and normalizes
    the result

    :param original: original image
    :param compressed: compressed image
    :return: distance from each pixel in image and clustered image
    """
    return original-compressed


def naive_recolor(image, clustered_image, indices, new_colors):
    image = image_distance(image, clustered_image)
    indices = np.reshape(indices, (image.shape[0], image.shape[1]))
    for i in range(clustered_image.shape[0]):
        for j in range(clustered_image.shape[1]):
            image[i, j] += new_colors[indices[i, j]]
    return image


def run_kmeans(arg_k, arg_d):
    print("RUNNING KMEANS")
    image = io.imread(arg_d)
    # Get the number of rows and columns
    rows = image.shape[0]
    cols = image.shape[1]
    # Normalize all the pixels by dividing all datapoints by 255
    image = image/255

    # make sure image is 3 dimensions, not 4
    dimension = image.shape[-1]
    print('image dimension is:', dimension)

    if dimension != 3:
        if (dimension == 4):
            image = image[:, :, :3]
        else:
            print('image is not valid')

    # Reshape the image so that the data points have 3 attributes, corresponding to RGB values (for each pixel)
    X = image.reshape(image.shape[0]*image.shape[1], 3)

    # Number of clusters
    K = int(arg_k)
    # Maximum number of times KMeans should run
    max_iters = 20

    # Create an instance of the KMeans class
    kmeans = KMeans(n_clusters=K, max_iter=max_iters).fit(X)
    # Run the instance of the KMeans class on the data X, with K clusters and max_iters
    print("Running k-means")
    centroids = kmeans.cluster_centers_
    idx = kmeans.labels_

    # Get the compressed version of data X
    X_recovered = centroids[idx]

    # print(f"Image Distance: {image_distance(X, X_recovered)}")

    # Reshape X_recovered into a 1-dimensional np array in order for io to display
    X_recovered = np.reshape(X_recovered, (rows, cols, 3))
    new_colors = [[.937, .258, .96], [.25, .96, .25],
                  [.3, .4, .5], [.12, .23, .45]]
    X_recovered = naive_recolor(image, X_recovered, idx, new_colors)

    io.imshow(X_recovered)
    io.show()

    # Save the compressed version of the original image
    io.imsave(args.o + "/output2.jpg", img_as_ubyte(X_recovered))
    print("Saved compressed image")


def main():
    args = parse_args()
    # Use io to read in the image pixel data

    webbrowser.open(
        'file://' + os.path.realpath('../frontend/index.html'), new=2)

    if args.gui == 'False':
        run_kmeans(args.k, args.d)
    else:
        args.d = None
        args.k = None


if __name__ == '__main__':
    main()
