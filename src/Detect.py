from tracker import *
import time
import cv2
from Audio import *
from random import *

class Detection():
	"""docstring for Detection"""
	def __init__(self, clip, Debug = False):
		print("Starting detection. . .")
		self.Debug = Debug
		self.tracker = EuclideanDistTracker()
		# self.object_detector = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=80)
		self.object_detector = cv2.createBackgroundSubtractorKNN(history=20, dist2Threshold=800, detectShadows = True)
		self.clip = clip
		self.frame = None
		self.detected_hole = False
		self.detections = []
		self.hole_coord = []
		self.board = []  
		self.color = 2 # -- 0 : white / 1: black
		self.is_white = False
		self.score_White = 0
		self.score_Black = 0
		self.DisplayGoal = 0
		self.cpt_frame = 0
		self.list_frame = []
		self.goal_index = 0
		self.count_goal = -1
		self.count_board = -1
		self.switch = -1
		self.started = False
		self.state_game = {'W': set(), 'B' : set()}
		self.last_state_game = {'W': set(), 'B' : set()}
		self.score1W = []
		self.score1B = []

	def starting_game(self):
		"""Initiate game and chose which team begin"""
		if randint(1,2) == 1:
			starter = "Black"
			self.switch = 0
		else:
			starter = "White"
			self.switch = 1

		if not self.Debug:
			phrase = "Starting Corn Hole game, "+starter+" team begin"
			assistant_speaks(phrase)

	def get_hole(self):
		"""Get hole coordinates and radius"""
		img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		img = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)
		hole = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 0.9, 120, param1 = 50, param2 = 30, minRadius = 20, maxRadius = 150)
		hole_rounded = np.uint16(np.around(hole))
		self.hole_coord = hole_rounded[0][0]
		self.detected_hole = True
		if self.hole_coord[2] > 41 : 
			self.hole_coord[2] -= 10
		elif self.hole_coord[2] < 31:
			self.hole_coord[2] += 4

		x, y ,r = self.hole_coord
		print("Hole detected: (x = {}, y = {}, r = {})"\
			.format(x,y,r))

	def get_board(self):
		"""Get board dimensions"""
		gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY) #convert roi into gray
		Blur=cv2.GaussianBlur(gray,(15,15),1) #apply blur to roi
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
				# cv2.drawContours(self.frame,cntrRect,-1,(0,255,0),2)
				self.board = cv2.boundingRect(i)

		print("Board detected : {}".format(self.board))

	def video_capture(self):
		ret, self.frame = self.clip.read()
		self.cpt_frame += 1

		self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
		self.list_frame.append(self.frame)

		try:
			height, width, _ = self.frame.shape 

		except AttributeError:
			print("Ending detection. . .")
			# assistant_speaks("Ending game")
			exit()

		#Hole and board detection : 
		if not self.detected_hole:
			self.get_hole()
			self.get_board()
			return


	def object_detection(self):
		"""Detect objects on screen"""
		mask = self.object_detector.apply(self.frame)

		mask_board = cv2.inRange(mask ,50,254)
		_, mask_goal = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)

		grid_RGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

		contour_board, _ = cv2.findContours(mask_board, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contour_goal, _ = cv2.findContours(mask_goal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		bright = cv2.inRange(grid_RGB ,130,254)

		xr, yr, wr, hr = self.board
		self.detections = []
		
		for cnt in contour_goal:
			# Calculate area and remove small elements
			area = cv2.contourArea(cnt)

			if area > 100 and area < 10000:
				x, y, w, h = cv2.boundingRect(cnt)
				cv2.drawContours(mask_goal, cnt, -1, 255, -1)
				a, b = (round(x+w/2), round(y+h/2))
				zone = bright[b-5:b+5,a-5:a+5]
				col = cv2.mean(zone)[0]
				if col < 150:  # If it's black team
					self.color = 1
					self.detections.append([x, y, w, h, self.color])
				else: # If it's white team
					self.color = 0
					self.detections.append([x, y, w, h, self.color])

		for cnt in contour_board:
			# Calculate area and remove small elements
			area = cv2.contourArea(cnt)
			if area > 100 and area < 10000:
				x, y, w, h = cv2.boundingRect(cnt)
				cv2.drawContours(mask_board, cnt, -1, 255, -1)
				a, b = (round(x+w/2), round(y+h/2))
				zone = bright[b-2:b+2,a-2:a+2]
				col = cv2.mean(zone)[0]
				if col < 150:  # If it's black team
					self.color = 1
					self.detections.append([x, y, w, h, self.color])
				else: # If it's white team
					self.color = 0
					self.detections.append([x, y, w, h, self.color])

	def display_game(self):
		self.video_capture()
		self.object_detection()


	def static_dist(self, coord):
		"""Return the distance between an object and the hole"""
		x,y,w,h = coord
		dx = x+w/2  - self.hole_coord[0]
		dy = y+h/2  - self.hole_coord[1]
		return math.hypot(dx , dy)

	def Distance(self,coord1, coord2):
		"""Return the distance between two objects"""
		dx = coord1[0] - coord2[0]
		dy = coord1[1] - coord2[1]
		return math.hypot(dx , dy)

	def border_lim(self,coord):
		"""Return True if an object is close to the border of the board, otherwise return False"""
		xr, yr, wr, hr = self.board
		x, y = coord
		if x < xr + 60 or x > xr + wr - 60:
			return True
		elif y < yr + 60 or y > yr + hr - 60:
			return True
		return False

	def update_state_game(self, objects, col):
		""" We check if the number of bags in dynamic > number of bag in static, it it's the case::
		we add bags detected in dynamic close to a bag in static in the static list in order to have the good number of bag in static 
		detection even if bags are really close to each other """
		xr, yr, wr, hr  = self.board
		if col == 'B':
			score = self.score1B

		if col == 'W':
			score = self.score1W

		for cnt in objects:
			if cv2.contourArea(cnt) > 1000 and cv2.contourArea(cnt) < 20000:
				x, y, w, h = cv2.boundingRect(cnt)
				a, b = (round(x+w/2), round(y+h/2))
				epsilon = 0.05*cv2.arcLength(cnt,True)
				approx = cv2.approxPolyDP(cnt,epsilon,True)
				if a > xr and a < xr + wr and len(approx) > 3:
					if b > yr and b < yr + hr and self.static_dist([x, y, w, h]) > self.hole_coord[2]:
						self.state_game[col].add((a,b))
						if len(score) > len(self.state_game[col]): # We check if the number of bag in static detection < number og bag in dynamic detection
							varB = len(self.state_game[col])
							for i in score:
								if self.Distance(i, (a,b)) < math.hypot(h,w) :
									self.state_game[col].add((a,b)) # We add in static list

	def update_score(self):
		"""Used to adjust the score when a bag is not anymore in board"""
		hole = self.hole_coord[0:2]
		for coord in self.last_state_game['W']: # self.last_state_game['W'] is all white bags which left the board
			if self.Distance(coord,hole) < self.hole_coord[2]*1.75 and self.Distance(coord,hole) > self.hole_coord[2]/3:
				self.score_White += 2 # If the bag coordinate are close to the hole we add +2
			elif self.border_lim(coord):
				self.score_White -= 1 # If the bag coordinate are close to borders of the board we add -1

		for coord in self.last_state_game['B']: # self.last_state_game['B'] is all black bags which left the board
			print(self.Distance(coord,hole))
			if self.Distance(coord,hole) < self.hole_coord[2]*1.75 and self.Distance(coord,hole) > self.hole_coord[2]/3:
				self.score_Black += 2 # If the bag coordinate are close to the hole we add +2
			elif self.border_lim(coord):
				self.score_Black -= 1 # If the bag coordinate are close to borders of the board we add -1


	def update_game(self):
		"""Used to detect all bags that left the board"""
		# if the size of the static list corresponding to the old frame > the size of the static list corresponding to the old frame:
		# We add in self.last_state_game['B'] all the bag which are only on the static list corresponding to the old frame
		if len(self.last_state_game['B']) > len(self.state_game['B']): 
			lb = []
			for i in self.last_state_game['B']:
				for j in self.state_game['B']:
					if self.Distance(i,j) < 100:
						lb.append(i)
						
			for b in lb:
				self.last_state_game['B'].remove(b)

		
		else:
			self.last_state_game['B'] = set()

		# We do the same for White
		if len(self.last_state_game['W']) > len(self.state_game['W']):
			lw = []
			for i in self.last_state_game['W']:
				for j in self.state_game['W']:
					if self.Distance(i,j) < 100:
						lw.append(i)
						
			for w in lw:
				self.last_state_game['W'].remove(w)
		
		
		else:
			self.last_state_game['W'] = set()
		
		self.update_score() # We call upadate_score in order to display the score corresponding
		self.last_state_game['W'] = set()
		self.last_state_game['B'] = set()
		for C, L in self.state_game.items(): # self.last_state_game = self.state_game
			for coord in L:
				self.last_state_game[C].add(coord)



	def static_detection(self):
		"""Detect all object on board and their color using the Static detection ( difference between the first frame and the actual frame)"""
		img1 = self.frame
		img2 = self.list_frame[0]


		# -- Get black and white objects
		diff1 = cv2.subtract(img2, img1)
		diff1 = cv2.GaussianBlur( cv2.cvtColor(diff1, cv2.COLOR_BGR2GRAY), (11,11), cv2.BORDER_DEFAULT)

		diff2 = cv2.subtract(img1, img2)
		diff2 = cv2.GaussianBlur( cv2.cvtColor(diff2, cv2.COLOR_BGR2GRAY), (13,13), cv2.BORDER_DEFAULT)

		bright_black = cv2.inRange(diff1 ,30, 255)
		bright_white = cv2.inRange(diff2 ,30, 255)
		
		blacks = cv2.findContours(bright_black, cv2.RETR_TREE ,cv2.CHAIN_APPROX_NONE)[0]
		whites = cv2.findContours(bright_white, cv2.RETR_TREE ,cv2.CHAIN_APPROX_NONE)[0]

		
		#-- List of objects on board
		self.state_game['W'] = set()
		self.state_game['B'] = set()

		self.update_state_game(blacks,'B')
		self.update_state_game(whites,'W')


		if self.cpt_frame % 50 == 0 and self.count_board < 0:
			self.update_game()



	def verif_goal(self):
		"""Score verification (+3)"""
		if self.tracker.goal:
			# -- Number of frame of goal
			self.goal_index = self.cpt_frame            
			if self.color == 0 and self.count_goal < 0:
				#-- White team scored
				self.switch = 0
				self.count_goal = 30
				self.is_white = True

			if self.color == 1 and self.count_goal < 0 :
				#-- Black team scored
				self.switch = 1
				self.count_goal = 30
				self.is_white = False

			if self.count_goal == 1:
				in_hole = False
				#-- If object detected in hole after 29 frames
				for id in self.tracker.list_goals:
					if self.tracker.distance(id,self.hole_coord) < self.hole_coord[2]/1.4:
						in_hole = True
						

				self.tracker.goal = False
				#-- Add 3 points if the bag is still in hole
				#-- Remove the bag from in-board list
				if in_hole:
					self.DisplayGoal = 15

					if self.tracker.first_color == 0 or self.tracker.white > self.tracker.black:
						self.score_White = self.score_White + 3
						self.tracker.is_detected = False

					elif self.tracker.center_points[id][2] == 0 and self.switch == 0:
						self.score_White = self.score_White + 3
					else:	
						self.score_Black = self.score_Black + 3
						self.tracker.is_detected = False

					self.tracker.white = 0
					self.tracker.black = 0					
					self.tracker.goal = False
					self.tracker.on_board = False


	def verif_board(self):
		"""Score verification (+1)"""

		#-- After 30 frames, verify on board bags

		if self.tracker.on_board and self.count_goal < 0:
			if self.color == 0:
				self.is_white = True

			if self.color== 1 :
				self.is_white = False

			self.tracker.on_board = False

			if self.count_board < 0:
				self.count_board = 50

		if self.count_board > -1:
			self.count_board -= 1
		
		if self.count_board == 20:
			in_board = False
			try:
				id = self.tracker.list_board[-1]
				if self.tracker.onBoard(id,self.board) and self.tracker.distance(id,self.hole_coord) > self.hole_coord[2]: 
					in_board = True
					xi, yi, ci = self.tracker.center_points[id]
					self.update_game()
					if ci == 0: # If the bag is white
						self.score_White = self.score_White + 1
						self.score1W.append(self.tracker.center_points[id])
						self.switch = 0
						self.tracker.is_detected = False

					else : # If the score is black

						self.score_Black = self.score_Black + 1
						self.score1B.append(self.tracker.center_points[id])
						self.switch = 1
						self.tracker.is_detected = False

			except IndexError:
				pass


	def verif_score(self):
		"""Increase and display score"""
		if self.count_goal > -1:
			self.count_goal -= 1

		self.verif_goal()
		self.verif_board()


	def verif_winner(self, score):
		"""End or restart game"""
		winner = ""

		#-- First team to reach argument score win
		if self.score_Black >= score:
			winner = "Black"

		if self.score_White >= score:
			winner = "White"
		
		qst = winner + "team won, do you want to replay ?"
		if winner != "":
			if self.ask_player(qst):
				self.restart_game()
			else:
				assistant_speaks("Ending game")
				print("Ending detection. . .")
				exit()

	def display_score(self):
		"""Show score on screen"""
		if self.DisplayGoal > 0:
			if self.score_White > 12:
				cv2.putText(self.frame, "WHITE TEAM WON!", (0 , round(self.frame.shape[1]/2) ), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255,255), 6)
			elif self.score_Black > 12:
				cv2.putText(self.frame, "BLACK TEAM WON!", (0 , round(self.frame.shape[1]/2) ), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 6)

			else:
				overlay = cv2.imread("img/goal.jpg")
				overlay = cv2.resize(overlay, self.frame.shape[0:2])
				# cv2.imshow("goal",overlay)
				cv2.addWeighted(overlay, 1, self.frame, 1 ,0, self.frame)
				cv2.putText(self.frame, "GOAL !", (0 , round(self.frame.shape[1]/2) ), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255), 10)
			self.DisplayGoal = self.DisplayGoal - 1
		
		if self.DisplayGoal == 5 and not self.Debug:
		  if self.ask_player("Goal, wanna see it in slow motion?"):
		      self.show_goal()

		if self.switch == 0:
			col = (0,0,0)
		else:
			col = (255,255,255)

		#-- Square color show which team has to play
		cv2.rectangle(self.frame, (round(self.frame.shape[0]/1.55), 10 ),\
		 (round(self.frame.shape[0]/1.55) + 50 , 60 ), col, -1)
		cv2.putText(self.frame, "Score: ", (0 , round(self.frame.shape[1]*1.1) ), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3 )
		cv2.putText(self.frame, "White Team: {}".format(self.score_White), (round(self.frame.shape[0]/2.50), \
			round(self.frame.shape[1]*1.2) ), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2 )
		cv2.putText(self.frame, "Black Team: {}".format(self.score_Black), (0 , round(self.frame.shape[1]*1.2) )\
			, cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2 )


	def corn_tracker(self):
		"""Study moving object position"""
		self.tracker.update_goal(self.detections, self.hole_coord, self.board)
		self.tracker.update_board(self.detections, self.hole_coord, self.board)

		self.static_detection()
		self.verif_score()
		self.display_score()

		x,y,w,h = self.board
		cv2.rectangle(self.frame, (x,y) , (x+w, y+h), (0,0,255), 1)
		
		frame = cv2.resize(self.frame, (720,640))
		cv2.imshow("Frame", frame)
		
		if not self.started: # If we start the game
			self.update_game()
			self.starting_game()
			self.started = True

		if not self.Debug: # If we want to have a winner
			self.verif_winner(12)
		
		key = cv2.waitKey(50)
		
		if key == ord('p'): # If we want to pause the program
			cv2.waitKey(-1)

		if key == 27:
			# assistant_speaks("Ending game")
			print("Ending detection. . .")
			return 0
		else:
			return 1


	def show_goal(self):
		"""Display the goal in slow motion"""
		for frame in self.list_frame[self.goal_index - 40:self.goal_index]:
			cv2.imshow('Ralenti',frame)
			key = cv2.waitKey(150) 
		cv2.destroyAllWindows() 

	def restart_game(self):
		"""Put all variable to initial value"""
		assistant_speaks("Restarting game")
		board = self.board
		clip = self.clip
		self.__init__(clip)
		self.board = board
		self.display_game()

	def ask_player(self, string):
		"""Vocal command"""
		assistant_speaks(string)
		answer = get_audio()
		if answer == "yes":
			return True
		else:
			return False

	def run(self):
		"""Running game"""
		while True:
			self.display_game()
			if self.corn_tracker() == 0:
				break