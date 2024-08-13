import future
import asyncio
import os
import time
from urllib.parse import urlparse
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)
import wget
from pyrogram import filters
from pyrogram.types import Message
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
from BrandrdXMusic import app
import asyncio
import os
import time
import wget
from urllib.parse import urlparse
from pyrogram import filters
from pyrogram.types import Message
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
from BrandrdXMusic import app
from time import time
import asyncio
from BrandrdXMusic.utils.extraction import extract_user
import asyncio
import os
import wget
from pyrogram import filters
from pyrogram.types import Message
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL

from BrandrdXMusic import app
from BrandrdXMusic.utils.extraction import extract_user
from time import time
from BrandrdXMusic.utils.extraction import extract_user
from urllib.parse import urlparse
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters, Client
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
from BrandrdXMusic import app
import wget

# Define a dictionary to track the last query timestamp for each user
user_last_CallbackQuery_time = {}
user_CallbackQuery_count = {}

# Define the threshold for query spamming (e.g., 1 query within 60 seconds)
SPAM_THRESHOLD = 1
SPAM_WINDOW_SECONDS = 30

SPAM_AUDIO_THRESHOLD = 1
SPAM_AUDIO_WINDOW_SECONDS = 30

BANNED_USERS = []


@Client.on_callback_query(filters.regex("downloadvideo") & ~filters.user(BANNED_USERS))
async def download_video(client, CallbackQuery):
    user_id = CallbackQuery.from_user.id
    current_time = time.time()
    cme = await client.get_me()

    # Check if the user has exceeded the query limit
    last_Query_time = user_last_CallbackQuery_time.get(user_id, 0)
    if current_time - last_Query_time < SPAM_WINDOW_SECONDS:
        # If the limit is exceeded, send a response and return
        await CallbackQuery.answer(
            "➻ Teu vídeo já tá pronto, me chama no pv, não enviei nada íntimo meu, relaxa.\n\n➥ Download da próxima música só depois de 30 segundos.",
            show_alert=True,
        )
        return
    else:
        # Update the last query time and query count
        user_last_CallbackQuery_time[user_id] = current_time
        user_CallbackQuery_count[user_id] = user_CallbackQuery_count.get(user_id, 0) + 1

    callback_data = CallbackQuery.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = CallbackQuery.from_user.id
    user_name = CallbackQuery.from_user.first_name
    chutiya = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    await CallbackQuery.answer("Tá, peraí...", show_alert=True)
    pablo = await client.send_message(
        CallbackQuery.message.chat.id,
        f"**Ei {chutiya}, peraí... tô baixando o teu vídeo...**",
    )
    if not videoid:
        await pablo.edit(
            f"**Pô {chutiya}, essa merda tua não achei no YouTube, tenta de novo (por mais que eu não vá fazer milagres)...**"
        )
        return

    search = SearchVideos(
        f"https://youtube.com/{videoid}", offset=1, mode="dict", max_results=1
    )
    mi = search.result()
    mio = mi.get("search_result", [])
    if not mio:
        await pablo.edit(
            f"**Pô {chutiya}, essa merda tua não achei no YouTube, tenta de novo (por mais que eu não vá fazer milagres)...**"
        )
        return

    mo = mio[0].get("link", "")
    thum = mio[0].get("title", "")
    fridayz = mio[0].get("id", "")
    thums = mio[0].get("channel", "")
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)

    except Exception as e:
        await pablo.edit(
            f"**Fala tu {chutiya}. Deu ruim pra baixar tua música.** \n**Foi esse erro aqui:** `{str(e)}`"
        )
        return

    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"Título:** [{thum}]({mo})\n\n**Canal:** {thums}\n\n**Solicitado por:** {chutiya}"
    try:
        await client.send_video(
            CallbackQuery.from_user.id,
            video=open(file_stark, "rb"),
            duration=int(ytdl_data["duration"]),
            file_name=str(ytdl_data["title"]),
            thumb=sedlyf,
            caption=capy,
            supports_streaming=True,
            progress_args=(
                pablo,
                f"**{chutiya} guenta aí...**\n\n**Enviando vídeo do YouTube...**",
                file_stark,
            ),
        )
        await client.send_message(
            CallbackQuery.message.chat.id,
            f"**Ei** {chutiya}\n\n**Baixei essa merda...**\n**➻ Áudio enviado no seu pv, não enviei nada íntimo meu, relaxa.**\n**➥ Clica [AQUI](tg://openmessage?user_id={cme.id})**",
        )
        await pablo.delete()
        for files in (sedlyf, file_stark):
            if files and os.path.exists(files):
                os.remove(files)

    except Exception as e:
        await pablo.delete()
        return await client.send_message(
            CallbackQuery.message.chat.id,
            f"**Pqp {chutiya} tem como me desbloquear para eu baixar o seu MARAVILHOSO VÍDEO cacete?!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"DESBLOQUEAR",
                            url=f"https://t.me/{cme.username}?start=info_{videoid}",
                        )
                    ]
                ]
            ),
        )


