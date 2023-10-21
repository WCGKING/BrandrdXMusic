import random
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.types import(InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, Message)
from config import LOGGER_ID as LOG_GROUP_ID
from KingX import app  

photo = [
    "https://te.legra.ph/file/56665c1fb7457fb847028.jpg",
    "https://te.legra.ph/file/936df101ca5b97ebdf44c.jpg",
    "https://te.legra.ph/file/a299c30ec42a6ed7eb5d0.jpg",
    "https://te.legra.ph/file/bebd65efe37c2ee7d8e32.jpg",
    "https://te.legra.ph/file/9141f3b892d77dd74a12b.jpg",
]


@app.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message):    
    chat = message.chat
    link = await app.export_chat_invite_link(message.chat.id)
    for members in message.new_chat_members:
        if members.id == app.id:
            count = await app.get_chat_members_count(chat.id)

            msg = (
                f"📝 ᴍᴜsɪᴄ ʙᴏᴛ ᴀᴅᴅᴇᴅ ɪɴ ᴀ ɴᴇᴡ ɢʀᴏᴜᴘ\n\n"
                f"____________________________________\n\n"
                f"🥀 ᴄʜᴀᴛ ɴᴀᴍᴇ: {message.chat.title}\n"
                f"🦋 ᴄʜᴀᴛ ɪᴅ: {message.chat.id}\n"
                f"💋 ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ: @{message.chat.username}\n"
                f"🙈 ᴄʜᴀᴛ ʟɪɴᴋ: [ᴄʟɪᴄᴋ]({link})\n"
                f"😍ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs: {count}\n"
                f"🔥 ᴀᴅᴅᴇᴅ ʙʏ: {message.from_user.mention}"
            )
            await app.send_photo(LOG_GROUP_ID, photo=random.choice(photo), caption=msg, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"sᴇᴇ ɢʀᴏᴜᴘ🙊", url=f"{link}")]
         ]))



@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        remove_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜꜱᴇʀ"
        title = message.chat.title
        username = f"@{message.chat.username}" if message.chat.username else "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
        chat_id = message.chat.id
        left = f"✫ <b><u>#ʟᴇꜰᴛ_ɢʀᴏᴜᴘ</u></b> ✫\n\nᴄʜᴀᴛ ᴛɪᴛʟᴇ : {title}\n\nᴄʜᴀᴛ ɪᴅ : {chat_id}\n\nʀᴇᴍᴏᴠᴇᴅ ʙʏ : {remove_by}\n\nʙᴏᴛ: @{app.username}"
        await app.send_photo(LOG_GROUP_ID, photo=random.choice(photo), caption=left)

#welcome

@app.on_message(filters.new_chat_members, group=3)
async def _greet(_, message):    
    chat = message.chat
    
    for member in message.new_chat_members:
        
            count = await app.get_chat_members_count(chat.id)

            msg = (
                f"🌷{member.id}ᴡᴇʟᴄᴏᴍᴇ ɪɴ ᴀ ɴᴇᴡ ɢʀᴏᴜᴘ🥳\n\n"
                f"🦋𝐂ʜᴀᴛ 𝐍ᴀᴍᴇ: {message.chat.title}\n"
                f"🔐𝐂ʜᴀᴛ 𝐔.𝐍: @{message.chat.username}\n"
                f"💖𝐔ʀ 𝐈d: {member.id}\n"
                f"✍️𝐔ʀ 𝐔.𝐍aмe: @{member.username}\n"
                f"👥𝐂ᴏᴍᴘʟᴇᴛᴇᴅ {count} ᴍᴇᴍʙᴇʀꜱ🎉"
            )
            await app.send_photo(message.chat.id, photo=random.choice(photo), caption=msg, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{app.username}?startgroup=true")]
         ]))

#tagall
