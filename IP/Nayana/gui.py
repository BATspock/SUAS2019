from flask import Flask, render_template, request, redirect
import gui_imageops
import numpy as np
import sys
sys.path.append('/Users/nayana/projects/interop/client')
import interop
import AdvancedHTMLParser

path = '/Users/nayana/projects/flask1/GUI/static/images'

#Temp Data
imgdata = np.load('data.npy')

parser = AdvancedHTMLParser.AdvancedHTMLParser()
parser.parseFile('/Users/nayana/projects/flask1/GUI/templates/html/gui_form.html')
myImage=parser.getElementById('MainImage')

app = Flask(__name__)
app.debug = True

colours = ['White', 'Black', 'Gray', 'Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Brown', 'Orange'] 
shapes = ['Circle', 'Semicircle', 'Quarter circle', 'Triangle','Square', 'Rectangle', 'Trapezoid', 'Pentagon', 'Hexagon', 'Heptagon', 'Octagon', 'Star', 'Cross','None']
orientations = ['N','NE','E','SE','S','SW','W','NW']
alphanumeric = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']

def fixstr(param):
   return str(param).replace('[','').replace(']','').replace('\'','').replace('\'','').capitalize()

def del_add(l,val):
   l.remove(val)
   l.append(val)
   return l

im = gui_imageops.ImageVals(0,[])

client = interop.Client(url='http://127.0.0.1:8000',username='testuser', password='testpass')

@app.route('/', methods=['GET','POST'])
def dropdown():   
                 
    im.getimg(im.imageArray,im.imageIndex)
    if not im.imageArray:
       return "Folder is empty"
       
    else:   
       x = im.image_src(im.imageArray,im.imageIndex).replace(path, '')
       
       i,_ = np.where(imgdata==x[1:])
       
       lcol = imgdata[i, 1]
       alnum = imgdata[i, 2]
       scol = imgdata[i, 3]
       shp = imgdata[i, 4]
       
       #Remove unwanted characters
       
       scol = fixstr(scol)
       lcol = fixstr(lcol)
       shp = fixstr(shp)
       alnum = fixstr(alnum)
       
       odlc_l_colours = del_add(colours.copy(),str(lcol))
       odlc_s_colours = del_add(colours.copy(),str(scol))
       shapes1 = del_add(shapes,str(shp))
       alphanumeric1 = del_add(alphanumeric,alnum.lower())
       
       return render_template('html/gui_form.html', odlc_l_colours = odlc_l_colours, odlc_s_colours = odlc_s_colours, shapes = shapes1,
       orientations = orientations, alphanumeric = alphanumeric1, x=str('../../static/images') + x,
       letter_col = lcol, alnum = alnum, shape_col = scol, shapeval = shp) 
        
@app.route('/submitForm', methods=['GET','POST'])
def submit_form():
    result = request.form
    letter_colour= request.form['letter_colour']
    alphanumericval= request.form['alphanumeric']
    bg_colour= request.form['bg_colour']
    shapeval= request.form['shape']
    orientationval= request.form['orientation']
   
    print('Submitting '+letter_colour+' '+alphanumericval+' '+bg_colour+' '+shapeval)
    
    send_image = im.image_src(im.imageArray,im.imageIndex)
        
    odlc = interop.Odlc(type='standard',
                        latitude=38.145215,
                        longitude=-76.427942,
                        orientation=orientationval,
                        shape=shapeval,
                        background_color=bg_colour,
                        alphanumeric=alphanumericval,
                        alphanumeric_color=letter_colour)
                        
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
    app.run(debug = True)