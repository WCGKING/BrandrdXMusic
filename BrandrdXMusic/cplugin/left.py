from BrandrdXMusic import app
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont
from os import environ
import random
from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup
from PIL import Image, ImageDraw, ImageFont
import asyncio, os, time, aiohttp
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from asyncio import sleep
from pyrogram import filters, Client, enums
from pyrogram.enums import ParseMode
from pyrogram import *
from pyrogram.types import *
from logging import getLogger
from BrandrdXMusic.utils.branded_ban import admin_filter
from BrandrdXMusic import app
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont
import random
import asyncio

random_photo = [
    "https://graph.org/file/eabab7e8a3e5df87a0b04.jpg",
    "https://graph.org/file/84956a27b8f85c90d5545.jpg",
    "https://graph.org/file/e1c47b075db35d5c1ec7a.jpg",
    "https://graph.org/file/872dc8af2a36bed43b9b6.jpg",
    "https://graph.org/file/427f4869a158126957747.jpg",
]

bg_path = "BrandrdXMusic/assets/userinfo.png"
font_path = "BrandrdXMusic/assets/hiroko.ttf"

get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)


async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: Union[int, str],
    profile_path: Optional[str] = None,
):
    bg = Image.open(bg_path)

    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((400, 400))
        bg.paste(resized, (440, 160), resized)

    img_draw = ImageDraw.Draw(bg)

    img_draw.text(
        (529, 627),
        text=str(user_id).upper(),
        font=get_font(46, font_path),
        fill=(255, 255, 255),
    )

    path = f"downloads/userinfo_img_{user_id}.png"
    bg.save(path)
    return path


@Client.on_chat_member_updated(filters.group, group=-24)
async def member_has_left(client: Client, member: ChatMemberUpdated):
    if (
        not member.new_chat_member
        and member.old_chat_member.status not in {"banned", "left", "restricted"}
        and member.old_chat_member
    ):
        user = (
            member.old_chat_member.user if member.old_chat_member else member.from_user
        )
        if user.photo:
            photo = await client.download_media(user.photo.big_file_id)
            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user.id,
                profile_path=photo,
            )
        else:
            welcome_photo = random.choice(random_photo)

        caption = f"**#New_Member_Left**\n\n**๏** {user.mention} **ʜᴀs ʟᴇғᴛ ᴛʜɪs ɢʀᴏᴜᴘ**\n**๏ sᴇᴇ ʏᴏᴜ sᴏᴏɴ ᴀɢᴀɪɴ..!**"
        button_text = "๏ ᴠɪᴇᴡ ᴜsᴇʀ ๏"
        deep_link = f"tg://openmessage?user_id={user.id}"

        message = await client.send_photo(
            chat_id=member.chat.id,
            photo=welcome_photo,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(button_text, url=deep_link)]]
            ),
        )

        async def delete_message():
            await asyncio.sleep(30)
            await message.delete()

        # Run the task
        asyncio.create_task(delete_message())
