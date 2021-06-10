import cv2
from tracker import *

# Create tracker object
tracker = EuclideanDistTracker()

#cap = cv2.VideoCapture("highway.mp4")
cap = cv2.VideoCapture("vid/lancer.mp4")

# Object detection from Stable camera
<<<<<<< HEAD
# 100 et 5
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=10)
#object_detector = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold = 400, detectShadows = False)
=======
#object_detector = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=10)
object_detector = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold = 400, detectShadows = False)
>>>>>>> 4577efc8e845c9d95fba17eb47f3f090aabd533b

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # Extract Region of interest
   # roi = frame[340: 720,500: 800]

    # 1. Object Detection
    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        
        if area > 2000  and area < 3000:
        #if area > 100:
            #print(area)
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            print(area)
            x, y, w, h = cv2.boundingRect(cnt)

            detections.append([x, y, w, h])

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("frame", frame)
    #cv2.imshow("Frame", frame)
    #cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()