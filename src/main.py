from Detect import *


def main():
	cap = cv2.VideoCapture("vid/video.mp4")
	D = Detection(cap)
	D.run()
	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()
	