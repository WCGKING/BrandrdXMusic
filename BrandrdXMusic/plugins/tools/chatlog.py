import random
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.types import(InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, Message)
from config import LOGGER_ID as LOG_GROUP_ID
from BrandrdXMusic import app  

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
                f"📝 𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧 𝗔𝗗𝗗𝗘𝗗 𝗜𝗡 𝗔 𝗡𝗘𝗪 𝗚𝗥𝗢𝗨𝗣\n\n"
                f"───────────────────────────\n\n"
                f"🥀 𝗖𝗛𝗔𝗧 𝗡𝗔𝗠𝗘: {message.chat.title}\n"
                
                f"🦋 𝗖𝗛𝗔𝗧 𝗜'𝗗: {message.chat.id}\n"
                
                f"💋 𝗖𝗛𝗔𝗧 𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘: @{message.chat.username}\n"
                
                f"🙈 𝗖𝗛𝗔𝗧 𝗟𝗜𝗡𝗞: [𝗖𝗟𝗜𝗖𝗞]({link})\n"
                
                f"😍𝗚𝗥𝗢𝗨𝗣 𝗠𝗘𝗠𝗕𝗘𝗥𝗦: {count}\n"
                
                f"❤️‍🔥 𝗔𝗗𝗗𝗘𝗗 𝗕𝗬: {message.from_user.mention}"
            )
            await app.send_photo(LOG_GROUP_ID, photo=random.choice(photo), caption=msg, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"★ 𝗦𝗘𝗘 𝗚𝗥𝗢𝗨𝗣 ★", url=f"{link}")]
         ]))


@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        remove_by = message.from_user.mention if message.from_user else "𝗨𝗡𝗞𝗠𝗢𝗪𝗡 𝗨𝗦𝗘𝗥 "
        title = message.chat.title
        username = f"@{message.chat.username}" if message.chat.username else "𝗣𝗥𝗜𝗩𝗔𝗧𝗘 𝗖𝗛𝗔𝗧"
        chat_id = message.chat.id
        left = f"✫ <b><u>#𝗟𝗘𝗙𝗧 𝗚𝗥𝗢𝗨𝗣</u></b> ✫\n\𝗖𝗛𝗔𝗧 𝗧𝗜𝗧𝗟𝗘 : {title}\n\𝗖𝗛𝗔𝗧 𝗜𝗗  : {chat_id}\n\n𝗥𝗘𝗠𝗢𝗩𝗘𝗗 𝗕𝗬 : {remove_by}\n\nʙᴏᴛ: @{app.username}"
        await app.send_photo(LOG_GROUP_ID, photo=random.choice(photo), caption=left)

#welcome

@app.on_message(filters.new_chat_members, group=3)
async def _greet(_, message):    
    chat = message.chat
    
    for member in message.new_chat_members:
        
            count = await app.get_chat_members_count(chat.id)

            msg = (
                f"🌷{member.id}𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐈𝐍 𝐀 𝐍𝐄𝐖 𝐆𝐑𝐎𝐔𝐏🥳\n\n"
                
                f"🦋𝐂𝐇𝐀𝐓 𝐍𝐀𝐌𝐄: {message.chat.title}\n"
                
                f"🔐𝐂𝐇𝐀𝐓 𝐔.𝐍: @{message.chat.username}\n"
                
                f"💖𝐔𝐑 𝐈'𝐃: {member.id}\n"
                
                f"✍️𝐔𝐑 𝐔.𝐍𝐀𝐍𝐄: @{member.username}\n"
            
                f"👥𝐂𝐎𝐌𝐏𝐋𝐄𝐓𝐄𝐃 {count} 𝐌𝐄𝐌𝐁𝐄𝐑𝐒🎉"
            )
            await app.send_photo(message.chat.id, photo=random.choice(photo), caption=msg, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"★ 𝐀𝐃𝐃 𝐌𝐄 𝐈𝐍 𝐘𝐎𝐔𝐑 𝐆𝐑𝐎𝐔𝐏 𝐁𝐀𝐁𝐘 ★", url=f"https://t.me/{app.username}?startgroup=true")]
         ]))

#tagall
