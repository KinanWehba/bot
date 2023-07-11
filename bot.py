import requests
import re
import hashlib
import base64
from datetime import datetime
from telegram import Update, LabeledPrice, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CallbackQueryHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    PreCheckoutQueryHandler,
)
import telebot

from keys import TOKEN, PAYMENT_PROVIDER_TOKEN, SECRET_CODE
base_url = ('http://127.0.0.1:5000/')
async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Welcome to Secret Crush Ai bot  /start\n السطر الثاني",)



async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    chat_id = update.message.from_user.id

    params = {
        'message_text': message_text,
        'username': username,
        'chat_id': chat_id,
        'first_name': first_name,
        'command': start_callback.__name__
    }
    r = requests.get(base_url+"msg_link", params=params)
    result = r.json()
    your_id = result['user_idd']
    facebook_share_link = f"https://www.facebook.com/sharer/sharer.php?u=https://t.me/SecretCrush_AiBot&{your_id}"

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"**رقم التعريف الخاص بك هو {your_id} \n\n Facebook: {facebook_share_link}")

async def hash_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    if message_text.startswith("#") and message_text[1:].isdigit() and len(message_text) == 7:
        message_text = int(update.message.text[1:])
        username = update.message.from_user.username
        first_name = update.message.from_user.first_name
        chat_id = update.message.from_user.id
        params = {
        'message_text': message_text,
        'username': username,
        'chat_id': chat_id,
        'first_name': first_name,
        'command': hash_callback.__name__
    }

        r = requests.get(base_url+"addcrush", params=params)
        result = r.json()
        msg_bot = result["msg_bot"]
        await context.bot.send_message(
        chat_id=chat_id,
        text=f"{msg_bot}",
    )
    else:
        pass







async def msg_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    chat_id = update.message.from_user.id

    params = {
        'message_text': message_text,
        'username': username,
        'chat_id': chat_id,
        'first_name': first_name,
        'command': msg_link.__name__
        }
    r = requests.get(base_url +"msg_link", params=params)
    result = r.json()
    userc_chatid=result["userc_chatid"]
    user_statuss=result["user_statuss"]
    

    if user_statuss == "activate" :


        if userc_chatid is not None :
            await context.bot.send_message(
        chat_id=userc_chatid,
        text=f"{message_text}",

#        text=f"**رقم التعريف الخاص بك هو : #{bot_msg}**\n\nيمكنك نشره لكي يتمكن المعجبين من التواصل معك\n\nكما يمكنك ان تتواصل مع الكراش بكتابة # ثم رقم تعريفه الشخصي\n\nسيتم حفظ معرف الكراش دائما اذا اردت تعديل رقم التعريف اضغط على /AddCrush\n\nاو /help للمساعدة",
    )
             
        else:
            await context.bot.send_message(
        chat_id=chat_id,
        text=f"الرجاء ادخال معرف الكراش",
#        text=f"**رقم التعريف الخاص بك هو : #{bot_msg}**\n\nيمكنك نشره لكي يتمكن المعجبين من التواصل معك\n\nكما يمكنك ان تتواصل مع الكراش بكتابة # ثم رقم تعريفه الشخصي\n\nسيتم حفظ معرف الكراش دائما اذا اردت تعديل رقم التعريف اضغط على /AddCrush\n\nاو /help للمساعدة",
    )


    else :
                await context.bot.send_message(
        chat_id=chat_id,
        text=f"المستخدم معطل",
#        text=f"**رقم التعريف الخاص بك هو : #{bot_msg}**\n\nيمكنك نشره لكي يتمكن المعجبين من التواصل معك\n\nكما يمكنك ان تتواصل مع الكراش بكتابة # ثم رقم تعريفه الشخصي\n\nسيتم حفظ معرف الكراش دائما اذا اردت تعديل رقم التعريف اضغط على /AddCrush\n\nاو /help للمساعدة",
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    # command handlers
    help_handler = CommandHandler("help", help_callback)
    start_handler = CommandHandler("start", start_callback)

    hash_handler = MessageHandler(filters.TEXT & filters.Regex(r"^#\d{6}$"), hash_callback)
    msg_handler = MessageHandler(filters.TEXT, msg_link)

    # register handlers
    app.add_handler(help_handler)
    app.add_handler(start_handler)
    app.add_handler(hash_handler)

    app.add_handler(msg_handler)
    app.run_polling()
print("hi")
