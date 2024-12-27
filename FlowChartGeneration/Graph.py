from graphviz import Digraph
from collections import deque
from LineType import LineType

class Node:

	def __init__(self,data):
		
		self.data = data
		self.childs = []
		self.weight_values = []

class Graph:

	def __init__(self, is_directed = True):
		self.__is_directed = is_directed 
		
		# Key: Identifier (in our case the line number - 1)
		# Value: the line of code content
		self.__nodes = {}

		self.__graph = Digraph()
		self.__graph.attr(rankdir='LR')


	def DisplayGraph(self):
		self.__graph.render('flow-chart', format='png', cleanup=True)


					
	def GetFlows(self,line_type ,root = None):
		
		if root == None:
			root = '-2'

		visited_nodes = {}
		dp = {}

		def DFS(node, weight_value):
			node = int(node)

			if node == -1:
				dp[-1] = "END"
				return ["END"]

			if line_type[node] == LineType.Loop and node not in visited_nodes:
				visited_nodes[node] = 1
				for i, child_identifier in enumerate(self.GetNode(node).childs):
					if self.GetNode(node).weight_values[i] == 'BODY':
						current_node_data = f" -> {self.GetNode(node).data}"
						all_possible_paths = [current_node_data + ' -> ' + path for path in DFS(child_identifier, 'BODY')]
						if len(all_possible_paths) == 0:
							all_possible_paths = [current_node_data]
						dp[node] = all_possible_paths
						return dp[node]

			elif line_type[node] == LineType.Loop and node in visited_nodes and visited_nodes[node] == 1 and weight_value == 'NEXT ITERATION':
				visited_nodes[node] += 1
				for i, child_identifier in enumerate(self.GetNode(node).childs):
					if self.GetNode(node).weight_values[i] == 'OUT':
						dp[node] = DFS(child_identifier, 'OUT')
						return dp[node]

			else:
				if node not in dp:
					# print(self.GetNode(node).data)
					visited_nodes[node] = 1

					current_node_data = f" -> {self.GetNode(node).data}"
					all_possible_paths = []

					for i, child_identifier in enumerate(self.GetNode(node).childs):
						child_paths = DFS(child_identifier, self.GetNode(node).weight_values[i])
						if child_paths != None:
							for path in child_paths:
								all_possible_paths.append(current_node_data + ' -> ' + path)
					if len(all_possible_paths) == 0:
						all_possible_paths = [current_node_data]
					dp[node] = all_possible_paths
				return dp[node]
				
		return DFS(root, '')
				
	def Size(self): return len(self.__nodes)

	def ExportGraph(self, line_type):
		with open(f"flow_chart.txt", "w") as f:
			for item in self.GetFlows(line_type):
				f.write(item + "\n")
					
	def AddNode(self, identifier, node, shape = 'rectangle', color = '#DDDDDD'):
		identifier = str(identifier)
		
		# node: must be on type of str or Node

		if isinstance(node, str):
			self.__nodes.update({identifier: Node(data=node)})
		elif isinstance(node, Node):
			self.__nodes.update({identifier: node})
		else:
			raise Exception("Wrong Node format, only accepting [string or Node class]")
		
		new_node = self.__nodes[identifier]

		# FOR UI
		self.__graph.node(identifier, new_node.data,style='filled',fillcolor=color,penwidth='3',shape = shape)

		return new_node


	def AddEdge(self, identifier1, identifier2, weight_value = '', passive_edge=False,color='black',font_color='black'):
		identifier1 = str(identifier1); identifier2 = str(identifier2)
		
		if(identifier2 not in self.__nodes[identifier1].childs):
			# if(passive_edge):
			# 	self.__graph.edge(identifier1, identifier2, label=weight_value, penwidth='1',color=color, fontcolor=font_color,constraints='false')
			# else:
			self.__nodes[identifier1].childs.append(identifier2)
			self.__nodes[identifier1].weight_values.append(weight_value)
			self.__graph.edge(identifier1, identifier2, label=weight_value, penwidth='3',color=color, fontcolor=font_color,constraints='false')
		
	
	def GetNode(self, identifier): return self.__nodes[str(identifier)]

	def GetRoot(self): return self.__nodes["-2"] # START


