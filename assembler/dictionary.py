# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		dictionary.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		22nd December 2018
#		Purpose :	Dictionary Classes
#
# ***************************************************************************************
# ***************************************************************************************

# ***************************************************************************************
#										Items
# ***************************************************************************************

class DictionaryItem(object):
	def __init__(self,name,value):
		self.name = name.strip().lower()
		self.value = value 
	def getName(self):
		return self.name
	def getValue(self):
		return self.value

class ConstantDictionaryItem(DictionaryItem):
	pass

class VariableDictionaryItem(DictionaryItem):
	pass

class ProcedureDictionaryItem(DictionaryItem):
	def __init__(self,name,value,paramBase,paramCount):
		DictionaryItem.__init__(self,name,value)
		self.paramBase = paramBase
		self.paramCount = paramCount
	def getParameterBase(self):
		return self.paramBase
	def getParameterCount(self):
		return self.paramCount

# ***************************************************************************************
#										Dictionary
# ***************************************************************************************

class Dictionary(object):
	def __init__(self):
		self.locals = {}
		self.globals = {}
	#
	#		Add a dictionary item
	#
	def addLocal(self,item):
		self._add(item,True)
	def addGlobal(self,item):
		self._add(item,False)
	#
	def _add(self,item,isLocal):
		target = self.locals if isLocal else self.globals
		if item in target:
			raise AssemblerException("Duplicate identifier")
		target[item.getName()] = item
	#
	#		Find a dictionary item
	#
	def find(self,itemName):
		itemName = itemName.strip().lower()
		if itemName in self.locals:
			return self.locals[itemName]
		if itemName is self.globals:
			return self.globals[itemName]
		return None
	#
	#		Purge locals
	#
	def purgeLocals(self):
		self.locals = {}

# ***************************************************************************************
#									Test Dictionary
# ***************************************************************************************

class TestDictionary(Dictionary):
	def __init__(self):
		Dictionary.__init__(self)
		self.addLocal(ConstantDictionaryItem("const42",42))
		self.addGlobal(VariableDictionaryItem("gv1",0x1000))
		self.addGlobal(VariableDictionaryItem("gv2",0x1002))
		self.addLocal(VariableDictionaryItem("lv1",0x2000))
		self.addLocal(VariableDictionaryItem("lv2",0x2002))
		self.addGlobal(ProcedureDictionaryItem("pr0",0x3000,0,0))
		self.addGlobal(ProcedureDictionaryItem("pr3",0x3003,0x1800,3))

if __name__ == "__main__":
	d = TestDictionary()		
	