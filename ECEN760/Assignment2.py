import numpy
import BipartiteUtils
import random


graph1 = BipartiteUtils.BipartGraph([])
#graph1.addChkNode(0)
N=2000
K=1000

for NodeIndex in range(0, K):
    graph1.addBitNode(NodeIndex)


rho=[1/float(K)]
rhoCDF=[]
rhoCDF.append(rho[0])

for i in range(1,K):
    rho.append(1/float(i*(i+1)))
    rhoCDF.append(rhoCDF[i-1]+rho[i])
        
#print rhoCDF[K-1]
for NodeIndex in range(0, N):
    if (NodeIndex%100 == 0):
        print "Check Node is %d" % NodeIndex
    graph1.addChkNode(NodeIndex)
    unif=random.random()
    i=-1
    degIdx=-1
    while unif>i:
        degIdx+=1
        i=rhoCDF[degIdx]
    
	graph1.ChkNodes[NodeIndex].degree=degIdx+1    
    attachments=random.sample(range(0,K),graph1.ChkNodes[NodeIndex].degree) 
    for j in attachments:
        graph1.addEdge([j,NodeIndex])    

E=graph1.getEdges()
print "Number of edges is %d" % len(E)
#for e in E:
    #eNodes=e.getNodes()
    #print eNodes[0], "---",eNodes[1]