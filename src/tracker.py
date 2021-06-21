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
        self.on_board = False
        self.list_goals = []
        self.list_board = []

    def distance(self, id1, coord):
        dx = self.center_points[id1][0]  - coord[0]
        dy = self.center_points[id1][1] - coord[1]
        return math.hypot(dx , dy)

    def onBoard(self, id1, coord):
        cx = self.center_points[id1][0] 
        cy = self.center_points[id1][1]
        
        xr, yr, wr, hr = coord
        if cx > xr and cx < xr + wr and cy > yr and cy < yr + hr - 30:

            return True
        else:
            return False

    def update(self, objects_rect, coord, dim_rect):
        # Objects boxes and ids
        objects_bbs_ids = []
        # Get center point of new object
        
        for rect in objects_rect:  
            x, y, w, h= rect
            cx = x + w/2
            cy = y + h/ 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                
                if dist < 40 and dist > 2:                    
                    if self.distance(id,coord) < coord[2]/2:
                        if id not in self.list_goals:
                            # print("Speed:{}".format(dist))
                            # print("Distance :{}".format(self.distance(id,coord)))
                            self.list_goals.append(id)
                            self.goal = True
                    else:
                         xr, yr, wr, hr = dim_rect
                         if cx > xr and cx < xr + wr and cy > yr and cy < yr + hr:
                             if id not in self.list_board:
                                self.list_board.append(id)
                                self.on_board = True


                if dist >= 40 and dist < 100:
                    self.center_points[id] = (cx, cy)
                    #print("id:{} \t x: {} y:{}".format(id,cx,cy))
                    if self.distance(id,coord) < coord[2]/1.4 and id not in self.list_goals:
                        # print("Speed:{}".format(dist))
                        # print("Distance :{}".format(self.distance(id,coord)))
                        self.list_goals.append(id)
                        self.goal = True
                        #print(self.list_goals)


                    same_object_detected = True

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                self.list_objects.append((cx,cy))
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1     
        
        return objects_bbs_ids