#!/usr/bin/env python
# coding: utf-8

# In[571]:


### Restrictions: x-ray must be oriented in correct direction, must be zoomed out reasonably
import cv2 as cv
# from matplotlib import pyplot as plt
import numpy as np
import math
import sys
import wx


# In[580]:

def process_img(imgpath):
#img = cv.imread("data/insta-xray3.jpg")
    img = cv.imread(imgpath)
# img = cv.imread("data/keinbocks.jpg")
#img = cv.imread("data/wrist.png")
# plt.imshow(img)


# In[581]:


    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    hist = cv.calcHist([gray], [0], None, [256], [0, 256])
    # plt.figure()
# plt.title("Grayscale Histogram")
    # plt.xlabel("Bins")
# plt.ylabel("# of Pixels")
    # plt.plot(hist)
# plt.show()
# plt.xlim([0, 256])

# Use histogram for thresholding

    sum = 0
    total = len(gray) * len(gray[0])
    percentile = 85
    threshlevel = 0

    for i in range(len(hist)):
        sum = sum + hist[i]
        if sum * 100 / total > percentile:
            break
        threshlevel = i
        
    print(threshlevel)


# In[582]:


    thresh = np.zeros_like(img)
    for x in range(len(img)):
        for y in range(len(img[0])):
            if img[x][y][0] < threshlevel:
                thresh[x][y] = 0
            else:
                thresh[x][y] = 255
#kernel = np.ones((5,5),np.uint8)
#thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
# plt.imshow(thresh)
            


# In[583]:


    img = cv.GaussianBlur(img,(5,5),0)

    kernel = np.zeros((5,5),np.float32)
    kernel[:2,:] = -1
    kernel[3:,:] = 1
    dstx = cv.filter2D(img,-1,kernel)
    dstx = cv.medianBlur(dstx, 7)

    kernely = np.zeros((5,5),np.float32)
    kernely[:,:2] = -1
    kernely[:,3:] = 1
    dsty = cv.filter2D(img,-1,kernely)
    dsty = cv.medianBlur(dsty, 5)
    dstx = dstx*2

# plt.imshow(dstx*2)
# plt.show()


# In[584]:


    horithresh = np.zeros_like(img)
    for x in range(len(img)):
        for y in range(len(img[0])):
            if dstx[x][y][0] < 80:
                horithresh[x][y] = 0
            else:
                horithresh[x][y] = 255
    horithresh = cv.medianBlur(horithresh, 5)

# In[585]:


    greylines = cv.cvtColor(horithresh, cv.COLOR_BGR2GRAY)
#kernel = np.ones((3,3),np.uint8)
#greylines = cv.erode(greylines,kernel,iterations = 1)
#kernel = np.ones((7,7),np.uint8)
#greylines = cv.dilate(greylines,kernel,iterations = 1)
# plt.imshow(greylines)


# In[586]:
    imgcopy = np.copy(img)

    lines = cv.HoughLinesP(greylines, 1, math.pi/180, 0, None, 40, 30);
    lowesty = 0
    ythresh = 5
    xthresh = 30
    xbounds = (0,0)
    angthresh = math.pi/7
    for x in range(0, len(lines)):
        for line in lines[x]:
            theta = math.atan2(line[3] - line[1], line[2] - line[0])
            if theta > -angthresh and theta < angthresh:
                lowesty = max(lowesty,  max(line[1], line[3]))
                xbounds = (line[0], line[2])

    nofracture = False
# Check if no fracture
    for x in range(0, len(lines)):
        for line in lines[x]:
            theta = math.atan2(line[3] - line[1], line[2] - line[0])
            if theta > -angthresh and theta < angthresh:
                if max(line[3], line[1]) > lowesty - ythresh:
                    if line[0] > xbounds[1] + xthresh and line[2] > xbounds[1] + xthresh:
                        nofracture = True
                    if line[0] < xbounds[0] - xthresh and line[2] < xbounds[0] - xthresh:
                        nofracture = True
                    

    if not nofracture:
        for x in range(0, len(lines)):
            for line in lines[x]:
                theta = math.atan2(line[3] - line[1], line[2] - line[0])
                if theta > -angthresh and theta < angthresh:
                    if lowesty <= max(line[1], line[3]) and max(line[1], line[3]) < 850:
                        pt1 = (line[0],line[1])
                        pt2 = (line[2],line[3])
                        cv.line(imgcopy, pt1, pt2, (0,255,0), 3)
                        break
                    if max(line[1], line[3]) >= 850:
                        nofracture = true
