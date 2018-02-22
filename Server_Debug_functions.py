
DEBUG = 1

def setDebug(debugValue):
   DEBUG = debugValue

   
def DebugPrint(datatype, varname, variable):
   if DEBUG:
      if datatype == 'dict':
         pDict(variable, varname)
      elif datatype == 'list':
         pList(variable, varname)
      elif datatype == 'varstring':
         pVarString(variable, varname)
      elif datatype == 'string':
         pString(variable)
   else: pass


def pDict(variable, varname):
   print('*******************************************')
   print('Name: {}').format(varname)
   print('*******************************************')
   for key, value in zip(variable.keys(), variable.values()):
      print('   key => {0} : value => {1}').format(key, value)
   print('*******************************************\n')

def pList(variable, varname):
   print('*******************************************')
   print('Name: {}').format(varname)
   print('*******************************************')
   for element in variable: print('   element => {}').format(element)
   print('*******************************************\n')

def pVarString(variable, varname):
   print('*******************************************')
   print('Name => {} : Value => {}').format(varname, variable)
   print('*******************************************\n')

def pString(variable):
   print('*******************************************')
   print('   {}').format(variable)
   print('*******************************************\n')
   


