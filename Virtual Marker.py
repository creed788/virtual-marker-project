import cv2 
import numpy as np

framewidth = 640
frameheight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameheight)
cap.set(4, framewidth)
cap.set(10, 150)

mycolors = [[0,76,109,255,107,255],
            [133, 56, 0, 159, 156, 255],
            [57, 76, 0, 100, 255, 255]]

mycolorvalues = [[51, 153, 255],
                [255, 0, 255],
                [0,255,0]]

mypoints = []     #[x, y, colorId]

def findcolor(img, mycolors, mycolorvalues):
  imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  count = 0
  newpoints = []
  for color in mycolors:
    lower = np.array(color[0:3])
    upper = np.array(color[3:6])
    mask = cv2.inRange(imghsv, lower, upper)
    x, y = getcontours(mask)
    cv2.circle(imgResult, (x, y), 10, mycolorvalues[count], cv2.FILLED)
    if x!= 0 and y!=0:
      newpoints.append([x, y, count])
    count +=1
    # cv2.imshow(str(color[0]), mask)
  return newpoints  

def getcontours(img):
  contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  x, y, w, h = 0, 0, 0, 0
  for cnt in contours:
    area = cv2.contourArea(cnt)
    
    if area>500:
      # print(area)
      #cv2.drawContours(imgResult, cnt, -1, (255,0,0), 3)
      para = cv2.arcLength(cnt, True)
      approx = cv2.approxPolyDP(cnt, 0.02*para, True)
      x, y, w, h = cv2.boundingRect(approx)
  return x+w//2, y

def drawoncanvas(mypoints, mycolorvalues):
  for point in mypoints:
    cv2.circle(imgResult, (point[0], point[1]), 10, mycolorvalues[point[2]], cv2.FILLED)


while True:
  success, img = cap.read()
  imgResult = img.copy()
  newpoints = findcolor(img, mycolors, mycolorvalues)
  if len(newpoints) != 0:
    for newp in newpoints:
      mypoints.append(newp)
  if len(newpoints)!= 0:
    drawoncanvas(mypoints, mycolorvalues)    

  cv2.imshow('result', imgResult)
  if cv2.waitKey(1) == ord('q'):
    break