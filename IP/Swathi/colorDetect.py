import cv2
import numpy as np
image=cv2.imread("color.png")
hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
lower=np.array([20,50,50])# appropriate lower margin
upper=np.array([255,255,255])# appropriate upper margin
mask=cv2.inRange(hsv, lower, upper)
res = cv2.bitwise_and(image,image, mask= mask)

cv2.imshow("Original",image)
cv2.imshow("Final",res)
cv2.waitKey(0)
cv2.destroyAllWindows()
