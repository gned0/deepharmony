# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup 
import time
from urllib.request import Request, urlopen
import random
import csv

# LEGEND FOR CLASSES NAMING
# 1.gif = Warrior
# 2.gif = Paladin
# 3.gif = Hunter
# 4.gif = Rogue
# 5.gif = Priest
# 6.gif = Death Knight
# 7.gif = Shaman
# 8.gif = Mage
# 9.gif = Warlock
# 11.gif = Druid
classes = ["Warrior", "Paladin", "Hunter", "Rogue", "Priest", "Death Knight", "Shaman", "Mage", "Warlock", "", "Druid"]  


# LEGEND FOR RACES NAMING
# <Num>-<Num> -> Second Num is for sex
# 1-*.gif = Human
# 2-*.gif = Orc
# 3-*.gif = Dwarf
# 4-*.gif = Night Elf
# 5-*.gif = Undead
# 6-*.gif = Tauren
# 7-*.gif = Gnome
# 8-*.gif = Troll
# 10-*.gif = Blood Elf
# 11-*.gif = Draenei
races = ["Human", "Orc", "Dwarf", "Night Elf", "Undead", "Tauren", "Gnome", "Troll", "", "Blood Elf", "Draenei"]
horde_faction = [1, 4, 5, 7, 9]  

specific_row = ['numBG', 'levelBracket', 'nameBG', 'factionWinner', 'dateBG', 'timeFinished']
specific_row2 = ['numBG', 'charName', 'charClass', 'charRace', 'charFaction', 'KB', 'D', 'HK', 'BH', 'DD', 'HD', 'FC', 'FR']
# Opening the html file. If the file 
# is present in different location,  
# exact location need to be mentioned 
# HTMLFileToBeOpened = open(r"C:\Users\kryas\Desktop\html\ChromieCraft PvPstats.html", "r", encoding="utf-8") 

numBG = "72199"

for doc in range(int(numBG), 72250, 1):
    
    print("Establishing connection with doc num: " + str(doc))

    req = Request(
        url='https://chromiecraft.com/apps/pvpstats/battleground.php?id=' + str(doc), 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    )
    
    with urlopen(req) as webPageResponse: 
        contents = webPageResponse.read() 
        
    webPageResponse.close()  
    
    print("Connection established and HTML copied")
    
    # Reading the file and storing in a variable 
    # contents = HTMLFileToBeOpened.read() 
      
    # Creating a BeautifulSoup object and 
    # specifying the parser  
    beautifulSoupText = BeautifulSoup(contents, 'lxml') 
      
    # print(beautifulSoupText)
      
    # Using the prettify method to modify the code 
    #  Prettify() function in BeautifulSoup helps 
    # to view about the tag nature and their nesting 
    # print(beautifulSoupText.body.prettify()) 
    
    
    from csv import writer
    
    # General BG data for BGs.csv
    
    # numBG = beautifulSoupText.find_all("tr", {"style": "color: #1a67f4; font-weight: bold;"})[0].find_all("td")[0].text
    print(str(doc))
    
    levelBracket = beautifulSoupText.find_all("p", {"class": "lead text-left"})[0].find_all("span")[0].text
    print(levelBracket)
    
    nameBG = beautifulSoupText.find_all("p", {"class": "lead text-left"})[0].find_all("span")[1].text
    print(nameBG)
    
    winnerCheck = beautifulSoupText.find_all("p", {"class": "lead text-center"})[0].find_all("span")
    if(winnerCheck):
        winner = winnerCheck[0].text.split()[0]
    else:
        winner = beautifulSoupText.find_all("p", {"class": "lead text-center"})[0].text
    print(winner)
    
    date = beautifulSoupText.find_all("p", {"class": "lead text-right"})[0].text.split()[0]
    print(date)
    
    timeBG = beautifulSoupText.find_all("p", {"class": "lead text-right"})[0].text.split()[1]
    print(timeBG) 
    print("\n")
    
    bgData = [str(doc), levelBracket, nameBG, winner, date, timeBG]
     
    
    
    
    
    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open(r"C:\Users\kryas\Desktop\html\BGs.csv", 'r', newline='') as f_object:
        reader = csv.reader(f_object)
        rows = list(reader)
    
    try:
        index = rows.index(specific_row)
    except ValueError:
        print("Specific row not found.")
        exit(0)
        
    rows.insert(index + 1, bgData)

    # Write the modified data back to the CSV file
    with open("C:/Users/kryas/Desktop/html/BGs.csv", 'w', newline='', encoding='utf-7') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    
    
    tmp = beautifulSoupText.find_all("table", {"id": "bg-table"})[0].find_all("tbody")[0].find_all("tr")
    
    
    # General BG data for playersBG.csv
    
    print("Num of players is: " + str(len(tmp)))
    
    bgCharData = []
    
    for char in tmp:
        
        # Char Name
        charName = char.strong.text
        # print(charName)
        
        # Char Class
        charClass = classes[int(char.find_all("img")[0]["src"].split("/")[2].split(".")[0]) - 1]
        # print(charClass)
        
        # Char Race
        charRace = races[int(char.find_all("img")[1]["src"].split("/")[2].split(".")[0].split("-")[0]) - 1]
        # print(charRace)
        
        # Char Faction
        if(int(char.find_all("img")[1]["src"].split("/")[2].split(".")[0].split("-")[0]) - 1 in horde_faction):
            charFaction = "Horde"
            # print("Horde")
        else:
            charFaction = "Alliance"
            # print("Alliance")
        
        # Killing Blows
        charKB = char.find_all("td")[2].text
        # print(charKB)
        
        # Deaths
        charDeaths = char.find_all("td")[3].text
        # print(charDeaths)
        
        # Honorable Kills
        charHK = char.find_all("td")[4].text
        # print(charHK)
        
        # Bonus Honor
        charBH = char.find_all("td")[5].text
        # print(charBH)
        
        # Damage Done
        charDD = char.find_all("td")[6].text
        # print(charDD)
        
        # Healing Done
        charHD = char.find_all("td")[7].text
        # print(charHD)
        
        # Flags Captured
        charFC = char.find_all("td")[8].text
        # print(charFC)
        
        # Flags Returned
        if(nameBG == "Eye of the Storm"):
            charFR = "-1"    
        else:
            charFR = char.find_all("td")[9].text
        # print(charFR)
        # print("\n")
    
        charData = [str(doc), charName, charClass, charRace, charFaction, charKB, 
                    charDeaths, charHK, charBH, charDD, charHD, charFC, charFR
                    ]
        bgCharData.append(charData)
        
        
        
    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open(r"C:\Users\kryas\Desktop\html\playersBG.csv", 'r', newline='') as f_object:
        reader = csv.reader(f_object)
        rows = list(reader)
    
    try:
        index = rows.index(specific_row2)
    except ValueError:
        print("Specific row not found.")
        exit(0)
        
    for rowChar in bgCharData:
        rows.insert(index + 1, rowChar)

    # Write the modified data back to the CSV file
    with open("C:/Users/kryas/Desktop/html/playersBG.csv", 'w', newline='', encoding='utf-7') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    # HTMLFileToBeOpened.close()
    
    print("Done extrapolating BG num " + str(doc))
    print("\n")
    
    # Old Timer between 16 and 24 seconds
    # sleepTime = random.randrange(16, 24)
    
    # New Timer between 3 and 5 seconds
    # sleepTime = random.randrange(3, 5)
    sleepTime = 2
    
    print("Sleeping")
    time.sleep(sleepTime)
    print("Done Sleeping for " + str(sleepTime))
    print("\n")
    # print("\n")
