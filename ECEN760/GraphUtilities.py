"""
Graph Utilities File

Contains Edge, Node, Graph and Utilities classes

"""

import numpy


class UndirectedEdge:
	"""Undirected Edge class"""

	def __init__(self, n1, n2):
		"""Constructor. Takes two node IDs as arguments"""
		self.node1=n1
		self.node2=n2

	def getNodes(self):
		"""Returns a list containing the two nodes of this edge"""
		return [self.node1, self.node2]

	def hasNodes(self, n1, n2):
		"""Takes two node IDs. Returns true if the IDs match the two nodes of this edge, regardless of order."""
		if(self.node1==n1 and self.node2==n2):
			return True

		if(self.node1==n2 and self.node2==n1):
			return True

		return False


class Node:
	""" Basic node class."""

	def __init__(self, name):
		"""Constructor. Takes a node ID"""
		self.ID=name
		self.neighbors=[]
		self.depth = 0

	def addNeighbors(self, nbs):
		"""Adds a list of neighbors to the current list. Takes a list of node IDs"""
		for i in range(0, len(nbs)):
			if(not nbs[i] in self.neighbors):
				self.neighbors.append(nbs[i])

	def replaceNeighbors(self, nbs):
		"""Replaces the current list of neighbors. Takes a list of node IDs"""
		self.neighbors=nbs

	def removeNeighbor(self, nb):
		"""Removes the specified node ID from the list of neighbors, if it exists"""
		if(nb in self.neighbors):
			self.neighbors.remove(nb)

	def getID(self):
		"""Returns node ID"""
		return self.ID

	def getNeighbors(self):
		"""Returns list of neighbors"""
		return self.neighbors

	def assignDepth(self, d):
		"""Assigns depth of node. Takes an integer"""
		self.depth=d


