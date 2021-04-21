import os
import argparse
import numpy as np
from skimage import io, img_as_ubyte
from sklearn.cluster import KMeans
import random
import string
import recolor


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

def cluster(k, image):
    print("Clustering")

    X = image.reshape(image.shape[0]*image.shape[1], 3)
    K = k

    kmeans = KMeans(n_clusters=K, max_iter=5)
    kmeans.fit(X)
    centroids = kmeans.cluster_centers_
    print("Centroids", centroids)

    return kmeans, centroids


def run_clustering(k, image, colors):
    kmeans, centroids = cluster(k, image)
    idx = kmeans.labels_
    X_recovered = centroids[idx]
    X_recovered = np.reshape(X_recovered, (image.shape[0], image.shape[1], 3))

    print("Recoloring")
    # new_colors = colors[:k]
    # print(new_colors)
    # new_colors = recolor.assign_new_colors_by_luminance(centroids, new_colors)
    
    # # naive palette picker given one color
    new_color = [247, 146, 242]
    # new_colors = recolor.naive_palette(centroids, new_color)
    new_colors = recolor.single_recolor(centroids, new_color)

    # recolor image
    X_recovered = recolor.naive_recolor(image, X_recovered, idx, new_colors)
    X_recovered = np.clip(X_recovered, 0, 1)
    rand_str = lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(n)])
    # Now to generate a random string of length 10
    s = rand_str(10)  
    print('random string', s)

    path = "static/" + s + ".jpeg"
    print("Output saved to output/" + path)

    io.imsave(path, img_as_ubyte(X_recovered))
    # io.imsave(path, img_as_ubyte(X_recovered))
    print("DONE")
    return path

def main():
    args = parse_args()

    image = io.imread(args.d)
    image = image/255
    path = run_clustering(args.k, image, [[186, 199, 219], [116, 96, 150],
                                   [209, 145, 82], [220, 232, 209]])

    io.imshow(path)
    io.show()

    # webbrowser.open(
    #     'file://' + os.path.realpath('../frontend/index.html'), new=2)


if __name__ == '__main__':
    main()
