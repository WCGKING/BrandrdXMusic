import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums, Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from BrandrdXMusic import app
from time import time
import asyncio
from BrandrdXMusic.utils.extraction import extract_user

# Define a dictionary to track the last message timestamp for each user
user_last_message_time = {}
user_command_count = {}
# Define the threshold for command spamming (e.g., 20 commands within 60 seconds)
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5

# ------------------------------------------------------------------------------- #

chatQueue = []

stopProcess = False

# ------------------------------------------------------------------------------- #


@Client.on_message(filters.command(["zombies", "Deletedaccounts"]))
async def remove(client, message):

    global stopProcess
    try:
        try:
            sender = await client.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except:
            has_permissions = message.sender_chat
        if has_permissions:
            bot = await client.get_chat_member(message.chat.id, "self")
            if client.status == ChatMemberStatus.MEMBER:
                await message.reply(
                    "Eu preciso de permissões de admin para remover contas excluídas."
                )
            else:
                if len(chatQueue) > 30:
                    await message.reply(
                        "Dá um tempo! Estou trabalhando no meu número máximo de 30 chats no momento. Tente novamente mais tarde."
                    )
                else:
                    if message.chat.id in chatQueue:
                        await message.reply(
                            "PORRA! ESPERA! Já tem um processo em andamento aqui caraio. Pelo menos usa /stop para iniciar um novo."
                        )
                    else:
                        chatQueue.append(message.chat.id)
                        deletedList = []
                        async for member in client.get_chat_members(message.chat.id):
                            if member.user.is_deleted == True:
                                deletedList.append(member.user)
                            else:
                                pass
                        lenDeletedList = len(deletedList)
                        if lenDeletedList == 0:
                            await message.reply("Nenhuma conta excluída neste grupo.")
                            chatQueue.remove(message.chat.id)
                        else:
                            k = 0
                            processTime = lenDeletedList * 1
                            temp = await client.send_message(
                                message.chat.id,
                                f"Total de {lenDeletedList} contas excluídas foram detectadas..\nTempo estimado: {processTime} segundos a partir de agora.",
                            )
                            if stopProcess:
                                stopProcess = False
                            while len(deletedList) > 0 and not stopProcess:
                                deletedAccount = deletedList.pop(0)
                                try:
                                    await client.ban_chat_member(
                                        message.chat.id, deletedAccount.id
                                    )
                                except Exception:
                                    pass
                                k += 1
                                await asyncio.sleep(10)
                            if k == lenDeletedList:
                                await message.reply(
                                    f"✅ Removido com sucesso todas as contas excluídas nesse grupo.."
                                )
                                await temp.delete()
                            else:
                                await message.reply(
                                    f"✅ Removido com sucesso {k} contas excluídas nesse grupo."
                                )
                                await temp.delete()
                            chatQueue.remove(message.chat.id)
        else:
            await message.reply(
                "Foi mal, mas só os **admin buceta** daqui conseguem usar esse comando."
            )
    except FloodWait as e:
        await asyncio.sleep(e.value)


# ------------------------------------------------------------------------------- #


@Client.on_message(filters.command(["admins", "staff"]))
async def admins(client, message):

    try:
        adminList = []
        ownerList = []
        async for admin in client.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        ):
            if admin.privileges.is_anonymous == False:
                if admin.user.is_bot == True:
                    pass
                elif admin.status == ChatMemberStatus.OWNER:
                    ownerList.append(admin.user)
                else:
                    adminList.append(admin.user)
            else:
                pass
        lenAdminList = len(ownerList) + len(adminList)
        text2 = f"**ɢʀᴏᴜᴘ sᴛᴀғғ - {message.chat.title}**\n\n"
        try:
            owner = ownerList[0]
            if owner.username == None:
                text2 += f"👑 Dono:\n└ {owner.mention}\n\n👮🏻 Admins\n"
            else:
                text2 += f"👑 Dono\n└ @{owner.username}\n\n👮🏻 Admins\n"
        except:
            text2 += f"👑 Dono\n└ <i>Hidden</i>\n\n👮🏻 Admins\n"
        if len(adminList) == 0:
            text2 += "└ <i>Admins estão ocultos.</i>"
            await client.send_message(message.chat.id, text2)
        else:
            while len(adminList) > 1:
                admin = adminList.pop(0)
                if admin.username == None:
                    text2 += f"├ {admin.mention}\n"
                else:
                    text2 += f"├ @{admin.username}\n"
            else:
                admin = adminList.pop(0)
                if admin.username == None:
                    text2 += f"└ {admin.mention}\n\n"
                else:
                    text2 += f"└ @{admin.username}\n\n"
            text2 += f"✅ **Número total de admins**: {lenAdminList}"
            await client.send_message(message.chat.id, text2)
    except FloodWait as e:
        await asyncio.sleep(e.value)


# ------------------------------------------------------------------------------- #


@Client.on_message(filters.command("bots"))
async def bots(client, message):

    try:
        botList = []
        async for bot in client.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.BOTS
        ):
            botList.append(bot.user)
        lenBotList = len(botList)
        text3 = f"**Lista de BOT - {message.chat.title}**\n\n🤖 BOTs\n"
        while len(botList) > 1:
            bot = botList.pop(0)
            text3 += f"├ @{bot.username}\n"
        else:
            bot = botList.pop(0)
            text3 += f"└ @{bot.username}\n\n"
            text3 += f"✅ **Número total de BOTs**: {lenBotList}**"
            await client.send_message(message.chat.id, text3)
    except FloodWait as e:
        await asyncio.sleep(e.value)


# ------------------------------------------------------------------------------- #
