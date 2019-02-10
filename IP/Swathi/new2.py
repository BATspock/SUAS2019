import cv2
import numpy as np
image=cv2.imread("green2.jpg")
f=open('data.txt','a')

hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
lower_red=np.array([0, 70, 50])
upper_red=np.array([10, 255, 255])

mask=cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(image,image, mask= mask)
H,S,V=hsv[0,0]
if (H<=10 and S<=255 and V<=255) and (H>=0 and S>=70 and V>=50):
    print('red')
    f.write('red')
    f.write("\n")
else:
    if(H<=150 and S<=255 and V<=255) and (H>=61 and S>=70 and V>=50):
     print('Green')
     f.write('Green')
     f.write("\n")
    else:
        if(H<=60 and S<=255 and V<=255) and (H>=35 and S>=70 and V>=50):
         print("Yellow")
         f.write("Yellow")
         f.write("\n")
        else:
            if(H<=220 and S<=255 and V<=255) and (H>=160 and S>=70 and V>=50):
             print("Blue")
             f.write("Blue")
             f.write("\n")
            else:
                 if(H<=34 and S<=255 and V<=255) and (H>=11 and S>=70 and V>=50):
                  print("Orange")
                  f.write("Orange")
                  f.write("\n")
                 else:
                     if(H<=290 and S<=255 and V<=255) and (H>=221 and S>=70 and V>=50):
                      print("Purple")
                      f.write("Purple")
                      f.write("\n")
                     else:
                         if(H<=340 and S<=255 and V<=255) and (H>=291 and S>=70 and V>=50):
                          print("Pink")
                          f.write("Pink")
                          f.write("\n")
                         
                     
                     
        

    
f.close()
    

'''
cv2.imshow("Original Image",image)
cv2.imshow("Detection",res)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
