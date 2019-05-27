import os
import PIL.Image
import time

path = '/Users/nayana/projects/flask1/Nayana_trial/static/images'
path1 = '/Users/nayana/projects/flask1/Nayana_trial/static/images_moved/'

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
        t = time.time()
        os.rename(self.imageArray[self.imageIndex], path1+'img'+str(t)+'.jpg')
        self.imageArray.remove(self.imageArray[self.imageIndex])
        if(self.imageIndex==len(self.imageArray)):
            self.imageIndex=0
        
        return None
        
    def image_src(self,imageArray,imageIndex):
       if self.imageArray:
          return self.imageArray[self.imageIndex]
          
    def metadata(self,imageArray,imageIndex):
       temp={}
       latlon={}
       latlon['lat'] = 0.0
       latlon['lon'] = 0.0
       imgpath = os.path.join(path,self.imageArray[self.imageIndex])
       img = PIL.Image.open(imgpath)
       try:
          for k, v in img._getexif().items():
             string=str(v).replace('{','').replace('}','')
             temp = dict((x.strip(), y.strip()) for x, y in (element.split(': ') for element in string.split(', ')))
             for k, v in temp.items():
                attr = k.replace('\'','').replace('\'','')
                if attr=='lat' or attr=='lon':
                   val = float(temp.get(k))
                   latlon[attr] = val
       except:
          pass
       return latlon