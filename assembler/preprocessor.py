# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		preprocessor.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		23rd December 2018
#		Purpose :	High Level Assembler - preprocessor stuff.
#
# ***************************************************************************************
# ***************************************************************************************

from error import *
import re

class PreProcessor(object):
	def __init__(self,codeGenerator):
		self.codeGenerator = codeGenerator
		self.globals = {}
	#
	#		Preprocessor
	#
	def process(self,source):
		source = self.tidyUp(source)												# tidy up.
		source = self.removeStringConstants(source)									# remove all the string constants.
		source = source.lower() 													# we can make it lower case.
		source = self.constantsAndGlobals(source)									# rip out constants/globals.
		source = self.splitProcedures(source)										# Split into procedures.
		return source
	#
	#		Tidy up tabs, double spaces, use semicolons to replace spaces and join together
	#		with CODENEWLINE markers
	#
	def tidyUp(self,source):
		source = [x if x.find("//") < 0 else x[:x.find("//")] for x in source]		# remove all comments
		source = PreProcessor.CODENEWLINE.join(source)								# put together lines with seperator.
		source = source.replace("\t"," ").replace("  "," ")							# remove tabs and some double spaces
		while source.find("  ") >= 0:												# remove the rest of the doubles
			source = source.replace("  "," ")
		return source.replace(" ",";")												# replace them with semicolons
	#
	#		Extract all string constants, replace with $xxx where xxx is an index into self.stringConstants[]
	#
	def removeStringConstants(self,source):
		self.stringConstants = []
		source = re.split("(\"[0-9a-zA-Z\_]+\")",source)							# parse out "char0-9a-z_"
		for i in range(0,len(source)):												# look for them
			if source[i][0] == '"':													# if found
				id = len(self.stringConstants)										# get the id 
				self.stringConstants.append(source[i][1:-1])						# save it.
				source[i] = "$"+str(id)												# replace with a marker
		return "".join(source)														# put it back together.
	#
	#		Rip out constants and globals and add them to the dictionary after validation.
	#
	def constantsAndGlobals(self,source):
		source = re.split("([a-z]+:[0-9a-z\.\_\:\=]+)",source)						# split them out
		AssemblerException.LINENUMBER = 1 											# track the line number.
		for i in range(0,len(source)):

			if source[i].startswith("global:"):										# global:<name>
				identifier = source[i][7:] 											# get identifier
				address = self.codeGenerator.allocSpace(1)							# allocate space for it.
				if re.match(PreProcessor.RX_IDENTIFIER,identifier) is None: 		# check valid identifier
					raise AssemblerException("Bad global "+source[i])
				self.addGlobal({"name":identifier,"type":"g","value":address})		# add it
				source[i] = "" 														# remove line.

			if source[i].startswith("const:"):										# const:<name>=<constant>
				m = re.match("^("+PreProcessor.RX_IDENTIFIER+")\=("+PreProcessor.RX_CONSTANT+")$",source[i][6:])
				if m is None:
					raise AssemblerException("Bad constant "+source[i])
				name = m.group(1)
				self.addGlobal({"name":name,"type":"c","value":int(m.group(2))}) 	# add global
				source[i] = "" 														# remove line.

			AssemblerException.LINENUMBER += source[i].count(PreProcessor.CODENEWLINE)
		return "".join(source) 														# put it back together.
	#
	#		Split the code into procedures
	#
	def splitProcedures(self,source):
		lineNumber = 1 																# track start line each proc															
		source = re.split("(proc\:"+PreProcessor.RX_IDENTIFIER+"\(.*?\))",source) 	# split up into bits.
		procedureList = [] 															# list of procedures.
		for i in range(0,len(source)):
			AssemblerException.LINENUMBER = lineNumber 

			if source[i].startswith("proc:"):										# found one.
				p = source[i].find("(")												# find starting parenthesis
				params = [x for x in source[i][p+1:-1].split(",") if x != ""]		# parameter bits
				for p1 in params:
					if re.match("^"+PreProcessor.RX_IDENTIFIER+"$",p1) is None:
						raise AssemblerException("Bad parameter "+p1)
				procDef = [lineNumber,source[i][5:p],params,source[i+1]] 			# make a procedure record
				procedureList.append(procDef)
			lineNumber += source[i].count(PreProcessor.CODENEWLINE)					# keep line number tracking
		return procedureList
	#
	#		Add a global
	#
	def addGlobal(self,info):
		if info["name"] in self.globals:
			raise AssemblerException("Duplicate name "+info["name"])
		self.globals[info["name"]] = info
	#
	#		Add a local
	#
	def addLocal(self,info):
		if info["name"] in self.locals:
			raise AssemblerException("Duplicate name "+info["name"])
		self.locals[info["name"]] = info



PreProcessor.RX_IDENTIFIER = "[a-z\_][a-z0-9\_\.\:]*"								# RX Match for an identifier.
PreProcessor.RX_CONSTANT = "\d+"													# RX Match for a decimal constant
PreProcessor.CODENEWLINE = "~"														# Character marking new line

# TODO For procedure base add parameters and locals for each, then substitute all identifiers
# TODO Except procedures.