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
import re

# ***************************************************************************************
#
#	The preprocessor takes source code and converts it to a structured list of 
#	compilable objects, which should all be independent. However, there is no
#	checking at all, so it will be done at compile time.
#
#	These can be: (examples in test code )
#		decimal constants
#		identifiers including indirection
#		binary operations followed by constants/identifiers
#		assignment including indirection
#		quoted string with _ for space, alphanumerics only.
#		complete constant, local, global, procedure defines
#		complete invocations of procedures.
#		keywords
#		statement group operators { }
#
# ***************************************************************************************

class PreProcessor(object):
	def __init__(self):
		self.splitter = re.compile("([\{\}\;\~\+\-\*\/\%\^\&\|\>\s])")
		self.identifierCheck = re.compile("^([a-z\_][0-9a-z\_\.\:]*)$")
		self.constantCheck = re.compile("^([0-9]+)$")
	#
	#		Pre process a file. Makes a text file into an array where every element is a self contained
	#		operation. 
	#
	def process(self,code):
		#
		#		Initial tidying up, remove comments and tabs
		#
		code = [x if x.find("//") < 0 else x[:x.find("//")] for x in code]				# Remove comments
		code = [x.replace("\t"," ").strip() for x in code]								# Remove tabs and strip
		#
		#		Join it together, using ~ as new line markers, and subidivde into lexical units
		#
		code = "~".join(code)															# make it a long string.
		code = self.splitter.split(code) 												# split it up into pieces.
		code = [x.strip() for x in code if x.strip() != ""]								# remove all empty bits
		#
		#		Look through for binary operations - if found add the term following to the operation
		#		for > this can be the identifier or identifier!term or identifier?term
		#
		for i in range(0,len(code)):													# package all binary ops.
			if len(code[i]) == 3:
				if code[i][0] == "'" and code[i][2] == "'":
					code[i] = str(ord(code[i][1]))
			if len(code[i]) == 1 and ">+-*/%&|^".find(code[i]) >= 0:					# standard binary operation.
				code[i] = code[i]+code[i+1] 
				code[i+1] = ""
		code = [x for x in code if x != "" and x != ";"]								# remove empty and superfluous ;
		return code


if __name__ == "__main__":
	code = """
		const:height=29;
		const:width=42;
		// Line 1
		word(b,23,c);a 'x'
		global:a,b,cc
		local:d,e,f
		d[2] + e + 42 + g > a > b!4 > b[c]
		height + width >e "simple_string"
		proc:demo(w1,w2) 
		{ hello(); }
		if <if =if then begin <until =until until for next 
	"""
	code = "".join([ code ] * 2)
	code = code.split("\n")
	pp = PreProcessor()
	xcode = pp.process(code)
	print("\n".join(["["+x+"]" for x in xcode]))
	print(len(code),len(xcode))
