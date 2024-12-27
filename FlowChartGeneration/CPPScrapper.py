from Graph import Graph, Node
from collections import deque
from RQueue import RQueue
from LineType import LineType

from Scrapper import Scrapper
class CPPScrapper(Scrapper):
    def __init__(self, code):
        super().__init__(code)

        # C++ meta data vars: =============================================
        self._loop_keywords = ['do','while','for','for_each']
        self._splitting_keywords = ['if','else if','else']
        # ====================================================================

        self._Process()

        self.graph.ExportGraph(self._line_type)
        self.graph.DisplayGraph()


    def _ProcessLine(self, line_of_code):
        pass

    def _Process(self):
        line_number = 0

        for line_of_code in self.code.splitlines():
            self._ProcessLine(line_of_code)
            line_number += 1
        
        if(line_number == 0): line_number = -1
        self.graph.AddEdge(line_number - 1, -1)