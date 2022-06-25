from tkinter import *
import tkinter.ttk as ttk
from CreateTables import *
from InsertingData import *
from DatabaseInfo import *
from SearchTables import *
import csv, hashlib, uuid, os, tkinter.messagebox, sqlite3

def SearchJobs(ID,choice):
  '''This function selects all the jobs with Client_ID of the slected client and then displays them in the table'''
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  #Selects the Jobs where Client_ID is equal to ID
  sqlCommand ="SELECT * FROM Jobs WHERE Client_ID = ?;"
  cursor.execute(sqlCommand,(ID,))
  result = cursor.fetchall()
  tableHeader = databaseInfo[1][2]
  #Calls CreateTable which creates the table
  CreateTable(result,0,3,frameTop,0,tableHeader,0)

def SearchInvoices(ID,choice):
  '''This function selects all the invoices that have a Job_ID equal to ID and displays them in a table'''
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  sqlCommand ="SELECT * FROM Invoices WHERE Job_ID = ?;"
  cursor.execute(sqlCommand,(ID,))
  result = cursor.fetchall()
  tableHeader = databaseInfo[1][1]
  #Calls CreateTable which creates the table
  CreateTable(result,0,2,frameTop,0,tableHeader,0)

def SearchReceipts(ID,choice):
  '''Selects all the Receipt_No's from Receipts_For_Job and then retrieves all the Receipts with the Receipt_No's retrieved'''
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  #Selects all the Receipt_No's from Receipts_For_Job with the selected jobs ID
  sqlCommand ="SELECT Receipt_No FROM Receipts_For_Job WHERE Job_ID = ?;"
  cursor.execute(sqlCommand,(ID,))
  result = cursor.fetchall()
  Receipt_Nos = []
  #Creates a list of the Receipt_No's
  for items in result:
    Receipt_Nos.append(result[result.index(items)][0])
  #Makes the list of Receipt_Nos a tuple so it can be inserted into the sql command
  Receipt_Nos = tuple(Receipt_Nos)
  #Creates a string with the correct number of placeholders for the list to be inserted into
  InsertList = "("
  for item in Receipt_Nos:
    InsertList = InsertList+"?,"
  InsertList = InsertList[:len(InsertList)-1]+")"
  #Selectes the Receipts from the Receipts table with the correct Receipt_Nos
  sqlCommand ="SELECT * FROM Receipts WHERE Receipt_No IN {};"
  cursor.execute(sqlCommand.format(InsertList),Receipt_Nos)
  result = cursor.fetchall()
  tableHeader = databaseInfo[1][4]
  #Calls CreateTable which creates the table
  CreateTable(result,0,5,frameTop,0,tableHeader,0)

def PasswordClear():
    '''This function clears the Username and Password Entry boxes and then diplays
       an Error message'''
    UsernameBox.delete (first=0, last=200)
    PasswordBox.delete (first=0, last=200)
    tkinter.messagebox.showerror("Incorrect", "Incorrect Username \n or Password")

def PasswordChecker():
    '''This function retrieves the password and username from the entries and then
       hashes it to compare with the stored password if the match it continues to open
       the program if not it calls PasswordClear() to reset the password input window
       and display an error message'''
    Username = (UsernameBox.get(),)
    Password = PasswordBox.get()
    salt = uuid.uuid4().hex
    hashedPassword = hashlib.sha512((Password+salt).encode()).hexdigest()
    FinalPassword = salt+'£$%£'+hashedPassword
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    #Retrieves the hashed password from the database
    cursor.execute("SELECT Password FROM UserDetails WHERE Username = ?",Username)
    storedPassword = cursor.fetchall()
    try:
        #This splits the storedPassword in to the salt and hashed password
        splitPass = storedPassword[0][0].split("£$%£")
        hashedPassword = hashlib.sha512((Password+splitPass[0]).encode()).hexdigest()
        #Compares the USer entered password to the stored password
        if hashedPassword == splitPass[1]:
            #Makes Correct a global so that the rest of the program knows the password
            #is true
            global Correct
            Correct = True
            top.destroy()
        else:
            PasswordClear()
    except:
        PasswordClear()

def InsertMerchant_ID(tree2,choice,frameTop):
    '''This function retrieves the Merchant ID that was selected by the user and then
       inserts this into the correct entry box'''
    try:
        items = tree2.item(tree2.selection())
        #Retrieves the information about the item as a dictionary
        values = items['values']#Selects only the the values from the dictionary
        ID = values[0]
        Column2.delete (first=0, last=200)
        Column2.insert (0, ID)
    except:
        print()

