from Detect import *
import os
import pathlib

def download_video():
	cap = cv2.VideoCapture(2)
	out = cv2.VideoWriter('vid/goal3.mp4',cv2.VideoWriter_fourcc(*"MJPG"), 30,(640,480))

	while(cap.isOpened()):
	    ret, frame = cap.read()
	    if ret==True:
	        cv2.imshow('frame',frame)
	        out.write(frame)
	        if cv2.waitKey(1) & 0xFF == ord('q'):
	            break
	    else:
	        break
	# Release everything if job is finished
	cap.release()
	out.release()
	cv2.destroyAllWindows()


def film():
	cap = cv2.VideoCapture(2)
	cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
	while(cap.isOpened()):
	    ret, frame = cap.read()
	    if ret==True:
	        cv2.imshow('frame',frame)
	        if cv2.waitKey(1) & 0xFF == 27:
	            break
	    else:
	        break
	# Release everything if job is finished
	cap.release()
	cv2.destroyAllWindows()


def main():
	cap = cv2.VideoCapture("vid/goal1.mp4")
	# cap = cv2.VideoCapture(2)
	cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
	D = Detection(cap, Debug = False)
	D.run()
	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass
	# __rootpath__ = str(pathlib.Path(__file__).parent.parent)
	# filenames = next(os.walk(__rootpath__), (None, None, []))[2]  # [] if no file	# download_video()
	# print(filenames)
	# film()
