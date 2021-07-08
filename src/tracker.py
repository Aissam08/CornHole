
import math
import numpy as np
import os

class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {} #-- object's id and position 
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
        self.first_color = -1 #-- first color detected
        self.is_detected = False

    def distance(self, id1, coord):
        """Give distance bitween objectd id1 and other point"""
        dx = self.center_points[id1][0]  - coord[0]
        dy = self.center_points[id1][1] - coord[1]
        return round(math.hypot(dx , dy))

    def inHole(self, obj, coord):
        """Tell if an object is in hole (coord)"""
        x, y = obj
        dx = x - coord[0]
        dy = y - coord[1]
        #-- Distance is in pixel
        if math.hypot(dx , dy) < coord[2]:
            return True

        return False

    def onBoard(self, id1, coord):
        """Tell if an object is on board"""
        cx = self.center_points[id1][0] 
        cy = self.center_points[id1][1]
        
        xr, yr, wr, hr = coord
        if cx > xr and cx < xr + wr and cy > yr and cy < yr + hr:
            return True
        else:
            return False


    def update_board(self, objects_rect, coord, dim_rect):
        """Analyse all moving object's position"""

        # Get center point of new object 
        for rect in objects_rect:  
            x, y, w, h, col = rect #-- bag position
            cx = x + w/2
            cy = y + h/ 2
            xr, yr, wr, hr = dim_rect #-- board dimensions
            same_object_detected = False
            for id, pt in self.center_points.items():
                #-- speed is in pixel by frame
                #-- used for computer vision, not exact values
                speed = math.hypot(cx - pt[0], cy - pt[1])
                if speed < 40 and speed > 10:    
                    if cx > xr and cx < xr + wr and cy > yr and cy < yr + hr:
                        if id not in self.list_board:
                            #-- Save all objects detected on board
                            self.list_board.append(id)
                            self.on_board = True
                    same_object_detected = True

            if same_object_detected is False:
                #-- new object detected
                self.center_points[self.id_count] = (cx, cy, col)
                self.id_count += 1
                if not self.is_detected:
                    #-- save its color
                    self.first_color = col
                    self.is_detected = True


    def update_goal(self, objects_rect, coord, dim_rect):
        """Analyse moving object from different mask"""       
        
        #-- same algorithm than update_board
        for rect in objects_rect:  
            x, y, w, h, col = rect
            cx = x + w/2
            cy = y + h/2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                speed= math.hypot(cx - pt[0], cy - pt[1])

                #-- slow objects
                if speed < 40 and speed> 10:   
                    #-- many black and points detected for all objects
                    #-- we keep the most present color 
                    if(col == 0):
                        self.white +=1
                    else:
                        self.black +=1
                    if self.distance(id,coord) < coord[2]/1.5:
                        #-- detected only objects which fall in hole
                        if id not in self.list_goals:
                            self.list_goals.append(id)
                            self.goal = True
                            if not self.inHole((cx,cy),coord):
                                #-- get color of last objects detected out of the hole
                                #-- in case if there are several bags in it
                                self.col = col
                                

                #-- fast objects
                if speed >= 40 and speed < 100:
                    self.center_points[id] = (cx, cy, col)
                    if(col == 0):
                        self.white +=1
                    else:
                        self.black +=1
                    if self.distance(id,coord) < coord[2]/1.4 and id not in self.list_goals:
                        self.list_goals.append(id)
                        self.goal = True

                        if not self.inHole((cx,cy),coord):
                            self.col = col

                    same_object_detected = True

            # New object is detected we assign the ID to that object
            if same_object_detected is False :
                self.center_points[self.id_count] = (cx, cy, col)
                #-- save new object's position and color
                self.id_count += 1
                if not self.is_detected:
                    self.first_color = col
                    self.is_detected = True
