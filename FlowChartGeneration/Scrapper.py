from abc import ABC, abstractmethod
from Graph import Graph, Node
from collections import deque
from RQueue import RQueue
from LineType import LineType
import re

class Scrapper(ABC):



    @property
    def _PreProcess(self) -> bool:
        """
            pre process the line and make it ready for processing and indicate wtheter it's a valid line to process or not like (comments, decorators, ...)
        """
        pass

    @property
    def _ProcessLine(self, line_of_code:str) -> None:
        pass

    @property
    def _Process(self) -> None: 
        pass

    @property
    def _PostProcess(self) -> None:
        pass

    
    def _ClearStrings(self, line_of_code):
        pattern = r"(['\"])(.*?)\1"
        matches = re.findall(pattern, line_of_code)
        filtered = [match[1] for match in matches]
        filtered_line_of_code = re.sub(
            pattern,
            lambda match: "" if match[2] in filtered else match.group(0),
            line_of_code,
        )
        return filtered_line_of_code
    

    def __FindIndex(self, line_of_code, keywords):
        index = None
        for keyword in keywords:
            keyword_index = line_of_code.find(keyword)
            if(keyword_index != -1):
                if index == None:
                    index = keyword_index
                else:
                    index = min(index, keyword_index)
        return index

    def _FindLoopIndex(self, line_of_code):
        return self.__FindIndex(line_of_code, self._loop_keywords)

    def _FindConditionIndex(self, line_of_code):
        return self.__FindIndex(line_of_code, self._splitting_keywords)
    


    def __init__(self, code:str) -> None:

        """
            this Class represent an abstract Scrapper of the Nodes, edges of the flowchart for all the inherited languages

            - each child class should has it's own meta data vars to specify it's own rules some of them are shared

            - there's 3 main methods that should be abstract to process each line according to it's corresponding language
            - PreProcess
            - Process
            - PostProcess
            
             
            Attributes:
                code (str): the input code script
                
        """
        self.code = code
        self.graph = Graph()

        # Mainly in the class implementation the "line_number" of the current code is considered the identifer of the current Node to process


        # meta data vars: ====================================================
        self._loop_keywords = [] # list of all loop keywords
        self._splitting_keywords = [] # list of all branches (if-conditions keywords)

        # each element in the stack is an index to the line code
        self._stack_of_loops = deque() 
        self._linking_requests = RQueue()

        self._last_loop = {}
        self._loop_level = {}
        self._line_type = {}
        self._existing_condition_keyword = {}
        # ====================================================================

        self.graph.AddNode(-2,"START",shape='oval',color='green')
        self.graph.AddNode(-1,"END",shape='oval',color='red')
        self._line_type[-2] = self._line_type[-1] = LineType.Procedural


    