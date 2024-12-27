from Graph import Graph, Node
from collections import deque
from RQueue import RQueue
from LineType import LineType


from Scrapper import Scrapper
class PythonScraper(Scrapper):
	"""
	Scrabing python files to create the needed nodes to generate a flowchart 
	"""

	def __init__(self, code:str, uniform_indentation_value:int = 4):
		super().__init__(code)

		
		self.uniform_indentation_value = uniform_indentation_value

	
		# python meta data vars: =============================================
		self._loop_keywords = ['do','while','for']
		self._splitting_keywords = ['if','elif','else']

		# each element in the stack is an index to the line code
		self._last_indentation_value = 0 #
		self._indentaion_value = {} #
		# ====================================================================

		self._indentaion_value[-2] = self._indentaion_value[-1] = 0

		self._Process() # Calls _PreProcess
		self._PostProcess()
		
		self.graph.ExportGraph(self._line_type)
		self.graph.DisplayGraph()


	def _GetIndentationValueOfLine(self, line_number):
		return self._indentaion_value[line_number]
	def _GetLineType(self, line_number):
		return self._line_type[line_number]

	def _GetBranchesParent(self, line_number, indentation_value, parent_allowed_types = [LineType.Procedural, LineType.Loop], exact_indentation_value=False, reverse=False) -> int:

		for i in range(line_number - 1, -1, -1):
			current_indentation = self._GetIndentationValueOfLine(i)
			if self._GetLineType(i) in parent_allowed_types and (current_indentation == indentation_value and exact_indentation_value or not exact_indentation_value and (current_indentation <= indentation_value and not reverse or current_indentation >= indentation_value and reverse)):
				return i
		return -2 # START node

	

	def _ProcessLine(self, line_number, line_of_code:str):
	
		current_indentation_value = len(line_of_code) - len(line_of_code.lstrip(' '))
		current_line_type = None
		self._indentaion_value[line_number] = current_indentation_value

		# ============================ Initializing the current Node =============================
		self.graph.AddNode(line_number, line_of_code.strip())

		if line_number == 0:
			self.graph.AddEdge(-2, line_number)
		# ============================ Initializing the current Node =============================

		last_loop_index = self._FindLoopIndex(line_of_code.strip())
		last_Condition_index = self._FindConditionIndex(line_of_code.strip())
		query_string = self._ClearStrings(line_of_code.lower())

		# check the type of the current line to scrap info for the required edges related to this node
		if(last_loop_index == 0):
			self._stack_of_loops.append(line_number)
			if line_number > 0:
				self._loop_level[line_number] = self._loop_level[line_number - 1] + 1
			else:
				self._loop_level[line_number] = 1
			current_line_type = LineType.Loop
		elif (last_Condition_index == 0):
			current_line_type = LineType.Condition
			if 'if' in query_string:
				self._existing_condition_keyword[line_number] = 'if'
			if 'elif' in query_string:
				self._existing_condition_keyword[line_number] = 'elif'
			if 'else' in query_string:
				self._existing_condition_keyword[line_number] = 'else'
		else:
			if 'continue' in query_string:
				self.graph.AddEdge(line_number, self._stack_of_loops[-1])
				current_line_type = LineType.TerminatorOfLoop
			elif 'break' in query_string:
				self._linking_requests.Push(line_number, self._GetIndentationValueOfLine(self._stack_of_loops[-1]))
				current_line_type = LineType.TerminatorOfLoop
			elif 'return' in query_string:
				current_line_type = LineType.TerminatorOfProgram			
				self.graph.AddEdge(line_number, -1, 'return')
			elif 'yield' in query_string:
				current_line_type = LineType.TerminatorOfProgram
				self.graph.AddEdge(line_number, -1, 'yield')
			else:
				current_line_type = LineType.Procedural
			
		self._line_type[line_number] = current_line_type
		if current_line_type != LineType.Loop:
			if line_number > 0:
				self._loop_level[line_number] = self._loop_level[line_number - 1]
			else:
				self._loop_level[line_number] = 0
		node_color = 'grey80'
		node_shape = 'rectangle'

		if current_line_type == LineType.Condition:
			node_color = 'green'
			node_shape = 'diamond'
		elif current_line_type == LineType.Loop:
			node_color = 'cornflowerblue'
			node_shape = 'rarrow'
		
		self.graph.AddNode(line_number, line_of_code.strip(), node_shape, color=node_color)

		# need some details
		if(current_indentation_value < self._last_indentation_value):

			for node_id in self._linking_requests.GetNodes(current_indentation_value):
				self.graph.AddEdge(node_id, line_number)
			self._linking_requests.Pop(current_indentation_value)

			last_loop_id = self._last_loop[line_number - 1]
			if(last_loop_id != -1 and current_indentation_value <= self._indentaion_value[last_loop_id]):
				self._stack_of_loops.pop()

		parent_allowed_types = [LineType.Procedural, LineType.Loop, LineType.Condition]
		prev_node_id = self._GetBranchesParent(line_number, current_indentation_value, parent_allowed_types)
	

		weight_value = ''
		font_color = 'black'

		if(self._GetLineType(prev_node_id) == LineType.Condition):
			if(self._GetIndentationValueOfLine(prev_node_id) == current_indentation_value):
				weight_value = 'FALSE'
				font_color = 'red'
			else:
				weight_value = 'TRUE'
				font_color = 'green'
		if(self._GetLineType(prev_node_id) == LineType.Loop):
			if(self._GetIndentationValueOfLine(prev_node_id) == current_indentation_value):
				weight_value = 'OUT'
				font_color = 'red'
			else:
				weight_value = 'BODY'
				font_color = 'green'

		self.graph.AddEdge(prev_node_id, line_number, weight_value, font_color=font_color)

		if len(self._stack_of_loops) > 0:
			self._last_loop[line_number] = self._stack_of_loops[-1]
		else:
			self._last_loop[line_number] = -1
		self._last_indentation_value = current_indentation_value
			

	def _PreProcess(self, line_of_code):
		if(len(line_of_code.strip()) == 0):
			return False
		if(len(line_of_code) == 0):
			return False
		
		# comment or a decorator
		if(self._ClearStrings(line_of_code.strip().lower())[0] in ['#',' @']):
			return False
		return True
	
	def _PostProcess(self):
		for id in range(self.graph.Size() - 2): # not counting the start and the end nodes
			current_node = self.graph.GetNode(id)
			line_type = self._GetLineType(id)
			if current_node.data == 'pass':
				pass

			if line_type not in [LineType.TerminatorOfLoop, LineType.TerminatorOfProgram] and (len(current_node.childs) == 0 or (len(current_node.childs) < 2 and line_type in [LineType.Condition, LineType.Loop] and not (line_type == LineType.Condition and self._existing_condition_keyword[id] == 'else') )):
				last_block_id = self._GetBranchesParent(id, self._indentaion_value[id] - self.uniform_indentation_value, parent_allowed_types=[LineType.Loop, LineType.Condition])
				if self._line_type[last_block_id] == LineType.Loop:
					self.graph.AddEdge(id, last_block_id, 'NEXT ITERATION', color='cornflowerblue')
				else:
					found = False
					for next_line in range(id + 1, self.graph.Size() - 2):
						if self._indentaion_value[next_line] < self._indentaion_value[id] and not (self._line_type[next_line] == LineType.Condition and self._existing_condition_keyword[next_line] in ['elif', 'else']):
							found = True
							
							last_loop_id = self._last_loop[id - 1] if id - 1 > 0 else -1
							if last_loop_id != -1 and self._indentaion_value[last_loop_id] >= self._indentaion_value[next_line]:
								self.graph.AddEdge(id, last_loop_id,'NEXT ITERATION', color='cornflowerblue')
							else:
								weight_value = 'BACK TO'
								if self._line_type[id] == LineType.Loop:
									weight_value = 'OUT'
								self.graph.AddEdge(id,next_line, weight_value)
							break
					if not found:
						self.graph.AddEdge(id, -1,'back to')


	def _Process(self):

		line_number = 0 # START if there's no code

		for line_of_code in self.code.splitlines():
			
			indentation_value = len(line_of_code) - len(line_of_code.lstrip(' '))
 
			# if there's like a SQL query in a str it will result for a conflect!

			for sub_line in line_of_code.split(';'):

				sub_line = sub_line.strip()
				sub_line = indentation_value * " " + sub_line

				if(self._PreProcess(sub_line)):
					self._ProcessLine(line_number, sub_line)
					line_number += 1

		if(line_number == 0): line_number = -1
		self.graph.AddEdge(line_number - 1, -1)

	
				

			




