from Detect import *


def download_video():
	cap = cv2.VideoCapture(2)
	#out = cv2.VideoWriter('vid/video4.mp4',cv2.VideoWriter_fourcc(*"MJPG"), 30,(640,480))

	while(cap.isOpened()):
	    ret, frame = cap.read()
	    if ret==True:
	        # frame = cv2.flip(frame,0)
	        cv2.imwrite("photo_vide.jpg",frame)
	        #contours, _ = cv2.findContours(frame, cv2.RETR_FLOODFILL, cv2.CHAIN_APPROX_SIMPLE)
	        #cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
	        # write the flipped frame
	       # out.write(frame)

	        cv2.imshow('frame',frame)
	        if cv2.waitKey(1) & 0xFF == ord('q'):
	            break
	    else:
	        break
	# Release everything if job is finished
	cap.release()
	# out.release()
	cv2.destroyAllWindows()


def main():
	cap = cv2.VideoCapture("vid/video.mp4")
	# cap = cv2.VideoCapture(2)
	D = Detection(cap)
	D.run()
	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	#main()
	#download_video()
	img1 = cv2.imread("photo.jpg")
	# img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
	img2 = cv2.imread("photo_vide.jpg")
	# img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
	img = np.abs(img2 - img1)
	# self.object_detector = cv2.createBackgroundSubtractorKNN(history=50, dist2Threshold=800, detectShadows = True)
	# mask = self.object_detector.apply(img1)
	# _, mask = cv2.threshold(mask, 253, 255, cv2.THRESH_BINARY)
	# grid_RGB = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
	# bright = cv2.inRange(grid_RGB ,70,254)
	# contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	while True:
		cv2.imshow("img",img)
		cv2.imshow("img1",img1)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	    
	cv2.destroyAllWindows()