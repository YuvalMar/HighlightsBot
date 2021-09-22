import requests
from telegram import InlineKeyboardButton


class Keyboards:
    otherKeyBoard=[]

    def __init__(self):
        otherLeagues=self.getLeagues()
        self.otherKeyBoard=self.generateOtherBoard(otherLeagues)

    def getOtherManu(self):
        return self.otherKeyBoard

    def getLeagues(self):
        jsonReq = requests.get('https://www.scorebat.com/video-api/v3/').json()
        otherLeagues = set()
        leagues = ["ITALY: Serie A", "FRANCE: Ligue 1", "ENGLAND: Premier League", "SPAIN: La Liga",
                   "GERMANY: Bundesliga"]
        for temp in jsonReq['response']:
            if "CHAMPIONS LEAGUE" not in temp['competition'] and temp['competition'] not in leagues:
                otherLeagues.add(temp['competition'].strip())
        return otherLeagues
    def generateOtherBoard(self,otherLeagues):
        tempKeyBoard=[]
        keyboard=[]
        j=0
        i=0
        list=[]
        totallist=[]
        leagueslist=[]
        for league in otherLeagues:
            leagueslist.append(league)
            if(j<4):
                temp = [InlineKeyboardButton(league, callback_data=league + "-Leag")]
                list.append(league)
                keyboard.append(temp)
                j+=1

            else:
                temp = [InlineKeyboardButton(league, callback_data=league + "-Leag")]
                keyboard.append(temp)
                i+=1
                totallist.append(list)
                list=[]
                if(i==1):
                    keyboard.append([InlineKeyboardButton("➡", callback_data="Men:" + str(i))])
                if(len(otherLeagues)%5==0 and i==len(otherLeagues)/5):
                    keyboard.append([InlineKeyboardButton("⬅", callback_data="Men:" + str(i - 2))])
                else:
                    if (i>1):
                        keyboard.append([InlineKeyboardButton("⬅", callback_data="Men:" +str(i-2)),InlineKeyboardButton("➡", callback_data="Men:" +str(i))])
                keyboard.append([InlineKeyboardButton("🏠", callback_data="Home" )])
                tempKeyBoard.append(keyboard)
                keyboard=[]
                j=0

        if(j!=0):
            totallist.append(list)
            keyboard.append([InlineKeyboardButton("⬅", callback_data="Men:" + str(i - 1))])
            tempKeyBoard.append(keyboard)

        return tempKeyBoard
    def relevantKeyBoard(self,i):
        return self.otherKeyBoard[i]


keyboard=Keyboards()
