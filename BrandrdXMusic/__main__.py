import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from BrandrdXMusic import app, userbot
from .logging import LOGGER
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.misc import sudo
from BrandrdXMusic.plugins import ALL_MODULES
from BrandrdXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("BrandrdXMusic.plugins" + all_module)
    LOGGER("BrandrdXMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Hotty.start()
    try:
        await Hotty.stream_call("https://te.legra.ph/file/a0c2e8dae9f17911aef70.mp4")
    except NoActiveGroupCall:
        LOGGER("BrandrdXMusic").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Hotty.decorators()
    LOGGER("BrandrdXMusic").info(
        "\x56\x61\x6c\x65\x6e\x63\x69\x61\x20\x4d\x75\x73\x69\x63\x20\x42\x6f\x74\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e\x2e\x2e\x2e\x20\x0a\x0a\x44\x72\x6f\x70\x20\x59\x6f\x75\x72\x20\x47\x69\x72\x6c\x66\x72\x69\x65\x6e\x64\x27\x73\x20\x4e\x75\x6d\x62\x65\x72\x20\x41\x74\x20\x40\x4a\x6f\x69\x6e\x49\x6e\x64\x69\x61\x6e\x4e\x61\x76\x79\x5f\x30\x30\x37\x20\x0a\x0a\x4a\x6f\x69\x6e\x20\x40\x43\x68\x65\x72\x69\x73\x68\x65\x64\x5f\x43\x6f\x6d\x6d\x75\x6e\x69\x74\x79\x20\x46\x6f\x72\x20\x41\x6e\x79\x20\x49\x73\x73\x75\x65\x73"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("BrandrdXMusic").info("Stopping Valencia Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
