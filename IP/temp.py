import cv2
import numpy as np
import os

image_folder_path = 'images/'

for image in os.listdir(image_folder_path):
	#print(image)
	img = cv2.imread(os.path.join(image_folder_path,image))
	#print(img)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imshow('Gray Scale', gray)
	#cv2.waitKey(0)
	gray = cv2.GaussianBlur(gray,(5,5), 0)
	cv2.imshow('After Guassian Blur', gray)
	#cv2.waitKey(0)
	kernel = np.ones((5,5), np.uint8)
	gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
	cv2.imshow('After Morphological Operations', gray)
	#cv2.waitKey(0)
	gray = cv2.Canny(gray, 70, 100)
	cv2.imshow('After Canny Edge Detection', gray)
	#cv2.waitKey(0)

	_,contour,_ = cv2.findContours(gray.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contour = sorted(contour, key=cv2.contourArea, reverse=True)[:5]
	j = 0
	for cnt in contour:
		x,y,w,h = cv2.boundingRect(cnt)
		cv2.imwrite('croppedImages/' + str(image) +  str(j) + '.png', img[y:y+h, x:x+w])
		j+=1

	cv2.waitKey(0)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		exit()


