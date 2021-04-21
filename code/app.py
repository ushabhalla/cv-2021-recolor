from flask import Flask, render_template, request
import json

from image_segmentation import run_clustering
from skimage import io, img_as_ubyte
import matplotlib.colors

curr_img = None

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/getmethod')
def get_javascript_data(jsdata):
    return curr_img


@app.route('/postmethod', methods=['POST'])
def get_post_javascript_data():
    image = request.form['image']
    k = request.form['kk']
    col1 = matplotlib.colors.to_rgb(request.form['col1'])
    c1 = [col1[0]*255, col1[1]*255, col1[2]*255]
    col2 = matplotlib.colors.to_rgb(request.form['col2'])
    c2 = [col2[0]*255, col2[1]*255, col2[2]*255]
    col3 = matplotlib.colors.to_rgb(request.form['col3'])
    c3 = [col3[0]*255, col3[1]*255, col3[2]*255]
    col4 = matplotlib.colors.to_rgb(request.form['col4'])
    c4 = [col4[0]*255, col4[1]*255, col4[2]*255]
    col5 = matplotlib.colors.to_rgb(request.form['col5'])
    c5 = [col5[0]*255, col5[1]*255, col5[2]*255]
    col6 = matplotlib.colors.to_rgb(request.form['col6'])
    c6 = [col6[0]*255, col6[1]*255, col6[2]*255]
    colors = [c1, c2, c3, c4, c5, c6]

    print(colors)
    k = int(k)
    img = io.imread(image)
    img = img/255
    image = run_clustering(k, img, colors)
    curr_img = image
    return image


if __name__ == '__main__':
    app.run()