def fnSelectItem(tree,choice,frameTop,tableHeader):
    '''This function tries to retrieve the item that the user has selected and then
       displays the correct buttons'''
    try:
        #Selects the array of items from the tree that was selected by the user
        items = tree.item(tree.selection())
        values = items['values']
        connection = sqlite3.connect("Database.db")
        cursor = connection.cursor()
        #Selects the data from the table with the unique identifier retrieve from the tree
        cursor.execute("SELECT * FROM {} WHERE {}=?".format(databaseInfo[0][choice-1],databaseInfo[1][choice-1][0]),(values[0],))
        result = cursor.fetchall()
    except:
        #Shows an error message 
        tkinter.messagebox.showerror("No Selection", "Please select an item from the table")
    try:
        result = result[0][0]
    except:
        print()
    if result == values[0]:
        try:
            if choice == 6:
                ID = values[1]
            else:
                ID = values[0]
            #Creates all the buttons to be displayed when an item is selected
            EditItemButton = ttk.Button(myGui, text = "Edit Item",width = 14,command = lambda : (EditData(choice,ID,tableHeader),EntryFrame.config(highlightthickness=3)))
            DeleteItemButton = ttk.Button(myGui, text = "Delete Item",width = 14,command = lambda : (DeleteData(choice,ID,databaseInfo),Refresh(choice,frameTop)))
            AddJobButton = ttk.Button(myGui, text = "Add Job",width = 14,command = lambda : (Refresh(3,frameTop)\
                                                                                          ,DisplayTable(3,frameTop,search),AddIDToColumn(ID)\
                                                                                          ,InsertData(3,EnterDataButton,frameTop,ID)\
                                                                                          ,EntryFrame.config(highlightthickness=3)))
            SearchJobsButton = ttk.Button(myGui, text = "Search Jobs",width = 14,command = lambda : (SearchJobs(ID,choice)))
            SearchInvoicesButton = ttk.Button(myGui, text = "Search Invoices",width = 14,command = lambda : (SearchInvoices(ID,choice)))
            SearchReceiptsButton = ttk.Button(myGui, text = "Search Receipts",width = 14,command = lambda : (SearchReceipts(ID,choice)))
            AddInvoiceButton = ttk.Button(myGui, text = "Add Invoice",width = 14,command = lambda : (Refresh(2,frameTop)\
                                                                                          ,DisplayTable(2,frameTop,search),AddIDToColumn(ID)\
                                                                                          ,InsertData(2,EnterDataButton,frameTop,ID)\
                                                                                          ,EntryFrame.config(highlightthickness=3)))
            AddReceiptButton = ttk.Button(myGui, text = "Add Reciept",width = 14,command = lambda : (Refresh(5,frameTop)\
                                                                                          ,DisplayTable(5,frameTop,search)\
                                                                                          ,InsertData(5,EnterDataButton,frameTop,ID),EntryFrame.config(highlightthickness=3)))
            EditItemButton.place(x=1080,y=50)
            DeleteItemButton.place(x=1080,y=80)
            if choice == 1:
                AddJobButton.place(x=1080,y=110)
                SearchJobsButton.place(x=1080,y=140)
            elif choice == 3:
                EditItemButton.place(x=1080,y=50)
                DeleteItemButton.place(x=1080,y=80)
                AddInvoiceButton.place(x=1080,y=110)
                AddReceiptButton.place(x=1080,y=140)
                SearchInvoicesButton.place(x=1080,y=170)
                SearchReceiptsButton.place(x=1080,y=200)
        except:
            print()
    else:
        try:
            RestoreButton = ttk.Button(myGui, text = "Restore Item",width = 14,command = lambda : (RestoreData(values,choice),csvLineSearch(values,choice),Refresh(choice,frameTop)))
            RestoreButton.place(x=1080,y=50)
            PermDeleteButton = ttk.Button(myGui, text = "Permanently"+"\n"+"Delete",width = 14,command = lambda : (csvLineSearch(values,choice),Refresh(choice,frameTop)))
            PermDeleteButton.place(x=1080,y=80)
        except:
            print()

def RestoreData(values,choice):
    '''This function restores an item that has been deleted from the database'''
    for items in values:#Select each column from every row
        listItem = list(items)#Makes the string a list
        try:
            listItem.remove(".")#Removes the decimal point
        except:
            print()
        values[values.index(items)]="".join(listItem)#Makes listItem back into a string
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    tableColumns = databaseInfo[1][choice-1]
    #Creates a string that can be inserted to complete the sql command so values can be inserted into the database
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
    sqlCommand = """INSERT INTO {});"""
    cursor.execute(sqlCommand.format(insertList),values[:len(tableColumns)])
    connection.commit()

