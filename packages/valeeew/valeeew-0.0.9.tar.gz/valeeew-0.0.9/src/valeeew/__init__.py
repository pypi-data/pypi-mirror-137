#function return the variable name 
def var_name(var, dir=locals()):
    for key, val in dir.items():
        if id(val) == id(var):
            return key
