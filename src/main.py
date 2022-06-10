from Detect import *

def download_video(file):
	cap = cv2.VideoCapture(2)
	out = cv2.VideoWriter("vid/{}.mp4".format(file),cv2.VideoWriter_fourcc(*"MJPG"), 30,(640,480))
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
	cap = cv2.VideoCapture(1)
	cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
	while(cap.isOpened()):
		ret, frame = cap.read()
		cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
		cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
		if ret==True:
			cv2.imshow('window',frame)
			if cv2.waitKey(1) & 0xFF == 27:
				break
		else:
			break
	# Release everything if job is finished
	cap.release()
	cv2.destroyAllWindows()


def main():
        if sys.argv[1] == 'video':
            cap = cv2.VideoCapture("vid/goal1.mp4")
        elif sys.argv[1] == 'play':
            cap = cv2.VideoCapture(3)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        D = Detection(cap, Debug = False)
        D.run()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
	try:
		if sys.argv[1] == 'test':
			film()
		else:
			main()
	except KeyboardInterrupt:
		pass
	except IndexError:
		print("Argument missing, use : main.py [video / play / test]")
