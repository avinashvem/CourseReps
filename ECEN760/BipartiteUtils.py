"""" 
BipartiteGraph Utilities File

Contains Bit Node, Check Node, Graph and Peeling decoder classes

"""""

import numpy
#import sys
#sys.path.append("../Tools/")


class Edge:
	"""Bit Node to Check Node, Edge class"""

	def __init__(self, n1, n2):
		"""Constructor. Takes bit and check node IDs as arguments"""
		self.node1=n1
		self.node2=n2

	def getNodes(self):
		"""Returns a list containing the bit and check nodes for this edge"""
		return [self.node1, self.node2]

	def hasNodes(self, n1, n2):
		"""Takes two node IDs. Returns true if the IDs match the two nodes of this edge in that order."""
		if(self.node1==n1 and self.node2==n2):
			return True
			
		return False


class BitNode:
	""" Basic node class."""

	def __init__(self, name):
		"""Constructor. Takes a node ID"""
		self.ID=name
		self.neighbors=[]
		self.degree= 0

	def addNeighbors(self, nbs):
		"""Adds a list of neighbors to the current list. Takes a list of node IDs"""
		for i in range(0, len(nbs)):
			if(not nbs[i] in self.neighbors):
				self.neighbors.append(nbs[i])
				self.degree+=1

	def replaceNeighbors(self, nbs):
		"""Replaces the current list of neighbors. Takes a list of node IDs"""
		self.neighbors=nbs
		self.degree=len(nbs)

	def removeNeighbor(self, nb):
		"""Removes the specified node ID from the list of neighbors, if it exists"""
		if(nb in self.neighbors):
			self.neighbors.remove(nb)
		self.degree=len(self.neighbors)

	def getID(self):
		"""Returns node ID"""
		return self.ID

	def getNeighbors(self):
		"""Returns list of neighbor IDs"""
		return self.neighbors


class ChkNode:
	""" Check node class."""

	def __init__(self, name):
		"""Constructor. Takes a node ID"""
		self.ID=name
		self.neighbors=[]
		self.chan = int(-1)
		self.degree= 0
		

	def addNeighbors(self, nbs):
		"""Adds a list of neighbors to the current list. Takes a list of node IDs"""
		for i in range(0, len(nbs)):
			if(not nbs[i] in self.neighbors):
				self.neighbors.append(nbs[i])
				self.degree+=1

	def replaceNeighbors(self, nbs):
		"""Replaces the current list of neighbors. Takes a list of node IDs"""
		self.neighbors=nbs
		self.degree=len(nbs)

	def removeNeighbor(self, nb):
		"""Removes the specified node ID from the list of neighbors, if it exists"""
		if(nb in self.neighbors):
			self.neighbors.remove(nb)
		self.degree=len(self.neighbors)
			

	def getID(self):
		"""Returns node ID"""
		return self.ID

	def getNeighbors(self):
		"""Returns list of neighbor IDs"""
		return self.neighbors


