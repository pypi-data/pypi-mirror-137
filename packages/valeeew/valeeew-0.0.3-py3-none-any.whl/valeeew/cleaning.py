#function to make a quick overview of your DATAframe
def overview(data):
  dupli = data.duplicated().sum()
  nul = (data.isna().mean()).sum()
  reslt = 0
  if dupli + nul == 0:
    a = "No duplicate and no null DATA"
  elif dupli == 0 and nul != 0:
    a = "Null DATA and nothing duplicate"
  elif dupli != 0 and nul == 0:
    a = "Duplicate DATA and nothing null"
  else:
    a = "Duplicate and null DATA"
  
  if a == "Duplicate DATA and nothing null" or "Duplicate and null DATA":
    reslt = data[(data.duplicated())== True]

  print(a)
  return reslt

# function to filter the values we want to keep
def keep(data, col, value):
    reslt = data[(data[col] == value) == True]
    return reslt

# function to filter the values we want to delete
def kick(data, col, value):
    reslt = data[(data[col] == value) == False]
    return reslt
