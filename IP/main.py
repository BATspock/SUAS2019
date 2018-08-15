#import dependencies
import cv2
import numpy as np 
import os
import pandas as pd
import pickle
import time
from scipy.misc import imread, imresize

def kmeans(im, no_of_clusters):
    Z = im.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(Z, no_of_clusters,None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    return(res.reshape((im.shape)), center)


#path to image folder
image_folder_path = 'images/'
img = os.listdir(image_folder_path)
#clf = pickle.load(open('../../SVMSavedModelF.pickle', 'rb'))

#count false positives in case of no target 
fasle_positives = 0
somei = 0
#for all the images in the folder
for im in img:
    i = cv2.imread(image_folder_path + str(im))
    #resize to 1000 X 800
    rx=i.shape[1]/1000
    ry=i.shape[0]/800
    i=cv2.resize(i, (int(i.shape[1]/rx),int(i.shape[0]/ry)))
    #make copy of original image for checking
    io = i.copy()
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
    #apply blur 
    i = cv2.GaussianBlur(i,(5,5), 0)
    #apply morpholgical operations
    #define kernel
    kernel = np.ones((5,5),np.uint8)
    i = cv2.morphologyEx(i, cv2.MORPH_CLOSE, kernel)
    #apply canny to detect edges
    i = cv2.Canny(i, 70, 100)
    #find contours in case no contour detected
    try:
        _,contour,_ = cv2.findContours(i.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #sort contours by area
        contour = sorted(contour, key=cv2.contourArea, reverse=True)[:5]
        #print(contour)
        #draw contours to check results // not necessary
        #cv2.drawContours(io, contour, -1, (0,255,122), 2)
        #create bounding boxes
        #pad to crate extra space
        pad = 50
        j = 0
        for cnt in contour:
            #print(j)
            x,y,w,h = cv2.boundingRect(cnt)
            #cv2.rectangle(io,(x-pad,y-pad),(x+w+pad,y+h+pad),(0,255,0),2)
            
            cv2.imwrite('croppedImages/' + str(im) +  str(j) + '.png', io[y-pad:y+h+pad, x-pad:x+w+pad])
            x1 = io[y-pad:y+h+pad, x-pad:x+w+pad]
            #lst = list((x.shape))
            
            smallsiz = np.min(x1.shape[:2])
            if smallsiz == 0:
                continue

            ### SIMPLE IMAGE CALCULATIONS:
	    # Create Folder called mbst to store cropped images
            #Apply k-means for image giving 2 clusters
            #Get the locations of all pixels belonging to each colour.
            # Take the mean distance from the center for both colours and subtract
            # For non-target images, the difference is very small, since both colours are randomly distributed
            # For target images, the difference between mean location of target object and the non target object is significantly high 
            

            x = imresize(x1, (72, 72, 3))
            x = x[4:68,4:68]
            z1,z2 = kmeans(x,2)
            indices1 = np.where(np.all(z1 == z2[0] , axis=-1))
            indices2 = np.where(np.all(z1 == z2[1] , axis=-1))
            diff1 = abs(np.mean(abs(indices1[0]-32)) - np.mean(abs(indices2[0]-32)))
            
            #cv2.imshow('abc',x)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            if diff1 > 7 :
                somei += 1
                cv2.imwrite('MBST/' + str(somei) + '.png', x)
            #j+=1

            

    #incase no contours are detected increase count of false positives
    except:
        print(j)
        fasle_positives +=1
        print('No target detected!!')
        continue

    #display edge image
    cv2.imshow('', io)
    #display final operational image
    cv2.imshow("t", i)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    

