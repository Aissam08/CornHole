from Detect import *


def main():
	cap = cv2.VideoCapture("vid/lancer3.mp4")
	#cap = cv2.VideoCapture(0)
	D = Detection(cap)
	D.run()
	cap.release()
	cv22.destroyAllWindows()


if __name__ == '__main__':
	main()
	