class BipartGraph:
	"""Bipartite graph class.
	"""

	def __init__(self, eds):
		"""Constructor. Takes a list of edge primitives, which is a list of two node IDs.
		Iterates through the edges, creates nodes for unique node IDs, and adds all edges and nodes.
		"""
		self.size = 0
		self.BitNodes = []
		self.ChkNodes = []
		self.edges = []
		for i in range(0, len(eds)):
			self.addEdge(eds[i])

	def containsBitNode(self, name):
		"""Returns true if bit node is in graph, false otherwise. Takes node ID as argument."""
		for i in range(0, len(self.nodes)):
			if(self.nodes[i].getID()==name):
				return True
		return False

	def containsCheckNode(self, name):
		"""Returns true if check node is in graph, false otherwise.Takes node ID as argument."""
		for i in range(0, len(self.nodes)):
			if(self.nodes[i].getID()==name):
				return True
		return False

	def containsEdge(self, edgep):
		"""Checks for an edge in the graph. Takes an edge primitive, which is a list of two node IDs. First ID is bit node, second ID is of Check node"""
		for e in self.edges:
			if(e.hasNodes(edgep[0], edgep[1])):
				return True

		return False

	def getBitNode(self, name):
		"""Checks if a given Bit Node ID exists in the graph. If not, it creates and adds a Bit Node for the given ID. Returns the Bit Node"""
		for i in range(0, len(self.BitNodes)):
			if(self.BitNodes[i].getID()==name):
				return self.BitNodes[i]
		newNode = BitNode(name)
		self.BitNodes.append(newNode)
		return self.BitNodes[len(self.BitNodes)-1]

	def getChkNode(self, name):
		"""Checks if a given Chk Node ID exists in the graph. If not, it creates and adds a Chk Node for the given ID. Returns the Chk Node"""
		for i in range(0, len(self.ChkNodes)):
			if(self.ChkNodes[i].getID()==name):
				return self.ChkNodes[i]
		newNode = ChkNode(name)
		self.ChkNodes.append(newNode)
		return self.ChkNodes[len(self.ChkNodes)-1]

	def getEdges(self):
		"""Returns list of edges"""
		return self.edges

	def getBitNodes(self):
		"""Returns list of Bit nodes"""
		return self.BitNodes

	def addBitNode(self, name):
		"""Adds a Bit node, based on Bit node ID"""
		newNode = BitNode(name)
		self.BitNodes.append(newNode)

	def addExistingBitNode(self, n):
		"""Adds a Bit node, based on existing BitNode object"""
		self.BitNodes.append(n)

	def getChkNodes(self):
		"""Returns list of Check nodes"""
		return self.ChkNodes

	def addChkNode(self, name):
		"""Adds a Check node, based on node ID"""
		newNode = ChkNode(name)
		self.ChkNodes.append(newNode)

	def addExistingChkNode(self, n):
		"""Adds a Check node, based on existing Node object"""
		self.ChkNodes.append(n)

	def addEdge(self, edgep):
		"""Adds an edge into the graph, and updates neighbors & degrees of relevant nodes.
		Takes an edge primitive, a list of two node IDs
		"""
		if(not self.containsEdge(edgep)):
			no1 = self.getBitNode(edgep[0])
			no2 = self.getChkNode(edgep[1])
			newEdge = Edge(edgep[0], edgep[1])
			self.edges.append(newEdge)
			no1.addNeighbors([no2.getID()])
			no2.addNeighbors([no1.getID()])

	def removeEdge(self, edgep):
		"""Removes an edge from the graph, and updates the neighbors of relevant nodes
		Takes an edge primitive.
		"""

		for i in range(0, len(self.edges)):
			if(self.edges[i].hasNodes(edgep[0], edgep[1])):
				self.edges.pop(i)
				break
		no1 = self.getBitNode(edgep[0])
		no2 = self.getChkNode(edgep[1])
		no1.removeNeighbor(edgep[1])
		no2.removeNeighbor(edgep[0])

	def removeBitNode(self, name):
		"""Removes a Bit node from the graph, and removes all edges connected to that node.
		Takes a node ID
		"""
		no = self.getBitNode(name)
		nbs = no.getNeighbors()
		while(len(nbs)>0):
			self.removeEdge([name, nbs[0]])
			nbs=no.getNeighbors()
		self.BitNodes.remove(no)
		
	def removeChkNode(self, name):
		"""Removes a check node from the graph, and removes all edges connected to that node.
		Takes a node ID
		"""
		no = self.getChkNode(name)
		nbs = no.getNeighbors()
		while(len(nbs)>0):
			self.removeEdge([nbs[0],name])
			nbs=no.getNeighbors()			
		self.ChkNodes.remove(no)

	def updateNeighbors(self):
		"""Iterates through edges and updates all neighbors"""
		#Remove all neighbors
		for i in range(0, len(self.BitNodes)):
			self.BitNodes[i].replaceNeighbors([])

		for i in range(0, len(self.ChkNodes)):
			self.ChkNodes[i].replaceNeighbors([])

		#Add new neighbors for each edge
		for i in range(0, len(self.edges)):
			currentNodes = self.edges[i].getNodes()
			no1 = self.getBitNode(currentNodes[0])
			no2 = self.getChkNode(currentNodes[1])
			no1.addNeighbors(no2.getID())
			no2.addNeighbors(no1.getID())

	def printGraph(self):
		"""Prints graphs nodes, neighbors, and edges. Should use ___str___()"""
		print "\n\t Bit Nodes:", self.BitNodes
		print "\n\t Check Nodes:", self.ChkNodes

		print("\n\t ---EDGES---")
		print("\n Bit Nodes  Check Nodes \n")
		for i in range(0, len(self.edges)):
			currentNodes = self.edges[i].getNodes()
			print(str(currentNodes[0])+" ---- "+str(currentNodes[1]))

	def __str__(self):
		"""Prints graphs nodes, neighbors, and edges"""
		fullstring = "\n\t Bit Nodes: "
		for i in self.BitNodes:
		    fullstring +=str(i.getId()) + "  "
		    
		fullstring+= "\n\t Check Nodes: "
		for i in self.ChkNodes:
		    fullstring +=str(i.getId()) + "  "

		print("\n\t ---EDGES---")
		print("\n Bit Nodes  Check Nodes \n")
		for i in range(0, len(self.edges)):
			currentNodes = self.edges[i].getNodes()
			print(str(currentNodes[0])+" ---- "+str(currentNodes[1]))
		
		fullstring+="\n\tEDGES---EDGES---\n Bit Nodes  Check Nodes \n"
		for i in range(0, len(self.edges)):
			currentNodes = self.edges[i].getNodes()
			fullstring += str(currentNodes[0])+" ---- "+str(currentNodes[1])+"\n"

		return fullstring


