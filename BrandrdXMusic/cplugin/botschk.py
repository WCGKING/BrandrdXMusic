import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from dotenv import load_dotenv
import config
from BrandrdXMusic.core.userbot import Userbot
from BrandrdXMusic import app
from datetime import datetime
from BrandrdXMusic.utils.database import get_assistant

# Assuming Userbot is defined elsewhere

last_checked_time = None


@Client.on_message(filters.command("botschk"))
async def check_bots_command(client, message):
    global last_checked_time
    try:
        # Start the Pyrogram client
        userbot = await get_assistant(message.chat.id)

        # Get current time before sending messages
        start_time = datetime.now()

        # Extract bot username from command
        command_parts = message.command
        if len(command_parts) == 2:
            bot_username = command_parts[1]
            response = ""  # Define response variable
            try:
                bot = await userbot.get_users(bot_username)
                bot_id = bot.id
                await asyncio.sleep(0.5)
                await userbot.send_message(bot_id, "/start")
                await asyncio.sleep(3)
                # Check if bot responded to /start message
                async for bot_message in userbot.get_chat_history(bot_id, limit=1):
                    if bot_message.from_user.id == bot_id:
                        response += (
                            f"╭⎋ {bot.mention}\n l\n╰⊚ **Status: TRABALHANDO 🟢**\n\n"
                        )
                    else:
                        response += f"╭⎋ [{bot.mention}](tg://user?id={bot.id})\n l\n╰⊚ **Status: DE FOLGA 🔴**\n\n"
            except Exception:
                response += f"╭⎋ {bot_username}\n l\n╰⊚ **Ou você forneceu o nome de usuário errado, caso contrário não posso verificar devido à limitação. **\n\n"
            # Update last checked time
            last_checked_time = start_time.strftime("%Y-%m-%d")
            await message.reply_text(f"{response}⏲️ Última verificação: {last_checked_time}")
        else:
            await message.reply_text(
                "Formato de comando inválido.\n\n Por favor use /botschk Nome_Bot\n\nTente :- `/botschk @COMBINADOMUSIC_bot`"
            )
    except Exception as e:
        await message.reply_text(f"Alguma coisa deu errado aí: {e}")
        print(f"Deu b.o durante o comando /botschk : {e}")