import os
import time

# Dicts to keep track of user query count and last query time
user_last_CallbackQuery_time = {}
user_CallbackQuery_count = {}


@Client.on_callback_query(filters.regex("downloadaudio") & ~filters.user(BANNED_USERS))
async def download_audio(client, CallbackQuery):
    user_id = CallbackQuery.from_user.id
    current_time = time.time()
    cme = await client.get_me()

    # Check if the user has exceeded the query limit
    last_Query_time = user_last_CallbackQuery_time.get(user_id, 0)
    if current_time - last_Query_time < SPAM_AUDIO_WINDOW_SECONDS:
        # If the limit is exceeded, send a response and return
        await CallbackQuery.answer(
            "➻ Tem alzheimer é?! Tu já pediu pra baixar esse essa porcaria, vai no pv checar no meu pv.\n\n➥ Download da próxima música só depois de 30 segundos.",
            show_alert=True,
        )
        return
    else:
        # Update the last query time and query count
        user_last_CallbackQuery_time[user_id] = current_time
        user_CallbackQuery_count[user_id] = user_CallbackQuery_count.get(user_id, 0) + 1

    callback_data = CallbackQuery.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = CallbackQuery.from_user.id
    user_name = CallbackQuery.from_user.first_name
    chutiya = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    await CallbackQuery.answer("Tá, peraí...", show_alert=True)
    pablo = await client.send_message(
        CallbackQuery.message.chat.id,
        f"**Ei {chutiya}, peraí... tô baixando o teu vídeo...**",
    )
    if not videoid:
        await pablo.edit(
            f"**Pô {chutiya}, essa merda tua não achei no YouTube, tenta de novo (por mais que eu não vá fazer milagres)...**"
        )
        return

    search = SearchVideos(
        f"https://youtube.com/{videoid}", offset=1, mode="dict", max_results=1
    )
    mi = search.result()
    mio = mi.get("search_result", [])
    if not mio:
        await pablo.edit(
            f"**Pô {chutiya}, essa merda tua não achei no YouTube, tenta de novo (por mais que eu não vá fazer milagres)...**"
        )
        return

    mo = mio[0].get("link", "")
    thum = mio[0].get("title", "")
    fridayz = mio[0].get("id", "")
    thums = mio[0].get("channel", "")
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "bestaudio/best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "outtmpl": "%(id)s.mp3",  # Output format changed to mp3
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)

    except Exception as e:
        await pablo.edit(
            f"**Fala tu {chutiya}. Deu ruim pra baixar tua música.** \n**Foi esse erro aqui:** `{str(e)}`"
        )
        return

    file_stark = f"{ytdl_data['id']}.mp3"  # Adjusted file extension
    capy = f"**Título:** [{thum}]({mo})\n\n**Canal:** {thums}\n\n**Solicitado por:** {chutiya}\n\n**Duração:** {int(ytdl_data['duration']) // 60}:{int(ytdl_data['duration']) % 60}"
    try:
        await client.send_audio(
            CallbackQuery.from_user.id,
            audio=open(file_stark, "rb"),
            title=str(ytdl_data["title"]),
            thumb=sedlyf,
            caption=capy,
            progress_args=(
                pablo,
                f"**{chutiya} guenta aí...**\n\n**Enviando vídeo do YouTube**",
                file_stark,
            ),
        )
        await client.send_message(
            CallbackQuery.message.chat.id,
            f"Ei {chutiya}**\n\nBaixei essa merda...**\n**➻ Áudio enviado no seu pv, não enviei nada íntimo meu, relaxa.**\n**➥  Clica [AQUI](tg://openmessage?user_id={cme.id})**",
        )

        await pablo.delete()
        for files in (sedlyf, file_stark):
            if files and os.path.exists(files):
                os.remove(files)

    except Exception as e:
        await pablo.delete()
        return await client.send_message(
            CallbackQuery.message.chat.id,
            f"**Pqp {chutiya} tem como me desbloquear para eu baixar o seu MARAVILHOSO VÍDEO cacete?!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"DESBLOQUEAR",
                            url=f"https://t.me/{cme.username}?start=info_{videoid}",
                        )
                    ]
                ]
            ),
        )
