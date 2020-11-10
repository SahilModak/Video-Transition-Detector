import numpy as np
import matplotlib.pylab as plt
import os
from matplotlib import pyplot
from matplotlib import image
from PIL import Image
import cv2
import shutil
import math
import func as func

def makeRowSTI(totalFrames,f_name):
  """
  the function takes in a parameter for the total number of frames, 
  calculates image height and width from the first frame, 
  makes a 3 dimensional array with dimensions (width, totalFrames, 3)
  these are the dimensions for the row STI, then, 
  using a loop to access all the frames and another loop within it to 
  process each pixel in the middle row of each frame and then assign these 
  pixels to the ith column representing the current frame being processed.
  """
  #calculating height and width
  lum_img= [] #STI
  imag = Image.open(f_name+"/frm1.jpg")
  width = imag.width
  height = imag.height
  #making a 3d array to represent STI
  for a in range(width):
    lum_img.append([])
    for b in range(totalFrames):
      lum_img[a].append([])
      for c in range(3):
        lum_img[a][b].append(0)
  #nested loop to process pixels from the middle row of each frame
  i=0
  while (i < totalFrames):
    img = plt.imread(f_name+"/frm"+str(i)+".jpg")
    j = 0
    while(j < width):
      lum_img[j][i] = img[int(height/2)][j]
      j = j + 1
    i=i+1
  #returning the STI 
  return np.array(lum_img)

def makeColSTI(totalFrames,f_name):
  """
  the function takes in a parameter for the total number of frames, 
  calculates image height and width from the first frame, 
  makes a 3 dimensional array with dimensions (height, totalFrames, 3)
  these are the dimensions for the STI, then, 
  using a loop to access all the frames and another loop within it to 
  process each pixel in the middle column of each frame and then assign these 
  pixels to the ith column representing the current frame being processed.
  """
  #calculating height and width
  lum_img = []
  imag = Image.open(f_name+"/frm1.jpg")
  width = imag.width
  height = imag.height
  #making a 3d array to represent STI
  for a in range(height):
    lum_img.append([])
    for b in range(totalFrames):
      lum_img[a].append([])
      for c in range(3):
        lum_img[a][b].append(0)

   #nested loop to process pixels from the middle column of each frame
  i = 0
  #loop to go over frames and columns in the STI
  while(i < totalFrames):
    #loop to go over pixels in each frame
    j = 0
    img = plt.imread(f_name+"/frm"+str(i)+".jpg")
    while(j < height):
      lum_img[j][i] = img[j][int(width/2)]
      j = j + 1
    i = i + 1
  #returning the STI 
  return np.array(lum_img)

def colourToChromaticity(img,f_name):
  """
  the function takes in a parameter for a frame, 
  calculates image height and width from the frame, 
  makes a 3 dimensional array with dimensions (height, width, 2), 
  these are the dimensions for the chromatized frame of the video, 
  then there is a nested loop to go over each pixel of the frame and
  chromatize them
  """
  #calculating height and width
  imag = Image.open(f_name+"/frm0.jpg")
  width = imag.width
  height = imag.height
  lum_img = []
  #making a 3d array to represent STI
  for a in range(height):
    lum_img.append([])
    for b in range(width):
      lum_img[a].append([])
      for c in range(2):
        lum_img[a][b].append(0)
  i = 0
  j = 0
  #nested loop to go over the all pixels in the frame
  while(i < height):
    j = 0
    while(j < width):
      #exception case for when r, g, b are all zero (black)
      if (img[i][j][0] == 0 and img[i][j][1] == 0 and img[i][j][2] == 0):
        lum_img[i][j][0] = 0
        lum_img[i][j][1] = 0
      else:
        #chromatization
        lum_img[i][j][0] = img[i][j][0]/(int(img[i][j][0]) + int(img[i][j][1]) + int(img[i][j][2]))
        lum_img[i][j][1] = img[i][j][1]/(int(img[i][j][0]) + int(img[i][j][1]) + int(img[i][j][2]))
      j = j + 1
    i = i + 1
  return lum_img

def makeHistogram(lst,f_name):
  """
  The function takes in one parameter in the form of a 2d list, 
  which holds chromatized pixel values for a row or column.
  The function calculates calculates image height and width from the frame
  then it cslculates the number of bins for pixel values in a histogram
  using Sturge's rule, 
  then, it makes a 2d array, of dimensions (bins, bins) to represent the histogram,
  another list hoding threhod values for comparison is made.
  The function makes a histogram by counting all values in the column/row
  b comparing them to the threshold values calculated earlier.
  """
  #calculating height and width
  imag = Image.open(f_name+"/frm0.jpg")
  width = imag.width
  height = imag.height
  #calculating the number of bins with sturges rule
  numberOfBins = int(1 + math.log(len(lst), 2))
  histogram = []

  #making 2d array filled with 0's for the histogram 
  for i in range(numberOfBins):
    histogram.append([])
    for j in range(numberOfBins):
      histogram[i].append(0)

  #making a array to store the maximum 
  #threshold values for the histogram
  comparisonArray = []
  for i in range(numberOfBins):
    comparisonArray.append(round(1/numberOfBins*(i + 1),7))
  #setting the maximum threshold value to 1
  comparisonArray[-1] = 1
  i = 0
  #nested loops to add values to the histogram
  #first loop to go over every element in the list of pixel values
  while (i < len(lst)):
    #second loop to compare all red pixels in the list
    for a in range(numberOfBins):
      #if to compare red values to histogram thresholds
      if(lst[i][0] <= comparisonArray[a]):
        #loop to compare all green values to the thresholds
        for b in range(numberOfBins):
          if(lst[i][1] <= comparisonArray[b]):
            #incrementing histogram values when the pixel fits the threshold
            histogram[a][b] = histogram[a][b] + 1
            break
        break
        #break statements to avoid counting pixels twice
    i = i + 1

  #normalizing histogram
  for i in range(numberOfBins):
    for j in range(numberOfBins):
      histogram[i][j] = histogram[i][j]/len(lst)
  return histogram

