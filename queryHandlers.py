import requests
from telegram import InlineKeyboardButton


def leagueHandler(data):
    jsonRes = requests.get('https://www.scorebat.com/video-api/v3/').json()
    teamsSet = set()
    league =data.split("-", 1)[0]
    if (league != "CHAMPIONS LEAGUE"):
        for attribute in jsonRes['response']:
            if league == attribute['competition']:
                teamsSet.add(attribute['title'].strip())

    else:
        for attribute in jsonRes['response']:
            if league in attribute['competition']:
                teamsSet.add(attribute['title'].strip())
    keyboard = []
    for team in teamsSet:
        temp = [InlineKeyboardButton(team, callback_data=team + ":Team")]
        keyboard.append(temp)

    if(":Menu" in data):
        keyboard.append([InlineKeyboardButton("⬅", callback_data="Men:" + data.split("Menu:",1)[1]),InlineKeyboardButton("🏠", callback_data="Home")])
    else:
        keyboard.append([InlineKeyboardButton("🏠", callback_data="Home")])
    return keyboard

def teamHandler(match):
    jsonRes = requests.get('https://www.scorebat.com/video-api/v3/').json()
    for attribute in jsonRes['response']:
        if match == attribute['title'].strip():
            for param in attribute['videos']:
                return(param['embed'].split("src='", 1)[1].split("'", 1)[0])