def EditData(choice,ID,tableHeader):
    '''This function inserts the data to be edited from the database into the entries, the user can then edit it and
       then press the enter data button to update the database by sending the data to the UpdateData function'''
    Column1.delete (first=0, last=200)
    Column2.delete (first=0, last=200)
    Column3.delete (first=0, last=200)
    Column4.delete (first=0, last=200)
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM {} WHERE {}=?".format(databaseInfo[0][choice-1],databaseInfo[1][choice-1][0]),(ID,))
    tableHeader = databaseInfo[1][choice-1]
    result = cursor.fetchall()
    #Inserts the data into the entries
    try:
        Column1.insert (0, result[0][1])
    except:
        print()
    try:
        Column2.insert (0, result[0][2])
    except:
        print()
    try:
        Column3.insert (0, result[0][3])
    except:
        print()
    try:
        Column4.insert (0, result[0][4])
    except:
        print()
    EnterDataButton.config(command=lambda : (UpdateData(choice,ID,tableHeader,Column1,Column2,Column3,Column4,databaseInfo),Refresh(choice,frameTop),EntryFrame.config(highlightthickness=0)))
    EnterDataButton.config(state=NORMAL)

def Refresh(choice,frameTop):
    '''This function clears the entries and re-displays the table to show if the database has been updated'''
    Column1.config(state=NORMAL)
    Column2.config(state=NORMAL)
    Column3.config(state=NORMAL)
    Column4.config(state=NORMAL)
    Column1.delete (first=0, last=200)
    Column2.delete (first=0, last=200)
    Column3.delete (first=0, last=200)
    Column4.delete (first=0, last=200)
    DisplayTable(choice,frameTop,search)

def AddIDToColumn(ID):
    '''This function inserts the ID into the entry Column1'''
    Column1.insert (0, ID)

def ConnectJobsAndReceipts(choice,ID):
    '''This function selects all the Receipt_Nos and then finds the larges one and therefore the most recent and inserts it into the linking table with the Job_ID'''
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    sqlCommand = """SELECT MAX(Receipt_No) FROM Receipts"""
    cursor.execute(sqlCommand)
    result = cursor.fetchall()
    secondID = result[len(result)-1]
    insertID = secondID[0]
    ID = (ID,insertID)
    retrieveEntries(choice,Column1,Column2,Column3,Column4,ID,databaseInfo)
    
def DisplayTable(choice,frameTop,search):
    '''This function retrieves the data to be displayed in the table and gets the table headers'''
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM {}".format(databaseInfo[0][choice-1]))
    tableHeader = databaseInfo[1][choice-1]
    result = cursor.fetchall()
    if choice == 5:
        cursor.execute("SELECT Merchant_ID,Merchant_Name FROM Merchants")
        tableHeader2 = ['Merchant_ID','Merchant_Name']
        result2 = cursor.fetchall()
    else:
        tableHeader2 = 0
        result2 = 0
    CreateTable(result,result2,choice,frameTop,search,tableHeader,tableHeader2)

def RecyclingBin(choice,frameTop):
    '''This function reads the items in the Deleted.csv file and then gets the table headers''' 
    result = []
    readFile=open("Deleted.csv", "r")
    for row in readFile:
        line=row.strip().split(",")
        for item in line:
            try:
                #Adds a "." to the end of any strings so the cannot be converted automaticaly to integers by the treeview widget
                line[line.index(item)] = line[line.index(item)]+"."
            except:
                print()
        if line[0] == databaseInfo[0][choice-1]+".":
            result.append(line[1:])
    readFile.close()
    tableHeader = databaseInfo[1][choice-1]
    CreateTable(result,0,choice,frameTop,0,tableHeader,0)

def csvLineSearch(values,choice):
    '''This function reads the data from the csv and then removes the row that has been restored or permanently deleted and then writes over the file but with the the row removed'''
    result = []
    readFile=open("Deleted.csv", "r")
    for row in readFile:
        line=row.strip().split(",")
        if line != ['']:
            result.append(line[1:])
    readFile.close()
    for items in values:
        listItem = list(items)
        try:
            listItem.remove(".")
        except:
            print()
        values[values.index(items)]="".join(listItem)
    for item in result:
        if result[result.index(item)] == values:
            result.remove(result[result.index(item)])
    for items in result:
        try:
            result.remove([])
        except:
            print()
        try:
            result[result.index(item)] = result[result.index(item)]+"."
        except:
            print()
    writeFile = open('Deleted.csv', 'w')
    deletedWriter = csv.writer(writeFile)
    data = [[databaseInfo[0][choice-1]]+result]
    deletedWriter.writerows(data)
    writeFile.close()
    
    
    
