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
        try:
            jsonReq = requests.get('https://www.scorebat.com/video-api/v3/',timeout=15).json()
        except:
            return 0

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
        for league in otherLeagues:
            if(j<4):
                temp = [InlineKeyboardButton(league, callback_data=league + "-Leag:Menu:"+str(i))]
                keyboard.append(temp)
                j+=1

            else:
                temp = [InlineKeyboardButton(league, callback_data=league + "-Leag:Menu:"+ str(i))]
                keyboard.append(temp)
                i+=1
                if(i==1):
                    keyboard.append([InlineKeyboardButton("🏠", callback_data="Home" ),InlineKeyboardButton("➡", callback_data="Men:" + str(i))])
                if(len(otherLeagues)%5==0 and i==len(otherLeagues)/5):
                    keyboard.append([InlineKeyboardButton("⬅", callback_data="Men:" + str(i - 2)),InlineKeyboardButton("🏠", callback_data="Home")])
                else:
                    if (i>1):
                        keyboard.append([InlineKeyboardButton("⬅", callback_data="Men:" +str(i-2)),InlineKeyboardButton("➡", callback_data="Men:" +str(i))])
                        keyboard.append([InlineKeyboardButton("🏠", callback_data="Home" )])
                tempKeyBoard.append(keyboard)
                keyboard=[]
                j=0

        if(j!=0):
            keyboard.append([InlineKeyboardButton("⬅", callback_data="Men:" + str(i - 1)),InlineKeyboardButton("🏠", callback_data="Home")])
            tempKeyBoard.append(keyboard)
        return tempKeyBoard

    def relevantKeyBoard(self,i):
        return self.otherKeyBoard[i]


