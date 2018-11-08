import cv2
import numpy as np
image=cv2.imread("color.png")
hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
lower_red=np.array([20,50,50])
upper_red=np.array([255,255,255])
mask=cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(image,image, mask= mask)

cv2.imshow("Original Image",image)
cv2.imshow("Detection",res)
cv2.waitKey(0)
cv2.destroyAllWindows()
