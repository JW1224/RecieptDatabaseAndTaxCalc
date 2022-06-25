import sqlite3
import tkinter.ttk as ttk
from tkinter import *
import csv
import tkinter.messagebox

def DeleteData(choice,ID,databaseInfo):
    '''This function gets the information to be deleted out of the database and saves it to a csv file. It then deletes the record from the database'''
    comfirmDelete = ComfirmDelete()
    if comfirmDelete == "yes":
        connection = sqlite3.connect("Database.db")
        cursor = connection.cursor()
        #Selects the item that is going to be deleted from the database
        cursor.execute("SELECT * FROM {} WHERE {}=?".format(databaseInfo[0][choice-1],databaseInfo[1][choice-1][0]),(ID,))
        result = cursor.fetchall()
        result = list(result[0])
        print("Result(from delete): ",result)
        #Appends the item to be deleted to the csv
        writeFile = open('Deleted.csv', 'a')
        deletedWriter = csv.writer(writeFile)
        data = [[databaseInfo[0][choice-1]]+result]
        deletedWriter.writerows(data)
        writeFile.close()
        connection = sqlite3.connect("Database.db")
        cursor = connection.cursor()
        ID = (ID,)
        #Deletes the item from the database
        cursor.execute("""DELETE FROM {} WHERE {} = ?;""".format(databaseInfo[0][choice-1],databaseInfo[1][choice-1][0]),ID)
        connection.commit()
    else:
        print()

def ComfirmDelete():
    '''Displays a window asking for comfirmation that the user would like to delete the selected record'''
    comfirmDelete = tkinter.messagebox.askquestion('Comfirm','Comfirm Delete?')
    return comfirmDelete

def UpdateData(choice,ID,tableHeader,Column1,Column2,Column3,Column4,databaseInfo):
    '''This function retrieves the data from the entries and then changes it to the correct format. It then inserts placeholder into the sql command and then inserts the data into these placeholders so it can be added into the database'''
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    values = []
    columns = []
    try:
        #Retrieves the contents of the entry and then converts it to an integer if it should be
        Column1Text = Column1.get()
        if databaseInfo[2][choice-1][1] == databaseInfo[2][choice-1][0]:
            Column1Text = int(Column1Text)
        else:
            print()
        values.append(Column1Text)
        columns.append(databaseInfo[1][choice-1][1])
    except:
        Column1Text = None
    try:
        Column2Text = Column2.get()
        if databaseInfo[2][choice-1][2] == databaseInfo[2][choice-1][0]:
            Column2Text = int(Column2Text)
        else:
            print()
        values.append(Column2Text)
        columns.append(databaseInfo[1][choice-1][2])
    except:
        Column2Text = None
    try:
        Column3Text = Column3.get()
        if databaseInfo[2][choice-1][3] == databaseInfo[2][choice-1][0]:
            Column3Text = int(Column3Text)
        else:
            print()
        values.append(Column3Text)
        columns.append(databaseInfo[1][choice-1][3])
    except:
        Column3Text = None
    try:
        Column4Text = Column4.get()
        if databaseInfo[2][choice-1][4] == databaseInfo[2][choice-1][0]:
            Column4Text = int(Column4Text)
        else:
            print()
        values.append(Column4Text)
        columns.append(databaseInfo[1][choice-1][4])
    except:
        Column4Text = None
    count = 0
    for items in columns:
        columns[count] = columns[count]+"=?"
        if count != len(columns)-1:
            columns[count] = columns[count]+","
        count = count+1
    print(columns)
    count = 0
    for items in columns:
        if count == 0:
            insertString = columns[0]
        else:
            insertString = insertString+str(columns[count])
        count = count+1
    values.append(ID)
    values = tuple(values)
    print(values)
    print(databaseInfo[0][choice-1],insertString,databaseInfo[1][choice-1][0])
    print(values, ID)
    #Updates the item in the database with the new data
    cursor.execute ("""
    UPDATE {}
    SET {}
    WHERE {}=?
    """.format(databaseInfo[0][choice-1],insertString,databaseInfo[1][choice-1][0]),values)
    connection.commit()


