import cv2

import cv2
import numpy as np

def limpiar(img):
	imgo = cv2.imread(img)
	#cv2.imshow("imgo",imgo)

	#Removing the background
	height, width = imgo.shape[:2]

	#Create a mask holder
	mask = np.zeros(imgo.shape[:2],np.uint8)

	#Grab Cut the object
	bgdModel = np.zeros((1,65),np.float64)
	fgdModel = np.zeros((1,65),np.float64)

	#Hard Coding the Rect… The object must lie within this rect.
	rect = (10,10,width-30,height-30)
	cv2.grabCut(imgo,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
	mask = np.where((mask==2)|(mask==0),0,1).astype("uint8")
	img1 = imgo*mask[:,:,np.newaxis]

	#Get the background
	background = cv2.absdiff(imgo,img1)

	#Change all pixels in the background that are not black to white
	background[np.where((background > [0,0,0]).all(axis = 2))] = [255,255,255]

	#Add the background and the image
	final = background + img1

	#To be done – Smoothening the edges….
	return final


sample1 = limpiar("1.png")
sample2 = limpiar("3.png")

sift = cv2.SIFT_create()

k1, des1 = sift.detectAndCompute(sample1, None)
k2, des2 = sift.detectAndCompute(sample2, None)

matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)

matches = matcher.knnMatch(des1, des2, 2)

matches_points = []

ratio_thresh = 0.4
matches_points = []
for m,n in matches:
    if m.distance < ratio_thresh * n.distance:
        matches_points.append(m)

keypoints = 0
if(len(k1)< len(k2)):
	keypoints = len(k1)
else:
	keypoints = len(k2)

print((len(matches_points), keypoints, (len(matches_points) / keypoints) * 100))


#print(matches_points)

#cv2.imshow("Sample1", sample1)#
#cv2.imshow("Sample2", sample2)

result = cv2.drawMatches(sample1, k1, sample2, k2, matches_points, None)
cv2.imshow("Result",result)
cv2.waitKey(0)
