#the following class is used to detect the shape of the largest contour detected in the image
#this is an iterative developement request other members to complete it especially for circles
#and objeccts with black bg
#this first version on Jan 24,2019 is just for facilitaing integration purpose
#Also "General Kenobi, Hello there!", "The needs of the many outweigh the needs of the few or the one"--Spock
#and "Trust no one" -- Batman

import cv2
import numpy as np 
from preprocess import preprocess

class ShapeDetector(object):
    def __init__(self, image_path):
        """
        input: path of image 
        """
        
        self.path = image_path
        self.im = cv2.imread(self.path)

    def detectshape(self):
        """
        output: the biggest shape detected in the image on the basis of perimeter

        """
        #preprocess the image to get the shape present 
        im_copy = self.im.copy()
        ob = preprocess(self.im)
        self.im, _ = ob.kmeans(3) #apply kmeans to remove background and foreground noise
        ob = preprocess(self.im)
        self.im = ob.GaussianBlur() #blur to enhance the edges
        ob = preprocess(self.im)
        self.im = ob.ChangeContrast(0.1) #contrast to bring out the shape

        self.im = cv2.Canny(self.im, 0, 127)#apply canny to detect edges
        _,contours,_ = cv2.findContours(self.im.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#detect exteranl contour
        
        contours = contours[0] #unpack the contour list
        
        shape = ""
        peri = cv2.arcLength(contours, True)
        approx = cv2.approxPolyDP(contours, 0.04*peri, True)#approximate the contour
    
        if len(approx) == 3:
            shape = "triangle"

        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            shape = "square" if ar >= 0.8 and ar <= 1.2 else "rectangle"
            
        elif len(approx) == 5:
            shape = "pentagon"

        elif len(approx) == 6:
            shape = "hexagon"

        #make quadrant and semicircle
        else:
            shape = "circle"
        
        
        return shape