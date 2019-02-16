import cv2
import numpy as np 

class preprocess:
    def __init__(self, image):
        self.im = image

    def Reshape(self, X, Y):
        """
        reshapes:
            width = X
            height = Y
        """
        return (cv2.resize(self.im, (int(self.im.shape[1]*X), int(self.im.shape[0]*Y))))
    
    def GaussianBlur(self, kernel_size = 9):
        """
        does Gaussian Blur, default kernel size = 9X9
        """
        return (cv2.GaussianBlur(self.im,(kernel_size,kernel_size),0))

    def Blur(self, kernel_size = 3):
        """
        default kernel size = 3X3
        """
        return (cv2.blur(self.im,(kernel_size, kernel_size)))

    def Erode(self, kernel_size = 5, iterations = 1):
        """
        erodes small white noises
        default kenel size = 5X5
        default iterations = 1
        """
        return (cv2.erode(self.im, np.ones((kernel_size, kernel_size), np.uint8), iterations))

    def Dilate(self, kernel_size = 5, iterations = 1):
        """
        increases white on black
        default kernel size = 5X5
        default iterations = 1
        """
        return (cv2.dilate(self.im,np.ones((kernel_size, kernel_size), np.uint8), iterations))

    def Opening(self, kernel_size = 5):
        """
        erosion followed by dilation
        default kernel size = 5X5
        """
        return (cv2.morphologyEx(self.im, cv2.MORPH_OPEN, np.ones((kernel_size, kernel_size))))

    def Closing(self, kernel_size = 5):
        """
        dilation follwed by erosion
        default kernel size = 5X5
        """
        return (cv2.morphologyEx(self.im, cv2.MORPH_CLOSE, np.ones((kernel_size, kernel_size), np.uint8)))
    
    def Sharpen(self, kernel_size = 9):
        """
        default kernel size = 9X9
        """
        kernel = np.zeros( (kernel_size, kernel_size), np.float32)
        kernel[int(kernel_size/2),int(kernel_size/2)] = 2.0   #Identity, times two! 

        #Create a box filter:
        boxFilter = np.ones((kernel_size,kernel_size), np.float32) / float(kernel_size*kernel_size)

        #Subtract the two:
        kernel = kernel - boxFilter

        #Note that we are subject to overflow and underflow here...but I believe that
        # filter2D clips top and bottom ranges on the output, plus you'd need a
        # very bright or very dark pixel surrounded by the opposite type.

        return (cv2.filter2D(self.im, -1, kernel))

    def addWeighted(self, kernel_size = 5,original_image_weight = 0.5, blurred_image_weight = 1.5):
        """
        basically add 2 images with different importance
        default kernel size = 5X5
        original image wighted = -0.5
        blurred image weighted = 1.5 //using Gaussiam blur
        """
        return(cv2.addWeighted(cv2.GaussianBlur(self.im,(kernel_size,kernel_size),0),blurred_image_weight, self.im,-1.0*(original_image_weight),0))
        
    def ChangeContrast(self, gamma = 1.0):
        """
        change contrast of an image
        gamma value 1 for same image
        gamma value greater than 1 to increase brightness
        gamma value less than 1 to make image darker
        """
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8") 
        # apply gamma correction using the lookup table
        return cv2.LUT(self.im, table)
    
    def kmeans(self, no_of_clusters):
        """
        k means to extract colors 
        returns ==> image after kmeans and values of the clusters created
        """
        Z = self.im.reshape((-1, 3))
        Z = np.float32(Z)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv2.kmeans(Z, no_of_clusters,None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        return(res.reshape((self.im.shape)), center)
