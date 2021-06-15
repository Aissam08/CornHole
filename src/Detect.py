from tracker import *
import time
import cv2
from Audio import *

class Detection():
    """docstring for Detection"""
    def __init__(self, clip):
        print("Starting detection. . .")
        self.tracker = EuclideanDistTracker()
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=150) #150
        self.clip = clip
        self.frame = None
        self.detected_hole = False
        self.detections = []
        self.contours = []
        self.hole_coord = []
        self.c = 2
        self.score_White = 0
        self.score_Black = 0
        self.DisplayGoal = 0

    def object_detection(self):
        ret, self.frame = self.clip.read()

        self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        try:
            height, width, _ = self.frame.shape
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
            return


        # 1. Object Detection
        mask = self.object_detector.apply(self.frame)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        #cv2.imshow("Mask", mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.detections = []

        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)

            if area > 285    and area < 2600:
                cv2.drawContours(self.frame, [cnt], -1, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.drawContours(mask, cnt, -1, 255, -1)
                r,b,v,_ = cv2.mean(self.frame, mask=mask)
                mean = (r+b+v)/3
                if mean< 100:  # If it's black team
                     self.c = 1
                     self.detections.append([x, y, w, h])
                else: # If it's white team
                    self.c = 0
                    self.detections.append([x, y, w, h])
                    

                
               # print(mean)
        

    def object_tracking(self):
        boxes_ids = self.tracker.update(self.detections, self.hole_coord)
        for box_id in boxes_ids:
            x, y, w, h,   id = box_id
            #cv2.putText(self.frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if self.tracker.goal:
            cv2.putText(self.frame, "GOAL !", (0 , round(self.frame.shape[1]/2) ), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255), 10)
            assistant_speaks("Do you want to see the video in slow motion ?")
            answer = get_audio()
            if answer == "yes":
                print("Yes")
            else:
                print("no")
            self.DisplayGoal = 15
            self.tracker.goal = False
            if self.c == 0:
                print("blanc")
                self.score_White = self.score_White + 1
            if self.c == 1:
                print("noir")
                self.score_Black = self.score_Black + 1
        
        if self.DisplayGoal > 0:
            cv2.putText(self.frame, "GOAL !", (0 , round(self.frame.shape[1]/2) ), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255), 10)
            self.DisplayGoal = self.DisplayGoal - 1

        cv2.putText(self.frame, "Score: ", (0 , round(self.frame.shape[1]*1.1) ), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3 )
        cv2.putText(self.frame, "White Team: {}".format(self.score_White), (round(self.frame.shape[0]/2.50), round(self.frame.shape[1]*1.2) ), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2 )
        cv2.putText(self.frame, "Black Team: {}".format(self.score_Black), (0 , round(self.frame.shape[1]*1.2) ), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2 )
        cv2.imshow("Frame", self.frame)
        #cv2.imshow("Frame", frame)
        #cv2.imshow("Mask", mask)

        key = cv2.waitKey(30)
        if key == 27:
            return 0
        else:
            return 1

    def get_hole(self):
        img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)
        hole = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 0.9, 120, param1 = 50, param2 = 30, minRadius = 20, maxRadius = 150)
        hole_rounded = np.uint16(np.around(hole))
        x,y,r = hole[0][0]
        self.detected_hole = True
        return x,y,r
        
    def run(self):
        while True:
            self.object_detection()
            if self.object_tracking() == 0:
                break