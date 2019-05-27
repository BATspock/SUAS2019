from flask import Flask, render_template, request, redirect
import gui_imageops
import numpy as np
import sys
sys.path.append('/Users/nayana/projects/flask1/interop/client')
from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2

import AdvancedHTMLParser

path = '/Users/nayana/projects/flask1/Nayana_trial/static/images'

parser = AdvancedHTMLParser.AdvancedHTMLParser()
parser.parseFile('/Users/nayana/projects/flask1/Nayana_trial/templates/html/gui_form.html')
myImage=parser.getElementById('MainImage')

app = Flask(__name__)
app.debug = True

colours = ['White', 'Black', 'Gray', 'Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Brown', 'Orange'] 
shapes = ['Circle', 'Semicircle', 'Quarter circle', 'Triangle','Square', 'Rectangle', 'Trapezoid', 'Pentagon', 'Hexagon', 'Heptagon', 'Octagon', 'Star', 'Cross']
orientations = ['N','NE','E','SE','S','SW','W','NW']
alphanumeric = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0']

dict_orient =	{"N":1, "NE":2, "E":3, "SE":4, "S":5, "SW":6, "W":7, "NW":8}

dict_shape =	{ "Circle":1, "Semicircle":2, "Quarter circle":3, "Triangle":4, "Square":5, "Rectangle":6, "Trapezoid":7, "Pentagon":8, "Hexagon":9, "Heptagon":10, "Octagon":11, "Star":12, "Cross":13}

dict_colour = {'White':1, 'Black':2, 'Gray':3, 'Red':4, 'Blue':5, 'Green':6, 'Yellow':7, 'Purple':8, 'Brown':9, 'Orange':10}

div_factor = 10000000

im = gui_imageops.ImageVals(0,[])

client = client.Client(url='http://127.0.0.1:8000',
                       username='testuser',
                       password='testpass')

@app.route('/', methods=['GET','POST'])
def dropdown():   
                 
    im.getimg(im.imageArray,im.imageIndex)
    
    if not im.imageArray:
       return "Folder is empty"
       
    else:
       fullpath = im.image_src(im.imageArray,im.imageIndex)
       x = im.image_src(im.imageArray,im.imageIndex).replace(path, '')
       latlon=im.metadata(im.imageArray,im.imageIndex)
       
       lat = latlon['lat']/div_factor
       lon = latlon['lon']/div_factor
       
       return render_template('html/gui_form.html', odlc_l_colours = colours, odlc_s_colours = colours, shapes = shapes,
       orientations = orientations, alphanumeric = alphanumeric, x=str('../../static/images') + x, path = fullpath, lat = lat, lon = lon) 
        
@app.route('/submitForm', methods=['GET','POST'])
def submit_form():
    result = request.form
    letter_colour= request.form['letter_colour']
    alphanumericval= request.form['alphanumeric']
    bg_colour= request.form['bg_colour']
    shapeval= request.form['shape']
    orientationval= request.form['orientation']
    
    send_image = im.image_src(im.imageArray,im.imageIndex)
    
    latlon=im.metadata(im.imageArray,im.imageIndex)
    
    odlc = interop_api_pb2.Odlc()
    
    odlc.type = interop_api_pb2.Odlc.STANDARD
    odlc.latitude=latlon.get('lat')/div_factor
    odlc.longitude=latlon.get('lon')/div_factor
    odlc.orientation = dict_orient[orientationval]
    odlc.shape=dict_shape[shapeval]
    odlc.shape_color=dict_colour[bg_colour]
    odlc.alphanumeric=alphanumericval
    odlc.alphanumeric_color=dict_colour[letter_colour]
    
    odlc = client.post_odlc(odlc)

    with open(send_image, 'rb') as f:
        image_data = f.read()
        client.put_odlc_image(odlc.id, image_data)  
    
    im.moveimg(im.imageArray,im.imageIndex)     
    
    return redirect("/")
    
@app.route('/previous', methods=['GET','POST'])
def previous_image():
    im.previousimg(im.imageArray,im.imageIndex,myImage)   
    return redirect("/")

@app.route('/next', methods=['GET','POST'])
def next_image():
    im.nextimg(im.imageArray,im.imageIndex,myImage)
    return redirect("/")
    
@app.route('/change', methods=['GET','POST'])
def delete_image():
    im.deleteimg(im.imageArray,im.imageIndex)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)