from telegram import InlineKeyboardButton

mainKeyboard = [

    [InlineKeyboardButton("Italy Seria A", callback_data='ITALY: Serie A-Leag')],
    [InlineKeyboardButton("France Ligue 1", callback_data='FRANCE: Ligue 1-Leag')],
    [InlineKeyboardButton("England Premier League", callback_data='ENGLAND: Premier League-Leag')],
    [InlineKeyboardButton("Spain La Liga", callback_data='SPAIN: La Liga-Leag')],
    [InlineKeyboardButton("Germany BundesLiga", callback_data='GERMANY: Bundesliga-Leag')],
    [InlineKeyboardButton("Champions League", callback_data='CHAMPIONS LEAGUE-Leag')],
    [InlineKeyboardButton("Other", callback_data='Other-Leag')]
]