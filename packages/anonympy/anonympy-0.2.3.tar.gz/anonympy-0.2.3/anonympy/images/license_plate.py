import cv2
import matplotlib.pyplot as plt
import numpy as np
import imutils

# READING AN IMAGE
img = cv2.imread('car.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow('image', gray)
##plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
##plt.show()



# Apply Filters and Find Edges for localization
bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
edged = cv2.Canny(bfilter, 30, 200) #Edge detection

cv2.imshow('edged', edged)



# Find Contours and Apply Mask
keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

# Loop through and find a rectangle 
location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break

print('Location: ', location)

cv2.circle(img, tuple(location[0][0]), 2, (255, 0,0), 2)
cv2.circle(img, tuple(location[1][0]), 2, (255, 0,0), 2)
cv2.circle(img, tuple(location[2][0]), 2, (255, 0,0), 2)
cv2.circle(img, tuple(location[3][0]), 2, (255, 0,0), 2)
cv2.imshow('final', img)
