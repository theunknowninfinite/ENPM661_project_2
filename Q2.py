#GiTHUB LINK-https://github.com/theunknowninfinite/ENPM661_project_2

import time 
import heapq as hq
import cv2
import numpy as np

#defining Node Object 
class node_object:
    def __init__(self,pt,cost,parent_node) :
        self.pt=pt
        self.cost=cost 
        self.parent_node=parent_node
        # self.node_id=node_id
    def __lt__(self,other):
        return self.cost < other.cost
    
# getting input from  user
def get_input():
    start_coor=tuple(int(item) for item in input("\n Start Node seperated by comma:").split(','))
    if not check_valid_points(start_coor):
        print("Wrong Start Node ,Please run proram again and enter proper value")
        exit()
    end_coor= tuple(int(item) for item in input("\n End Node seperated by comma:").split(','))
    if not check_valid_points(end_coor):
        print("Wrong End Node ,Please run proram again and enter proper value")
        exit()
    if end_coor == start_coor:
        print ("Start and End are the Same Exiting.PLease run program again")
        exit()
    return start_coor,end_coor


#checking if point is clear of any obstructions 
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
#checking if point is valid 
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
        

#all possible actions with cost 
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

#node id for easy to track  and random dict keys 
def node_id(node):
    x,y=node.pt
    key = 1022*x + 111*y 
    return key

# start of the algorithim
def dijkstra(start_point,end_point):

    start=start_point
    end=end_point
    #defining lists 
    start_id=node_id(start)
    ntv={} #nodes to visit 
    ntv[(start_id)]= start  

    visited_nodes={}#nodes explored 
    log=[]
    hq.heappush(log,[start.cost,start])
    list_of_all_nodes=[] #all nodes generated 

    #starting of algorithim
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
    #the end 
    return list_of_all_nodes,end_of_search

#for backtracking path 
def backtrack_path(end_point):
    list_of_points=[]
    list_of_points.append(end_point.pt)

    parent=end_point.parent_node
    test=parent.pt
    while parent != None:
        list_of_points.append(parent.pt)
        parent=parent.parent_node
    
    list_of_points.reverse()
    return list_of_points


#drawing map only 
def draw_map():

    green=(0,225,0)
    blue=(255,0,0)
    red=(0,0,255)
    #red is bloated green is without bloating 
    canvas=np.zeros((250,600,3))
    triangle=np.array([[460,225],[460,25],[510,125]])
    # triangleb=np.array([[455,240],[455,10],[515,125]])
    triangleb=np.array([[455,246],[455,3],[516,125]])
    hexagon=np.array([[235.05,162.5],[235.05,87.5],[300,50],[364.95,87.5],[364.95,162.5],[300,200]])
    hexagonb=np.array([[230.05,165.5],[230.05,84.5],[300,45],[369.95,84.5],[369.95,165.5],[300,205]])
    hexagon=np.round(hexagon,0).astype(np.int32)
    hexagonb=np.round(hexagonb,0).astype(np.int32)

    
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
    cv2.imshow('Map', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return canvas
 
#draw all explored nodes and backtraacked path 
def draw_points(canvas,backtrack_nodes,all_nodes):
    color_path=(255,0,0)
    counter=0
    color_nodes=(20,220,0)
    print(canvas.shape)
    height= canvas.shape[0]
    for i in all_nodes:
                x,y=i[0].pt
                canvas[height-y,x]= color_nodes
                counter += 1
                if counter == 100:
                    counter = 0
                    # canvas=cv2.flip(canvas,0)
                    cv2.imshow('Path', canvas)
                    cv2.waitKey(1)
    for i in backtrack_nodes:
                canvas[height-i[1],i[0]]= color_path
                counter += 1
                # print(y,x)
                if counter == 100:
                    counter = 0
                    # canvas=cv2.flip(canvas,0)
                    cv2.imshow('Path', canvas)
                    cv2.waitKey(1)
    cv2.imshow('Path', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



#main function
if __name__== '__main__':
    #getting input from user 
    start,end=get_input()
    # start=(5,5)
    # end=(515,145)
    
    #start of timer 
    st_time=time.time()
    start_node=node_object(start,0,None)
    end_node=node_object(end,0,None)
    all_points_generated,goal_reached=dijkstra(start_node,end_node)
   
    #goal found hooray 
    if goal_reached:
        backtrack_points=backtrack_path(end_node)
        print(backtrack_points,len(backtrack_points))
        img=draw_map()
        draw_points(img,backtrack_points,all_points_generated)
    else:
        print("No path found")
    #end timer 
    end_time=time.time()-st_time
    #printing time taken for loop and plotting 
    print("Total time for execution was ",end_time)