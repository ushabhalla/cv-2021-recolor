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
    parser.add_argument('-d', help='path to data file', default='../data/irises.jpeg')
    parser.add_argument('-k', help='number of image cluster from [4,7]', type=int, default=4)
    parser.add_argument('-o', help='output image file', default='output.jpg')
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



def paper_thing():
    """
    first init kmeans with white and black cluster centers with init

    """
    pass



def main():
    args = parse_args()

    image = io.imread(args.d)
    image = image/255

    X = image.reshape(image.shape[0]*image.shape[1], 3)
    K = args.k


    print("Clustering")
    kmeans = KMeans(n_clusters=K, max_iter=20)
    kmeans.fit(X)

    centroids = kmeans.cluster_centers_
    print(centroids)
    idx = kmeans.labels_
    X_recovered = centroids[idx]
    X_recovered = np.reshape(X_recovered, (image.shape[0], image.shape[1], 3))

    print("Recoloring")
    new_colors = [[186, 199, 219], [116, 96, 150], [209, 145, 82], [220, 232, 209]]
    new_colors = np.array(new_colors)/255
    X_recovered = naive_recolor(image, X_recovered, idx, new_colors)
    X_recovered = np.clip(X_recovered, 0, 1)

    io.imshow(X_recovered)
    io.show()

    print("Output saved to output/" + args.o)
    io.imsave("output/" + args.o, img_as_ubyte(X_recovered))


if __name__ == '__main__':
    main()
