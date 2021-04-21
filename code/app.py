from flask import Flask, render_template, request
import json

from image_segmentation import run_clustering
from skimage import io, img_as_ubyte

curr_img = None

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/getmethod')
def get_javascript_data(jsdata):
    return curr_img


@app.route('/postmethodlol', methods=['POST'])
def get_post_javascript_data():
    image = request.form['image']
    k = request.form['kk']
    k = int(k)
    img = io.imread(image)
    image = run_clustering(k, img)
    curr_img = image
    print('post done')
    return image


if __name__ == '__main__':
    app.run()
