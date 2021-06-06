from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    CallbackQueryHandler
from telegram import (
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton
)

from database import Database
import commands
import globals


database = Database("malumotlar.db")

def start_command(update,context):
    chat_id = update.message.from_user.id
    user = database.get_chat_id(chat_id)

    update.message.reply_text("Ismingizni kiriting:",)


    contact_button = [[KeyboardButton('Contact', request_contact=True)]]
    update.message.reply_text(text="Telefon raqamingizni kiriting:",
                              reply_markup=ReplyKeyboardMarkup(contact_button))

def messege_handler(update, context):
    msg = update.message.text
    chat_id = update.message.from_user.id
    user = database.get_chat_id(chat_id)
    state = context.user_data.get('state', 0)

    if state == 1:
        database.update_user(state, chat_id, msg)


    elif state == 2:
        database.update_user(state, chat_id, msg)

    elif state == 3:
        database.update_user(state, chat_id, msg)
    else:
        return msg

    if user:
        if  user['f_name']:
            update.message.reply_text(text="Ismingizni kiriting")
            context.user_data['state'] = 1

        elif  user['l_name']:
            update.message.reply_text(text="Familiyangizni kiriting")
            context.user_data['state'] = 2

        elif  user['contact']:
            update.message.reply_text(text="Telefon raqamingizni kiriting")
            context.user_data['state'] = 1
        else:
            context.user_data['state'] = 4


def contact_handler(update, context):
    msg_phone = update.message.contact.phone_number
    chat_id = update.message.from_user.id
    state = context.user_data.get('state', 0)
    database.update_user(state,msg_phone, chat_id)
    return messege_handler(update, context)







def main():
    updater = Updater("1542491519:AAFEazocWUU-3X0xMt4cALD4gtzsGYuMhSY")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    # dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    # dispatcher.add_handler(CallbackQueryHandler(callback_handler))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()