# import ast
# from graphviz import Digraph

# def add_ast_nodes(dot, node, parent_name=None):
#     """ Recursively add AST nodes and edges to a Graphviz Digraph. """
#     # Create a unique name for each node
#     node_name = str(id(node))
    
#     # Add the current node
#     if isinstance(node, ast.AST):  # Make sure it's an AST node
#         node_label = node._class_._name_
#         if isinstance(node, ast.Constant):
#             node_label += f": {getattr(node, 'value', '')}"
#         elif isinstance(node, ast.Name):
#             node_label += f": {getattr(node, 'id', '')}"
#         elif isinstance(node, ast.For):
#             node_label += f" for {getattr(node.target, 'id', '')} in {ast.dump(node.iter)}"
#         elif isinstance(node, ast.If):
#             node_label += f" if {ast.dump(node.test)}"
#         elif isinstance(node, ast.While):
#             node_label += f" while {ast.dump(node.test)}"
        
#         dot.node(node_name, node_label)
        
#         if parent_name:
#             dot.edge(parent_name, node_name)
        
#         # Recurse for all fields in the AST node
#         for field, value in ast.iter_fields(node):
#             if isinstance(value, list):
#                 for item in value:
#                     add_ast_nodes(dot, item, node_name)
#             elif isinstance(value, ast.AST):
#                 add_ast_nodes(dot, value, node_name)

