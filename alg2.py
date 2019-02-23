import cv2
import numpy as np

cap = cv2.VideoCapture(0)
frameBuffer = []
N=  30

def add(buf, frame, N):
	buf.append(frame)
	if len(buf) >= N:
		buf = buf[1:]
	return buf

def mean_buf(buf):
	return np.mean(np.array(buf), axis=0)

def N_minMaxLoc(frame,N):
	maxlocs = []
	for i in range(N):
		minval, maxval, minLoc, maxLoc = cv2.minMaxLoc(mean_img)
		maxlocs.append(maxLoc)
		frame[maxLoc[1], maxLoc[0]] = 0
	return maxlocs

def get_sum_around(frame, point, s):
	x,y = point
	return np.sum(frame[y-s:y+s, x-s:x+s])





while(1):

	# Take each frame
	_, frame = cap.read()
	ret, thresh = cv2.threshold(frame, 254, 255, cv2.THRESH_BINARY)
	red = thresh[:,:,1]
	frameBuffer = add(frameBuffer, thresh, N)
	avg = mean_buf(frameBuffer)
	#print(avg.shape)
	diff = np.subtract(thresh, avg)
	# set all negatives to zero
	ret, diff = cv2.threshold(diff, 0,0, cv2.THRESH_TOZERO)

	#print(np.max(diff))
	#print(np.min(diff))
	#ret, thresh2 = cv2.threshold(diff, 240, 255, cv2.THRESH_BINARY)
	
	diff = diff.astype("uint8")
	detector = cv2.SimpleBlobDetector_create()
	keypoints = detector.detect(diff)
	#im_with_keypoints = cv2.drawKeypoints(diff, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	#print(keypoints)

	mean_img = np.mean(diff, axis=2)
	mean_img = mean_img.astype("uint8")
	#mean_img = cv2.GaussianBlur(mean_img, (5,5),0)
	#minval, maxval, minLoc, maxLoc = cv2.minMaxLoc(mean_img)
	#maxlocs = N_minMaxLoc(mean_img, 5)
	#sums = [get_sum_around(mean_img, maxloc, 20) for maxloc in maxlocs]
	#print(sums)
	#estmax = maxlocs[np.argmax(np.array(sums))]
	#print(estmax)
	#highlighted_img = cv2.circle(diff, estmax, 10,(255,0,0),2)
	#for m in maxlocs:
	#	highlighted_img = cv2.rectangle(diff,(m[0]-20, m[1]-20), (m[0] + 20, m[1] + 20), (0,255,0),3)
	#for maxloc in maxlocs:
	#	highlighted_img = cv2.circle(diff, maxloc, 10,(255,0,0),2)
	#	print(get_sum_around(mean_img,maxloc,2))
	
	#methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
	#for method in methods:
	#	template = np.ones([20,20,3]) * 255.
	#	res = cv2.matchTemplate(diff, template, eval(method))
	#	cv2.imshow(str(method), res)

	# let's try erosion... see what happens wit hthat
	kernel = np.ones((5,5), np.uint8)
	#img_erosion = cv2.erode(diff, kernel, iterations = 2)
	img_dilate = cv2.dilate(diff, kernel, iterations = 2)

	#maxlocs = N_minMaxLoc(img_dilate, 5)
	#sums = [get_sum_around(img_dilate, maxloc, 20) for maxloc in maxlocs]
	#print(sums)
	#estmax = maxlocs[np.argmax(np.array(sums))]
	#print(estmax)
	#highlighted_img = cv2.circle(diff, estmax, 10,(255,0,0),2)

	#detector = cv2.SimpleBlobDetector_create()
	#keypoints = detector.detect(img_dilate)
	#print(keypoints)

	old_img_dilate = img_dilate.astype("uint8")
	img_dilate = cv2.cvtColor(old_img_dilate, cv2.COLOR_BGR2GRAY)
	circles = cv2.HoughCircles(img_dilate, cv2.HOUGH_GRADIENT, 1,20,param1=30,param2=15,minRadius=1, maxRadius=20)
	if circles is None:
		circles = []
	if len(circles) >= 1:
		for circle in circles:
			x,y,r = circle[0]
			img_dilate = cv2.circle(img_dilate, (x,y), r, (0,0,255),3)
	print(circles)


	


	cv2.imshow("average", avg)
	cv2.imshow('my webcam', red)
	cv2.imshow("diff", diff)
	#cv2.imshow("thresh2", thresh2)
	#cv2.imshow("blobs", im_with_keypoints)
	cv2.imshow("mean", mean_img)
	#cv2.imshow("contours", conts)
	#cv2.imshow("highlights", highlighted_img)
	#cv2.imshow("erosion", img_erosion)
	cv2.imshow("old_dilate", old_img_dilate)
	cv2.imshow("dilation", img_dilate)



	if cv2.waitKey(1) == 27: 
 		break  # esc to quit