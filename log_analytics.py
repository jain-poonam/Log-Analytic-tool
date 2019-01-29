import os,re
import codecs
import sys
from docutils.parsers.rst.directives import encoding
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.rcsetup as rcsetup

print(matplotlib.matplotlib_fname())

"To create connection with db"
def create_connection():
    conn = sqlite3.connect('test.db')
    ##TO Reset The Table for every Run
    conn.execute("DROP TABLE DATALOG")
    print("Opened database successfully")
    return conn

"To create table"    
def create_table(conn):
    conn.execute('''CREATE TABLE DATALOG
         (ID INT PRIMARY KEY     NOT NULL,
         DATE           TEXT    NOT NULL,
         TIME           TEXT     NOT NULL,
         PRIORITY        CHAR(1),
         TAG         TEXT);''')
    print("Table created successfully")

def get_items(conn):
    cursor = conn.execute("SELECT ID,DATE,TIME,PRIORITY,TAG from DATALOG")
    for row in cursor:
        print("==========Printing a New Row=========")
        print("ID = ", row[0])
        print("DATE = ", row[1])
        print ("TIME = ", row[2])
        print ("PRIORITY = ", row[3])
        print ("TAG = ", row[4]), "\n"
    
"To extract data from the logcat text file"  
def logdata_extraction(): 
    ##List to return Extracted data
    resultedData=[]
    with open("/Users/pyjain/logcat.txt",encoding="utf") as f:
        count = 0;
        for lines in f:  
            myArray = []
            myArray = lines.split(" ")
            if(myArray.__len__() > 8):
                extractedData=[]
                count +=1
                extractedData.append(count)
                extractedData.append(myArray[0])
                extractedData.append(myArray[1])
                extractedData.append(myArray[6])
                extractedData.append(myArray[7])
                resultedData.append(extractedData)
    return resultedData

"To load data  into the table created"
def load_data(dataToBeLoaded,conn):
    count = 0;
    c=conn.cursor()
    if dataToBeLoaded.__len__() > 0:
        for data in dataToBeLoaded:
            c.execute('insert into DATALOG values (?,?,?,?,?)',data)
    c.close()

"To create bar graph using database values"
def create_graph(conn):
    c = conn.cursor()
    c.execute('SELECT PRIORITY FROM DATALOG')
    data = c.fetchall()
    values = dict()
    counts = []
    objects = ('I', 'V', 'W', 'D', 'E')
    y_pos = np.arange(len(objects))
    
    for row in data:
        if row in values:
            values[row] += 1
        else:
            values[row] = 1
            
    print(values)
    
    for key, value in values.items():
        counts.append(value)
    print(counts)
    plt.bar(y_pos, counts, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('COUNT')
    plt.title('TAGS USED')
    plt.savefig("/Users/pyjain/graph.png")
              
    
##Resulted List with All Data
myList = logdata_extraction()
print(myList.__len__())
conn = create_connection()
create_table(conn)
load_data(myList,conn)
# get_items(conn)
create_graph(conn)
conn.close()
        

