from queue import PriorityQueue
import numpy as np
from sortedcollections import OrderedSet
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
import time
import pygame
import vidmaker
import math


#Create a empty canvas with value as 0
canvas=np.full((1200, 500), 0)

#Obstacles
rectangle1_coordinates=[[100,100],[175,100],[175,500],[100,500]]
rectangle1_offsetcoordinates=[[95,95],[180,95],[180,500],[95,500]]
rectangle2_coordinates=[[275,0],[350,0],[350,400],[275,400]]
rectangle2_offsetcoordinates=[[270,0],[355,0],[355,405],[270,405]]
polygon1_coordinates=[[900,50],[1100,50],[1100,450],[900,450],[900,375],[1020,375],[1020,125],[900,125]]
polygon1_offsetcoordinates=[[895,45],[1105,45],[1105,455],[895,455],[895,370],[1015,370],[1015,130],[895,130]]

#Hexagon Coordinates
hexagon=[]
offsethexagon=[]
for angle in np.array([30, 90, 150, 210, 270, 330]):
    x = 650 + 155 * np.cos(np.radians(angle))
    y = 250 + 155 * np.sin(np.radians(angle))
    offsethexagon.append([x, y])

for angle in np.array([30, 90, 150, 210, 270, 330]):
    x = 650 + 150 * np.cos(np.radians(angle))
    y = 250 + 150 * np.sin(np.radians(angle))
    hexagon.append([x, y])   

#Creating Obstacles on Canvas
rectangle1 = Polygon(rectangle1_offsetcoordinates, closed=True)
rectangle2 = Polygon(rectangle2_offsetcoordinates, closed=True)
hexagon = Polygon(offsethexagon, closed=True)
polygon = Polygon(polygon1_offsetcoordinates, closed=True)

#Canvas offset boundary
canvas[0:5,:],canvas[1195:,:],canvas[:,0:5],canvas[:,495:]=1,1,1,1

#Mark the obstacle space value as 1
for y in range(500):
    for x in range(1200):
        if rectangle1.contains_point((x, y)):
            canvas[x, y] = 1
        if rectangle2.contains_point((x, y)):
            canvas[x, y] = 1
        if hexagon.contains_point((x, y)):
            canvas[x, y] = 1
        if hexagon.contains_point((x, y)):
            canvas[x, y] = 1
        if polygon.contains_point((x, y)):
            canvas[x, y] = 1
            
