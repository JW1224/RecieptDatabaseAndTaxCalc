import sqlite3

def Search(choice,databaseInfo,value):
  '''This function searches the database table chosen by the user
     for the value provided using a linear search and then returns
     the result'''
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  searchResult = []
  rowList = []
  sqlCommand ="SELECT * FROM {};"
  cursor.execute(sqlCommand.format(databaseInfo[0][choice-1]))
  try:
    value = int(value)
  except:
    print()
  for row in cursor:
    for item in row:
      print(item)
      if item == value or item == str(value):
        if row[0] not in rowList:
          searchResult.append(row)
          rowList.append(row[0])
      else:
        try:
          splitItem = item.split()
          for word in splitItem:
            if word == value or word == str(value) or \
            (splitItem[1]+" "+splitItem[2]) == value or \
            (splitItem[3]+" "+splitItem[4]) == value:
              if row[0] not in rowList:
                searchResult.append(row)
                rowList.append(row[0])
        except:
          pass
  return searchResult
