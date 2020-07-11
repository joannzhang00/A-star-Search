class Node:
    INFINIT = 100000

    def __init__(self, name):
        self.name = name
        self.parent = None                      # The parent is also a node object
        self.neighbors = {}                     # A dictionary containing (node, dist) pairs,
                                                # where node is the neighbor of the current node, and dist is the distance between
                                                # the neighbor node and the current node
        self.dist_from_start = Node.INFINIT     # distance from the start to the current node - the g cost

    def __str__(self):
        result = "Name:\t\t" + self.name + "\nNeighbors:\t"
        for (neighbor, dist) in self.neighbors.items():
            result += "(" + neighbor.getName() + ", " + str(dist) + "), "
        return result[:-2]  #remove the last ,

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def setParent(self, p):
        self.parent = p

    def get_dist_from_start(self):
        return self.dist_from_start

    def set_dist_from_start(self, d):  # d corresponds to the g score/cost in the A* algorithm
        self.dist_from_start = d

    def getNeighbors(self):
        return self.neighbors.items() 

    def addNeigbor(self, n, dist):
        if n not in self.neighbors.keys():
            self.neighbors[n] = dist


