# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		democodegen.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		22nd December 2018
#		Purpose :	Dummy Code Generator class
#
# ***************************************************************************************
# ***************************************************************************************

# ***************************************************************************************
#					This is a code generator for an idealised CPU
# ***************************************************************************************

class DemoCodeGenerator(object):
	def __init__(self):
		self.pc = 0x1000
		self.vars = 0x2000
		self.ops = { "+":"add","-":"sub","*":"mul","/":"div","%":"mod","&":"and","|":"ora","^":"xor" }
	#
	#		Load a constant or variable into the accumulator.
	#
	def loadAccumulator(self,isConstant,value):
		src = ("#${0:04x}" if isConstant else "(${0:04x})").format(value)
		print("${0:04x}  lda  {1}".format(self.pc,src))
		self.pc += 1
	#
	#		Do a binary operation on a constant or variable on the accumulator
	#
	def binaryOperation(self,operator,isConstant,value):
		if operator == "!" or operator == "?":
			self.binaryOperation("+",isConstant,value)
			print("${0:04x}  lda  [a].{1}".format(self.pc,"b" if operator == "?" else "w"))
			self.pc += 1
		else:
			src = ("#${0:04x}" if isConstant else "(${0:04x})").format(value)
			print("${0:04x}  {1}  {2}".format(self.pc,self.ops[operator],src))
			self.pc += 1
	#
	#		Store direct
	#
	def storeAccumulator(self,value):
		print("${0:04x}  lda  (${1:04x})".format(self.pc,value))
		self.pc += 1
	#
	#		Allocate space for n variables. Must be a continuous block.
	#
	def allocSpace(self,count):
		addr = self.vars
		self.vars += (2 * count)
		print("${0:04x}  dw   {1}".format(addr,",".join(["$0000"]*count)))
		return addr
	#
	#		Load A with address of string constant
	#
	def loadStringConstant(self,string):
		sAddr = self.pc
		print("${0:04x}  db   \"{1}\",0".format(self.pc,string))
		self.pc += len(string)+1
		self.loadAccumulator(True,sAddr)

if __name__ == "__main__":
	cg = DemoCodeGenerator()
	cg.loadAccumulator(True,42)
	cg.loadAccumulator(False,42)	
	cg.binaryOperation("&",True,44)
	cg.binaryOperation("&",False,44)	
	cg.binaryOperation("?",True,2)
	cg.binaryOperation("!",True,4)
	cg.storeAccumulator(46)
	cg.allocSpace(4)
	cg.allocSpace(1)	
	cg.loadStringConstant("Hello world!")