import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import random
import time
import sys
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import csv
 
# setting path
sys.path.append('../parentdirectory')

import scraper

pesuID = 931592628640813177
botID = 931592628640813177
confessChannel = 1032709445534359627
GUILD_ID = 1032709443860832426
MOD_LOGS = 1032709445324652604

class scraper_cog(commands.Cog):

    def __init__(self, client):
         self.client = client

    #Get the cards codes from the lsit of cards that Karuta has sent
    @cog_ext.cog_slash(
        name="scrape",
        description="Scrapes data from PESU academy",
        guild_ids=[GUILD_ID],
        options=[
            create_option(
                name="c",
                description="The campus",
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                        name="EC",
                        value="ec"
                    ),
                    create_choice(
                        name="RR",
                        value="rr"
                    )
                ]
            ),
            create_option(
                name="yr",
                description="Year of joining",
                option_type=3,
                required=True
            )
        ]
    )

    async def scrape(self, ctx, c, yr):
        await ctx.reply("Running scraper")
        if (c == "ec"):
            st = "PES2"
        else:
            st = "PES1"

        #print("Running")
        opts = Options()
        opts.headless = True
        browser = Firefox(options=opts)
        #print("Browser running")
        fName = "batch_of_" + yr + ".csv"
        f = open(fName, "a")
        f1 = open("errors.txt", "a")
        #print("Files created")
        for i in range(1, 4000):
            if (i >= 1 and i <= 9):
                s = "000" + str(i)
            elif (i >= 10 and i <= 99):
                s = "00" + str(i)
            elif (i >= 100 and i <= 999):
                s = "0" + str(i)
            else:
                s = str(i)
            browser.get('https://pesuacademy.com')
            sleep(2)
            browser.find_element(By.ID, "knowClsSection").click()
            inp = browser.find_element(By.ID, "knowClsSectionModalLoginId")
            inputPRN = st + yr + "0" + s
            inp.send_keys(inputPRN)
            try:
                browser.find_element(By.ID, "knowClsSectionModalSearch").click()
                sleep(1)
                semValue = browser.find_element(By.XPATH, "//*[@id='knowClsSectionModalTableDate']/tr/td[4]").text
                if("CIE" in semValue):
                    semValue = browser.find_element(By.XPATH, "//*[@id='knowClsSectionModalTableDate']/tr[2]/td[4]").text
                prn = browser.find_element(By.XPATH, "//*[@id='knowClsSectionModalTableDate']/tr/td[1]").text
                srn = browser.find_element(By.XPATH, "//*[@id='knowClsSectionModalTableDate']/tr/td[2]").text
                semValue = browser.find_element(By.XPATH, "//*[@id='knowClsSectionModalTableDate']/tr/td[4]").text
                section = browser.find_element(By.XPATH, "//*[@id='knowClsSectionModalTableDate']/tr/td[5]").text
                cycle = browser.find_element(By.XPATH, "//*[@id='knowClsSectionModalTableDate']/tr/td[6]").text
                strCamp = browser.find_element(By.XPATH, "//*[@id='knowClsSectionModalTableDate']/tr/td[7]").text
                stream = browser.find_element(By.XPATH, "//*[@id='knowClsSectionModalTableDate']/tr/td[8]").text
                campus = browser.find_element(By.XPATH, "//*[@id='knowClsSectionModalTableDate']/tr/td[9]").text
                name = browser.find_element(By.XPATH, "//*[@id='knowClsSectionModalTableDate']/tr/td[3]").text
                strRow = prn + "," + srn + "," + semValue + "," + section + "," + cycle + "," + strCamp + "," + stream + "," + campus + "," + name
                print("Got for", prn)
                f.write(strRow + "\n")
            except:
                f1.write(inputPRN+"\n")
                print(inputPRN, "error")
        f.close()
        f1.close()
        #print("File closed")
        browser.close()
        #print("Browser closed")


def setup(client):
    client.add_cog(scraper_cog(client))
