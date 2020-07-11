from priorityqueue import PriorityQueue
from node import Node
import pandas as pd


def preprocess(graphfile, heuristicfile = None):
    graph = {}              # A dictionary containing the (name, node) pairs
    heuristics = {}         # A dictionary containing the direct/straight-line distances between nodes
                            # The key is a tuple (name1, name2), the value is the heuristic distance

    # process the graph information using pandas' dataframe
    graphframe = pd.read_csv(graphfile)
    
    #start your code here ...
    # iterate through each row and extract the node names from the first two columns, and the distance from the 3rd column
    # make sure to set node1's neighbor to be node2, and node2's neighbor to be node1 in the graph (dictionary)
    for lineNum in range(len(graphframe)):
        city1 = graphframe.iloc[lineNum, 0]
        city2 = graphframe.iloc[lineNum, 1]
        distance = graphframe.iloc[lineNum, 2]
        
        if city1 not in graph.keys():
            graph[city1] = Node(city1)
        if city2 not in graph.keys():
            graph[city2] = Node(city2)  
            
        if (Node(city2), distance) not in graph[city1].getNeighbors():
            graph[city1].addNeigbor(graph[city2], distance)
        if (Node(city1), distance) not in graph[city2].getNeighbors():
            graph[city2].addNeigbor(graph[city1], distance)
    
    #sort the neighbors dictionary for later search in priority queue
    for node in graph.values():
        node.neighbors = {city: dist for city, dist in sorted(node.getNeighbors(), \
                                                              key = lambda tup: tup[1], reverse = False)}
    
    #end your code here...
    
    #process the heuristic information
    if heuristicfile != None:
        #start your code here ...
        heuristicframe = pd.read_csv(heuristicfile)
        heuristicframe['Distance'].astype('int64')
        for line in range(len(heuristicframe)):
            #get cities' name and distance in a tuple
            c1 = heuristicframe.iloc[line][0]
            c2 = heuristicframe.iloc[line][1]
            dis = heuristicframe.iloc[line][2]

            #store the heuristic info dictionary
            heuristics[(c1, c2)] = dis 

        #end your code here ...
    else:
        heuristics = None

    return graph, heuristics



# When no heuristics is used, this method is called Uniform-Cost Search
def a_star_search(start, goal, heuristics = None):
    visited =[]
    frontier = PriorityQueue()
    start.set_dist_from_start(0)
    if heuristics is None:
        h_dist = 0
    else:
        h_dist = heuristics.get((start.getName(), goal.getName()), 0)
    frontier.insertItem(h_dist, start)#key should be the sum of distance from start and h()
    

    #implement the algorithm
    while not frontier.isEmpty():
        #start your code here ...
        if heuristics is None:
            h_dist2 = 0
        else:
            h_dist2 = heuristics.get((frontier.queue[0][1].getName(), goal.getName()), 0)
        
        #update the distance from start in the node
        frontier.queue[0][1].set_dist_from_start((frontier.minKey() - h_dist2))
        v = frontier.removeMin()#return the 1st node in the priority queue
        visited.append(v)
        
        if v.getName() == goal.getName():
            #Include this line before returning the path (when the goal is found)
            print("\nThe total number of nodes visited:", len(visited))
            return retrieve_path(v, start)
        else:
            neighbors = v.getNeighbors()
            for (item, diskey) in neighbors:
                if  not (item in visited):
                    if heuristics is None:
                        h_dist3 = 0
                    else:
                        h_dist3 = heuristics.get((item.getName(), goal.getName()), 0)
                    
                    dist = diskey + v.get_dist_from_start() + h_dist3

                    if  not (frontier.contains(item)):
                        frontier.insertItem(dist, item)
                        item.setParent(v)
                    else:
                        for tup in frontier.queue:
                            if tup[1] == item:
                                if dist < tup[0]:
                                    frontier.update(dist,item)
                                    tup[1].setParent(v)


    #end your code here ...

# Check out the retrievePath function in bfs.py in our class exercise and get an idea about how this function works
def retrieve_path(currNode, startNode):
    path = [currNode]
    # start your code here ...
    while currNode != startNode:
        path.insert(0, currNode.getParent())
        currNode = currNode.getParent()

    # end your code here ...

    return path

def main():
    useHeuristics = input("Do you like to use heuristics in search? (Y/N): ").upper()
    if useHeuristics == 'Y':
        graph, heuristics = preprocess('graph.csv', "directdists.csv")
    else:
        graph, heuristics = preprocess('graph.csv')

    start, goal = None, None
    while start is None or goal is None:
        startname = input("Enter the start name: ").upper()
        goalname = input("Enter the goal name: ").upper()
        start = graph.get(startname, None)
        goal = graph.get(goalname, None)

    path = a_star_search(start, goal, heuristics)
    print("The path from", start.getName(), "to", goal.getName(), ": ", end = "")

    for node in path[0:-1]:
        print(node.getName(), end = " --> ")
    print(path[-1].getName())
    print("The total distance:", path[-1].get_dist_from_start())

main()
