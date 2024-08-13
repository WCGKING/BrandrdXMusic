import asyncio
from BrandrdXMusic.misc import SUDOERS
from BrandrdXMusic.core.userbot import Userbot
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from BrandrdXMusic.utils.branded_ban import admin_filter
from BrandrdXMusic.utils.decorators.userbotjoin import UserbotWrapper
from BrandrdXMusic.utils.database import get_assistant, is_active_chat

links = {}


@Client.on_message(
    filters.group & filters.command(["userbotjoin", "assistantjoin"]) & ~filters.private
)
async def join_group(client, message):

    a = await client.get_me()
    chat_id = message.chat.id
    userbot = await get_assistant(message.chat.id)
    userbot_id = userbot.id
    done = await message.reply("**Calma aí enquanto eu tô chamando o meu assistente**...")
    await asyncio.sleep(1)
    # Get chat member object
    chat_member = await client.get_chat_member(chat_id, a.id)

    # Condition 1: Group username is present, bot is not admin
    if (
        message.chat.username
        and not chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        try:
            await userbot.join_chat(message.chat.username)
            await done.edit_text("**✅ O assistente entrou.**")
        except Exception as e:
            await done.edit_text("**Eu preciso de poder de admin para desbanir e convidar meu assistente ôporra!**")

    # Condition 2: Group username is present, bot is admin, and Userbot is not banned
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        try:
            await userbot.join_chat(message.chat.username)
            await done.edit_text("**✅ O assistente entrou.**")
        except Exception as e:
            await done.edit_text(str(e))

    # Condition 3: Group username is not present/group is private, bot is admin and Userbot is banned
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await client.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in [
            ChatMemberStatus.BANNED,
            ChatMemberStatus.RESTRICTED,
        ]:
            try:
                await client.unban_chat_member(chat_id, userbot.id)
                await done.edit_text("**Desbanindo meu assistente...**")
                await userbot.join_chat(message.chat.username)
                await done.edit_text(
                    "**✅ O meu assistente foi banido, mas ainda bem que agora foi desbanido e entrou no grupo, senão eu já tinha derrubado sabosta.**"
                )
            except Exception as e:
                await done.edit_text(
                    "**Não tá dando pra entrar leigo... Me dá permissão de banimento e de convite de usuário ou tira o ban do meu assistente (@zerinhogod) manualmente e tente novamente usando /userbotjoin.**"
                )
        return

    # Condition 4: Group username is not present/group is private, bot is not admin
    if (
        not message.chat.username
        and not chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        await done.edit_text("**Eu preciso de poder de admin para desbanir e convidar meu assistente ôporra!**")

    # Condition 5: Group username is not present/group is private, bot is admin
    if (
        not message.chat.username
        and chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        try:
            try:
                userbot_member = await client.get_chat_member(chat_id, userbot.id)
                if userbot_member.status not in [
                    ChatMemberStatus.BANNED,
                    ChatMemberStatus.RESTRICTED,
                ]:
                    await done.edit_text("**✅ O assistente já entrou.**")
                    return
            except Exception as e:
                await done.edit_text("**Por favor, aguarde enquanto convido o assistente.**.")
                await done.edit_text("**Por favor, aguarde enquanto convido o assistente.**...")
                invite_link = await client.create_chat_invite_link(
                    chat_id, expire_date=None
                )
                await asyncio.sleep(2)
                await userbot.join_chat(invite_link.invite_link)
                await done.edit_text("**✅ Assistente entrou nessa espelunca.**")
        except Exception as e:
            await done.edit_text(
                f"**Descobri que meu assistente não entrou nessa bosta grupo e não consigo convidá-lo porque NÃO TENHO A PORRA DE PERMISSÃO DE ADMIN para convite de usuários. Me dá essa bosta de permissão e tenta novamente com o comando /userbotjoin.**\n\n**➥ ID:** @{userbot.username}"
            )

    # Condition 6: Group username is not present/group is private, bot is admin and Userbot is banned
    if (
        not message.chat.username
        and chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        userbot_member = await client.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in [
            ChatMemberStatus.BANNED,
            ChatMemberStatus.RESTRICTED,
        ]:
            try:
                await client.unban_chat_member(chat_id, userbot.id)
                await done.edit_text(
                    "**Assistente está desbanido.**\n**Assistente está desbanido.:- /userbotjoin.**"
                )
                invite_link = await client.create_chat_invite_link(
                    chat_id, expire_date=None
                )
                await asyncio.sleep(2)
                await userbot.join_chat(invite_link.invite_link)
                await done.edit_text(
                    "**A porra do meu assistente foi banido, agora está desbanido e entrou no chat. Se não fosse tirar, já ia derrubar esse grupo...**"
                )
            except Exception as e:
                await done.edit_text(
                    f"**Descobri que meu assistente não entrou nessa bosta grupo e não consigo convidá-lo porque NÃO TENHO A PORRA DE PERMISSÃO DE ADMIN para convite de usuários. Me dá essa bosta de permissão e tenta novamente com o comando /userbotjoin.**\n\n**➥ ID:** @{userbot.username}"
                )
        return


@Client.on_message(filters.command("userbotleave") & filters.group & admin_filter)
async def leave_one(client, message):
    try:
        userbot = await get_assistant(message.chat.id)
        await userbot.leave_chat(message.chat.id)
        await client.send_message(
            message.chat.id, "**✅ Userbot deixou o grupo.**"
        )
    except Exception as e:
        print(e)


@Client.on_message(filters.command(["leaveall"]) & SUDOERS)
async def leave_all(client, message):
    if message.from_user.id not in SUDOERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **Userbot** saindo de todos os grupos!")
    try:
        userbot = await get_assistant(message.chat.id)
        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1002198719573:
                continue
            try:
                await userbot.leave_chat(dialog.chat.id)
                left += 1
                await lol.edit(
                    f"**Userbot saindo de todos os grupos...**\n\n**Saiu:** {left} chats.\n**Falhou:** {failed} grupos."
                )
            except BaseException:
                failed += 1
                await lol.edit(
                    f"**Userbot saindo...**\n\n**Saiu:** {left} grupos.\n**Falhou:** {failed} grupos."
                )
            await asyncio.sleep(3)
    finally:
        await client.send_message(
            message.chat.id,
            f"**✅ Saiu de:* {left} grupos.\n**❌ Falhou em:** {failed} grupos.",
        )
