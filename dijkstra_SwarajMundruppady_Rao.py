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

#Obstacle end point/ coordinates
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
            
#To convert coordinates to pygame coordinate system
def coords_pygame(coords, height):
    return (coords[0], height - coords[1])

# Create the map visualization using pygame
def create_map(visit, backtrack, start, Goal):
    pygame.init()
    #Screen Size
    size = [1200, 500]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Dijkstra_Swaraj")
    video = vidmaker.Video("Dijkstra_SwarajMundruppady_Rao.mp4", late_export=True)

    done = False
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill("white")
        
        # Draw obstacles
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
        
        #Visualisation of the explored nodes
        for j in visit:
            n+=1
            pygame.draw.circle(screen, (50, 137, 131), coords_pygame(j, 500), 1)
            if n%50==0:
                video.update(pygame.surfarray.pixels3d(screen).swapaxes(0, 1), inverted=False)
                pygame.display.update()
        pygame.draw.circle(screen, (0, 255, 0), coords_pygame(start, 500), -3)
        pygame.draw.circle(screen, (0, 255, 0), coords_pygame(Goal, 500), -3)
        counter=0
        #Visualisation of the path generated using backtracking
        for i in backtrack:
            pygame.draw.circle(screen, (255, 255, 0), coords_pygame(i, 500), 1)
            if counter%50==0:
                video.update(pygame.surfarray.pixels3d(screen).swapaxes(0, 1), inverted=False)
            pygame.display.update()
        pygame.draw.circle(screen, (255, 255, 0), coords_pygame(start, 500), 1)
        pygame.draw.circle(screen, (255, 255, 0), coords_pygame(Goal, 500), 1)
        done = True
    pygame.time.wait(5000)
    pygame.quit()
    video.export(verbose=True)
 
 # Function to check if a given coordinate is inside an obstacle   
def check_obstacles(coordinates):
    if canvas[coordinates[0], coordinates[1]]==1:
        return False
    return True

# Function to get input for start and goal positions
def input_start(prompt):
    while True:
        print("Enter", prompt, "node (x between 5 and 1194, y between 5 and 494) (Sample Input: 10,10): ")
        input_str = input()
        A = [int(i) for i in input_str.split(',')]
        A_1 = (A[0], A[1])
        if not (0 <= A[0] < 1200 and 0 <= A[1] < 500):
            print("Enter valid input (x between 5 and 1194, y between 5 and 494)")
        elif not check_obstacles(A_1):
            print("The entered input lies on the obstacles or is not valid, please try again")
        else:
            return A_1
        
# Function to check conditions and update the priority queue
def check_conditions(que, coordinates, cost_to_come):
    if coordinates in touch:
        if touch[coordinates] > cost_to_come:
            new_que = (cost_to_come, coordinates)
            Path[coordinates] = que[1]
            Q.put(new_que)
            touch[coordinates] = cost_to_come
            return
        else:
            return
    new_que = (cost_to_come, coordinates)
    Path[coordinates] = que[1]
    Q.put(new_que)
    touch[coordinates] = cost_to_come

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

## Generate Path using backtracking
def generate_path(path, start, Goal):
    backtrack = []
    key = path.get(Goal)
    backtrack.append(Goal)
    backtrack.append(key)
    while (key != start):
        key = path.get(key)
        backtrack.append(key)
    backtrack.reverse()
    return backtrack

# Dijkstra Algorithm implementation
def dijkstra_algorithm():
    #for calculating time required to run the code
    start_time = time.time()
    while (Q.qsize() != 0):
        queue = Q.get()
        # If current node is not the goal node continue exploring the map
        if (queue[1] != goal):
            if queue[1] not in visit:
                #if current node not in visited nodes add the node and explore all the possible points of the map using actions
                visit.add(queue[1])
                # Check all possible moves
                if (queue[1][1]+1 >= 0 and queue[1][1]+1 <= 500):
                    moveup(queue)
                if (queue[1][1]-1 >= 0 and queue[1][1]-1 <= 500):
                    movedown(queue)
                if (queue[1][0]-1 >= 0 and queue[1][0]-1 <= 1200):
                    moveleft(queue)
                if (queue[1][0]+1 >= 0 and queue[1][0]+1 <= 1200):
                    moveright(queue)
                if (queue[1][1]+1 <= 500 and queue[1][0]-1 >= 0):
                    moveupleft(queue)
                if (queue[1][0]+1 <= 1200 and queue[1][1]+1 <= 500):
                    moveupright(queue)
                if (queue[1][0]-1 >= 0 and queue[1][1]-1 >= 0):
                    movedownleft(queue)
                if (queue[1][0]+1 <= 1200 and queue[1][1]-1 <= 500):
                    movedownright(queue)
        else:
            print('success')
            # Generate and print the path
            Backtrack = generate_path(Path, Start, goal)
            print(Backtrack)
            print('-----------')
            print(queue)
            end_time = time.time()
            path_time = end_time - start_time
            print('Time to calculate path:', path_time, 'seconds')
            # Visualize the path using pygame
            create_map(visit, Backtrack, Start, goal)
            break


Start = input_start('Start Position')
goal = input_start('Goal Position')
print(Start, goal)
visit = OrderedSet()
touch = {}
Path = {}
Q = PriorityQueue()
Q.put((0, Start))
dijkstra_algorithm()
