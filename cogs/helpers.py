import discord
from discord.ext import commands
import sqlite3 #required to work with sqlite database for registering server members


class helpers(commands.Cog):
    def __init__(self, client):
        self.client = client

    def getuser(self, RegNo=""):
        if(RegNo == ""):
            return['error']
        f = open('cogs/verified.csv', 'r')
        srn_list = [line.split(',')[3] for line in list(filter(None, f.read().split('\n')))]
        if(RegNo in srn_list):
            f.close()
            return ['Done']
        f.close()
        file = None
        if ('PES12018' in RegNo or 'PES22018' in RegNo):
            file = open('cogs/batch_list_2018.csv', 'r')
        elif ('PES1UG19' in RegNo or 'PES2UG19' in RegNo):
            file = open('cogs/batch_list_2019.csv', 'r')
        elif ('PES1UG20' in RegNo or 'PES2UG20' in RegNo):
            file = open('cogs/batch_list_2020.csv', 'r')
        elif ('PES1UG21' in RegNo or 'PES2UG21' in RegNo):
            file = open('cogs/batch_list_2021.csv', 'r')
        elif ('PES1UG22' in RegNo or 'PES2UG22' in RegNo):
            file = open('cogs/batch_list_2022.csv', 'r')
        else:
            file = None

        if file == None:
            return ['No match']
        for lin in file:
            if(RegNo in lin):
                f.close()
                return lin.split(',')
        file.close()
        return ['Error']
    """   
        con = sqlite3.connect("verified.db") #assuming name of database
        #creating connection object to a db file
        cur = con.cursor() #creating cursor to execute queries
        query = "SELECT SRN FROM verified WHERE SRN = {RegNo}"
        if(RegNo!=""):
            res = cur.execute(query.format(RegNo = RegNo)) #executes queries
        else:
            return['error']
        if res!='NULL':
            con.close() #closes connection object if no matching entry is found
            return['Done']
        con.close()
        con2 = None
        #assuming db names
        if ('PES12018' in RegNo or 'PES22018' in RegNo):
            con2 = sqlite3.connect('batch_list_2018.db')
        elif ('PES1UG19' in RegNo or 'PES2UG19' in RegNo):
            con2 = sqlite3.connect('batch_list_2019.db')
        elif ('PES1UG20' in RegNo or 'PES2UG20' in RegNo):
            con2 = sqlite3.connect('batch_list_2020.db')
        elif ('PES1UG21' in RegNo or 'PES2UG21' in RegNo):
            con2 = sqlite3.connect('batch_list_2021.db')
        elif ('PES1UG22' in RegNo or 'PES2UG22' in RegNo):
            con2 = sqlite3.connect('batch_list_2022.db')

        if con2 == None:
            return ['no match']
        else:
            cur = con.cursor()
            #assuming table name
            res = cur.execute("SELECT * FROM list WHERE SRN = {RegNo}".format(RegNo = RegNo))
            if(res!='NULL'):
                con2.close()
                return res.split(',') #splits the results around commas
        
        con2.close()
        return ['error']
    """


    def getDeverified(self, regNo = ""):
        dat = ""
        ret = False
        file1 = open('cogs/verified.csv', 'r')

        for line in file1:
            if(regNo not in line.split(',')): #CSV files are comma separated and so it is necessary to split them by commas to make the data usable and easy to manipulate
                dat += line
            else:
                ret = True

        file1.close() #closes the file object
        file1 = open('cogs/verified.csv', 'w')
        file1.write(dat)
        file1.close()

        return ret


    def getVerified(self, a = ""):
        if(a == ""):
            return ['unverified']
        file = open('cogs/verified.csv', 'r')

        for line in file:
            line = line.split(',')
            if(len(line) > 5):
                if(a == line[1]):
                    file.close()
                    return line
        file.close()
        return ['unverified']


def setup(client):
    client.add_cog(helpers(client))