def CreateTable(result,result2,choice,frameTop,search,tableHeader,tableHeader2):
    '''This function creates the table and then retrieves the data from thew database to filll the table with. It also creates the buttons and labels that go around the table'''
    var = IntVar()
    frameTop.destroy()#Destroys and recreates the frame to remove the old table
    frameTop = Frame(myGui)
    frameTop.place(x=0,y=0)
    C3 = Canvas(frameTop, height=340, width=1200)
    C3.create_rectangle(5, 5, 1195, 330, fill='',width = 1,outline="grey")
    C3.pack()
    container = Frame(frameTop)
    container.place(x=25,y=85)
    if choice == 5 and result2 != 0:
        container2 = Frame(frameTop)#Creates a container for the second table on the receipts page
        container2.place(x=705,y=85)
        tree2 = ttk.Treeview(columns=tableHeader2,show="headings")#Creates a second table
        vsb2 = Scrollbar(orient="vertical", command=tree2.yview)
        tree2.configure(yscrollcommand=vsb2.set)
        tree2.grid(column=0, row=0, in_=container2)
        vsb2.grid(column=1, row=0, sticky='ns', in_=container2)
        container2.grid_columnconfigure(0, weight=1)
        container2.grid_rowconfigure(0, weight=1)
        column = 0
        while column < len(tableHeader2):
            tree2.column(tableHeader2[column],width=150)
            column = column + 1
        for col in tableHeader2:
            tree2.heading(col, text=col.title(), anchor = "w")
        for x in result2:
            tree2.insert('', 'end', values=x)#Insert the data into the second table
        for col in tableHeader2:
            #Sets the command attached to the table header
            tree2.heading(col, text=col.title(), anchor = "w",command=lambda c2=col: Tree2Sort(aList,c2,tree2,choice,tableHeader,frameTop,fullList,result,result2,tableHeader2))
    TableNameLabel = Label(myGui,text=("Table: "+databaseInfo[0][choice-1]),font=("Ariel",30))#Creates the label saying the table name
    TableNameLabel.place(x=140,y=20)
    HomeButton = Button(myGui,image=housePhoto,bd=0,state=NORMAL,command=lambda : Radiobutton1.invoke())#Creates the home button
    HomeButton.place(x=10,y=10)
    binButton = Button(myGui,image=binPhoto,bd=0,state=NORMAL,command=lambda : RecyclingBin(choice,frameTop))#Creates the recycling bin button
    binButton.place(x=1080,y=250)
    tree = ttk.Treeview(columns=tableHeader,show="headings")#Creates the table
    vsb = Scrollbar(orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.grid(column=0, row=0, in_=container)
    vsb.grid(column=1, row=0, sticky='ns', in_=container)
    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)
    column = 0
    while column < len(tableHeader):
        tree.column(tableHeader[column],width=150)
        column = column + 1
    for col in tableHeader:
        tree.heading(col, text=col.title(), anchor = "w")
    if search == True:
        value = SearchBox.get()
        SearchBox.delete (first=0, last=200)
        result = Search(choice,databaseInfo,value)
        search == False
    aList = []
    fullList = []
    for col in tableHeader:
        tree.heading(col, text=col.title(), anchor = "w",command=lambda c=col: (Sort(aList,c,tree,0,choice,tableHeader,frameTop,fullList,result2,tableHeader2))) 
    for x in result:
        #Inserts data into the table
        tree.insert('', 'end', values=x)
    if choice == 5:
        InsertButton = ttk.Button(myGui, text = "Insert Merchant_ID",width = 14,command = lambda : InsertMerchant_ID(tree2,choice,frameTop))
        InsertButton.place(x=960,y=20)
    SelectButton = ttk.Button(myGui, text = "Select Item",width = 14,command = lambda : fnSelectItem(tree,choice,frameTop,tableHeader))
    SelectButton.place(x=1080,y=20)
    SearchBox.config(state=NORMAL)
    SearchButton.config(state=NORMAL,command = lambda : DisplayTable(choice,frameTop,True))

def Tree2Sort(aList,c2,tree2,choice,tableHeader,frameTop,fullList,result,result2,tableHeader2):
    '''This function retrieves data from tree2 and then retrieves data from the database in order
       if these lists match the list is reversed as it was already in order'''
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    for child in tree2.get_children(''):
        counter = 0
        aList = []
        rowList = []
        for item in tableHeader2:
            rowList.append(tree2.set(child,counter))
            counter = counter + 1
        fullList.append(rowList)
    cursor.execute("SELECT Merchant_ID,Merchant_Name FROM Merchants ORDER BY {}".format(c2))
    result2 = cursor.fetchall()
    if result2 == fullList:
        result2 = list(reversed(result2))
    CreateTable(result,result2,choice,frameTop,False,tableHeader,tableHeader2)