def GetColumnNames(choice,databaseInfo):
    '''This function retrieves a list of column names and returns it the main file to be used as label names'''
    tableColumns = []
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    sql_command = """PRAGMA table_info({})"""
    cursor.execute(sql_command.format(databaseInfo[0][choice-1]))
    result = cursor.fetchall()
    count = 0
    while count <= (len(result)-1):
        if result[count][5] == 0:
            tableColumns.append(result[count][1])
        count = count+1
    #Inserts an empty string as the labels need a string in the text field
    correct = False
    while correct == False:
        if len(tableColumns)<4:
            tableColumns.append("")
        elif len(tableColumns)==4:
            correct = True
    return tableColumns

def retrieveEntries(choice,Column1,Column2,Column3,Column4,ID,databaseInfo):
    '''This retrieves the data from the entries and then creates one string that is then inserted into the command. The values are then inserted into the placeholders within this string'''
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    try:
        Column1Text = Column1.get()
        if Column1Text == "":
            #If nothing is entered in the entries, the text none is stored instead
            Column1Text = "None"
    except:
        Column1Text = "None"
    try:
        Column2Text = Column2.get()
        if Column2Text == "":
            Column2Text = "None"
    except:
        Column2Text = "None"
    try:
        Column3Text = Column3.get()
        if Column3Text == "":
            Column3Text = "None"
    except:
        Column3Text = "None"
    try:
        Column4Text = Column4.get()
        if Column4Text == "":
            Column4Text = "None"
    except:
        Column4Text = "None"
    try:
        #Makes the value an integer if it should be stored as that in the database
        if databaseInfo[2][choice-1][1] == databaseInfo[2][choice-1][0]:
            Column1Text = int(Column1Text)
        else:
            print()
    except:
        print()
    try:
        if databaseInfo[2][choice-1][2] == databaseInfo[2][choice-1][0]:
            Column2Text = int(Column2Text)
        else:
            print()
    except:
        print()
    try:
        if databaseInfo[2][choice-1][3] == databaseInfo[2][choice-1][0]:
            Column3Text = int(Column3Text)
        else:
            print()
    except:
        print()
    try:
        if databaseInfo[2][choice-1][4] == databaseInfo[2][choice-1][0]:
            Column4Text = int(Column4Text)
        else:
            print()
    except:
        print()
    if choice <= 6:
        table_names = databaseInfo[0][choice-1]
        tableColumns =[]
        sql_command = """PRAGMA table_info({})"""
        cursor.execute(sql_command.format(table_names,))
        result = cursor.fetchall()
        count = 0
        while count <= (len(result)-1):
            if result[count][5] == 0:
                tableColumns.append(result[count][1])
            count = count+1
        values = (Column1Text,Column2Text,Column3Text,Column4Text)
    elif choice > 6:
        choice = choice-6
        values = (ID,Column1Text,Column2Text,Column3Text,Column4Text)
        tableColumns = databaseInfo[1][choice-1]
    if choice == 6:
        values =(ID)
    #Creates a string to be inserted into the sql command
    columnNames = "("
    count = 0
    for columns in tableColumns:
        columnNames = columnNames+str(tableColumns[count])
        if count != len(tableColumns)-1:
            columnNames = columnNames+","
        else:
            columnNames = columnNames+") "
        count = count+1
    numberOfValues = "?"
    done = False
    count = 0
    while done == False:
        if count < len(tableColumns)-1:
            numberOfValues = numberOfValues+",?"
        else:
            done = True
        count = count+1
    insertList = databaseInfo[0][choice-1]+columnNames+"VALUES ("+numberOfValues
    print(insertList)
    #Inserts the data into the database
    sql_command = """INSERT INTO {});"""
    cursor.execute(sql_command.format(insertList),values[:len(tableColumns)])
    connection.commit()

