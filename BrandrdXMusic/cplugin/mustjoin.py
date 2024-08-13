from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from BrandrdXMusic import app
from config import SUPPORT_CHANNEL

# --------------------------

MUST_JOIN = SUPPORT_CHANNEL.split("/")[-1]


# ------------------------
@Client.on_message(filters.incoming & filters.private, group=-17)
async def must_join_channel(client: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_photo(
                    photo="https://graph.org/file/3fb3f4c8a1250c6a50af1.jpg",
                    caption=f"Tô vendo aqui que tu não entrou no [grupo suporte]({link}) Mas se tu quiser me usar (lá ele) entra no [grupo suporte]({link}) e tenta de novo. ",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("ENTRAR", url=link),
                            ]
                        ]
                    ),
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"Me deixa como administrador no chat: {MUST_JOIN} (MUST_JOIN)!")
