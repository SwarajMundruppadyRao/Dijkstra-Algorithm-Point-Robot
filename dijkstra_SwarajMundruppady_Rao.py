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

#Pygame map generation
def coords_pygame(coords, height):
    return (coords[0], height - coords[1])

def rect_pygame(coords, height, obj_height):
    return (coords[0], height - coords[1] - obj_height)

def create_map(visit, backtrack, start, Goal):
    pygame.init()
    size = [1200, 500]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Visualization")
    video = vidmaker.Video("Dijkstra_swarajmr.mp4", late_export=True)

    done = False
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill("white")
        pygame.draw.rect(screen, "blue", [95,0, 85, 405], 0)
        pygame.draw.rect(screen, "red",  [100,0, 75, 400], 0)
        pygame.draw.rect(screen, "blue", [270,95,85,405], 0)
        pygame.draw.rect(screen, "red", [275,100, 75, 400], 0)
        pygame.draw.polygon(screen, "blue", ([784.903811, 327.886751], [650, 405.7735], [515.096189, 327.886751], [515.096189, 172.113249], [650,94.226497],[784.903811,172.113249]), 0)
        pygame.draw.polygon(screen, "red", [[650,400], [520.096189,325], [520.096189,175],[650,100],[779.903811,175],[779.903811,325]], 0)
        pygame.draw.polygon(screen, "blue", ([895,130],[895,45],[1105,45],[1105,455],[895,455],[895,370],[1015,370],[1015,130]), 0)
        pygame.draw.polygon(screen, "red", ([900,50],[1100,50],[1100,450],[900,450],[900,375],[1020,375],[1020,125],[900,125]), 0)
        pygame.draw.rect(screen, "blue", [0,0, 1200, 500], 5)
        pygame.draw.circle(screen, (255, 255, 0), coords_pygame(start, 500), 1)
        pygame.draw.circle(screen, (255, 255, 0), coords_pygame(Goal, 500), 1)
        n=0
        for j in visit:
            n+=1
            pygame.draw.circle(screen, (50, 137, 131), coords_pygame(j, 500), 1)
            if n%50==0:
                video.update(pygame.surfarray.pixels3d(screen).swapaxes(0, 1), inverted=False)
                pygame.display.update()
        pygame.draw.circle(screen, (0, 255, 0), coords_pygame(start, 500), -3)
        pygame.draw.circle(screen, (0, 255, 0), coords_pygame(Goal, 500), -3)
        counter=0
        for i in backtrack:
            pygame.draw.circle(screen, (255, 255, 0), coords_pygame(i, 500), 1)
            if counter%50==0:
                video.update(pygame.surfarray.pixels3d(screen).swapaxes(0, 1), inverted=False)
            pygame.display.update()
        pygame.draw.circle(screen, (255, 255, 0), coords_pygame(start, 500), 1)
        pygame.draw.circle(screen, (255, 255, 0), coords_pygame(Goal, 500), 1)
        done = True
        
    pygame.time.wait(10000)
    pygame.quit()
    video.export(verbose=True)
    
def check_obstacles(coordinates):
    if canvas[coordinates[0], coordinates[1]]==1:
        return False
    return True

def input_start(prompt):
    while True:
        print("Enter", prompt, "node (x between 0 and 1499, y between 0 and 499) (Sample Input: 10,10): ")
        input_str = input()
        A = [int(i) for i in input_str.split(',')]
        A_1 = (A[0], A[1])
        if not (0 <= A[0] < 1500 and 0 <= A[1] < 500):
            print("Enter valid input (x between 0 and 1499, y between 0 and 499)")
        elif not check_obstacles(A_1):
            print("The entered input lies on the obstacles or is not valid, please try again")
        else:
            return A_1
#Defining Actions and associated cost addition(c2c)
def moveup(que):
    coordinates = (que[1][0], que[1][1]+1)
    if check_obstacles(coordinates) and coordinates not in visit:
        cost_to_come = que[0] + 1
        check_conditions(que, coordinates, cost_to_come)

def movedown(que):
    coordinates = (que[1][0], que[1][1]-1)
    if check_obstacles(coordinates) and coordinates not in visit:
        cost_to_come = que[0] + 1
        check_conditions(que, coordinates, cost_to_come)

def moveleft(que):
    coordinates = (que[1][0]-1, que[1][1])
    if check_obstacles(coordinates) and coordinates not in visit:
        cost_to_come = que[0] + 1
        check_conditions(que, coordinates, cost_to_come)

def moveright(que):
    coordinates = (que[1][0]+1, que[1][1])
    if check_obstacles(coordinates) and coordinates not in visit:
        cost_to_come = que[0] + 1
        check_conditions(que, coordinates, cost_to_come)

def moveupleft(que):
    coordinates = (que[1][0]-1, que[1][1]+1)
    if check_obstacles(coordinates) and coordinates not in visit:
        cost_to_come = que[0] + 1.4
        check_conditions(que, coordinates, cost_to_come)


def moveupright(que):
    coordinates = (que[1][0]+1, que[1][1]+1)
    if check_obstacles(coordinates) and coordinates not in visit:
        cost_to_come = que[0] + 1.4
        check_conditions(que, coordinates, cost_to_come)


def movedownleft(que):
    coordinates = (que[1][0]-1, que[1][1]-1)
    if check_obstacles(coordinates) and coordinates not in visit:
        cost_to_come = que[0] + 1.4
        check_conditions(que, coordinates, cost_to_come)

def movedownright(que):
    coordinates = (que[1][0]+1, que[1][1]-1)
    if check_obstacles(coordinates) and coordinates not in visit:
        cost_to_come = que[0] + 1.4
        check_conditions(que, coordinates, cost_to_come)
