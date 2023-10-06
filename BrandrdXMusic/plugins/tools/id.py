from BrandrdXMusic import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@app.on_message(filters.command("id"))
def ids(_, message):
    reply = message.reply_to_message
    if reply:
        button = InlineKeyboardButton("✯ ᴄʟᴏsᴇ ✯", callback_data="close")
        markup = InlineKeyboardMarkup([[button]])
        message.reply_text(
            f"User {reply.from_user.first_name} ID is : {reply.from_user.id}",
            reply_markup=markup
        )
    else:
        button = InlineKeyboardButton("✯ ᴄʟᴏsᴇ ✯", callback_data="close")
        markup = InlineKeyboardMarkup([[button]])
        message.reply(
           f"ᴛʜɪs ɢʀᴏᴜᴩ's ɪᴅ ɪs: {message.chat.id}",
           reply_markup=markup
        )
