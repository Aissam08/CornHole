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
        self.goal = False
        self.list_goals = []

# (140,120)
# (145,115)
# (390,130)

    def distance(self, id1, coord):
        dx = self.center_points[id1][0]  - coord[0]
        dy = self.center_points[id1][1] - coord[1]
        return math.hypot(dx , dy)

    def update(self, objects_rect,coord):
        # Objects boxes and ids
        objects_bbs_ids = []
        #if len(objects_rect) > 0:
        # Get center point of new object
       
        
        for rect in objects_rect:
            
            x, y, w, h= rect
            cx = x + w/2
            cy = y + h/ 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                #print(dist)

                if dist > 30 and dist < 800:
                    self.center_points[id] = (cx, cy)
                    #print(self.distance(id,coord))
                    #print("id:{} \t x: {} y:{}".format(id,cx,cy))
                    if self.distance(id,coord) < coord[2] and id not in self.list_goals:
                        self.list_goals.append(id)
                        #print(self.distance(id,coord))
                        #print(self.list_goals)
                        #print(id)                
                        # print("id:{} \t dist:{} ".format(id,self.distance(id,coord)))
                        self.goal = True
                    same_object_detected = True
                    # break
               # if dist < 8 :
                        # print("fixe")
                        # print(x)
                        # print(y)
                    
                #     same_object_detected = True
                #     #print("Objet fixe : {}".format(id))


            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                self.list_objects.append((cx,cy))
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        """
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center
        
        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()       
        """
        return objects_bbs_ids
        

"""
    def distance(self, id1):
        dx = self.center_points[id1][0]  - 140 #video 2
        dy = self.center_points[id1][1] - 120
      #  dx = self.center_points[id1][0]  - 125 #video3
      #  dy = self.center_points[id1][1] - 90
       # dx = self.center_points[id1][0]  - 130 video 2v2
       # dy = self.center_points[id1][1] - 110
        return round(math.hypot(dx , dy),4)

"""