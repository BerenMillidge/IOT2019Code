import cv2
import numpy as np
from imutils import contours
from skimage import measure
import imutils


cap = cv2.VideoCapture(0)
bitstr = ""
sumlist = [0]
def add(l, sumval, N):
	l.append(sumval)
	if len(l) >= N:
		l = l[1:]
	return l

while True:
	_, frame = cap.read()
	s = np.sum(frame)
	sumlist = add(sumlist, s, 100)
	mu = sum(sumlist) / len(sumlist)
	diff = s - mu
	print(diff)
	bit = 0
	if diff > 0:
		bit = 1
	print(bit)
	bitstr += str(bit)
	print(bitstr)

	cv2.imshow("webcam", frame)
	if cv2.waitKey(1) == 27: 
 		break  # esc to quit
