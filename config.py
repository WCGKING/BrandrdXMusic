import re
import os
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = "24542160"
API_HASH = "143ef5efcaf0f2b259dcd0ea2cfaf336"

# Get your token from @BotFather on Telegram.
BOT_TOKEN = "7643915863:AAEqo5PJCI1K13iJliOFr9epYkWTr3jywAM"

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = "mongodb://anshganava4444:anshganava4444@cluster0-shard-00-00.4eott.mongodb.net:27017,cluster0-shard-00-01.4eott.mongodb.net:27017,cluster0-shard-00-02.4eott.mongodb.net:27017/?replicaSet=atlas-jkh5an-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=Cluster0"
MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", None)
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 900))

# Chat id of a group for logging bot's activities
LOGGER_ID = "-1002035748224"

# Get this value from @Eternal_society on Telegram by /id
OWNER_ID = "5031182800"

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/WCGKING/BrandrdXMusic",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = "https://t.me/et_bot_logs"
SUPPORT_CHAT = "https://t.me/sorcerers_680"
                                                 

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


# Get your pyrogram v2 session from @BRANDEDSTRINGSESSION_BOT on Telegram
STRING1 = "BQF2e9AAvzU0MWYTricZt9y2mMnUZu55Gwt8GotIZ7npPEtCTB8qyR32nPHBo5WF_hSkt6TZf5-E4h6EYHmAz2MGjjq5BGJIfyrbj-Pizdln7byUKAqWRN7N5QwOyCKA-R55CZc0mBlOP9ILXgrlAr1VlTku9BNaHc_hv6o4cJGtcBVoDJSyeUfLRMp_3uaqBrWSF9i-8qVNfB2veHagwACVKRfjhru1vGJfHN_HebeJDveLzWDprY4bvtGZcP9LGpuwXlwiRkjNId87tBTGorj2yS86qfV19vrWOcaQICsULrMuUzZ8BkTRpzND_ZXqQs8e3nX1_FqLOu9luU7zotpE3ut6DgAAAAEr4cHQAA"
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


START_IMG_URL = "https://i.ibb.co/23X2SMdq/1fa2ead78035.jpg"
    "START_IMG_URL", "https://te.legra.ph/file/62c76ac2095332a0ede75.jpg"
)
PING_IMG_URL = "https://i.ibb.co/C32LkWrx/ec3cb5d8cce0.jpg"
    "PING_IMG_URL", "https://te.legra.ph/file/4f59fb748e1990acfa297.jpg"
)
PLAYLIST_IMG_URL = "https://i.ibb.co/C32LkWrx/ec3cb5d8cce0.jpg"
STATS_IMG_URL = "https://i.ibb.co/C32LkWrx/ec3cb5d8cce0.jpg"
TELEGRAM_AUDIO_URL = "https://i.ibb.co/C32LkWrx/ec3cb5d8cce0.jpg"
TELEGRAM_VIDEO_URL = "https://i.ibb.co/C32LkWrx/ec3cb5d8cce0.jpg"
STREAM_IMG_URL = "https://i.ibb.co/C32LkWrx/ec3cb5d8cce0.jpg"
SOUNCLOUD_IMG_URL = "https://i.ibb.co/C32LkWrx/ec3cb5d8cce0.jpg"
YOUTUBE_IMG_URL = "https://i.ibb.co/C32LkWrx/ec3cb5d8cce0.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://i.ibb.co/7JfhcMnv/37ff54f50ea1.jp"
SPOTIFY_ALBUM_IMG_URL = "https://i.ibb.co/7JfhcMnv/37ff54f50ea1.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://i.ibb.co/7JfhcMnv/37ff54f50ea1.jpg"


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
