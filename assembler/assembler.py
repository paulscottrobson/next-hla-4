# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		processor.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		22nd December 2018
#		Purpose :	Pre-processor of string arrays to assembleable format.
#
# ***************************************************************************************
# ***************************************************************************************

from error import *
from dictionary import *
from democodegen import *
from processor import *
import re

# ***************************************************************************************
#											Assembler
# ***************************************************************************************

class Assembler(object):
	def __init__(self,codeGenerator,dictionary):
		self.codeGenerator = codeGenerator 								# code generator
		self.dictionary = dictionary 									# dictionary
		self.processor = PreProcessor() 								# code pre-processor.

	def assemble(self,sourceCode):
		self.source = self.processor.process(sourceCode) 				# process the code into chunks
		self.pos = 0 													# position 
		AssemblerException.LINENUMBER = 1								# set up the line number.
		while self.pos < len(self.source):
			self.assembleInstruction()

	def assembleInstruction(self):
		word = self.source[self.pos] 									# get the next word.
		self.pos += 1
		#
		#		~ indicates a new line in the original source.
		#
		if word == "~": 												# new line number
			AssemblerException.LINENUMBER += 1
			return
		#
		#		{ groups }
		#
		if word == "{":
			while self.pos < len(self.source) and self.source[self.pos] != "}":
				self.assembleInstruction()
			if self.pos == len(self.source):
				raise AssemblerException("Missing }")
			self.pos += 1 												# skip over }
			return
		#
		#		binary operation
		#

		#
		#		right assignment.
		#

		#
		#		global/local/proc definition
		#

		#
		#		identifier/constant
		#

		#
		#		procedure invocation
		#
		print(word,AssemblerException.LINENUMBER)

if __name__ == "__main__":
	code = """
		42 * lv1 & lv1[4] lv1[lv2]
		{ +2 -3 }

	""".split("\n")
	asm = Assembler(DemoCodeGenerator(),TestDictionary())
	asm.assemble(code)