def Sort(aList,col,tree,iterations,choice,tableHeader,frameTop,fullList,result2,tableHeader2):
    '''This function retrives all the data from the tree, it then sends it to the MergeSort()
       function and compares the sorted list to the original, if it is the same the list is
       reversed'''
    result = []
    fullList = []
    originalList = []
    for child in tree.get_children(''):
        counter = 0
        aList = []
        rowList = []
        for item in tableHeader:
            rowList.append(tree.set(child,counter))
            counter = counter + 1
        count = tableHeader.index(col)
        aList.append(tree.set(child,count))
        fullList.append(rowList)
        result.append(aList)
        originalList.append(aList)
    aList = result
    if databaseInfo[2][choice-1][tableHeader.index(col)] == databaseInfo[2][choice-1][0]:
        for items in result:
            aList[result.index(items)][0] = int(aList[result.index(items)][0])
    aList = MergeSort(aList)#,col,tree,0,choice,tableHeader,frameTop,fullList)
    rowCount = 0
    result = []
    same = 0
    if aList == originalList:
        aList = list(reversed(aList))
    for items in aList:
        for row in fullList:
            if row[tableHeader.index(col)] == items[0] or row[tableHeader.index(col)] == str(items[0]):
                result.append(row)
                fullList.remove(row)
    try:
        for items in result:
            aList[result.index(items)][0] = str(aList[result.index(items)][0])
    except:
        print()
    CreateTable(result,result2,choice,frameTop,False,tableHeader,tableHeader2)
        
