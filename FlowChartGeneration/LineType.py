from enum import Enum

class LineType(Enum):
	Procedural = -1
	Loop = 0
	Condition = 1
	TerminatorOfLoop = 2
	TerminatorOfProgram = 4