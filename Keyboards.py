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
        for league in otherLeagues:
            if(j<5):
                temp = [InlineKeyboardButton(league, callback_data=league + "-Leag")]
                keyboard.append(temp)
                j+=1
            else:
                i+=1
                if(i==1):
                    keyboard.append([InlineKeyboardButton("Next ->", callback_data="Men:" + str(i))])
                if(i+1> len(otherLeagues)/5):
                    keyboard.append([InlineKeyboardButton("<- Prev", callback_data="Men:" +str(i-2))])
                if(len(otherLeagues)%5==0 and i+1==len(otherLeagues)/5):
                    keyboard.append([InlineKeyboardButton("<- Prev", callback_data="Men:" + str(i - 2))])
                else:
                    if (i>1):
                        keyboard.append([InlineKeyboardButton("<- Prev", callback_data="Men:" +str(i-2)),InlineKeyboardButton("Next ->", callback_data="Men:" +str(i))])
                        #keyboard.append([InlineKeyboardButton("Next ->", callback_data="Men:" +str(i))])
                tempKeyBoard.append(keyboard)
                keyboard=[]
                j=0

        return tempKeyBoard
    def relevantKeyBoard(self,i):
        return self.otherKeyBoard[i]


keyboard=Keyboards()
#print(len(keyboard.relevantKeyBoard(3)))