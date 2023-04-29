import csv
import sqlite3

try:
    # Connecting to the batch_list database
    connection = sqlite3.connect('batch_list.db')

    # Creating a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Table Definition
    create_table = '''CREATE TABLE IF NOT EXISTS batchlist(
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

    # Creating the table into our database
    cursor.execute(create_table)

    # Opening the sample_batch_list.csv file
    file = open('docs/sample_batch_list.csv', 'r')

    # Reading the contents of the sample_batch_list.csv file
    contents = csv.reader(file)

    # Skip header row
    next(contents)

    # Importing the contents of the file into the batchlist table
    for row in contents:
        cursor.execute("INSERT INTO batchlist (PRN, SRN, Semester, Section, Cycle, DeptCampus, Stream, Campus, Name) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

    # SQL query to retrieve all data from the batchlist table to verify that the data of the csv file has been successfully inserted into the table
    select_all = "SELECT * FROM batchlist"
    cursor.execute(select_all)

    # Output to the console screen
    rows = cursor.fetchall()
    for r in rows:
        print(r)

    # Committing the changes
    connection.commit()

except Exception as e:
    print("Error: ", e)

finally:
    # closing the database connection
    if (connection):
        connection.close()
