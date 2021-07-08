
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
        self.col = 0
        self.white = 0
        self.black = 0
        self.first_color = -1
        self.is_detected = False

    def distance(self, id1, coord):
        dx = self.center_points[id1][0]  - coord[0]
        dy = self.center_points[id1][1] - coord[1]
        return math.hypot(dx , dy)

    def inHole(self, obj, coord):
        x, y = obj
        dx = x - coord[0]
        dy = y - coord[1]
        # print("Distance : {} \t color :".format(round(math.hypot(dx , dy))),end=" ")
        if math.hypot(dx , dy) < coord[2]:
            return True

        return False

    def onBoard(self, id1, coord):
        cx = self.center_points[id1][0] 
        cy = self.center_points[id1][1]
        
        # A ajouter : Retourner False quand on est dans le trou 
        xr, yr, wr, hr = coord
        if cx > xr and cx < xr + wr and cy > yr and cy < yr + hr:
            return True
        else:
            return False


    def update_board(self, objects_rect, coord, dim_rect):
        objects_bbs_ids = []
        for rect in objects_rect:  
            x, y, w, h, col = rect
            cx = x + w/2
            cy = y + h/ 2
            xr, yr, wr, hr = dim_rect
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                if dist < 40 and dist > 10:    
                    if cx > xr and cx < xr + wr and cy > yr and cy < yr + hr:
                        if id not in self.list_board:
                            self.list_board.append(id)
                            self.on_board = True
                    same_object_detected = True

            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy, col)
                self.list_objects.append((cx,cy))
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1
                if not self.is_detected:
                    self.first_color = col
                    # print("Board -  coord : ({},{}) \t col : {}".format(cx,cy,col))
                    self.is_detected = True


    def update_goal(self, objects_rect, coord, dim_rect):
        # Objects boxes and ids
        objects_bbs_ids = []
        # Get center point of new object
        
        for rect in objects_rect:  
            x, y, w, h, col = rect
            cx = x + w/2
            cy = y + h/ 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                if dist < 40 and dist > 10:              
                    #if self.distance(id,coord) < coord[2]/1.5:
                    if self.inHole((cx,cy),coord):
                        if id not in self.list_goals:
                            self.list_goals.append(id)
                            self.goal = True
                            # if  not self.inHole((cx,cy),coord):
                            self.col = col
                            if(self.col == 0):
                                self.white +=1
                            else:
                                self.black +=1


                if dist >= 40 and dist < 100:
                    self.center_points[id] = (cx, cy, col)
                    #print("id:{} \t x: {} y:{}".format(id,cx,cy))
                    if self.distance(id,coord) < coord[2]/1.4 and id not in self.list_goals:
                        # print("Speed:{}".format(dist))
                        # print("Distance :{}".format(self.distance(id,coord)))
                        # print(id)
                        # print(self.center_points[id])
                        self.list_goals.append(id)
                        self.goal = True
                        if  not self.inHole((cx,cy),coord):
                            self.col = col
                            if(self.col == 0):
                                self.white +=1
                            else:
                                self.black +=1


                    same_object_detected = True

            # New object is detected we assign the ID to that object
            if same_object_detected is False :
                self.center_points[self.id_count] = (cx, cy, col)
                self.list_objects.append((cx,cy))
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1
                if not self.is_detected:
                    self.first_color = col
                    self.is_detected = True

        
        # new_center_points = {}
        # for obj_bb_id in objects_bbs_ids:
        #     _, _, _, _, object_id = obj_bb_id
        #     center = self.center_points[object_id]
        #     new_center_points[object_id] = center
        
        # # Update dictionary with IDs not used removed
        # self.center_points = new_center_points.copy()
        # return objects_bbs_ids