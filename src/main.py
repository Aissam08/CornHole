from Detect import *


def main():
	cap = cv2.VideoCapture("vid/lancer2.mp4")
	#cap = cv2.VideoCapture(2)
	D = Detection(cap)
	D.run()
	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()
	