def histogramDiff(histo1, histo2):
  """
  the functiion takes two histograms as 2d arrays as parameters, 
  calculates the histogram difference between them, using a nested loop
  """
  difference = 0
  i = 0
  #nested loop to compare every element in the two histogram
  while( i < len(histo1)):
    j = 0
    while(j < len(histo2)):
      if(histo1[i][j] <= histo2[i][j]):
        difference = difference + histo1[i][j]
      else:
        difference = difference + histo2[i][j]
      j = j + 1
    i = i + 1
  return difference

def makeColHistoIntersection(totalFrames,f_name):
  """
  the function takes in a parameter for the total number of frames, 
  calculates image height and width from the first frame, 
  makes a 3 dimensional array with dimensions (width, totalFrames, 3)
  these are the dimensions for the STI, chromatizes the entire frame
  column by column, makes histograms and calculates their difference
  and stores it to make an STI.
  """
  #calculating height and width
  imag = Image.open(f_name+"/frm0.jpg")
  width = imag.width
  height = imag.height

  #making a 3d array to represent STI
  lum_img = []
  for a in range(width):
    lum_img.append([])
    for b in range(totalFrames):
      lum_img[a].append([])
      for c in range(3):
        lum_img[a][b].append(0)


  #nested while loops to go over every pixel in every column in every frame 
  i = 0
  #loop to go over every frame
  while(i < totalFrames - 1):
    #taking in two frames at a time to calculate 
    #histogram difference betwween time t and t-1
    img1 = plt.imread(f_name+"/frm" + str(i) +".jpg")
    img2 = plt.imread(f_name+"/frm"+str(i + 1)+".jpg")
    #chromatizing the frame
    chromatImg1 = colourToChromaticity(img1,f_name)
    chromatImg2 = colourToChromaticity(img2,f_name)
    j = 0
    k = 0
    #lists to store pixel data from chromatized columns 
    col1 = [0]*height
    col2 = [0]*height
    #nested loops for going over all pixels in rows and columns
    while(j < width):
      k = 0
      while(k < height):
        col1[k] = chromatImg1[k][j]
        col2[k] = chromatImg2[k][j]
        k = k + 1
      #making histograms from columns 
      histo1 = makeHistogram(col1,f_name)
      histo2 = makeHistogram(col2,f_name)
      #calculating the histogram difference and making STI
      lum_img[j][i][0] = histogramDiff(histo1, histo2)
      j = j + 1
    i = i + 1
  return np.array(lum_img)



def makeRowHistoIntersection(totalFrames,f_name):
  """
  the function takes in a parameter for the total number of frames, 
  calculates image height and width from the first frame, 
  makes a 3 dimensional array with dimensions (width, totalFrames, 3)
  these are the dimensions for the STI, chromatizes the entire frame
  row by row, makes histograms and calculates their difference
  and stores it to make an STI.
  """
  #calculating height and width
  imag = Image.open(f_name+"/frm0.jpg")
  width = imag.width
  height = imag.height

  #making a 3d array to represent STI
  lum_img = []
  for a in range(height):
    lum_img.append([])
    for b in range(totalFrames):
      lum_img[a].append([])
      for c in range(3):
        lum_img[a][b].append(0)

  #nested while loops to go over every pixel in every row in every frame 
  i = 0
  #loop to go over every frame
  while(i < totalFrames - 1):
    #taking in two frames at a time to calculate 
    #histogram difference betwween time t and t-1
    img1 = plt.imread(f_name+"/frm" + str(i) +".jpg")
    img2 = plt.imread(f_name+"/frm"+str(i + 1)+".jpg")
    #chromatizing the frame
    chromatImg1 = colourToChromaticity(img1,f_name)
    chromatImg2 = colourToChromaticity(img2,f_name)
    j = 0
    k = 0
    #lists to store pixel data from chromatized rows 
    row1 = [0]*width
    row2 = [0]*width
    #nested loops for going over all pixels in rows and columns
    while(j < height):
      k = 0
      while(k < width):
        row1[k] = chromatImg1[j][k]
        row2[k] = chromatImg2[j][k]
        k = k + 1
      #making histograms from columns 
      histo1 = makeHistogram(row1,f_name)
      histo2 = makeHistogram(row2,f_name)
      #calculating the histogram difference and making STI
      lum_img[j][i][0] = histogramDiff(histo1,histo2)
      j = j + 1
    i = i + 1

  return np.array(lum_img)

def createThresholdSTI(img):
  """
  The function takes in a STI as a parameter and compares pixels to a 
  fixed threshod of 0.7, anything greater than 0.7 indicates that there 
  is not much change so is assigned the value of white (1, 1, 1), 
  all other values are assigned black, this helps us see the diagonal 
  transition line much more easily.
  """

  #nested loop to go over all pixels in the STI
  for i in range(len(img)):
    for j in range(len(img[0])):
      if(img[i][j][0] > 0.7):
        img[i][j][0] = 1
        img[i][j][1] = 1
        img[i][j][2] = 1
      else:
        img[i][j][0] = 0

  return np.array(img)

