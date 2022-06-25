import sqlite3

def fnCreateTables():
    '''This function tries to create the database so that if the database was not transfered with the program it will not break'''
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    try:
        sqlCommand = """
        CREATE TABLE "Clients" (
	`Client_ID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Client_First_Name`	TEXT,
	`Client_Last_Name`	TEXT,
	`Client_Address`	TEXT,
	`Client_Telephone_Number`	TEXT,
        )"""
        cursor.execute(sqlCommand)
    except:
        print("Could not create table")

    try:
        sqlCommand = """
        CREATE TABLE "Invoices" (
	`Invoice_No`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Job_ID`	INTEGER,
	`Money_Invoiced`	INTEGER,
	`Date_Invoiced`	TEXT,
	`Date_Paid`	TEXT,
        )"""
        cursor.execute(sqlCommand)
    except:
        print("Could not create table")

    try:
        sqlCommand = """
        CREATE TABLE "Jobs" (
	`Job_ID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Client_ID`	INTEGER,
	`Job_Description`	TEXT,
        )"""
        cursor.execute(sqlCommand)
    except:
        print("Could not create table")

    try:
        sqlCommand = """
        CREATE TABLE "Merchants" (
	`Merchant_ID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Merchant_Name`	TEXT,
	`Merchant_Address`	TEXT,
	`Merchant_Telephone`	TEXT,
        )"""
        cursor.execute(sqlCommand)
    except:
        print("Could not create table")

    try:
        sqlCommand = """
        CREATE TABLE "Reciepts" (
	`Reciept_No`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Money_Spent`	INTEGER,
	`Merchant_ID`	INTEGER,
	`Reciept_Date`	TEXT,
        )"""
        cursor.execute(sqlCommand)
    except:
        print("Could not create table")

    try:
        connection = sqlite3.connect("Database.db")
        cursor = connection.cursor()
        sqlCommand = """
        CREATE TABLE "Reciepts_For_Job" (
	`Job_ID`	INTEGER,
	`Reciept_No`	INTEGER,
        )"""
        cursor.execute(sqlCommand)
    except:
        print("Could not create table")

    try:
        connection = sqlite3.connect("Database.db")
        cursor = connection.cursor()
        sqlCommand = """
        CREATE TABLE "UserDetails" (
	`Username`	TEXT PRIMARY KEY,
	`Password`	TEXT,
        )"""
        cursor.execute(sqlCommand)
    except:
        print("Could not create table")
    connection.close()
