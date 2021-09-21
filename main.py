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
import os
import time
import urllib.request

import requests
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging
import Constants

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""

    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    name= update.message.from_user.first_name
    print(name)
    #+  'Please choose:', reply_markup=reply_markup

    update.message.reply_text("Hello " +name + " \n ")

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")

def help(update, context):
    """Send a message when the command /help is issued."""

    update.message.reply_text('Help!')





def echo(update, context):
    """Echo the user message."""
    #telebot=telegram.Bot("1969164922:AAFarz1cKoaP3l8ONCtK9ae8SU-13tAJljM")
    telebot = bot.Bot(Constants.Api_Key)
    team=update.message.text

    teamsJson = requests.get('https://www.scorebat.com/video-api/v3/').json()
    highlights=[]
    for teams in teamsJson['response'] :
        if(team in teams['title']):
            for param in teams['videos']:
                 highlights.append(param['embed'].split("src='",1)[1].split("'",1)[0])

    update.message.reply_text("Enjoy ")
    for highlight in highlights:
        update.message.reply_text(highlight)
        time.sleep(1)
    videoUrl="https://www.youtube.com/watch?v=6b-1jjvEOI4"
    #update.message.reply_document(videoUrl)
    photoUrl="https://upload.wikimedia.org/wikipedia/he/thumb/a/a2/Hapoel_Haifa_Football_Club_Logo.png/200px-Hapoel_Haifa_Football_Club_Logo.png"
    #telebot.sendPhoto(chat_id=update.message.chat.id,photo=photoUrl)
    #videoTry=urllib.request.urlretrieve(videoUrl, 'video_name.mp4')
    #file_id=telebot.sendVideo(chat_id=update.message.chat.id,video=open("videotry.mp4","rb"),timeout=10000)
    #telebot.sendVideo(chat_id=update.message.chat.id,video="BAACAgQAAxkDAAIBD2FIxJ7M2-rbn1TC9wVr5HJ83UGcAAIjDAACK2hJUjhAQxWqqgHWIAQ")
    #print(file_id)
    #telebot.sendDocument(chat_id=update.message.chat.id,document=videoUrl)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(Constants.Api_Key,base_url="http://localhost:8081/bot",use_context=True)
    pid=os.getpid()
    print(pid)
    #updater.bot.logOut()
    #bot=telegram.Bot

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hello", start))
    dp.add_handler(CommandHandler("help", help))
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