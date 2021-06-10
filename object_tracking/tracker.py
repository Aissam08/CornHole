import math
import numpy as np
import os

class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        self.list_objects = []
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

# (140,120)
# (145,115)
# (390,130)
    def distance(self, id1):
        dx = self.center_points[id1][0]  - 140
        dy = self.center_points[id1][1] - 120
       # dx = self.center_points[id1][0]  - 125
       # dy = self.center_points[id1][1] - 90
        return round(math.hypot(dx , dy),4)

    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []
        #if len(objects_rect) > 0:
        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = x #(x + x + w) // 2
            cy = y #(y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False

            #print(self.center_points)
            #print("objet : {} -- {} x: {} y: {}".format(id,self.distance(id),cx,cy))
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                #print(dist)
                if dist > 10 and dist < 800:
                    self.center_points[id] = (cx, cy)
                    if self.distance(id) < 25:
                        print("object : {} is in hole".format(id))
                    else:
                       # print("object {} : \t distance to hole : {} \t position: ({},{})".format(id,self.distance(id),cx,cy))
                        objects_bbs_ids.append([x, y, w, h, id])
                     
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                self.list_objects.append((cx,cy))
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center
        
        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        
        return objects_bbs_ids
        