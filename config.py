import re
import os
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = 26268653
API_HASH = "fe49634b55eea98671533859d04ea81d"
BOT_TOKEN = "5759235328:AAFYSpHzvjCSvReZ5Q92cefapPOpqv2hZxU"
MONGO_DB_URI = "mongodb+srv://Yash1:Yash1@cluster0.jvuxh49.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 120))
MUSIC_BOT_NAME = "˹ʟʙ ✘ ᴍᴜꜱɪᴄ˼"
LOGGER_ID= -1001861619812
OWNER_ID = 5016109398

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/Visionx-x/BrandrdXMusic",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/learningbots79")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/learning_bots")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))

# Auto Gcast/Broadcast Handler (True = broadcast on , False = broadcast off During Hosting, Dont Do anything here.)
AUTO_GCAST = os.getenv("AUTO_GCAST")

# Auto Broadcast Message That You Want Use In Auto Broadcast In All Groups.
AUTO_GCAST_MSG = getenv("AUTO_GCAST_MSG", "")

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


# Get your pyrogram v2 session
STRING1 = "BQFFG-oAmoOyYFzqZStPa0q7dtgCC6sb-bX4ul8cymQst2_ENpIf9nF-HlEyilQwkEi5hZylZlIMI9wEARv_l-rUa-b0WkQuVowOvCBhlDr3Q4HQd62KxFvcfqnEeuwXvbC4U1ViTwhBEEOqeXlhBqZaynUj1bJM6E0Yqp-Ep3fMik3tn2aEupxH7si7IgmnYPVSIPFM1z8PTuH9lf77D0unxEuDrX8IwBm5MCsDYMYoxcddyxjdCW_2mfZcg4QPcP3-4jMBNkxv7w0tGaMPDR_aBSSriNexR6cmqY6ydmtGlM1grRpzm0HzuT2FDEAhu9hngyG8OCll3gx1IXiSCS7DfRUAywAAAAF-tP5GAA"
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
    "START_IMG_URL", "https://graph.org/file/cc290ee58069d09a1ade7.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://graph.org/file/cc290ee58069d09a1ade7.jpg"
)
PLAYLIST_IMG_URL = "https://graph.org/file/cc290ee58069d09a1ade7.jpg"
STATS_IMG_URL = "https://graph.org/file/cc290ee58069d09a1ade7.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org/file/cc290ee58069d09a1ade7.jpg"
TELEGRAM_VIDEO_URL = "https://graph.org/file/cc290ee58069d09a1ade7.jpg"
STREAM_IMG_URL = "https://graph.org/file/cc290ee58069d09a1ade7.jpg"
SOUNCLOUD_IMG_URL = "https://graph.org/file/cc290ee58069d09a1ade7.jpg"
YOUTUBE_IMG_URL = "https://graph.org/file/cc290ee58069d09a1ade7.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://graph.org/file/cc290ee58069d09a1ade7.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://graph.org/file/cc290ee58069d09a1ade7.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://graph.org/file/cc290ee58069d09a1ade7.jpg"

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
