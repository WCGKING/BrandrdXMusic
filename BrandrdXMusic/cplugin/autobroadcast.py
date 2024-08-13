import asyncio
import datetime
from pyrogram import Client
from config import START_IMG_URL, AUTO_GCAST_MSG, AUTO_GCAST, LOGGER_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from typing import Dict, List, Union
from BrandrdXMusic.utils.database import get_served_chats_clone
from BrandrdXMusic import userbot
from BrandrdXMusic.core.mongo import mongodb, pymongodb

AUTO_GCAST = True

START_IMG_URLS = "https://te.legra.ph/file/fe4373a26d55df8ed04e5.png"

MESSAGES = f"""**ㅤㅤㅤ⚠️⚠️⚠️⚠️⚠️📡

O combinado nunca sai caro...

**"""


BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "JUNTE-SE A NÓS",
                url=f"https://t.me/combinadomusic",
            )
        ]
    ]
)

MESSAGE = f"""**Sou muito melhor que muita JBL por aí...

🎧 PLAY + VPLAY + CPLAY 🎧

➥ Mensagem de boas vindas - aviso de saída do grupo, tagall, vctag, ban - mute, poesias, letras, músicas - download de vídeo, etc

🔐Use [/start](https://t.me/https://t.me/COMBINADOMUSIC_bot?start=help) para me conhecer.

➲ BOT :** @COMBINADOMUSIC_bot"""

BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "ME ADICIONE NO SEU GRUPO",
                url=f"https://t.me/COMBINADOMUSIC_bot?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users",
            )
        ]
    ]
)

caption = MESSAGES

TEXT = """**O gcast automático está ativado para que o gcast/transmissão automática seja feito em todos os grupos continuamente. **\n**Pode ser interrompido colocando a variável [auto_gcast = (deixe em branco e não escreva nada)]**"""


async def send_message_to_chats(client: Client):
    try:
        chats = await get_served_chats_clone()

        for chat_info in chats:
            chat_id = chat_info.get("chat_id")
            if isinstance(chat_id, int):  # Check if chat_id is an integer
                try:
                    await client.send_photo(
                        chat_id,
                        photo=START_IMG_URLS,
                        caption=caption,
                        reply_markup=BUTTONS,
                    )
                    await asyncio.sleep(
                        1
                    )  # Sleep for 100 second between sending messages
                except Exception as e:
                    pass  # Do nothing if an error occurs while sending message
    except Exception as e:
        pass  # Do nothing if an error occurs while fetching served chats


async def continuous_cbroadcast():
    # Send TEXT once when bot starts

    while True:
        if AUTO_GCAST:
            try:
                await send_message_to_chats(client)
            except Exception as e:
                pass

        # Wait for 100000 seconds before next broadcast
        await asyncio.sleep(5)


# Start the continuous broadcast loop if AUTO_GCAST is True
if AUTO_GCAST:
    asyncio.create_task(continuous_cbroadcast())
