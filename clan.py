import requests as req
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = {'https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'}

credentials = ServiceAccountCredentials.from_json_keyfile_name('Clash-da94d4b00c6d.json', scope)

spreadsheet = gspread.authorize(credentials)

school = spreadsheet.open('School').sheet1

school.clear()

class player:


    def __init__(self, aName, aTag, xp, trophies, donations, rank):
        self.name = aName
        self.gTag = aTag
        self.newStatus = False
        self.xp = xp
        self.trophies = trophies
        self.donations = donations
        self.rank = rank



#base csv file for comparing
infile = "clan-9QGPV2GJ-2018-08-08-00-08-39.csv"

#open base file for reading
file = open(infile, "r")


#going to make a clone of the original without the special characters
clone = open('originalClone.csv', 'w')

file.readline()
for line in file:
    en = line.encode('ascii', 'replace')
    clone.write(en.decode())

clone.close()
file.close()

#this will grab the clan csv file
r = req.get("https://royaleapi.com/clan/9QGPV2GJ/csv")

dailyCSV = open("daily.csv", "w")

#converts request into string for manipulating
plainText = str(r.text)

#this helps when creating the spreadsheet, deletes extra spaces
fintext = plainText.replace("\r", "")

#replaces special characters with ?
newtext = fintext.encode('ascii', 'replace')

#creating the spreadsheet for comparing
try:
    for i in newtext.decode():
        dailyCSV.write(str(i))

except UnicodeEncodeError:
    print("player values suck")


#will use to populate the dictionaries in player object
statList = ["XP", "Trophies", "Rank", "Donations"]

dailyCSV.close()

#empty lists to add player objects
orList = []
curList = []

#open created files for reading
original = open('originalClone.csv', 'r')
current = open('daily.csv', 'r')

#Final output file
finalOut = open('clanStats.csv', 'w')
finalOut.write('Name, Tag, XP, Trophies, Donations, Rank\n')

school.append_row(['Name', 'Tag', 'XP', 'Trophies +/-', 'Donations', 'Rank'])


for line in original:
    new = line.split(',')
    orList.append(player(new[1], new[0], new[3], new[4] ,new[9] ,new[7]))
original.close()

current.readline()
for line in current:
    new = line.split(',')
    curList.append(player(new[1], new[0], new[3], new[4], new[9], new[7]))
current.close()


tagList = []

for i in orList:
    tagList.append(i.gTag)

for players in curList:
    if tagList.__contains__(players.gTag):
        for each in orList:
            if players.gTag == each.gTag:
                  school.append_row([players.name, players.gTag, players.xp, str(int(players.trophies)- int(each.trophies)),
                                     str(int(players.donations) - int(each.donations)), players.rank])
                  finalOut.write(players.name + ',')
                  finalOut.write(players.gTag + ',')
                  finalOut.write(players.xp + ',')
                  finalOut.write(str(int(players.trophies)- int(each.trophies)) + ',')
                  finalOut.write(str(int(players.donations) - int(each.donations)) + ',')
                  finalOut.write(players.rank)
                  finalOut.write('\n')
    else:
        players.newStatus = True
        school.append_row([players.name, players.gTag, players.xp, str(int(players.trophies)- int(each.trophies)),
                                     str(int(players.donations) - int(each.donations)), players.rank, 'new member'])
        finalOut.write(players.name + ',')
        finalOut.write(players.gTag + ',')
        finalOut.write(players.xp + ',')
        finalOut.write(players.trophies + ',')
        finalOut.write(players.donations + ',')
        finalOut.write(players.rank)
        finalOut.write('\n')

finalOut.close()