import cv2
import numpy as np
from imutils import contours
from skimage import measure
import imutils

cap = cv2.VideoCapture(0)

roi = np.zeros([40,40])

sumlist = [0]
masksumlist = [0]
bitstr = ""
trueString = ""
prevChar = ""
repeatNum = 0

prevFrame = np.zeros([480,640])


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

def calculate_circularities(areas, arclengths):
	circs = []
	#print(len(areas))
	#print(len(arclengths))
	for (area, arclen) in zip(areas, arclengths):
		if area == 0:
			circs.append(0)
		else:
			perim = 4 * np.pi * arclen
			#print("perim: " + str(perim) + " area: " + str(area))
			circs.append(perim/area)

	return circs

def find_most_circular(circularities):
	smallest = 1e8
	smallindex = 0
	for i,circ in enumerate(circularities):
		if circ != 0:
			if np.abs(circ) <= smallest:
				smallest = np.abs(circ)
				smallindex = i
	return smallest, smallindex

def euclid_distance(p1, p2):
	total = 0
	for (e1, e2) in zip(p1,p2):
		total += np.square(e1-e2)
	return np.sqrt(total)

def near_frame_edge(shape,x,y,step):
	if y - 20 <= 0 or y + 20 >= shape[0]:
		return True
	if x - 20 <= 0 or x + 20 >= shape[1]:
		return True
	return False




def parse_chars(char, repeatNum):
	# a very simple parsing scheme
	s = ""
	if repeatNum <= 3:
		s += char
	if repeatNum >3 and repeatNum <= 5:
		s += char + char
	if repeatNum >5 and repeatNum <=7:
		s += char + char + char
	if repeatNum > 8:
		for i in range(int(repeatNum /3) + 2):
			s += char
	return s

# assuming a static background I can just add
def add_saturating(l, frame, N):
	if len(l) <= N:
		l.append(frame)
	return l

def add(l, sumval, N):
	l.append(sumval)
	if len(l) >= N:
		l = l[1:]
	return l

prevCoords = None
frameBuffer = []


while(1):

	# Take each frame
	_, frame = cap.read()
	#print(frame.shape)
	ret, thresh = cv2.threshold(frame, 254, 255, cv2.THRESH_BINARY)

	red = thresh[:,:,1]
	green = thresh[:,:,0]
	blue = thresh[:,:,2]
	avg = (green + blue) / 2
	#red = red - avg
	labels,num = measure.label(red, neighbors=8,background = 0, return_num=True)
	#print(num)
	mask = np.zeros(red.shape, dtype="uint8")
 
# loop over the unique components
	for label in np.unique(labels):
		# if this is the background label, ignore it
		if label == 0:
			continue
	 
		# otherwise, construct the label mask and count the
		# number of pixels 
		labelMask = np.zeros(red.shape, dtype="uint8")
		labelMask[labels == label] = 255
		numPixels = cv2.countNonZero(labelMask)
	 
		# if the number of pixels in the component is sufficiently
		# large, then add it to our mask of "large blobs"
		#print("Num pixels: ", numPixels)
		if numPixels > 20 and numPixels < 200:
			mask = cv2.add(mask, labelMask)
	#thresh = cv2.erode(red, None, iterations=4)
	#thresh = cv2.dilate(red, None, iterations=4) - look into doing this later! for more complex scenes?
	#edges = cv2.Canny(red, 100,200)
	#circles = cv2.HoughCircles(red, cv2.HOUGH_GRADIENT, 1,20,param1=30,param2=15,minRadius=1, maxRadius=30)
	#print(circles)
	#if circles is None:
	#	circles = []
	#if len(circles) >= 1:
	#	for circle in circles:
	#		if np.sum(np.array(circle)) > 0:
	#			x,y,r = circle[0]
	#			red = cv2.circle(np.copy(red), (x,y), r,255,3)

	#mask = cv2.erode(mask, None, iterations=2)
	#cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
	#cv2.CHAIN_APPROX_SIMPLE)
	#cnts = imutils.grab_contours(cnts)
	#print(cnts)
	#cnts = contours.sort_contours(cnts)[0]
 
