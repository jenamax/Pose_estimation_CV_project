import numpy as np
import cv2 
import glob
from matplotlib import pyplot as plt


def differ(rho, theta, marks_rhos, marks_thetas):
    trsh = 170
    if len(marks_rhos) == 0:  # if no lines were examined => treat current one as separate
        return True

    # compute coordinates of intersection point of current line and normal from origin
    x0 = rho * np.cos(theta)
    y0 = rho * np.sin(theta)

    for i in range(0, len(marks_rhos)):  # traverse list of parameters
        # compute coordinates of intersection point of line from list and normal from origin
        x1 = marks_rhos[i] * np.cos(marks_thetas[i])
        y1 = marks_rhos[i] * np.sin(marks_thetas[i])

        # use distance by x and y between intersection points as metrics of similarity;
        if abs(x0 - x1) < trsh and abs(y0 - y1) < trsh:
            return False
    return True

def intersection(line1, line2):
    """Finds the intersection of two lines given in Hesse normal form.

    Returns closest integer pixel locations.
    See https://stackoverflow.com/a/383527/5087436
    """
    [rho1, theta1] = line1
    [rho2, theta2] = line2
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    return (x0, y0)

def CoM(img):
	x = 0
	y = 0
	for i in range(0, img.shape[0]):
		for j in range(0, img.shape[1]):
			x += img[i, j] * j 
			y += img[i, j] * i
	x /= np.sum(img)
	y /= np.sum(img)
	return (int(x), int(y))

bg = cv2.imread("images/background.png", 0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
cap = cv2.VideoCapture("best_res.avi")
k = 0
while True:
	try:
		ret, img = cap.read()
		seg = np.copy(img)
		seg = seg - cv2.GaussianBlur(seg,(51,51),0)

		ker_size = 13
		kernel = np.ones((ker_size,ker_size),np.float32)/ker_size**2
		#seg = cv2.filter2D(seg,-1,kernel)
		seg = cv2.Canny(seg, 130, 180)
		kernel = np.ones((7,7),np.uint8)
		seg = cv2.dilate(seg, kernel, iterations = 1)
		seg = 255 - seg
		seg = cv2.medianBlur(seg,3)
		#seg = cv2.dilate(seg, kernel, iterations = 1)

		com = CoM(seg)
		thrs = int(np.sum(seg) // 31000)
		print(thrs)
		lines = cv2.HoughLines(seg,1,np.pi/180,thrs)
		thetas = []
		rhos = []
		for l in lines[0:20]:
			for rho,theta in l:
				a = np.cos(theta)
				b = np.sin(theta)
				x0 = a*rho
				y0 = b*rho
				x1 = int(x0 + 10000*(-b))
				y1 = int(y0 + 10000*(a))
				x2 = int(x0 - 10000*(-b))
				y2 = int(y0 - 10000*(a))
				if differ(rho, theta, rhos, thetas):
						cv2.line(seg, (x1, y1), (x2, y2), [255, 0, 0], 1)
						thetas.append(theta)
						rhos.append(rho)

				#cv2.line(seg,(x1,y1),(x2,y2),255,2)
		cv2.imwrite("res.png", seg)
		found = False
		seg = cv2.cvtColor(seg, cv2.COLOR_GRAY2RGB)
		for i in range(0, len(rhos)):
			for j in range(0, len(rhos)):
				if abs(thetas[i] - thetas[j]) > 0.5:
					p = intersection([rhos[i], thetas[i]], [rhos[j], thetas[j]])
					theta_x = min(thetas[i], thetas[j])
					theta_y = max(thetas[i], thetas[j])
					px = (int(p[0] + np.sign(com[0] - p[0]) * 100 * np.cos(theta_x)), int(p[1] + np.sign(com[1] - p[1]) * 100 * np.sin(theta_x)))
					py = (int(p[0] + np.sign(com[0] - p[0]) * 100 * np.cos(theta_y)), int(p[1] + np.sign(com[1] - p[1]) * 100 * np.sin(theta_y)))
					cv2.circle(seg, p, 20, (255, 0, 0), thickness=-1)
					cv2.circle(seg, px, 20, (255, 0, 0), thickness=-1)
					cv2.circle(seg, py, 20, (255, 0, 0), thickness=-1)
					found = True
					break
			if found:
				break
		out.write(seg)
		seg = np.concatenate([img, seg])
		cv2.imwrite("segmented/" + str(k) + ".png", seg)
		k += 1

		print("Edge pos: ", p)
		print("X axis (two points): ", p, px)
		print("Y axis (two points): ", p, py)
		print()
	except KeyboardInterrupt:
		cap.release()
		out.release()
		break