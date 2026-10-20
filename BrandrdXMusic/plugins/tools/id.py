from BrandrdXMusic import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@app.on_message(filters.command("id"))
async def ids(_, message):
    button = InlineKeyboardButton(
        " ᴄʟᴏsᴇ ",
        callback_data="close"
    )
    markup = InlineKeyboardMarkup([[button]])

    if message.reply_to_message:
        reply = message.reply_to_message

        if reply.from_user:
            text = (
                f"<b><blockquote>"
                f"👤 ᴜsᴇʀ ɴᴀᴍᴇ: {reply.from_user.first_name}\n"
                f"🆔 ᴜsᴇʀ ɪᴅ: <code>{reply.from_user.id}</code>\n\n"
                f"💬 ᴄʜᴀᴛ ɪᴅ: <code>{message.chat.id}</code>"
                f"</blockquote></b>"
            )
        else:
            text = (
                f"<b><blockquote>"
                f"💬 ᴄʜᴀᴛ ɪᴅ: <code>{message.chat.id}</code>\n"
                f"⚠️ ᴛʜɪs ᴍᴇssᴀɢᴇ ʜᴀs ɴᴏ ᴜsᴇʀ"
                f"</blockquote></b>"
            )

        await message.reply_text(
            text,
            reply_markup=markup,
        )

    else:
        text = (
            f"<b><blockquote>"
            f"👥 ɢʀᴏᴜᴘ ɴᴀᴍᴇ: {message.chat.title}\n"
            f"🆔 ɢʀᴏᴜᴘ ɪᴅ: <code>{message.chat.id}</code>\n\n"
            f"👤 ʏᴏᴜʀ ᴜsᴇʀ ɪᴅ: <code>{message.from_user.id}</code>"
            f"</blockquote></b>"
        )

        await message.reply_text(
            text,
            reply_markup=markup,
        )
