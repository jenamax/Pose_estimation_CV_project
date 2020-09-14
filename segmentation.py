import numpy as np
import cv2 
import glob
from sklearn.cluster import DBSCAN

bg = cv2.imread("images/background.png", 0)
for file in glob.glob("images/*"):
	img = cv2.imread(file, 0)
	seg = img
	seg = seg - cv2.GaussianBlur(seg,(51,51),0)

	ker_size = 13
	kernel = np.ones((ker_size,ker_size),np.float32)/ker_size**2
	#seg = cv2.filter2D(seg,-1,kernel)
	seg = cv2.Canny(seg, 130, 180)
	kernel = np.ones((7,7),np.uint8)
	seg = cv2.dilate(seg, kernel, iterations = 1)
	seg = 255 - seg
	seg = cv2.medianBlur(seg,3)
	seg = cv2.dilate(seg, kernel, iterations = 1)
	lines = cv2.HoughLines(seg,1,np.pi/180,30)
	for l in lines[0:30]:
		for rho,theta in l:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 10000*(-b))
			y1 = int(y0 + 10000*(a))
			x2 = int(x0 - 10000*(-b))
			y2 = int(y0 - 10000*(a))

			cv2.line(seg,(x1,y1),(x2,y2),255,2)
	# X = []
	# for i in range(0, seg.shape[1]):
	# 	for j in range(0, seg.shape[0]):
	# 		if seg[j, i] == 255:
	# 			X.append([i, j])
	# X = np.asarray(X)
	# clustering = DBSCAN(eps=2, min_samples=14).fit(X)
	# print(clustering.labels_)

	# C = X[clustering.labels_ == 1]
	# clust = np.zeros(seg.shape)
	# for c in C:
	# 	clust[c[1], c[0]] = 255
 
	

	cv2.imwrite("segmented/" + file.split("/")[1], seg)