# def visualize_ast(code):
#     tree = ast.parse(code)
#     dot = Digraph(comment='AST Visualization')

#     # Start by adding the root node (the module)
#     add_ast_nodes(dot, tree)

#     # Render the tree into a file (e.g., in PDF or PNG format)
#     dot.render('ast_tree', format='png', cleanup=True)  # You can change the format to 'pdf', 'jpeg', etc.
#     dot.view('ast_tree')  # This will open the generated image in a viewer

# # Test code
# code = """
# for i in range(5):
#     if i % 2 == 0:
#         print(i)
#     else:
#         print(i * 2)

# while True:
#     break
# """
# with open('python_example.py','r') as f: code = f.read()

# visualize_ast(code)

	


	


		


# import ast
# from graphviz import Digraph

# def add_flowchart_nodes(dot, node, parent_name=None):
#     """ Recursively add simplified flowchart nodes and edges to a Graphviz Digraph. """
#     node_name = str(id(node))
    
#     if isinstance(node, ast.For):
#         # Loop: for item in range()
#         node_label = f"for {getattr(node.target, 'id', '')} in {ast.dump(node.iter)}"
#         dot.node(node_name, node_label, shape='box')
#     elif isinstance(node, ast.While):
#         # Loop: while condition
#         node_label = f"while {ast.dump(node.test)}"
#         dot.node(node_name, node_label, shape='box')
#     elif isinstance(node, ast.If):
#         # Conditional: if condition
#         node_label = f"if {ast.dump(node.test)}"
#         dot.node(node_name, node_label, shape='diamond')
#     elif isinstance(node, ast.Expr):
#         # Action/Expression like print or any other statement
#         node_label = "Action"
#         dot.node(node_name, node_label, shape='box')
#     else:
#         return

#     if parent_name:
#         dot.edge(parent_name, node_name)

#     # Recurse for all children in the AST node
#     for field, value in ast.iter_fields(node):
#         if isinstance(value, list):
#             for item in value:
#                 add_flowchart_nodes(dot, item, node_name)
#         elif isinstance(value, ast.AST):
#             add_flowchart_nodes(dot, value, node_name)

# def visualize_flowchart(code):
#     tree = ast.parse(code)
#     dot = Digraph(comment='Simplified Flowchart')

#     # Start by adding the root node (module body)
#     add_flowchart_nodes(dot, tree)

#     # Render the flowchart into a file (e.g., in PNG format)
#     dot.render('simplified_flowchart', format='png', cleanup=True)  # You can change the format to 'pdf', etc.
#     dot.view('simplified_flowchart')  # This will open the generated image in a viewer

# # Test code
# code = """
# for i in range(5):
#     if i % 2 == 0:
#         print(i)
#     else:
#         print(i * 2)

# while True:
#     break
# """

# visualize_flowchart(code)
 		