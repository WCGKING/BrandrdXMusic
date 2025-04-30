import asyncio

from BrandrdXMusic import app
from pyrogram import filters
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import MUSIC_BOT_NAME

@app.on_message(filters.command(["alive"]))
async def start(client: Client, message: Message):
    await message.reply_video(
        video=f"https://t.me/melodysongss/4",
        caption=f"❤️ Hello Everyone \n\n🔮 ɪ ᴀᴍ Melody Music\n\n✨ မင်းတို့ရဲ့ Group မှာထည့်ပြီး သီချင်းဖွင့်နိုင်ပါတယ်။\n\n💫 တစ်ခုခုမေးချင်ရင် အုံနာကို ဆက်သွယ်နိုင်ပါတယ်။🤍...\n\n━━━━━━━━━━━━━━━━━━❄",
        reply_markup=InlineKeyboardMarkup(
            [
               [
            InlineKeyboardButton(
                text="☆ Owner 💗 ", url=f"https://t.me/nnaynay1112221"
            ),
            InlineKeyboardButton(
                text="☆ ꜱᴜᴘᴘᴏʀᴛ 💗", url=f"https://t.me/melody_cchat"
            ),
        ],
                [
            InlineKeyboardButton(
                text="☆ ADD💗", url=f"https://t.me/melodm_bot?startgroup=true"
            ),
                ],
                [
                    InlineKeyboardButton(
                        "✯ ᴄʟᴏsᴇ ✯", callback_data="close"
                    )
                ],
            ]
        )
    )
