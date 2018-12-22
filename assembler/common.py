# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		common.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		22nd December 2018
#		Purpose :	NextHLA Common Code.
#
# ***************************************************************************************
# ***************************************************************************************

import re

# ***************************************************************************************
#									Exception
# ***************************************************************************************

class AssemblerException(Exception):
	pass

# ***************************************************************************************
#								  Word Scanners
# ***************************************************************************************

class BaseScanner(object):
	def __init__(self,dictionary = None,target = "test"):
		if not BaseScanner._staticSetup:
			BaseScanner._staticSetup = True
			BaseScanner.DICTIONARY = dictionary
			BaseScanner.TARGET = target 
			BaseScanner.C_IDENTIFIER = re.compile("^[a-z\_][a-z\_0-9]*$")
			BaseScanner.C_CONSTANT = re.compile("^\-?[0-9]+$")
		self.create()
	#
	#		Create scanners own stuff if needed, compiled regEx etc.
	#
	def create(self):
		pass 
	#
	#		Quick check does a fast check. It's default is to do a test to see if
	#		the 'quick check character' is present. This is "is it worth checking properly"
	#
	def quickCheck(self,word):
		return word.find(self.quickCheckCharacter()) >= 0
	#
	#		Quick check character, should be returned.
	#
	def quickCheckCharacter(self):
		assert False,"Not implemented"
	#
	#		Standard full check. If it passes this, we know it's this type of instruction.
	#		it can still fail syntactically.
	#
	def slowCheck(self,word):
		assert False,"Not implemented"
	#
	#		This is a slower, more precise check.
	#
	def check(self,word):
		passed = False
		if self.quickCheck(word):
			passed = self.slowCheck()
			if passed:
				if BaseScanner.TARGET == "test":
					self.codeGenerateDummy(word)
				elif BaseScanner.TARGET == "z80":
					self.codeGenerateZ80(word)
				else:
					assert False,"Code Generator "+BaseScanner.TARGET+" not implemented"
	#
	#		Code Generators
	#
	def codeGenerateDummy(self,word):
		assert False,"Not implemented"
	def codeGenerateZ80(self,word):
		assert False,"Not implemented"

BaseScanner._staticSetup = False

if __name__ == "__main__":
	test = BaseScanner()
	print(BaseScanner.TARGET)
	samples = ["_a","42","demo_42","-13"]
	for s in samples:
		print("====== "+s+" =====")
		print(BaseScanner.C_IDENTIFIER.match(s))
		print(BaseScanner.C_CONSTANT.match(s))		

