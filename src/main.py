from Detect import *


def download_video():
	cap = cv2.VideoCapture(3)
	#out = cv2.VideoWriter('vid/video4.mp4',cv2.VideoWriter_fourcc(*"MJPG"), 30,(640,480))

	while(cap.isOpened()):
	    ret, frame = cap.read()
	    if ret==True:
	        #frame = cv2.flip(frame,0)

	        # write the flipped frame
	        #out.write(frame)

	        cv2.imshow('frame',frame)
	        if cv2.waitKey(1) & 0xFF == ord('q'):
	            break
	    else:
	        break
	# Release everything if job is finished
	cap.release()
	#out.release()
	cv2.destroyAllWindows()


def main():
	cap = cv2.VideoCapture("vid/video4.mp4")
	#cap = cv2.VideoCapture(2)
	D = Detection(cap)
	D.run()
	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()
	#download_video()
