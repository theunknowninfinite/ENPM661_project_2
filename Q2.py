import time 
import heapq as hq
import cv2
import numpy as np


def check_if_in_obstacle(point):
    x,y=point
    obstruction_flag=False

    # print(point)
    if (((39*x)+70*(y)-14860)>=0) and (((39*x)-70*(y)-8550)<=0) and (((39*x)+70*(y)-26050)<=0) and (((39*x)-70*(y)+2650)>=0) and  (230<x<370):
        obstruction_flag=True
        # print("in Hexagon")

    if (((23*x)+(12*y)-13345)<=0) and (((23*x)-(12*y)-10345)<=0) and x>=455:
        obstruction_flag=True
        # print("In triangle")
    if (x>=95) and (x<=155) and ((y<=105) or (y>=145)):
        obstruction_flag=True
        # print("in one or two of the rectangles")

    if not obstruction_flag:
        # print("Point Clear")
        return False 
    
    elif obstruction_flag:
        # print("Point in Obstruction")
        return True


def check_valid_points(point):
    x,y=point
    if x<5 or x>595 or y<5 or y>245:
        # print("invalid Point")
        valid_point=False
        return valid_point
    # if x<0 or x>600 or y<0 or y>250:
    #     # print("invalid Point")
    #     valid_point=False
    #     return valid_point
    
    flag_ob=check_if_in_obstacle(point)
    if (flag_ob == True):
        # print("Point in Obstruction in FN Check valid Point")
        valid_point=False
        return valid_point
    
    else:
        valid_point = True
        return valid_point


def actionset(point,cost):
    
    px,py=point
    cost=cost
    
    list_of_actions=[]
    actions=[[1,0,1],[-1,0,1],[0,1,1],[0,-1,1],[1,1,1.4],[-1,-1,1.4],[-1,1,1.4],[1,-1,1.4]]
   
    for idx in actions:
        x=px+idx[0]
        y=py+idx[1]
        cost1= cost+idx[2]
        
        if (check_valid_points((x,y))==True):
            list_of_actions.append(((x,y),cost1))

    return list_of_actions
        
def draw_points(canvas):
    color_path=(255,0,0)
    counter=0
    for x in range(5,596):
        for y in range(5,246):
            if check_valid_points((x,y)):
                canvas[y,x]= color_path
                counter += 1
                # print(y,x)
                if counter == 100:
                    counter = 0
                    cv2.imshow('Explored Nodes', canvas)
                    cv2.waitKey(1)

    cv2.imshow('All Explored Nodes', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




def draw_map():
    #red is bloated green is without bloating 

    canvas=np.zeros((250,600,3))
    triangle=np.array([[460,225],[460,25],[510,125]])
    # triangleb= np.array([[455,228],[455,22],[515,125]])
    triangleb=np.array([[455,240],[455,10],[515,125]])
    hexagon=np.array([[235.05,162.5],[235.05,87.5],[300,50],[364.95,87.5],[364.95,162.5],[300,200]])
    hexagonb=np.array([[230.05,165.5],[230.05,84.5],[300,45],[369.95,84.5],[369.95,165.5],[300,205]])
    hexagon=np.round(hexagon,0).astype(np.int32)
    hexagonb=np.round(hexagonb,0).astype(np.int32)

    green=(0,225,0)
    blue=(255,0,0)
    red=(0,0,255)
    smaller_track=np.array([[5,5],[594,244],[0,245],[595,0]])
    cv2.rectangle(canvas,[5,5],[595,245],(255,255,255),thickness=-1)
    cv2.fillPoly(canvas,[hexagonb],red)
    cv2.fillPoly(canvas,[triangleb],red)
    cv2.rectangle(canvas,[95,5],[155,105],color=red,thickness=-1)
    cv2.rectangle(canvas,[95,245],[155,145],red,thickness=-1)

    
    cv2.fillPoly(canvas,[triangle],green)
    cv2.fillPoly(canvas,pts=[hexagon],color=green)
    cv2.rectangle(canvas,[100,5],[150,100],green,thickness=-1)
    cv2.rectangle(canvas,[100,245],[150,150],green,thickness=-1)

    # canvas=cv2.flip(canvas,0)
    # cv2.imshow('Djikstra's Map', canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return canvas



canvas=draw_map()
draw_points(canvas)

