import cv2
import numpy as np
from constance import config

"""
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

def limpiarBytes(imgo):

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


def comparar(sample1, sample2):
	sift = cv2.SIFT_create()

	#Prepare
	k1, des1 = sift.detectAndCompute(sample1, None)
	k2, des2 = sift.detectAndCompute(sample2, None)

	#Descpriptor Ecueation
	matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)

	#algorith knn 100% de exactitud
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

	#cv2.imshow("Sample1", sample1)
	#cv2.imshow("Sample2", sample2)

	result = cv2.drawMatches(sample1, k1, sample2, k2, matches_points, None)
	cv2.imshow("Result",result)
	cv2.waitKey(0)

def compararBytes(sample1, sample2):
	sift = cv2.SIFT_create()

	#Prepare
	k1, des1 = sift.detectAndCompute(sample1, None)
	k2, des2 = sift.detectAndCompute(sample2, None)

	#Descpriptor Ecueation
	matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)

	#algorith knn 100% de exactitud
	matches = matcher.knnMatch(des1, des2, 2)

	matches_points = []

	#0.4
	ratio_thresh = 0.6
	matches_points = []
	for m,n in matches:
	    if m.distance < ratio_thresh * n.distance:
	        matches_points.append(m)

	keypoints = 0
	if(len(k1)< len(k2)):
		keypoints = len(k1)
	else:
		keypoints = len(k2)

	return len(matches_points), keypoints, (len(matches_points) / keypoints) * 100


#sample1 = limpiar("1.png")
#sample2 = limpiar("2.png")

#comparar(sample1, sample2)
"""

def readBytesCV2(read):
	image = np.asarray(bytearray(read), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	return image

def compare2():
	# Cargar las imágenes de las huellas dactilares
	img1 = cv2.imread('1.png', 0)
	img2 = cv2.imread('3.png', 0)

	# Extraer las características de las huellas dactilares mediante el detector de minutias de OpenCV
	detector = cv2.SIFT_create()
	keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
	keypoints2, descriptors2 = detector.detectAndCompute(img2, None)

	# Establecer el umbral de similitud para determinar si las huellas dactilares son de la misma persona
	umbral_similitud = config.UMBRAL_SIMILITUD

	# Utilizar el algoritmo de coincidencia de fuerza bruta de OpenCV para comparar las características de ambas huellas dactilares
	matcher = cv2.BFMatcher()
	matches = matcher.knnMatch(descriptors1, descriptors2, k=2)

	# Filtrar las coincidencias por similitud
	good_matches = []
	for m, n in matches:
		if m.distance < umbral_similitud * n.distance:
			good_matches.append(m)

	# Determinar si las huellas dactilares corresponden a la misma persona en función del número de coincidencias encontradas
	
	if len(good_matches) > 100:
		print("Las huellas dactilares corresponden a la misma persona")
	else:
		print("Las huellas dactilares corresponden a personas diferentes")

	result = cv2.drawMatches(img1, keypoints1, img2, keypoints2, good_matches, None)
	cv2.imshow("Result",result)
	cv2.waitKey(0)

def compareBytes2(img1, img2):

	# Extraer las características de las huellas dactilares mediante el detector de minutias de OpenCV
	detector = cv2.SIFT_create()
	keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
	keypoints2, descriptors2 = detector.detectAndCompute(img2, None)

	# Establecer el umbral de similitud para determinar si las huellas dactilares son de la misma persona
	umbral_similitud = 0.7

	# Utilizar el algoritmo de coincidencia de fuerza bruta de OpenCV para comparar las características de ambas huellas dactilares
	matcher = cv2.BFMatcher()
	matches = matcher.knnMatch(descriptors1, descriptors2, k=2)

	# Filtrar las coincidencias por similitud
	good_matches = []
	for m, n in matches:
		if m.distance < umbral_similitud * n.distance:
			good_matches.append(m)

	# Determinar si las huellas dactilares corresponden a la misma persona en función del número de coincidencias encontradas
	
	if len(good_matches) > config.CANTIDAD_COINCIDENCIAS:
		print("Las huellas dactilares corresponden a la misma persona: " + str(len(good_matches)))
		return True
	else:
		print("Las huellas dactilares corresponden a personas diferentes "+ str(len(good_matches)))
		return False

def compareLote(metrica, metricas):
	metrica_image = readBytesCV2(metrica)
	for m in metricas:
		if(compareBytes2(metrica_image, cv2.imread(m.imagen.path, 0))):
			return m
	return None
