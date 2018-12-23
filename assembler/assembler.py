# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		assembler.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		23rd December 2018
#		Purpose :	High Level Assembler
#
# ***************************************************************************************
# ***************************************************************************************

from error import *
from democodegen import *
from preprocessor import *
import re

# ***************************************************************************************
#											Assembler
# ***************************************************************************************

class Assembler(object):
	def __init__(self,codeGenerator):
		self.codeGenerator = codeGenerator
		self.preProcessor = PreProcessor(codeGenerator)

	def assemble(self,source):
		source = self.preProcessor.process(source)
		for x in source:
			print(">>",x)
		print(self.preProcessor.globals)
		
if __name__ == "__main__":

	code = """
		global:glv0
		const:democ=42
		const:democ2=39
		proc:demo(a,b,c) {
			a+b+c>glv1[4]
		} // comment
		PROC:Demo2(a,b,c) {} // comment
		proc:noparams() {}
		"Hello_world"
		global:glv1
		global:glv2
		b = 42 

	"""
	code = "".join(code * 1)

	code = code.split("\n")
	asm = Assembler(DemoCodeGenerator())
	code = asm.assemble(code)

