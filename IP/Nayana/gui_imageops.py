import os

path = '/Users/nayana/projects/flask1/GUI/static/images'
path1 = '/Users/nayana/projects/flask1/GUI/static/images_moved/'

class ImageVals:
    
    def __init__(self,imageArray,imageIndex):
        self.imageIndex = 0
        self.imageArray = []

    def getimg(self,imageArray,imageIndex):

        for subdir, dirs, files in os.walk(path):
            for file in files:
                filepath = os.path.join(subdir, file)
                statinfo = os.stat(filepath)
                if statinfo.st_size!=0:
                    if filepath.endswith('.jpg') or filepath.endswith('.JPG') or filepath.endswith('.png') or filepath.endswith('.PNG'):
                        if filepath not in self.imageArray:
                            self.imageArray.append(filepath)                        
        return None

    def previousimg(self,imageArray,imageIndex,myImage):
        if (self.imageIndex!=0):
            self.imageIndex=self.imageIndex-1
            myImage.setAttribute('src','images/'+self.imageArray[self.imageIndex])
            return None
    
    def nextimg(self,imageArray,imageIndex,myImage):
        if (self.imageIndex!=len(self.imageArray)-1):
            self.imageIndex += 1
            myImage.setAttribute('src','images/'+self.imageArray[self.imageIndex])
            return None
    
    def deleteimg(self,imageArray,imageIndex):
        os.unlink(self.imageArray[self.imageIndex])
        self.imageArray.remove(self.imageArray[self.imageIndex])
        if(self.imageIndex==len(self.imageArray)):
            self.imageIndex=0

        return None
        
    def moveimg(self,imageArray,imageIndex):
        old_file = os.path.join(path,self.imageArray[self.imageIndex])
        new_file = os.path.join(path1,self.imageArray[self.imageIndex])
        os.rename(self.imageArray[self.imageIndex], path1+'img'+str(imageIndex)+'.jpg')
        self.imageArray.remove(self.imageArray[self.imageIndex])
        if(self.imageIndex==len(self.imageArray)):
            self.imageIndex=0
        
        return None
        
    def image_src(self,imageArray,imageIndex):
       if self.imageArray:
          return self.imageArray[self.imageIndex]
    