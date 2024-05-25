import time
from datetime import datetime

import psutil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import SUPPORT_CHAT, PING_IMG_URL
from .utils import StartTime
from BrandrdXMusic.utils import get_readable_time


@Client.on_message(filters.command("ping"))
async def ping_clone(client: Client, message: Message):
    i = await client.get_me()
    hmm = await message.reply_photo(
        photo=PING_IMG_URL, caption=f"{i.mention} ɪs ᴘɪɴɢɪɴɢ..."
    )
    upt = int(time.time() - StartTime)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    start = datetime.now()
    resp = (datetime.now() - start).microseconds / 1000
    uptime = get_readable_time((upt))

    await hmm.edit_text(
        f"""➻ ᴩᴏɴɢ : `{resp}ᴍs`

<b><u>{i.mention} sʏsᴛᴇᴍ sᴛᴀᴛs :</u></b>

๏ **ᴜᴩᴛɪᴍᴇ :** {uptime}
๏ **ʀᴀᴍ :** {mem}
๏ **ᴄᴩᴜ :** {cpu}
๏ **ᴅɪsᴋ :** {disk}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("❄ sᴜᴘᴘᴏʀᴛ ❄", url=SUPPORT_CHAT),
                    InlineKeyboardButton(
                        "✨ 𝙰𝙳𝙳 𝙼𝙴✨",
                        url=f"https://t.me/{i.username}?startgroup=true",
                    ),
                ],
            ]
        ),
    )
