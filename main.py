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
PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ["TOKEN"]
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging
import Constants
import queryHandlers

from Keyboards import Keyboards

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
flag=False
otherKeyboard=Keyboards()
if(not otherKeyboard.getLeagues()):
    flag=True


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):

    name= update.message.from_user.first_name
    update.message.reply_text("Hello " +name + " , Please use /highlights to enable my power. ")

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if("-Leag" in query.data and "Other" not in query.data):
        reply_markup = InlineKeyboardMarkup(queryHandlers.leagueHandler(query.data))
        query.edit_message_text('This are the current available matches : ', reply_markup=reply_markup)

    if (":Team" in query.data):
        match = query.data.split(":", 1)[0]
        query.message.reply_text("Enjoy the highlights of : " + match)
        keyboard=[]
        keyboard.append([InlineKeyboardButton("Close", callback_data="Close"),InlineKeyboardButton("🏠", callback_data="NewHome")])
        reply_markup=InlineKeyboardMarkup(keyboard)
        query.message.reply_text(queryHandlers.teamHandler(match),reply_markup=reply_markup)

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

        if("New" not in query.data):
            query.edit_message_text('Please choose the relevant League : ', reply_markup=reply_markup)
        else:
            query.message.reply_text('You are a true fan, Please choose the relevant league : ', reply_markup=reply_markup)

    if("Close" in query.data):
        query.message.reply_text("See you soon!")

def highlights(update, context):
    """Send a message when the command /help is issued."""

    keyboard = Constants.mainKeyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose the relevant League : ' , reply_markup=reply_markup)

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text("Sorry I don't understand that, Write /highlights to enable my power")


def error(update, context):
    """Log Errors caused by Updates."""
    #update.message.reply_text("Sorry I'm not available at the moment.")
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    #base_url="http://localhost:8081/bot" // Add it to function in order to run Localy

    updater = Updater(TOKEN,use_context=True)
    #if(flag):
        #error(error)
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