def MergeSort(aList):
    '''This function merge sorts a list that is given to it and returns the sorted list'''
    if len(aList)>1:
        mid = len(aList)//2
        lefthalf = aList[:mid]
        righthalf = aList[mid:]

        MergeSort(lefthalf)
        MergeSort(righthalf)
          
        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                aList[k]=lefthalf[i]
                i=i+1
            else:
                aList[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            aList[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            aList[k]=righthalf[j]
            j=j+1
            k=k+1
    return  aList

def InsertData(choice,EnterDataButton,frameTop,ID):
    '''This function changes the label text to match the table column names, it also changes the command attached to the button
       It also changes the state of the entries so that data cannot be entered into boxes it should not be'''
    ColumnNames = GetColumnNames(choice,databaseInfo)
    EnterDataLabel.config(text=("Insert into: "+"\n"+databaseInfo[0][choice-1]))
    ColumnLabel1.config(text=ColumnNames[0])
    ColumnLabel2.config(text=ColumnNames[1])
    ColumnLabel3.config(text=ColumnNames[2])
    ColumnLabel4.config(text=ColumnNames[3])
    EnterDataButton.config(state=NORMAL)
    EnterDataButton.config(command=lambda : (retrieveEntries(choice,Column1,Column2,Column3,Column4,ID,databaseInfo)\
                                             ,Refresh(choice,frameTop)\
                                             ,InsertData(choice,EnterDataButton,frameTop,ID),EntryFrame.config(highlightthickness=0)),state=DISABLED)
    Column1.config(state=DISABLED)
    Column2.config(state=DISABLED)
    Column3.config(state=DISABLED)
    Column4.config(state=DISABLED)
    Radiobutton1.deselect()
    Radiobutton2.deselect()
    Radiobutton3.deselect()
    Radiobutton4.deselect()
    Radiobutton5.deselect()
    #Radiobutton6.deselect()
    EntryFrame.config(highlightthickness=0)
    if choice == 1:
        Radiobutton1.select()
        Column1.config(state=NORMAL)
        Column2.config(state=NORMAL)
        Column3.config(state=NORMAL)
        Column4.config(state=NORMAL)
        EnterDataButton.config(state=NORMAL)
    elif choice == 2:
        Radiobutton2.select()
        Column1.config(state=DISABLED)
        Column2.config(state=NORMAL)
        Column3.config(state=NORMAL)
        Column4.config(state=NORMAL)
        EnterDataButton.config(state=NORMAL)
    elif choice == 3:
        Radiobutton3.select()
        Column1.config(state=DISABLED)
        Column2.config(state=NORMAL)
        EnterDataButton.config(state=NORMAL)
    elif choice == 4:
        Radiobutton4.select()
        Column1.config(state=NORMAL)
        Column2.config(state=NORMAL)
        Column3.config(state=NORMAL)
        EnterDataButton.config(state=NORMAL)
    elif choice == 5:
        Radiobutton5.select()
        Column1.config(state=NORMAL)
        Column2.config(state=NORMAL)
        Column3.config(state=NORMAL)
        EnterDataButton.config(state=NORMAL)
        EnterDataButton.config(command=lambda : (retrieveEntries(choice,Column1,Column2,Column3,Column4,ID,databaseInfo)\
                                                 ,Refresh(choice,frameTop)\
                                                 ,InsertData(choice,EnterDataButton,frameTop,ID)\
                                                 ,ConnectJobsAndReceipts(6,ID),EntryFrame.config(highlightthickness=0)))

def CalculateTax():
    '''This function retrieves data used to calculate the tax from the database and from the TaxData csv file
       It then calculates Income tax and National Insurance using this data'''
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    #Selects all the money invoiced
    sqlCommand = "SELECT Money_Invoiced FROM Invoices"
    cursor.execute(sqlCommand)
    result = cursor.fetchall()
    TotalTurnover = 0
    for items in result:
        #Adds together all the invoices
        TotalTurnover = TotalTurnover + items[0]
    #Selects all the money spent in receipts
    sqlCommand = "SELECT Money_Spent FROM Receipts"
    cursor.execute(sqlCommand)
    result = cursor.fetchall()
    TotalExpenditure = 0
    for items in result:
        #Add together all the money spent in receipts
        TotalExpenditure = TotalExpenditure + items[0]
    NetProfit = TotalTurnover-TotalExpenditure
    data_list = []
    readFile=open("TaxData.csv", "r")
    for row in readFile:
        try:
            line=row.strip().split(",")
            data_list.append((int(line[0]),int(line[1]),int(line[2]),int(line[3])))
        except:
            print()
    readFile.close()
    BasicRateBox.delete (first=0, last=200)
    PersonalAllowanceBox.delete (first=0, last=200)
    LPLBox.delete (first=0, last=200)
    UPLBox.delete (first=0, last=200)
    BasicRateBox.insert (0, data_list[0][0])
    PersonalAllowanceBox.insert (0, data_list[0][1])
    LPLBox.insert (0, data_list[0][2])
    UPLBox.insert (0, data_list[0][3])
    TaxDue = (NetProfit-data_list[0][1])*(data_list[0][0]/100)
    if NetProfit < data_list[0][3]:
         NationalInsurance = (NetProfit-data_list[0][2])*0.09
    elif NetProfit < data_list[0][2]:
        NationalInsurance = 0
    elif NetProfit >  data_list[0][3]:
        NationalInsurance = NetProfit-(data_list[0][3]*0.02)
    #Displays the calculated values as labels and a formatted to have only two decimal places and have a pound sign
    TaxDueValue = Label(myGui,text='£{:,.2f}'.format(TaxDue),font=("Ariel",15))
    NationalInsuranceValue = Label(myGui,text='£{:,.2f}'.format(NationalInsurance),font=("Ariel",15))
    TaxDueValue.place(x=900,y=530)
    NationalInsuranceValue.place(x=900,y=570)
    RecalculateButton = Button(myGui,text="Recalculate",state=NORMAL,command=lambda : (GetTaxData(),CalculateTax()))
    RecalculateButton.place(x=900,y=610)

def GetTaxData():
    '''Retrieves the Tax Data values used to calculate the Tax Values from a csv file'''
    BasicRate = int(BasicRateBox.get())
    PersonalAllowance = int(PersonalAllowanceBox.get())
    LPL = int(LPLBox.get())
    UPL = int(UPLBox.get())
    writeFile = open('TaxData.csv', 'w')
    taxWriter = csv.writer(writeFile)
    data = [[BasicRate,PersonalAllowance,LPL,UPL]]
    taxWriter.writerows(data)
    writeFile.close()

def CloseProgram():
    '''Closes the program'''
    os._exit(0)

def ExitProgram():
    '''Displays a comfirmation message before calling the CloseProgram() function if
       the user comfirms they want to close the window'''
    comfirmExit = tkinter.messagebox.askquestion('Close Window','Exit Program?')
    if  comfirmExit == "yes":
        CloseProgram()

def programInfo():
    '''Displays information about the program'''
    tkinter.messagebox.showinfo('About','Tax Calculator')

def changePassword():
    '''This function displays the pasword entry window'''
    top = Tk()
    Correct = False
    UserNameLabel = Label(top, text="Username:")
    UserName = StringVar()
    UsernameBox = Entry(top,textvariable=UserName, width=22,bd=5)
    UserName.set('')
    PassWordLabel = Label(top, text="Password:")
    PassWord = StringVar()
    PasswordBox = Entry(top,textvariable=PassWord, width=22,bd=5)
    PassWord.set('')
    PasswordButton = Button(top,text="Login",command=lambda : UpdatePassword(UsernameBox,PasswordBox,top))
    UserNameLabel.pack()
    UsernameBox.pack()
    PassWordLabel.pack()
    PasswordBox.pack()
    PasswordButton.pack()
    top.mainloop()

def UpdatePassword(UsernameBox,PasswordBox,top):
    '''This function retrieves the values from the entries and changes the password that is stored in the database'''
    Username = UsernameBox.get()
    Password = PasswordBox.get()
    salt = uuid.uuid4().hex
    hashedPassword = hashlib.sha512((Password+salt).encode()).hexdigest()
    FinalPassword = salt+'£$%£'+hashedPassword
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM UserDetails;""")
    cursor.execute("INSERT INTO UserDetails (Username,Password) VALUES (?,?);",(Username,FinalPassword))
    connection.commit()
    top.destroy()

#Creates a window before the main window  
top = Tk()
Correct = False
UserNameLabel = Label(top, text="Username:")
UserName = StringVar()
UsernameBox = Entry(top,textvariable=UserName, width=22,bd=5)
UserName.set('')
PassWordLabel = Label(top, text="Password:")
PassWord = StringVar()
PasswordBox = Entry(top,textvariable=PassWord, width=22,bd=5,show="*")
PassWord.set('')
PasswordButton = Button(top,text="Login",command=lambda : PasswordChecker())
UserNameLabel.pack()
UsernameBox.pack()
PassWordLabel.pack()
PasswordBox.pack()
PasswordButton.pack()
top.mainloop()

if Correct == False:
    #Exits the program if the password box is closed and the password was incorrect
    os._exit(0)

#Attempts to create the tables
fnCreateTables()
#Get the information about the program 
databaseInfo = RetrieveDatabaseInfo()
#Creates the gui and sets the size and name
myGui = Tk()
myGui.title("Tax Program")
myGui.geometry("1200x700+100+100")

frameLeft = Frame(myGui)
frameLeft.place(x=0,y=350)

frameRight = Frame(myGui)
frameRight.place(x=605,y=350)

frameTop = Frame(myGui)
frameTop.place(x=0,y=0)

Canvas0 = Canvas(frameLeft, height=350, width=600)
Canvas0.create_rectangle(5, 5, 590, 345, fill='',width = 1,outline="grey")

menuVar1 = IntVar()
menuVar2 = IntVar()
menuVar3 = IntVar()

top = ""
ID = 0
search = False

Label1 = Label(myGui, text="Database")

Canvas2 = Canvas(frameRight, height=350, width=600)
Canvas2.create_rectangle(5, 5, 590, 345, fill='',width = 1,outline="grey")

Canvas3 = Canvas(frameTop, height=350, width=1200)
Canvas3.create_rectangle(5, 5, 1195, 330, fill='',width = 1,outline="grey")

ViewTable = Label(myGui, text="View Table",font=("Ariel",15))
ViewTable.place(x=15,y=390)

radioFrame = Frame(myGui)
radioFrame.place(x=15,y=420)
choice = 0
var = IntVar()
#Creates the radio button that allows the user to navigate between pages
Radiobutton1 = Radiobutton(radioFrame, text=databaseInfo[0][0], variable=var, value=1,command=lambda : (Refresh(1,frameTop)\
                                                                                     ,DisplayTable(1,frameTop,search)\
                                                                                     ,InsertData(1,EnterDataButton,frameTop,ID)))
Radiobutton1.pack(anchor= "w")
Radiobutton2 = Radiobutton(radioFrame, text=databaseInfo[0][1], variable=var, value=2,command=lambda : (Refresh(2,frameTop)\
                                                                                      ,DisplayTable(2,frameTop,search)\
                                                                                      ,InsertData(2,EnterDataButton,frameTop,ID)))
Radiobutton2.pack(anchor= "w")
Radiobutton3 = Radiobutton(radioFrame, text=databaseInfo[0][2], variable=var, value=3,command=lambda : (Refresh(3,frameTop)\
                                                                                      ,DisplayTable(3,frameTop,search)\
                                                                                      ,InsertData(3,EnterDataButton,frameTop,ID)))
Radiobutton3.pack(anchor= "w")
Radiobutton4 = Radiobutton(radioFrame, text=databaseInfo[0][3], variable=var, value=4,command=lambda : (Refresh(4,frameTop)\
                                                                                      ,DisplayTable(4,frameTop,search)\
                                                                                      ,InsertData(4,EnterDataButton,frameTop,ID)))
Radiobutton4.pack(anchor= "w")
Radiobutton5 = Radiobutton(radioFrame, text=databaseInfo[0][4], variable=var, value=5,command=lambda : (Refresh(5,frameTop)\
                                                                                      ,DisplayTable(5,frameTop,search)\
                                                                                      ,InsertData(5,EnterDataButton,frameTop,ID)))
Radiobutton5.pack(anchor= "w")
Radiobutton6 = Radiobutton(radioFrame, text=databaseInfo[0][5], variable=var, value=6,command=lambda : (Refresh(6,frameTop)\
                                                                                      ,DisplayTable(6,frameTop,search)\
                                                                                      ,InsertData(6,EnterDataButton,frameTop,ID)))
Radiobutton6.pack(anchor= "w")

EntryFrame = Frame(myGui,highlightbackground="red",highlightthickness=0)
EntryFrame.place(x=355,y=400)
SearchFrame = Frame(myGui)
SearchFrame.place(x=175,y=420)
Column1Name = StringVar()
Column1 = Entry(EntryFrame,textvariable=Column1Name, width=22,bd=5,state=DISABLED)
Column1Name.set('')
Column2Name = StringVar()
Column2 = Entry(EntryFrame,textvariable=Column2Name, width=22,bd=5,state=DISABLED)
Column2Name.set('')
Column3Name = StringVar()
Column3 = Entry(EntryFrame,textvariable=Column3Name, width=22,bd=5,state=DISABLED)
Column3Name.set('')
Column4Name = StringVar()
Column4 = Entry(EntryFrame,textvariable=Column4Name, width=22,bd=5,state=DISABLED)
Column4Name.set('')
SearchVar = StringVar()
SearchBox = Entry(SearchFrame,textvariable=SearchVar, width=22,bd=5,state=DISABLED)
SearchVar.set('')
SearchButton = Button(SearchFrame,text="Search",state=DISABLED,command=lambda : Search(choice,databaseInfo))
SearchLabel = Label(SearchFrame,text="Search")
EnterDataButton = Button(EntryFrame,text="Enter Data",state=DISABLED,command=lambda : retrieveEntries(choice,Column1,Column2,Column3,Column4,ID))
EnterDataLabel = Label(EntryFrame,font=("Ariel",15))
ColumnLabel1 = Label(EntryFrame)
ColumnLabel2 = Label(EntryFrame)
ColumnLabel3 = Label(EntryFrame)
ColumnLabel4 = Label(EntryFrame)
BasicRateLabel = Label(myGui,text="Basic Rate (%)",font=("Ariel",10))
BasicRateVar = StringVar()
BasicRateBox = Entry(myGui,textvariable=BasicRateVar, width=22,bd=5,state=NORMAL)
BasicRateVar.set('')
BasicRateLabel.place(x=620,y=370)
BasicRateBox.place(x=900,y=370)
PersonalAllowanceLabel = Label(myGui,text="Personal Allowance",font=("Ariel",10))
PersonalAllowanceVar = StringVar()
PersonalAllowanceBox = Entry(myGui,textvariable=PersonalAllowanceVar, width=22,bd=5,state=NORMAL)
PersonalAllowanceVar.set('')
PersonalAllowanceLabel.place(x=620,y=410)
PersonalAllowanceBox.place(x=900,y=410)
LPLLabel = Label(myGui,text="Lower Profit Limit",font=("Ariel",10))
LPLVar = StringVar()
LPLBox = Entry(myGui,textvariable=LPLVar, width=22,bd=5,state=NORMAL)
LPLVar.set('')
LPLLabel.place(x=620,y=450)
LPLBox.place(x=900,y=450)
UPLLabel = Label(myGui,text="Upper Profit Limit",font=("Ariel",10))
UPLVar = StringVar()
UPLBox = Entry(myGui,textvariable=UPLVar, width=22,bd=5,state=NORMAL)
UPLVar.set('')
UPLLabel.place(x=620,y=490)
UPLBox.place(x=900,y=490)
TaxDueLabel = Label(myGui,text="Tax Due: ",font=("Ariel",15))
TaxDueLabel.place(x=620,y=530)
NationalInsuranceLabel = Label(myGui,text="National Insurance Due: ",font=("Ariel",15))
NationalInsuranceLabel.place(x=620,y=570)
EnterDataLabel.pack(side=TOP)
ColumnLabel1.pack(side=TOP)
Column1.pack(side=TOP)
ColumnLabel2.pack(side=TOP)
Column2.pack(side=TOP)
ColumnLabel3.pack(side=TOP)
Column3.pack(side=TOP)
ColumnLabel4.pack(side=TOP)
Column4.pack(side=TOP)
EnterDataButton.pack(side=TOP)
SearchLabel.pack(side=TOP)
SearchBox.pack(side=TOP)
SearchButton.pack(side=TOP)
SearchLabel.pack(side=TOP)
#Creates Images that can be used for buttons
housePhoto=PhotoImage(file="house-xxl.gif")
binPhoto=PhotoImage(file="recycle-bin_318-35857.gif")
#Creates the menu bar
menuBar = Menu(myGui)
fileMenu = Menu(menuBar,tearoff=0)
settingsMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Change Password", command=changePassword)
fileMenu.add_command(label="Close", command=ExitProgram)
fileMenu.add_separator()
fileMenu.add_command(label="About", command=programInfo)
myGui.config(menu=menuBar)
Canvas0.pack()
Canvas2.pack()
Canvas3.pack()
CalculateTax()
Label1.place(x=20,y=345)
Radiobutton1.invoke()
#Makes the GUI not resizable
myGui.resizable(0,0)
#Changes the close button command to ExitProgram
myGui.protocol("WM_DELETE_WINDOW", ExitProgram)
myGui.mainloop()
