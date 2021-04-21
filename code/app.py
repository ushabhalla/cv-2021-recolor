from flask import Flask, render_template, request
import json

from image_segmentation import run_kmeans

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

    run_kmeans(k, image)
    curr_img = image
    return image


if __name__ == '__main__':
    app.run()