class Peeling:
	"""peeling decoder on a Bipartite graph class.
	"""
	def __init__(self, G,chan):
		"""Constructor. Takes a graph and channel output vector as arguments"""
		self.graph=G
		for i in range(0,len(self.graph.ChkNodes)):
		    self.graph.ChkNodes[i].chan=chan[i]
		self.deg1Chks=[]
		
	def peelBit(self,BitID):
		"""Removes a Bit Node and all its edges from the graph. Takes the bit Node ID as argument"""
		self.graph.removeBitNode(BitID)	
		
	def peelChk(self,chkID):
		"""Removes a Chk Node and all its edges from the graph. Takes the Chk Node ID as argument"""
		self.graph.removeChkNode(chkID)

	def zeroStep(self):
		"""Removes the first degree 1 Chk Node and all its edges from the graph. If none is found exits the programme."""
		self.deg1Chks_constr()
		if len(self.deg1Chks)>0:
			i = self.deg1Chks[0]
		else: 
			print "There are no Degree 1 Check Nodes. Exiting"
			return	

		inbs=i.neighbors
		no=self.graph.getBitNode(inbs[0])
		
		if len(inbs)>1:
			print "There is an error. Degree 1 node has more than 1 connection\n"
		elif len(inbs)==0:
			self.graph.ChkNodes.remove(i)		
		else:
			self.peelBit(no.getID())
			
		self.deg1Chks_constr()
	    
	def peelIter(self):
		
		if len(self.deg1Chks)>0:
			i = self.deg1Chks[0]
		else: 
			print "There are no Degree 1 Check Nodes. Exiting"
			return	
		nbs=i.neighbors
		
		if len(nbs)>1:
			print "There is an error. Degree 1 node has more than 1 connection\n"
			exit
		iDeg=i.degree
		
		if iDeg!=0:
			no=self.graph.getBitNode(nbs[0])
			self.peelChk(i.getID())
#			print "Removing Bit node",no.getID(), "and its %d neighbors" % len(no.neighbors)
			self.peelBit(no.getID())
		
		self.deg1Chks_constr()          
		
	def deg1Chks_constr(self):
		self.deg1Chks=[]
		for j in self.graph.ChkNodes:
			if j.degree==0:
				self.graph.ChkNodes.remove(j)
			elif j.degree==1:
				self.deg1Chks.append(j)
				
	