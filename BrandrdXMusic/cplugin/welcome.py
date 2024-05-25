from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont
from os import environ
import requests
import random
from BrandrdXMusic import userbot
from BrandrdXMusic.misc import SUDOERS
from pyrogram import *
from pyrogram.types import *
from BrandrdXMusic.utils.branded_ban import admin_filter
import random
from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup
from PIL import Image, ImageDraw, ImageFont
import asyncio, os, time, aiohttp
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from asyncio import sleep
from pyrogram import filters, Client, enums
from pyrogram.enums import ParseMode
from pyrogram import *
from pyrogram.types import *
from logging import getLogger
from BrandrdXMusic.utils.branded_ban import admin_filter
import os
from BrandrdXMusic.misc import SUDOERS
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import *
from pyrogram.types import *
from logging import getLogger


random_photo = [
    "https://graph.org/file/e36ca3c73f08d4c04b9b6.jpg",
    "https://graph.org/file/970955ce30672302943c1.jpg",
    "https://graph.org/file/e38d003cff04e6dffb5b2.jpg",
    "https://graph.org/file/98f6187aa4d3d3954ccdc.jpg",
    "https://graph.org/file/f4b34351a59061ba1c61b.jpg",
]
# --------------------------------------------------------------------------------- #


LOGGER = getLogger(__name__)


class WelDatabase:
    def __init__(self):
        self.data = {}

    async def find_one(self, chat_id):
        return chat_id in self.data

    async def add_wlcm(self, chat_id):
        if chat_id not in self.data:
            self.data[chat_id] = {"state": "on"}  # Default state is "on"

    async def rm_wlcm(self, chat_id):
        if chat_id in self.data:
            del self.data[chat_id]


wlcm = WelDatabase()


class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None


def circle(pfp, size=(500, 500), brightness_factor=10):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    pfp = ImageEnhance.Brightness(pfp).enhance(brightness_factor)
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


def welcomepic(pic, user, chatname, id, uname, brightness_factor=1.3):
    background = Image.open("BrandrdXMusic/assets/wel2.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp, brightness_factor=brightness_factor)
    pfp = pfp.resize((892, 880))
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("BrandrdXMusic/assets/font.ttf", size=95)
    welcome_font = ImageFont.truetype("BrandrdXMusic/assets/font.ttf", size=45)

    # Draw user's name with shining red fill and dark saffron border
    draw.text((1770, 1015), f": {user}", fill=(255, 0, 0), font=font)
    draw.text(
        (1770, 1015),
        f": {user}",
        fill=None,
        font=font,
        stroke_fill=(255, 153, 51),
        stroke_width=6,
    )

    # Draw user's id with shining blue fill and white border
    draw.text((1530, 1230), f": {id}", fill=(0, 0, 139))
    draw.text(
        (1530, 1230),
        f": {id}",
        fill=None,
        font=font,
        stroke_fill=(255, 255, 255),
        stroke_width=0,
    )

    # Draw user's username with white fill and green border
    draw.text((2030, 1450), f": {uname}", fill=(255, 255, 255), font=font)
    draw.text(
        (2030, 1450),
        f": {uname}",
        fill=None,
        font=font,
        stroke_fill=(0, 128, 0),
        stroke_width=6,
    )

    # Resize photo and position
    pfp_position = (255, 323)
    background.paste(pfp, pfp_position, pfp)

    # Calculate circular outline coordinates
    center_x = pfp_position[0] + pfp.width / 2
    center_y = pfp_position[1] + pfp.height / 2
    radius = min(pfp.width, pfp.height) / 2

    # Draw circular outlines
    draw.ellipse(
        [
            (center_x - radius - 10, center_y - radius - 10),
            (center_x + radius + 10, center_y + radius + 10),
        ],
        outline=(255, 153, 51),
        width=25,
    )  # Saffron border

    draw.ellipse(
        [
            (center_x - radius - 20, center_y - radius - 20),
            (center_x + radius + 20, center_y + radius + 20),
        ],
        outline=(255, 255, 255),
        width=25,
    )  # White border

    draw.ellipse(
        [
            (center_x - radius - 30, center_y - radius - 30),
            (center_x + radius + 30, center_y + radius + 30),
        ],
        outline=(0, 128, 0),
        width=25,
    )  # Green border

    background.save(f"downloads/welcome#{id}.png")
    return f"downloads/welcome#{id}.png"


@Client.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(client: Client, message):  # Added 'message' as a parameter
    usage = "**ᴜsᴀɢᴇ:**\n**⦿ /welcome [on|off]**"
    if len(message.command) == 1:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        A = await wlcm.find_one(chat_id)
        state = message.text.split(None, 1)[1].strip().lower()
        if state == "off":
            if A:
                await message.reply_text("**ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ !**")
            else:
                await wlcm.add_wlcm(chat_id)
                await message.reply_text(
                    f"**ᴅɪsᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ** {message.chat.title}"
                )
        elif state == "on":
            if not A:
                await message.reply_text("**ᴇɴᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ.**")
            else:
                await wlcm.rm_wlcm(chat_id)
                await message.reply_text(
                    f"**ᴇɴᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ ** {message.chat.title}"
                )
        else:
            await message.reply_text(usage)
    else:
        await message.reply("**sᴏʀʀʏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴇɴᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ!**")


@Client.on_chat_member_updated(filters.group, group=-13)
async def greet_new_member(
    client: Client, member: ChatMemberUpdated
):  # Added 'client' and 'member' as parameters
    chat_id = member.chat.id
    count = await client.get_chat_members_count(chat_id)
    A = await wlcm.find_one(chat_id)
    if A:
        return

    user = member.new_chat_member.user if member.new_chat_member else member.from_user

    # Add the modified condition here
    if member.new_chat_member and not member.old_chat_member:

        try:
            pic = await client.download_media(
                user.photo.big_file_id, file_name=f"pp{user.id}.png"
            )
        except AttributeError:
            pic = "BrandrdXMusic/assets/upic.png"
        if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
            try:
                await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
            except Exception as e:
                LOGGER.error(e)
        try:
            welcomeimg = welcomepic(
                pic, user.first_name, member.chat.title, user.id, user.username
            )
            button_text = "๏ ᴠɪᴇᴡ ɴᴇᴡ ᴍᴇᴍʙᴇʀ ๏"
            add_button_text = "๏ ᴋɪᴅɴᴀᴘ ᴍᴇ ๏"
            deep_link = f"{user.id}"
            add_link = f"https://t.me/BRANDED_KUDI_BOT?startgroup=true"
            temp.MELCOW[f"welcome-{member.chat.id}"] = await client.send_photo(
                member.chat.id,
                photo=welcomeimg,
                caption=f"""
**❅────✦ ᴡᴇʟᴄᴏᴍᴇ ✦────❅**

▰▰▰▰▰▰▰▰▰▰▰▰▰
**➻ ɴᴀᴍᴇ »** {user.mention}
**➻ ɪᴅ »** `{user.id}`
**➻ ᴜ_ɴᴀᴍᴇ »** @{user.username}
**➻ ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs »** {count}
▰▰▰▰▰▰▰▰▰▰▰▰▰

**❅─────✧❅✦❅✧─────❅**
""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(button_text, user_id=deep_link)],
                        [InlineKeyboardButton(text=add_button_text, url=add_link)],
                    ]
                ),
            )
        except Exception as e:
            LOGGER.error(e)