# plt.imshow(imgcopy);


# In[587]:


    for x in range(len(img)):
        for y in range(len(img[1])):
            if dstx[x][y][0] < 110:
                horithresh[x][y] = 0
            else:
                horithresh[x][y] = 255


# In[568]:


#kernel = np.zeros((5,5),np.float32)
#kernel[:,:2] = -1
#kernel[:,3:] = 1
#dsty = cv.filter2D(img,-1,kernel)
# plt.imshow(dsty)


# In[ ]:

    print(nofracture)
    cv.imwrite("out.png", imgcopy)
    return ("out.png", nofracture)

# In[ ]:

# process_img(sys.argv[1])

# def scale_bitmap(bitmap, width, height):
    # image = bitmap.ConvertToImage()
    # image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    # result = wx.Bitmap(image)
    # return result

# imagesize = 500
# class MyFrame(wx.Frame):    
    # def __init__(self):
        # super().__init__(parent=None, title='Broke Detector', size=(1060, 750))
        # self.panel = wx.Panel(self, -1, (imagesize, imagesize))
        # self.panel.SetPosition((0, 100))

        # self.choosebtn = wx.Button(self,-1,"Choose Posterior X-Ray") 
        # self.choosebtn.Bind(wx.EVT_BUTTON,self.OnOpen) 
        # self.choosebtn.SetPosition((30, 25))

        # self.chooselat = wx.Button(self,-1,"Choose Lateral X-Ray") 
        # self.chooselat.Bind(wx.EVT_BUTTON,self.OnOpen) 
        # self.chooselat.SetPosition((30, 55))

        # self.msg = wx.StaticText(self,-1) 
        # self.msg.SetLabel("Choose and image!") 
        # self.msg.SetPosition((300, 40))

        # # self.srcimg = wx.Image("data/wrist.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # # self.srcimg = scale_bitmap(self.srcimg, imagesize, self.srcimg.GetHeight() /
                # # self.srcimg.GetWidth() * imagesize)
        # # self.srcimg = wx.StaticBitmap(self, -1, self.srcimg, (10, 5),
                # # (self.srcimg.GetWidth(), self.srcimg.GetHeight()))
        # # self.srcimg.SetPosition((20, 100))

        # self.Show()

    # def OnOpen(self, event):
# # Create open file dialog
        # openFileDialog = wx.FileDialog(frame, "Open", "", "", 
              # "Images  (*.jpg)|*.jpg|(*.png)|*.png", 
               # wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        # openFileDialog.ShowModal()
        # path = openFileDialog.GetPath()
        # openFileDialog.Destroy()
        # res = process_img(path)
        # print(res)
        # restr = res[0]

        # if res[1]:
            # self.msg.SetLabel("Phew! No fracture found!") 
        # else:
            # self.msg.SetLabel("Oh no! Fracture detected!") 

        # self.srcimg = wx.Image(path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # self.srcimg = scale_bitmap(self.srcimg, imagesize, self.srcimg.GetHeight() /
                # self.srcimg.GetWidth() * imagesize)
        # self.srcimg = wx.StaticBitmap(self, -1, self.srcimg, (10, 5),
                # (self.srcimg.GetWidth(), self.srcimg.GetHeight()))
        # self.srcimg.SetPosition((20, 100))

        # self.finimg = wx.Image(restr, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # self.finimg = scale_bitmap(self.finimg, imagesize, self.finimg.GetHeight() /
                # self.finimg.GetWidth() * imagesize)
        # self.finimg = wx.StaticBitmap(self, -1, self.finimg, (10, 5),
                # (self.finimg.GetWidth(), self.finimg.GetHeight()))
        # self.finimg.SetPosition((40 + imagesize, 100))

# if __name__ == '__main__':
    # app = wx.App()
    # frame = MyFrame()
    # app.MainLoop()

