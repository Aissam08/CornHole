from tracker import *
import time
import cv2
from Audio import *

class Detection():
	"""docstring for Detection"""
	def __init__(self, clip):
		print("Starting detection. . .")
		self.tracker = EuclideanDistTracker()
		# self.object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=800)
		self.object_detector = cv2.createBackgroundSubtractorKNN(history=100, dist2Threshold=800, detectShadows = True)
		self.clip = clip
		self.frame = None
		self.out = None
		self.detected_hole = False
		self.detections = []
		self.contours = []
		self.hole_coord = []
		self.board = []
		self.c = 2
		self.is_white = False
		self.score_White = 0
		self.score_Black = 0
		self.DisplayGoal = 0
		self.cpt_frame = 0
		self.list_frame = []
		self.goal_index = 0
		self.count_goal = -1
		self.count_board = -1
		#self.save()

	def save(self):
		width = int(self.clip.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
		height = int(self.clip.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
		self.size = (width, height)
		self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
		self.out = cv2.VideoWriter('output.avi', self.fourcc, 20.0, self.size)

	def object_detection(self):
		ret, self.frame = self.clip.read()
		self.cpt_frame += 1

		self.list_frame.append(self.frame)

		self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
		
		try:
			height, width, _ = self.frame.shape
			#self.out.write(self.frame)
		except AttributeError:
			print("Ending detection. . .")
			exit()

		# Hole detection : 
		if not self.detected_hole:
			self.hole_coord = self.get_hole()
			print("Hole detected: (x = {}, y = {}, r = {})"\
				.format(self.hole_coord[0],self.hole_coord[1],\
					self.hole_coord[2]))

			self.detected_hole = True

			self.get_rectangle()
			return


		# 1. Object Detection
		#blurred_frame = cv2.GaussianBlur(self.frame, (167,167), cv2.BORDER_DEFAULT) 
		mask = self.object_detector.apply(self.frame)
		_, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
		#cv2.imshow("Mask", blurred_frame)
		contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		self.detections = []
		i = 0

		for cnt in contours:
			i += 1
			# Calculate area and remove small elements
			area = cv2.contourArea(cnt)
			# if area > 20:
			# 	print(area)
			if area > 100 and area < 2600:
				cv2.drawContours(self.frame, [cnt], -1, (0, 255, 0), 2)
				x, y, w, h = cv2.boundingRect(cnt)
				#print("num : {} \t x: {} \t y: {} \t w: {} \t h: {}".format(i,x,y,w,h))
				cv2.drawContours(mask, cnt, -1, 255, -1)
				r,b,v,_ = cv2.mean(self.frame, mask=mask)
				#print("Couleur: (r = {}, b = {}, v = {})".format(r,b,v))
				mean = (r+v)/2
				#print("Vert : {}".format(v))
				
				if v < 40:  # If it's black team
					 self.c = 1
					 self.detections.append([x, y, w, h])
				else: # If it's white team
					self.c = 0
					self.detections.append([x, y, w, h])
				#print(mean)
				

		

	def object_tracking(self):
		boxes_ids = self.tracker.update(self.detections, self.hole_coord, self.board)
		for box_id in boxes_ids:
			x, y, w, h, id = box_id
			cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

		if self.tracker.goal:
			self.goal_index = self.cpt_frame
			cv2.putText(self.frame, "GOAL !", (0 , round(self.frame.shape[1]/2) ), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255), 10)

			if self.c == 0 and self.count_goal < 0:
				#self.score_White = self.score_White + 3	
				self.count_goal = 30
				#print("blanc")
				self.is_white = True

			if self.c == 1 and self.count_goal < 0 :
				#self.score_Black = self.score_Black + 3
				self.count_goal = 30
				#print("noir")
				self.is_white = False

			if self.count_goal > -1:
				self.count_goal -= 1

			#print(self.count_goal)

			if self.count_goal == 5:
				in_hole = False
				for id in self.tracker.list_goals:
					if self.tracker.distance(id,self.hole_coord) < self.hole_coord[2]:
						in_hole = True	
						#print(self.tracker.distance(id,self.hole_coord))				
				self.tracker.goal = False
				if in_hole:
					if self.is_white:
						self.score_White = self.score_White + 3
					else:
						self.score_Black = self.score_Black + 3
					
					assistant_speaks("Do you want to see your goal in slow motion ?")
					answer = get_audio()

					if answer == "yes":
						print("Yes")
						self.show_goal()
					else:
						print("no")


					self.DisplayGoal = 15
					self.tracker.goal = False


		if self.tracker.on_board and self.count_goal < 0:
			
			self.tracker.on_board = False

			if self.c == 0 and self.count_board < 0:
				self.score_White = self.score_White + 1
				self.count_board = 10

			if self.c == 1 and self.count_board < 0 :
				self.score_Black = self.score_Black + 1
				self.count_board = 10





		if self.count_board > -1:
			self.count_board -= 1

		if self.DisplayGoal > 0:
			cv2.putText(self.frame, "GOAL !", (0 , round(self.frame.shape[1]/2) ), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255), 10)
			self.DisplayGoal = self.DisplayGoal - 1
		
	   

		cv2.putText(self.frame, "Score: ", (0 , round(self.frame.shape[1]*1.1) ), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3 )
		cv2.putText(self.frame, "White Team: {}".format(self.score_White), (round(self.frame.shape[0]/2.50), round(self.frame.shape[1]*1.2) ), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2 )
		cv2.putText(self.frame, "Black Team: {}".format(self.score_Black), (0 , round(self.frame.shape[1]*1.2) ), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2 )
		cv2.imshow("Frame", self.frame)
		


		key = cv2.waitKey(1) #60
		if key == 27:
			return 0
		else:
			return 1

	def get_hole(self):
		img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		img = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)
		hole = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 0.9, 120, param1 = 50, param2 = 30, minRadius = 20, maxRadius = 150)
		hole_rounded = np.uint16(np.around(hole))
		x,y,r = hole_rounded[0][0]
		self.detected_hole = True
		return x,y,r
	
	def get_triangle(self):
		image_obj = self.frame
		gray = cv2.cvtColor(image_obj, cv2.COLOR_BGR2GRAY)
		kernel = np.ones((4, 4), np.uint8)
		dilation = cv2.dilate(gray, kernel, iterations=1)
		blur = cv2.GaussianBlur(dilation, (5, 5), 0)

		thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
		contours, _ = cv2.findContours(\
			thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		coordinates = []
		for cnt in contours:
				# [point_x, point_y, width, height] = cv2.boundingRect(cnt)
			approx = cv2.approxPolyDP(
				cnt, 0.07 * cv2.arcLength(cnt, True), True)
			if len(approx) == 4:
				coordinates.append([cnt])
				cv2.drawContours(image_obj, [cnt], 0, (0, 0, 255), 3)
		cv2.imwrite("result.png", image_obj)


	def get_rectangle(self):
		gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY) #convert roi into gray
		Blur=cv2.GaussianBlur(gray,(5,5),1) #apply blur to roi
		Canny=cv2.Canny(Blur,10,50) #apply canny to roi

		#Find my contours
		contours =cv2.findContours(Canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]

		#Loop through my contours to find rectangles and put them in a list, so i can view them individually later.
		cntrRect = []
		for i in contours:
				epsilon = 0.05*cv2.arcLength(i,True)
				approx = cv2.approxPolyDP(i,epsilon,True)
				
				if cv2.contourArea(i) > 70000 and len(approx) == 4:
					cntrRect.append(approx)
					cv2.drawContours(self.frame,cntrRect,-1,(0,255,0),2)
					self.board = cv2.boundingRect(i)

		print(self.board)
		cv2.imwrite("rectangle.png",self.frame)


	def show_goal(self):
		for frame in self.list_frame[self.goal_index - 50:self.goal_index]:
			cv2.imshow('Ralenti', frame)
			key = cv2.waitKey(100)
			if key == 27:
				break    
		cv2.destroyAllWindows()	

	def run(self):
		while True:
			self.object_detection()
			if self.object_tracking() == 0:
				break