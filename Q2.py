import time 
import heapq as hq
import cv2
import numpy as np

class node_object:
    def __init__(self,pt,cost,parent_node) :
        self.pt=pt
        self.cost=cost 
        self.parent_node=parent_node
        # self.node_id=node_id
    def __lt__(self,other):
        return self.cost < other.cost
    

def get_input():
    start_coor=tuple(int(item) for item in input("\n Start Node:").split(','))
    if not check_valid_points(start_coor):
        print("Wrong Start Node ,Please run proram again and enter proper value")
        exit()
    end_coor= tuple(int(item) for item in input("\n End Node:").split(','))
    if not check_valid_points(end_coor):
        print("Wrong End Node ,Please run proram again and enter proper value")
        exit()
    if end_coor == start_coor:
        print ("Start and End are the Same Exiting.PLease run program again")
        exit()
    return start_coor,end_coor



def check_if_in_obstacle(point):
    x,y=point
    obstruction_flag=False

    # print(point)
    if (((39*x)+70*(y)-14860)>0) and (((39*x)-70*(y)-8550)<0) and (((39*x)+70*(y)-26050)<0) and (((39*x)-70*(y)+2650)>0) and  (230<x<370):
        obstruction_flag=True
        # print("in Hexagon")

    # if (((23*x)+(12*y)-13345)<0) and (((23*x)-(12*y)-10345)<0) and x>455:
    #     obstruction_flag=True
        # print("In triangle")
    if (((121*x)+(61*y)-70061)<0) and (((121*x)-(61*y)-54815)<0) and x>455:
        obstruction_flag=True
        # print("In triangle")

    if (x>95) and (x<155) and ((y<105) or (y>145)):
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
    # if x<0 or x>595 or y<0 or y>245:
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
    #node is in the form of cost,index,parent_index,point
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


def node_id(node):
    x,y=node.pt
    key = 1022*x + 111*y 
    return key

def dijkstra(start_point,end_point):

    start=start_point
    end=end_point

    start_id=node_id(start)
    ntv={}
    ntv[(start_id)]= start  

    visited_nodes={}
    log=[]
    hq.heappush(log,[start.cost,start])
    list_of_all_nodes=[]

    while (len(log) !=0):
        current_node= hq.heappop(log)[1]
        list_of_all_nodes.append([current_node])
        current_node_id=node_id(current_node)
        if current_node.pt == end.pt:
            end.parent_node = current_node.parent_node
            end.cost=current_node.cost
            print("Goal Point Reached") # change 
            end_of_search=True
            return list_of_all_nodes,end_of_search
        if current_node_id in visited_nodes:
            continue
        else:
            visited_nodes[current_node_id]= current_node
        del ntv[current_node_id]

        action=actionset(current_node.pt,current_node.cost)
        for idx in action:
            new_node=node_object(idx[0],idx[1],current_node) #NEEDS TO BE DEFINED 
            new_node_id=node_id(new_node)

            if not check_valid_points(new_node.pt):
                continue 
            elif new_node_id in visited_nodes:
                continue
            if new_node_id in ntv:
                if  ntv[new_node_id].cost>new_node.cost:
                    ntv[new_node_id].cost = new_node.cost
                    ntv[new_node_id].parent_node = new_node.parent_node
            else:
                ntv[new_node_id]=new_node

            hq.heappush(log,[new_node.cost,new_node])
        end_of_search=False

    return list_of_all_nodes,end_of_search

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


canvas=draw_map()
draw_points(canvas)

