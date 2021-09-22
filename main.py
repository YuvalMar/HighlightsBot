#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""


import logging

from datetime import datetime

import pytz
import requests
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging
import Constants
from Keyboards import Keyboards

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

otherKeyboard=Keyboards()
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""

    """Sends a message with three inline buttons attached."""
    if (not pollCheck(update.message.date)):
        return
    name= update.message.from_user.first_name
    update.message.reply_text("Hello " +name + " \n ")

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    jsonRes = requests.get('https://www.scorebat.com/video-api/v3/').json()
    teamsSet = set()
    if("-Leag" in query.data and "Other" not in query.data):
        league=query.data.split("-",1)[0]
        if(league != "CHAMPIONS LEAGUE") :
            for attribute in jsonRes['response']:
                if league == attribute['competition']:
                    teamsSet.add(attribute['title'].strip())

        else :
            for attribute in jsonRes['response']:
                if league in attribute['competition']:
                    teamsSet.add(attribute['title'].strip())
        keyboard=[]
        for team in teamsSet :
            temp=[InlineKeyboardButton(team,callback_data=team+":Team")]
            keyboard.append(temp)
        keyboard.append([InlineKeyboardButton("🏠", callback_data="Home")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text('This are the current available matches : ', reply_markup=reply_markup)
    if (":Team" in query.data):
        highlights=set()
        match = query.data.split(":", 1)[0]
        for attribute in jsonRes['response']:
            if match == attribute['title'].strip():
                for param in attribute['videos']:
                    highlights.add(param['embed'].split("src='", 1)[1].split("'", 1)[0])
                    break
        query.message.reply_text("Enjoy the highlights of : " + match)
        for highlight in highlights:
            query.message.reply_text(highlight)
    if("Other" in query.data):
        reply_markup=InlineKeyboardMarkup(otherKeyboard.relevantKeyBoard(0))
        query.edit_message_text('Please choose the relevant League : ', reply_markup=reply_markup)
    if("Men" in query.data):
        i=query.data.split(":",1)[1]
        reply_markup = InlineKeyboardMarkup(otherKeyboard.relevantKeyBoard(int(i)))
        query.edit_message_text('Please choose the relevant League : ', reply_markup=reply_markup)
    if("Home" in query.data):
        keyboard = Constants.mainKeyboard
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text('Please choose the relevant League : ', reply_markup=reply_markup)


def highlights(update, context):
    """Send a message when the command /help is issued."""
    if(not pollCheck(update.message.date)):
        return
    keyboard = Constants.mainKeyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose the relevant League : ' , reply_markup=reply_markup)





def echo(update, context):
    """Echo the user message."""
    if (not pollCheck(update.message.date)):
        return
    update.message.reply_text("Sorry I don't understand that, Write /highlights to enable my power")




def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def pollCheck(msgDate):
    datediff=int((datetime.now(pytz.utc)-msgDate).days)
    return (datediff==0)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    #base_url="http://localhost:8081/bot" // Add it to function in order to run Localy
    updater = Updater(Constants.Api_Key,use_context=True)


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hello", start))
    dp.add_handler(CommandHandler("highlights", highlights))
    dp.add_handler(CallbackQueryHandler(button))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()