class Graph:
	"""Basic graph class.
	Assumed to be an undirected graph, but contains a function for implied directed edges.
	"""

	def __init__(self, eds):
		"""Constructor. Takes a list of edge primitives, which is a list of two node IDs.
		Iterates through the edges, creates nodes for unique node IDs, and adds all edges and nodes.
		"""
		self.size = 0
		self.nodes = []
		self.edges = []
		for i in range(0, len(eds)):
			self.addEdge(eds[i])

	def containsNode(self, name):
		"""Returns true if node is in graph, false otherwise"""
		for i in range(0, len(self.nodes)):
			if(self.nodes[i].getID()==name):
				return True
		return False

	def containsEdge(self, edgep):
		"""Checks for an undirected edge in the graph. Takes an edge primitive, which is a list of two node IDs. Order of nodes is irrelevant"""
		for e in self.edges:
			if(e.hasNodes(edgep[0], edgep[1])):
				return True

		return False

	def containsDirectedEdge(self, edgep):
		"""Checks for a directed edge in the graph. Takes an edge primitive, which is a list of two node IDs.
		First node ID is the source, second is the destination.
		"""
		for e in self.edges:
			currentNodes = e.getNodes()
			if(edgep[0]==currentNodes[0] and edgep[1] == currentNodes[1]):
				return True
		return False

	def getNode(self, name):
		"""Checks if a given node ID exists in the graph. If not, it creates and adds a node for the given ID. Returns the node"""
		for i in range(0, len(self.nodes)):
			if(self.nodes[i].getID()==name):
				return self.nodes[i]
		newNode = Node(name)
		self.nodes.append(newNode)
		return self.nodes[len(self.nodes)-1]

	def getEdges(self):
		"""Returns list of edges"""
		return self.edges

	def getNodes(self):
		"""Returns list of nodes"""
		return self.nodes

	def addNode(self, name):
		"""Adds a node, based on node ID"""
		newNode = Node(name)
		self.nodes.append(newNode)

	def addExistingNode(self, n):
		"""Adds a node, based on existing Node object"""
		self.nodes.append(n)

	def assignDepths(self, curDepth, curNodeID):
		"""Recursively assigns depths from the curNodeID, given the curDepth.
		To assign all depths from the root, run graph.assignDepths(0, 'rootID')
		"""
		nod = self.getNode(curNodeID)
		curDepth+=1
		nod.assignDepth(curDepth)
		neighbs = nod.getNeighbors()
		for n in neighbs:
			if(self.containsDirectedEdge([n, curNodeID])):
				self.assignDepths(curDepth, n)

	def assignUndirectedDepths(self, curDepth, curNodeID,nod_covered):
		"""Recursively assigns depths from the curNodeID, given the curDepth.
		To assign all depths from the root, run graph.assignUndirectedDepths(0, 'rootID')
		"""
		nod_covered.append(curNodeID)
		nod = self.getNode(curNodeID)
		nod.assignDepth(curDepth)
		curDepth+=1		
		neighbs = nod.getNeighbors()
		for n in neighbs:
		    if self.containsEdge([n, curNodeID]) and not n in nod_covered:
		        nod_covered.append(n)
		        self.assignUndirectedDepths(curDepth,n,nod_covered)


	def addEdge(self, edgep):
		"""Adds an edge into the graph, and updates neighbors of relevant nodes.
		Takes an edge primitive, a list of two node IDs
		"""
		if(not self.containsEdge(edgep)):
			no1 = self.getNode(edgep[0])
			no2 = self.getNode(edgep[1])
			newEdge = UndirectedEdge(edgep[0], edgep[1])
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
		no1 = self.getNode(edgep[0])
		no2 = self.getNode(edgep[1])
		no1.removeNeighbor(edgep[1])
		no2.removeNeighbor(edgep[0])

	def removeNode(self, name):
		"""Removes a node from the graph, and removes all edges connected to that node.
		Takes a node ID
		"""
		no = self.getNode(name)
		nbs = no.getNeighbors()
		while(len(nbs)>0):
			self.removeEdge([name, nbs[0]])
			nbs=no.getNeighbors()
		self.nodes.remove(no)

	def updateNeighbors(self):
		"""Iterates through edges and updates all neighbors"""
		#Remove all neighbors
		for i in range(0, len(self.nodes)):
			self.nodes[i].replaceNeighbors([])

		#Add new neighbors for each edge
		for i in range(0, len(self.edges)):
			currentNodes = self.edges[i].getNodes()
			no1 = self.getNode(currentNodes[0])
			no2 = self.getNode(currentNodes[1])
			no1.addNeighbors(no2.getID())
			no2.addNeighbors(no1.getID())

	def printGraph(self):
		"""Prints graphs nodes, neighbors, and edges. Should use ___str___()"""
		print("\n\tNODES:")
		for i in range(0, len(self.nodes)):
			print(str(self.nodes[i].getID())+"\t"+str(self.nodes[i].getNeighbors()))
		print("\n\tEDGES:")
		for i in range(0, len(self.edges)):
			currentNodes = self.edges[i].getNodes()
			print(str(currentNodes[0])+" ---- "+str(currentNodes[1]))

	def __str__(self):
		"""Prints graphs nodes, neighbors, and edges"""
		fullstring = "\n\tNODES:\n"
		for i in range(0, len(self.nodes)):
			fullstring+=(str(self.nodes[i].getID())+"\t"+str(self.nodes[i].getNeighbors())+"\n")
		fullstring+="\n\tEDGES:\n"
		for i in range(0, len(self.edges)):
			currentNodes = self.edges[i].getNodes()
			fullstring+=(str(currentNodes[0])+" ---- "+str(currentNodes[1])+"\n")
		return fullstring


class Utils:
	"""Utilities class. Contains functions for converting graph objects to and from text representation"""
	#graph=Graph()
	    
	def __init__(self, G):
 		"""Constructor. Takes graph as argument"""
		self.graph=G
		

	def graphToText(self):
		"""Returns text representation of Graph object. Takes Graph object."""
		totalstring = ""
		totalstring+=(str(len(self.graph.nodes))+"\n")
		totalstring+=(str(len(self.graph.edges))+"\n")
		for e in self.graph.edges:
			currentNodes = e.getNodes()
			totalstring+=(str(currentNodes[0])+" "+str(currentNodes[1])+"\n")

		return totalstring
		
def getGraph(textrep):
	"""Returns Graph object from text representation. Takes a string"""
	tokens = textrep.split()
	if(len(tokens)%2 != 0):
		print("File not formatted correctly: detected an odd number of tokens")
		return Graph([])
	edgs = []
	i = 2
	while(i<len(tokens)-1):
		currentEdge = [tokens[i], tokens[i+1]]
		edgs.append(currentEdge)
		i+=2
	Gr = Graph(edgs)
	return Gr