# loop over the contours
	#for (i, c) in enumerate(cnts):
		# draw the bright spot on the image
	#	(x, y, w, h) = cv2.boundingRect(c)
	#	((cX, cY), radius) = cv2.minEnclosingCircle(c)
	#	cv2.circle(mask, (int(cX), int(cY)), int(radius),
	#		(0, 0, 255), 3)
	#	cv2.putText(mask, "#{}".format(i + 1), (x, y - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

	"""labels,num = measure.label(mask, neighbors=8,background = 0, return_num=True)
				print(num)
				mask = np.zeros(red.shape, dtype="uint8")
			 
			# loop over the unique components
				for label in np.unique(labels):
					# if this is the background label, ignore it
					if label == 0:
						continue
				 
					# otherwise, construct the label mask and count the
					# number of pixels 
					labelMask = np.zeros(red.shape, dtype="uint8")
					labelMask[labels == label] = 255
					numPixels = cv2.countNonZero(labelMask)
				 
					# if the number of pixels in the component is sufficiently
					# large, then add it to our mask of "large blobs"
					print("Num pixels: ", numPixels)
					if numPixels > 20 and numPixels < 1000:
						mask = cv2.add(mask, labelMask)"""

	#mask = cv2.dilate(mask,None, iterations=1)
	frameBuffer = add(frameBuffer, mask, 100)
	avg = np.mean(np.array(frameBuffer), axis=0)
	#print(avg.shape)
	mask = np.subtract(mask, avg)
	ret, mask = cv2.threshold(mask, 0,0, cv2.THRESH_TOZERO)
	ret, mask = cv2.threshold(mask,240, 255, cv2.THRESH_BINARY)
	#mask = np.subtract(mask, prevFrame)
	#ret, mask = cv2.threshold(mask, 0,0, cv2.THRESH_TOZERO)
	mask = mask.astype("uint8")
	prevFrame = mask



	minval, maxval, minLoc, maxLoc = cv2.minMaxLoc(mask) 
	im2, cnts,hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


	if len(cnts) > 0:
		areas = [cv2.contourArea(c) for c in cnts]
		arcLengths = [cv2.arcLength(c, True) for c in cnts]
		#print(areas)
		#print(arcLengths)
		circularities = calculate_circularities(areas, arcLengths)
		smallval, smallindex = find_most_circular(circularities)

		#print(circularities)

		#print("most circular: " + str(smallval) + "  " + str(smallindex))
		# need to filter contours by circularity as it does result in a useful contour?
		cnt = cnts[smallindex]
		#print(cnt)
		#cnt = cnts[np.argmax(areas)]
		#mask = cv2.drawContours(mask.copy(), cnts, -1, 255., 3)
		x,y,w,h = cv2.boundingRect(cnt)
		#print(x,y,w,h)
		cx,cy = (int(x+0.5*w), int(y+0.5*h))
		mask = cv2.rectangle(mask,(x,y),(x+w,y+h),255.,3)
		frameBuffer = add_saturating(frameBuffer, mask, 100)
		avg = np.mean(np.array(frameBuffer), axis=0)
		#print(avg.shape)

		if prevCoords is None:
			prevCoords = (cx,cy)
		dist = euclid_distance((cx,cy), prevCoords)
		#print("Dist:", dist)
		if dist <= 100 or 1 == 1:
			if not near_frame_edge(frame.shape, x,y,20):
				roi = frame[cy-15:cy+15,cx-15:cx+15]

			prevCoords = (cx,cy)

	s = np.sum(roi)
	#print("sum: ", s)
	sumlist = add(sumlist, s, 50)
	mu = sum(sumlist) / len(sumlist)
	#print(len(sumlist))
	#print("mu", mu)
	diff = s - mu
	#print(diff)
	bit = 1

	smask = np.sum(mask)
	masksumlist = add(masksumlist, smask, 50)
	mumask = sum(masksumlist) / len(masksumlist)
	diffmask = smask - mumask
	print(diffmask)

	bit = 0
	if diffmask > 0:
		bit = 1
	bitstr += str(bit)
	print(bitstr)


	#if diff >= 0: 
	#	bit = 0

	#char = str(bit)
	#bitstr += char
	#print(bit)
	#print(bitstr)
	#if char == prevChar:
	#	repeatNum +=1
	#else:
	#	trueString += parse_chars(char, repeatNum)
	#	repeatNum = 0
	#	print(trueString)
	#prevChar = char



	#mask = cv2.circle(mask, (maxLoc[0], maxLoc[1]), 20, 255., 3)
	#light = frame[maxLoc[1]-20: maxLoc[1]+20, maxLoc[0]-20:maxLoc[0]+20]
	#print(light.shape)

#
	cv2.imshow("webcam", frame)
	cv2.imshow("red", red)
	cv2.imshow("mask", mask)
	cv2.imshow("roi", roi)
	#cv2.imshow("light", light)
	#cv2.imshow("thresh", thresh)
	#cv2.imshow("edges", edges)


	if cv2.waitKey(1) == 27: 
 		break  # esc to quit