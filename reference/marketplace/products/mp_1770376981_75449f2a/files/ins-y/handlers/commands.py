from core.bot import bot
from core.constants import Messages
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, Messages.WELCOME, parse_mode='Markdown')
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, Messages.WELCOME, parse_mode='Markdown')
