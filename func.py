import numpy as np
import matplotlib.pylab as plt
import os
from matplotlib import pyplot
from matplotlib import image
import cv2
import shutil
from PIL import Image


def show(photo):
  pyplot.imshow(photo)
  pyplot.show()
  return

# Opens and Extracts Frames from the Video File
def extractframes(v_path, f_path):
    #creating a tmp directory
    path = str(f_path)
    try:
        os.mkdir(path)
    except OSError as e:
        print ("Creation of the directory %s failed" % path)
        print("Error: %s : %s" % (path, e.strerror))
    else:
        print ("Successfully created the directory %s " % path)
    #open video
    cap= cv2.VideoCapture(str(v_path))
    i=0
    #save frames to tmp directory
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite(f_path+"/frm"+str(i)+".jpg",frame)
        i+=1
    return i

# Opens and Extracts Frames from the Video File and resize them
def extractframesResize(v_path, f_path):
    #creating a tmp directory
    path = str(f_path)
    try:
        os.mkdir(path)
    except OSError as e:
        print ("Creation of the directory %s failed" % path)
        print("Error: %s : %s" % (path, e.strerror))
    else:
        print ("Successfully created the directory %s " % path)
    #open video
    cap= cv2.VideoCapture(str(v_path))
    i=0
    #save frames to tmp directory
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite(f_path+"/frm"+str(i)+".jpg",frame)
        
        image = Image.open(f_path+"/frm"+str(i)+".jpg")
        new_image = image.resize((32, 32))
        new_image.save(f_path+"/frm"+str(i)+".jpg")

        i+=1

    return i

#Delete tmp directory created
def deletefolder(f_name):
    path = str(f_name)
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("Error: %s : %s" % (path, e.strerror))
    else:
        print ("Successfully deleted the directory %s" % path)
    return

