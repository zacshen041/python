import cv2 
import numpy as np 
img = cv2.imread('d:/code/python/opencv/page.jpg',cv2.IMREAD_GRAYSCALE) 
retval, threshold = cv2.threshold(img, 8, 255, cv2.THRESH_BINARY)
cv2.COVAR_COLS
#th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,155, 1) 
cv2.imshow('original',img) 
cv2.imshow('Adaptive threshold',threshold)
cv2.waitKey(0) 
cv2.destroyAllWindows()


