import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = 21306346
API_HASH = "506b68cd27bef3595cf02a605094c11b"
BOT_TOKEN = "7188036509:AAHn9MIo6fkIHfqx1swhS6-BfSQmJRPdMEQ"
MONGO_DB_URI = "mongodb+srv://Bhumi:Bhumi99@cluster0.ue8p4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 60))

LOG_GROUP_ID = -1002244957657
OWNER_ID = 1321591503

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/rishabhops/alice",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/TIGERBHUMISINGH")
SUPPORT_CHAT = getenv("SUPPORT_GROUP", "https://t.me/+DzLMBmzrr0g5M2Vl")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))


# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))


# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 2145386496))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes


# Get your pyrogram v2 session from Replit
STRING1 = "24556677-LWyyyopFA6lOJPew1BQ-hu-dzqY2NkTYFubl3lp3Dpa0_cxyRFZy61K0S38iPBpjSObm3qNYnE25Ja94SrSkecVMKz8DHwyK6Km34WT-3dS1P17eEX2C13cbLsbWLwBUn-J1-lllVUEOxdL0v8hlLRbOwkde1qphWn5_WwM1nlU3Qp7N2YyysxR5aMI55cizsGHMX3O5b8ny76M5fjJBqd_a6tWhLFKKD1v5GVTj_r389vhPh4EDp21GJpHMgHLjkXEgAAAAF-tP5GAA"
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
    "START_IMG_URL", "https://graph.org/file/f2a2bfb6c39b29a8e4ecc.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://graph.org/file/f2a2bfb6c39b29a8e4ecc.jpg"
)
PLAYLIST_IMG_URL = "https://graph.org/file/f2a2bfb6c39b29a8e4ecc.jpg"
STATS_IMG_URL = "https://graph.org/file/f2a2bfb6c39b29a8e4ecc.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org/file/f2a2bfb6c39b29a8e4ecc.jpg"
TELEGRAM_VIDEO_URL = "https://graph.org/file/f2a2bfb6c39b29a8e4ecc.jpg"
STREAM_IMG_URL = "https://graph.org/file/f2a2bfb6c39b29a8e4ecc.jpg"
SOUNCLOUD_IMG_URL = "https://graph.org/file/f2a2bfb6c39b29a8e4ecc.jpg"
YOUTUBE_IMG_URL = "https://graph.org/file/f2a2bfb6c39b29a8e4ecc.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://graph.org/file/f2a2bfb6c39b29a8e4ecc.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://graph.org/file/f2a2bfb6c39b29a8e4ecc.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://graph.org/file/f2a2bfb6c39b29a8e4ecc.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_GROUP:
    if not re.match("(?:http|https)://", SUPPORT_GROUP):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_GROUP url is wrong. Please ensure that it starts with https://"
        )
