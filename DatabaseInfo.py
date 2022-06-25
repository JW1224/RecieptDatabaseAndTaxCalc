import sqlite3

def RetrieveDatabaseInfo():
    '''This function retrieves the database information and then puts all of the data needed by the program into an array'''
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    #Retrieves the information about all of the tables in the database
    sqlCommand = "SELECT * FROM sqlite_master WHERE type='table';"
    cursor.execute(sqlCommand)
    result = cursor.fetchall()
    #Saves just the names of the tables
    table1 = result[0][1]
    tableNames = [table1]
    try:
        table2 = result[1][1]
        tableNames.append(table2)
    except:
        print()
    try:
        table3 = result[2][1]
        tableNames.append(table3)
    except:
        print()
    try:
        table4 = result[3][1]
        tableNames.append(table4)
    except:
        print()
    try:
        table5 = result[4][1]
        tableNames.append(table5)
    except:
        print()
    try:
        table6 = result[5][1]
        tableNames.append(table6)
    except:
        print()
    try:
        table7 = result[6][1]
        tableNames.append(table7)
    except:
        print()
    try:
        table8 = result[7][1]
        tableNames.append(table8)
    except:
        print()
    #Removes the table that stores the values for the auto-increment of the other tables 
    tableNames.remove('sqlite_sequence')
    tableNames.remove('UserDetails')
    tableNames.sort()
    i = 0
    columnNames = []
    tableColumns = []
    tableColumns_type = []
    tableColumns_type = []
    columnNamesType = []
    for names in tableNames:
        #Gets the information about the table names in tableNames
        sqlCommand = """PRAGMA table_info({})"""
        cursor.execute(sqlCommand.format(tableNames[i],))
        i = i+1
        result = cursor.fetchall()
        count = 0
        while count <= (len(result)-1):
            tableColumns.append(result[count][1])
            tableColumns_type.append(result[count][2])
            count = count+1
        columnNames.append(tableColumns)
        columnNamesType.append(tableColumns_type)
        tableColumns = []
        tableColumns_type = []
    databaseInfo = [tableNames,columnNames,columnNamesType]
    return databaseInfo
