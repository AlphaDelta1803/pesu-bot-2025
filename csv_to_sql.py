# Import required modules
import csv
import sqlite3
try:
    # Connecting to the geeks database
    connection = sqlite3.connect('batch_list.db')

    # Creating a cursor object to execute
    # SQL queries on a database table
    cursor = connection.cursor()

    # Table Definition
    create_table = '''CREATE TABLE batchlist(
                    PRN VARCHAR(13) NOT NULL,
                    SRN VARCHAR(13) NOT NULL,
                    Semester VARCHAR(5) NOT NULL,
                    Section VARCHAR(9) NOT NULL,
                    Cycle VARCHAR(20) NOT NULL,
                    DeptCampus VARCHAR(20) NOT NULL,
                    Stream VARCHAR(5) NOT NULL,
                    Campus VARCHAR(25) NOT NULL,
                    Name VARCHAR(20) NOT NULL);
                    '''

    # Creating the table into our
    # database
    cursor.execute(create_table)

    # Opening the person-records.csv file
    file = open('docs/sample_batch_list.csv')

    # Reading the contents of the
    # person-records.csv file
    contents = csv.reader(file)

    # SQL query to insert data into the
    # person table
    insert_records = "INSERT INTO batchlist (PRN, SRN, Semester, Section, Cycle, DeptCampus, Stream, Campus, Name) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"

    # Importing the contents of the file
    # into our person table
    cursor.executemany(insert_records, contents)

    # SQL query to retrieve all data from
    # the person table To verify that the
    # data of the csv file has been successfully
    # inserted into the table
    select_all = "SELECT * FROM batchlist"
    rows = cursor.execute(select_all).fetchall()

    # Output to the console screen
    for r in rows:
        print(r)

    # Committing the changes
    connection.commit()

    # closing the database connection
    connection.close()
except:
    print("Table already exists")