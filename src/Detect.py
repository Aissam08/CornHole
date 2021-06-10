from tracker import *
import cv2

class Detection():
    """docstring for Detection"""
    def __init__(self, clip):
        print("Starting detection. . .")
        self.tracker = EuclideanDistTracker()
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=100)
        self.clip = clip
        self.detections = []
        self.roi = None
        self.contours = []
        self.detected_hole = False
        self.hole_coord = []

    def object_detection(self):
        ret, frame = self.clip.read()

        #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        try:
            height, width, _ = frame.shape
        except AttributeError:
            print("Ending detection. . .")
            exit()

        # Extract Region of interest
        self.roi = frame 

        # Hole detection : 
        if not self.detected_hole:
            self.hole_coord = self.get_hole()
            print("Hole detected: (x = {}, y = {}, r = {})"\
                .format(self.hole_coord[0],self.hole_coord[1],\
                    self.hole_coord[2]))

            self.detected_hole = True
            return


        # 1. Object Detection
        mask = self.object_detector.apply(self.roi)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        #cv2.imshow("Mask", mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.detections = []

        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)

            if area > 285    and area < 2600:
                cv2.drawContours(self.roi, [cnt], -1, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(cnt)
                self.detections.append([x, y, w, h])
        

    def object_tracking(self):
        boxes_ids = self.tracker.update(self.detections, self.hole_coord)
        for box_id in boxes_ids:
            x, y, w, h, id = box_id
            cv2.putText(self.roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(self.roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.imshow("Frame", self.roi)
        #cv2.imshow("Frame", frame)
        #cv2.imshow("Mask", mask)

        key = cv2.waitKey(30)
        if key == 27:
            return 0
        else:
            return 1

    def get_hole(self):
        img = cv2.cvtColor(self.roi, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)
        hole = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 0.5, 120, param1 = 50, param2 = 30, minRadius = 20, maxRadius = 150)
        hole_rounded = np.uint16(np.around(hole))
        x,y,r = hole[0][0]
        self.detected_hole = True
        return x,y,r
        
    def run(self):
        while True:
            self.object_detection()
            if self.object_tracking() == 0:
                break

<<<<<<< HEAD:src/Detect.py
=======

# Create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("vid/lancer2.mp4")
D = Detection(cap)
D.run()
cap.release()
cv2.destroyAllWindows()



"""
0 : Truc inutile
1 : Sac noir près du trou
2 : Sac rouge en haut à gauche
3/4/5 : Objets immobiles
"""
>>>>>>> 02dcaa456b4b59386fcf4e175622cade04791b48:object_tracking/Detect.py
