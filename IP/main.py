#import dependencies
import cv2
import numpy as np 
import os
#path to image folder
image_folder_path = '/home/adityakishore/workspace/SUAS2019/IP/images/'
img = os.listdir(image_folder_path)

#count false positives in case of no target 
fasle_positives = 0
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
        #draw contours to check results // not necessary
        #cv2.drawContours(io, contour, -1, (0,255,122), 2)

        #create bounding boxes
        #pad to crate extra space
        pad = 50
        j = 0
        for cnt in contour:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(io,(x-pad,y-pad),(x+w+pad,y+h+pad),(0,255,0),2)
            cv2.imwrite('/home/adityakishore/workspace/SUAS2019/IP/croppedImages/' + str(im) +  str(j) + '.png', io[y-pad:y+h+pad, x-pad:x+w+pad])
            j+=1

    #incase no contours are detected increase count of false positives
    except:
        fasle_positives +=1
        print('No target detected!!')
        continue

    #display edge image
    cv2.imshow('', io)
    #display final operational image
    cv2.imshow("t", i)
    cv2.waitKey(0)
    cv2.destroyAllWindows()