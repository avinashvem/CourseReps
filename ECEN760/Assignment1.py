"""" 
Solution for HW 1

"""""

import numpy
import sys
sys.path.append("../Tools/")
import GraphUtilities


f1 = open("../../../JF/ECEN760-Spring2016/Graphs/Assignment1_graph1.txt", "r") #provide the relative path
graph1_txt=f1.read()
f1.close

g1=GraphUtilities.getGraph(graph1_txt)
#g1.printGraph()

numNodes=len(g1.nodes)
numEdges=len(g1.edges)
print "# of Nodes=%d. # of Edges=%d. \n" % (numNodes, numEdges)


# Counting ancestors
ancst=numpy.zeros(numNodes,dtype=int)     
for e in g1.edges:
    currEdge=e.getNodes()
    ancst[int(currEdge[1])]+=1  
print "# of acestors for each node are: ", ancst, ".\n"


# Counting levels as seen from different nodes and then radius """"
radius=numpy.zeros(numNodes)
for i in range(0,len(g1.nodes)):
    g1.assignUndirectedDepths(0,g1.nodes[i].getID(),[])
    tmp_rad=numpy.zeros(numNodes)
    for j in range(0,len(g1.nodes)):
 	    tmp_rad[j]= int(g1.nodes[j].depth)
    radius[i]=int(max(tmp_rad))
     
print "Radius of the undirected graph is %d. \n" % min(radius)


#Degree distribution
numNeighbs=[]
for i in g1.nodes:
    numNeighbs.append(len(i.neighbors))
    
print "# of neighbors for each node: ", numNeighbs, ".\n"



