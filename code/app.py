from flask import Flask, render_template, request
import json

from image_segmentation import run_clustering
from skimage import io as io_skimage
from skimage import img_as_ubyte
import matplotlib.colors

from PIL import Image
import urllib.request
from io import BytesIO
import base64 


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
    user_image_loaded = request.form['userImage']

    print(colors)
    print('image true?', user_image_loaded)
    k = int(k)

    # print('image before:', image)
    if (user_image_loaded == '1'):
        im = Image.open(BytesIO(base64.b64decode(image)))
        im.save('image.png', 'PNG')
        img = io_skimage.imread('image.png')
    else:
        print('this is running')
        img = io_skimage.imread(image)
    
    img = img/255
    #make sure image is 3 dimensions, not 4    
    dimension = img.shape[-1]
    print('image dimension is:', dimension)
    if dimension != 3:
        if (dimension == 4):
            img = img[:,:,:3]
        else:
            print('image is not valid')

    outout_image = run_clustering(k, img, colors)
    print('post done')
    return outout_image

if __name__ == '__main__':
    app.run()
