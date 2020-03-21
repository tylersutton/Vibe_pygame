# Python program for Kruskal's algorithm to find
# Minimum Spanning Tree of a given connected,
# undirected and weighted graph
# from https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
# This code is contributed by Neelam Yadav

from random import randint, shuffle

from collections import defaultdict

#Class to represent a graph
class Graph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.V = width*height #No. of vertices
        self.graph = [] # default dictionary
                                # to store graph

    # function to add an edge to graph
    def addEdge(self, u, v, w=10):
        self.graph.append([u, v, w])

    # function to see if an edge exists between u and v
    def isEdge(self, u, v):
        for x, y, _ in self.graph:
            if (u == x and v == y) or (u == y and v == x):
                return True
        return False

    def isNode(self, u):
        for x, y, _ in self.graph:
            if x == u or y == u:
                return True
        return False

    # A utility function to find set of an element i
    # (uses path compression technique)
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    # A function that does union of two sets of x and y
    # (uses union by rank)
    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        # Attach smaller rank tree under root of
        # high rank tree (Union by Rank)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot

        # If ranks are same, then make one as root
        # and increment its rank by one
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    # The main function to construct MST using Kruskal's
        # algorithm
    def KruskalMST(self):
        result = [] #This will store the resultant MST
        i = 0 # An index variable, used for sorted edges
        e = 0 # An index variable, used for result[]

            # Step 1:  Sort all the edges in non-decreasing
                # order of their weight.  If we are not allowed to change the
                # given graph, we can create a copy of graph
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        # Create V subsets with single elements
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        # Number of edges to be taken is equal to V-1
        while e < self.V -1:
            # Step 2: Pick the smallest edge and increment
                    # the index for next iteration
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            # If including this edge does't cause cycle,
                        # include it in result and increment the index
                        # of result for next edge
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
            # Else discard the edge
        return result
    
    def pruneDeadEnds(self, dead_ends):
        dead_ends_pruned = 0
        while dead_ends_pruned < dead_ends:
            num_neighbors = [0 for _ in range(self.width*self.height)]
            for u, v, w in self.graph:
                num_neighbors[u] += 1
                num_neighbors[v] += 1
            dead_ends_left = False
            for u, v, w in self.graph:
                if num_neighbors[u] == 1 or num_neighbors[v] == 1:
                    # print("removing edge " + str(u) + ":" + str(v))
                    self.graph.remove([u, v, w])
                    dead_ends_pruned += 1
                    if dead_ends_pruned >= dead_ends:
                        return
                    else:
                        dead_ends_left = True
            if not dead_ends_left:
                return
        return

    def addRandomEdges(self, num_edges):
        num_neighbors = [0 for _ in range(self.width*self.height)]
        for u, v, w in self.graph:
            num_neighbors[u] += 1
            num_neighbors[v] += 1
        dead_nodes = []
        for i in range(self.width*self.height):
            if num_neighbors[i] == 0:
                dead_nodes.append(i)
        
        addable_edges = []
        
        for y in range(self.height):
            for x in range(self.width):
                if x < self.width - 1:
                    u = y*self.width + x
                    v = y*self.width + x + 1
                    if u != v and u not in dead_nodes and v not in dead_nodes and not self.isEdge(u, v):
                        addable_edges.append((u, v, 100+randint(-50, 50)))
                if y < self.height - 1:
                    u = y*self.width + x
                    v = (y+1)*self.width + x
                    if u != v and u not in dead_nodes and v not in dead_nodes and not self.isEdge(u, v):
                        addable_edges.append((u, v, 100+randint(-50, 50)))
        
        shuffle(addable_edges)
        added_edges = 0

        while added_edges < num_edges:
            if len(addable_edges) == 0:
                break
            self.graph.append(addable_edges[0])
            addable_edges.pop(0)
            
        return

            
def makeGraph(width, height):
    graph = Graph(width, height)
    # start by drawing square grid of edges
    for y in range(height):
        for x in range(width):
            u = (y*width) + x
            v = (y*width) + x + 1
            w = ((y+1)*width) + x
            if x < width-1 and v < width*height:
                graph.addEdge(u, v, 100+randint(-50, 50))
            if y < height-1 and w < width*height:
                graph.addEdge(u, w, 100+randint(-50, 50))
    # then make random diagonal connections
    for y in range(height-1):
        for x in range(width-1):
            chance = randint(0, 99)
            if chance < 50:
                u = (y*width) + x
                v = ((y+1)*width) + x + 1
                graph.addEdge(u, v, 75+randint(-50, 50))
            else:
                u = (y*width) + x + 1
                v = ((y+1)*width) + x
                graph.addEdge(u, v, 75+randint(-50, 50))
    return graph

def makeMapGraph(width, height):
    graph = makeGraph(width, height)
    spanning_tree = graph.KruskalMST()
    graph.graph = spanning_tree
    '''
    print("Following are the edges in the constructed graph")
    for u, v, weight in graph.graph:
        #print str(u) + " -- " + str(v) + " == " + str(weight)
        print("%d -- %d == %d" % (u, v, weight))
    '''
    graph.pruneDeadEnds(dead_ends=3)
    '''
    print("Following are the edges in the graph after pruning")
    for u, v, weight in graph.graph:
        #print str(u) + " -- " + str(v) + " == " + str(weight)
        print("%d -- %d == %d" % (u, v, weight))
    '''
    graph.addRandomEdges(num_edges=3)
    '''
    print("Following are the edges in the graph after random additions")
    for u, v, weight in graph.graph:
        #print str(u) + " -- " + str(v) + " == " + str(weight)
        print("%d -- %d == %d" % (u, v, weight))
    '''
    
    return graph
'''
def main():
    graph = makeMapGraph(4, 3)
    # print the contents of result[] to display the built MST

if __name__ == '__main__':
    main()
'''