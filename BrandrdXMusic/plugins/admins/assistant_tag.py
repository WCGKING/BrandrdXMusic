import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait

from BrandrdXMusic.utils.database import get_assistant
from BrandrdXMusic import app
from BrandrdXMusic.utils.branded_ban import admin_filter

SPAM_CHATS = []

@app.on_message(
    filters.command(
        ["atag", "aall", "amention", "amentionall"], prefixes=["/", "@", ".", "#"]
    )
    & admin_filter
)
async def atag_all_useres(_, message):
    userbot = await get_assistant(message.chat.id)
    if message.chat.id in SPAM_CHATS:
        return await message.reply_text(
            "ᴛᴀɢɢɪɴɢ ᴘʀᴏᴄᴇss ɪs ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴛᴏᴘ sᴏ ᴜsᴇ /acancel"
        )
    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        await message.reply_text(
            "** ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴛᴀɢ ᴀʟʟ, ʟɪᴋᴇ »** `@aall Hi Friends`"
        )
        return
    if replied:
        SPAM_CHATS.append(message.chat.id)
        usernum = 0
        usertxt = ""
        async for m in app.get_chat_members(message.chat.id):
            if message.chat.id not in SPAM_CHATS:
                break
            usernum += 1
            usertxt += f"[{m.user.first_name}](tg://openmessage?user_id={m.user.id})"
            if usernum == 14:
                await userbot.send_message(
                    message.chat.id,
                    f"{replied.text}\n\n{usertxt}",
                    disable_web_page_preview=True,
                )
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass
    else:
        text = message.text.split(None, 1)[1]

        SPAM_CHATS.append(message.chat.id)
        usernum = 0
        usertxt = ""
        async for m in app.get_chat_members(message.chat.id):
            if message.chat.id not in SPAM_CHATS:
                break
            usernum += 1
            usertxt += f'<a href="tg://openmessage?user_id={m.user.id}">{m.user.first_name}</a>'

            if usernum == 14:
                await userbot.send_message(
                    message.chat.id, f"{text}\n{usertxt}", disable_web_page_preview=True
                )
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass



async def cancelcmd(_, message):
    chat_id = message.chat.id
    if chat_id in SPAM_CHATS:
        try:
            SPAM_CHATS.remove(chat_id)
        except Exception:
            pass
        return await message.reply_text("**ᴛᴀɢɢɪɴɢ ᴘʀᴏᴄᴇss sᴜᴄᴄᴇssғᴜʟʟʏ sᴛᴏᴘᴘᴇᴅ!**")

    else:
        await message.reply_text("**ɴᴏ ᴘʀᴏᴄᴇss ᴏɴɢᴏɪɴɢ!**")
        return
