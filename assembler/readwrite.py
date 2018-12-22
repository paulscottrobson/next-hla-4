# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		readwrite.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		22nd December 2018
#		Purpose :	Load and save memory scanners.
#
# ***************************************************************************************
# ***************************************************************************************

from common import *

class LoadDirectScanner(BaseScanner):
	def quickCheckCharacter(self):
 		return "!"
	def getRegularExpression(self):
		return BaseScanner.C_IDENTIFIER+"\!"

if __name__ == "__main__":
	l1 = LoadDirectScanner()
	print(BaseScanner.TARGET)
	samples = ["_a!","42","demo_42","-13"]
	for s in samples:
		print("====== "+s+" =====")
		print(l1.check(s))

