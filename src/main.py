from Detect import *


def main():
	cap = cv2.VideoCapture("vid/video.mp4")

	#cap = cv2.VideoCapture(3)
	D = Detection(cap)
	D.run()
	cap.release()
	cv2.destroyAllWindows()

	# cap = cv2.VideoCapture(3)

	# # Check if the webcam is opened correctly
	# if not cap.isOpened():
	#     raise IOError("Cannot open webcam")

	# while True:
	#     ret, frame = cap.read()
	#     frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
	#     cv2.imshow('Input', frame)

	#     c = cv2.waitKey(1)
	#     if c == 27:
	#         break

	# cap.release()
	# cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
	