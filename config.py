import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", None)
MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", None)
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 900))

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", None))

# Get this value from @BRANDRD_ROBOT on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", 6642099030))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/Kurama-fox/princeMusic.git",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/+PYBPkeXKPpRlNzZl")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/+PYBPkeXKPpRlNzZl")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))


# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "bcfe26b0ebc3428882a0b5fb3e872473")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "907c6a054c214005aeae1fd752273cc4")


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "50"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))

SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "180"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "2000"))

# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes


# Get your pyrogram v2 session from @BRANDEDSTRINGSESSION_BOT on Telegram
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}


START_IMG_URL = getenv(
    "START_IMG_URL", "https://wallpapers.com/images/high/neon-anime-musical-artist-hatsune-miku-7y1x3vtfjuin2wr1.webp"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://wallpapers.com/images/high/music-anime-red-hair-61ybliqiyj5nw12e.webp"
)
PLAYLIST_IMG_URL = "https://img.freepik.com/free-photo/girl-with-guitar-shirt-that-says-i-am-girl_1340-32640.jpg?t=st=1706883265~exp=1706886865~hmac=e5cde86421afcfc0bec2b8f79aa79fe6466760dc0031021285b37b369aec34f0&w=1380"
STATS_IMG_URL = "https://img.freepik.com/free-photo/front-view-anime-couple-playing-guitar_23-2150970747.jpg?t=st=1706883360~exp=1706886960~hmac=6d920a865401fd1b7ba3020ebb926d689067634ce91bf2a305f553b661f0474b&w=1800"
TELEGRAM_AUDIO_URL = "https://img.freepik.com/free-vector/gradient-lo-fi-illustration_23-2149375747.jpg?w=996&t=st=1706883497~exp=1706884097~hmac=71770d5c7d25392d24ed70b505387db809f45a6f8a60ae0e6f1619bfc08f1ba6"
TELEGRAM_VIDEO_URL = "https://img.freepik.com/free-photo/beautiful-anime-character-cartoon-scene_23-2151035171.jpg?t=st=1706883738~exp=1706887338~hmac=d97e22f5584f9ee31a75b6000682e44fe801f64244728007226c7d405abe061e&w=740"
STREAM_IMG_URL = "https://img.freepik.com/free-photo/full-shot-ninja-wearing-equipment_23-2150960820.jpg?t=st=1706883873~exp=1706887473~hmac=d3b31e7926ffa9cdcbfffc50365dd1cbac415654e38d4c55e95640a2444f8c9c&w=740"
SOUNCLOUD_IMG_URL = "https://img.freepik.com/free-photo/still-life-with-musical-instrument_23-2150466299.jpg?t=st=1706883961~exp=1706887561~hmac=7924e44990d107828e235c265e7015dcfcf6f956f97eba08e421efaae8394870&w=740"
YOUTUBE_IMG_URL = "https://img.freepik.com/free-photo/men-women-embrace-sunset-generative-ai_188544-12581.jpg?w=1800&t=st=1706884154~exp=1706884754~hmac=cf5484517938030f03e02f1d0b63505cafa322150b43bda337a93f1f615f8964"
SPOTIFY_ARTIST_IMG_URL = "https://img.freepik.com/free-photo/medium-shot-anime-couple-hugging_23-2150970652.jpg?t=st=1706884323~exp=1706887923~hmac=42fb5fa6f6bac5c0da99f471ba78a816f1e7e12943ceb3ce79cd5c2b87dbb7fd&w=1380"
SPOTIFY_ALBUM_IMG_URL = "https://img.freepik.com/free-photo/medium-shot-couple-hugging-fantasy-world_23-2150900443.jpg?t=st=1706884413~exp=1706888013~hmac=17b090baeb7fe4b24cb70f4bb3b91350f1e7e3bf40b6de2525c1580f58a99140&w=996"
SPOTIFY_PLAYLIST_IMG_URL = "https://img.freepik.com/free-photo/full-shot-couple-hugging-fantasy-world_23-2150900473.jpg?t=st=1706884471~exp=1706888071~hmac=9f25d303cfdd9f173d42add803a037f2c8e0f40c5a9422bf18520aeb1674a13b&w=996"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
