#https://github.com/WCGKING/BrandrdXMusic

import random
import re
import string

import lyricsgenius as lg
from requests.exceptions import HTTPError, RequestException
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from BrandrdXMusic import app
from BrandrdXMusic.utils.decorators.language import language
from config import BANNED_USERS, lyrical


# Use your Genius API token here.
# Prefer storing it in an environment variable.
api_key = "YOUR_GENIUS_API_TOKEN"

y = lg.Genius(
    api_key,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    remove_section_headers=True,
)
y.verbose = False


@app.on_message(filters.command(["lyrics"]) & ~BANNED_USERS)
@language
async def lrsearch(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(_["lyrics_1"])

    title = message.text.split(None, 1)[1].strip()
    if not title:
        return await message.reply_text(_["lyrics_1"])

    m = await message.reply_text(_["lyrics_2"])

    try:
        song = y.search_song(title, get_full_info=False)
    except (HTTPError, RequestException) as e:
        print(f"Lyrics Genius HTTP error: {e}")
        return await m.edit(
            "Lyrics search is temporarily unavailable. Please try again later."
        )
    except Exception as e:
        print(f"Lyrics search error: {e}")
        return await m.edit(
            "Could not fetch lyrics right now. Please try again later."
        )

    if song is None:
        return await m.edit(_["lyrics_3"].format(title))

    lyric = song.lyrics or ""
    if not lyric.strip():
        return await m.edit(_["lyrics_3"].format(title))

    lyric = re.sub(r"\d*Embed", "", lyric).strip()

    ran_hash = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=10)
    )
    lyrical[ran_hash] = lyric

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["L_B_1"],
                    url=f"https://t.me/{app.username}?start=lyrics_{ran_hash}",
                )
            ]
        ]
    )

    return await m.edit(_["lyrics_4"], reply_markup=upl)
