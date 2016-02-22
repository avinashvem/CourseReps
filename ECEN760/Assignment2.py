import numpy
import BipartiteUtils
import random
import copy

graph_main = BipartiteUtils.BipartGraph([])
N=300
K=100
eras=0.5
Nsims=int(1e1)

#Soliton is the rho with which degrees are picked
rho=[1/float(K)]
rhoCDF=[0, rho[0]]
print rhoCDF
for i in range(1,K):
    rho.append(1/float(i*(i+1)))
    rhoCDF.append(rhoCDF[i]+rho[i])


for NodeIndex in range(0, K):
    graph_main.addBitNode(NodeIndex)
        
for NodeIndex in range(0, N):
    if (NodeIndex%100 == 0):
        print "Check Node is %d" % NodeIndex
    graph_main.addChkNode(NodeIndex)
    unif=random.random()
    i=0
    degIdx=0
    while unif>i:
        degIdx+=1
        i=rhoCDF[degIdx]

    attachments=random.sample(range(0,K),degIdx) 
    for j in attachments:
        graph_main.addEdge([j,NodeIndex])    


E=graph_main.getEdges()
print "Number of edges is %d" % len(E)

print len(graph_main.BitNodes),len(graph_main.ChkNodes)
for z in range(0,Nsims):
	graph1=copy.deepcopy(graph_main)
	erasIdx=random.sample(range(0,N),int(eras*K))
	chan=[]
	for i in range(0,N):
		chan.append(0)
	for i in erasIdx:
		chan[i]=-2
	print "Chan is %d long \n" % len(chan)
	
	PeelGraph=BipartiteUtils.Peeling(graph1,chan)
	print "Graph1 Nodes are-",len(graph1.BitNodes),len(graph1.ChkNodes)
	print "Graph Main Nodes are-",len(graph1.BitNodes),len(graph1.ChkNodes)
	PeelGraph.zeroStep()
	remBitNodes=len(PeelGraph.graph.BitNodes)
	remChkNodes=len(PeelGraph.graph.ChkNodes)
	Num_deg1Chks=len(PeelGraph.deg1Chks)
	print remBitNodes, remChkNodes, Num_deg1Chks
	
	while (remBitNodes>0 and Num_deg1Chks>0):
		PeelGraph.peelIter()
		remBitNodes=len(PeelGraph.graph.BitNodes)
		remChkNodes=len(PeelGraph.graph.ChkNodes)
		Num_deg1Chks=len(PeelGraph.deg1Chks)
		
		PeelGraph.deg1Chks_constr()	
		remChkNodes=len(PeelGraph.graph.ChkNodes)
	
	print "Remaining Bit and Check Nodes in the graph are %d-%d." %(remBitNodes,remChkNodes) 
	print "Remaining Edges in the graph are %d." % len(PeelGraph.graph.edges)
	
	del PeelGraph
	print "z=",z
		
	

#for i in graph1.BitNodes:
#	print "Bit node", i.getID(), "degree is :",i.degree, " neighbors are:", i.neighbors

#for i in graph1.ChkNodes:
#	print "Chk node", i.getID(), "degree is :",i.degree, " neighbors are:", i.neighbors
	
#print "Remaining Bit and Check Nodes in the graph are %d-%d and degree 1 check nodes are %d" %(remBitNodes,remChkNodes,Num_deg1Chks) 