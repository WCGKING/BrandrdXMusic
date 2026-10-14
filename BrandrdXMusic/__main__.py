import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from BrandrdXMusic import LOGGER, app, userbot
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.misc import sudo
from BrandrdXMusic.plugins import ALL_MODULES
from BrandrdXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if not any(
        [
            config.STRING1,
            config.STRING2,
            config.STRING3,
            config.STRING4,
            config.STRING5,
        ]
    ):
        LOGGER(__name__).error(
            "Assistant client variables not defined, exiting..."
        )
        return

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)

    except Exception:
        LOGGER(__name__).exception(
            "Failed to load banned users from database"
        )

    try:
        await app.start()

        for all_module in ALL_MODULES:
            importlib.import_module(
                "BrandrdXMusic.plugins" + all_module
            )

        LOGGER("BrandrdXMusic.plugins").info(
            "Successfully imported modules."
        )

        await userbot.start()
        await Hotty.start()

        try:
            await Hotty.stream_call(
                "https://graph.org/file/e999c40cb700e7c684b75.mp4"
            )
        except NoActiveGroupCall:
            LOGGER("BrandrdXMusic").error(
                "No active voice chat found in the configured log group. "
                "Start its voice chat and restart the bot."
            )
            return
        except Exception:
            LOGGER("BrandrdXMusic").exception(
                "Initial stream failed"
            )
            return

        await Hotty.decorators()

        LOGGER("BrandrdXMusic").info(
            "BrandrdXMusic started successfully."
        )

        await idle()

    except Exception:
        LOGGER("BrandrdXMusic").exception(
            "An error occurred while running the bot"
        )
        raise

    finally:
        try:
            await Hotty.stop()
        except Exception:
            LOGGER("BrandrdXMusic").exception(
                "Failed to stop the voice call client"
            )

        try:
            await userbot.stop()
        except Exception:
            LOGGER("BrandrdXMusic").exception(
                "Failed to stop the assistant client"
            )

        try:
            await app.stop()
        except Exception:
            LOGGER("BrandrdXMusic").exception(
                "Failed to stop the bot client"
            )

        LOGGER("BrandrdXMusic").info(
            "BrandrdXMusic stopped."
        )


if __name__ == "__main__":
    asyncio.run(init())
