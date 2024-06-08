import os
import random

from PIL import Image, ImageDraw
from pyrogram import filters
from pyrogram.enums import ChatAction, ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import OWNER_ID
from BrandrdXMusic import app


@app.on_message(
    filters.command(
        ["couples", "couple"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
)
async def couples(app, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")
    try:
        msg = await message.reply_text("❣️")
        list_of_users = []

        async for i in app.get_chat_members(message.chat.id, limit=50):
            if not i.user.is_bot and not i.user.is_deleted:
                list_of_users.append(i.user.id)

        c1_id = random.choice(list_of_users)
        c2_id = random.choice(list_of_users)
        while c1_id == c2_id:
            c1_id = random.choice(list_of_users)

        photo1 = (await app.get_chat(c1_id)).photo
        photo2 = (await app.get_chat(c2_id)).photo

        N1 = (await app.get_users(c1_id)).mention
        N2 = (await app.get_users(c2_id)).mention

        try:
            p1 = await app.download_media(photo1.big_file_id, file_name="pfp.png")
        except Exception:
            p1 = "BrandrdXMusic/assets/upic.png"
        try:
            p2 = await app.download_media(photo2.big_file_id, file_name="pfp1.png")
        except Exception:
            p2 = "BrandrdXMusic/assets/upic.png"
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = f"tg://openmessage?user_id={OWNER_ID[0]}"

        img1 = Image.open(f"{p1}")
        img2 = Image.open(f"{p2}")

        img = Image.open("BrandrdXMusic/assets/Couple.png")

        img1 = img1.resize((390, 390))
        img2 = img2.resize((390, 390))

        mask = Image.new("L", img1.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img1.size, fill=255)

        mask1 = Image.new("L", img2.size, 0)
        draw = ImageDraw.Draw(mask1)
        draw.ellipse((0, 0) + img2.size, fill=255)

        img1.putalpha(mask)
        img2.putalpha(mask1)

        draw = ImageDraw.Draw(img)

        img.paste(img1, (125, 196), img1)
        img.paste(img2, (780, 196), img2)

        img.save(f"test_{cid}.png")

        TXT = f"""
**ᴛᴏᴅᴀʏ's sᴇʟᴇᴄᴛᴇᴅ ᴄᴏᴜᴘʟᴇs 🌺 :

{N1} + {N2} = ❣️

**
"""
        await app.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        await message.reply_photo(
            f"test_{cid}.png",
            caption=TXT,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ᴍʏ ᴄᴜᴛᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ 🌋", user_id=OWNER)]]
            ),
        )
        await msg.delete()
        try:
            os.remove(f"./downloads/pfp1.png")
            os.remove(f"./downloads/pfp2.png")
            os.remove(f"test_{cid}.png")
        except Exception:
            pass
    except Exception as e:
        print(str(e))
    try:
        os.remove(f"./downloads/pfp1.png")
        os.remove(f"./downloads/pfp2.png")
        os.remove(f"test_{cid}.png")
    except Exception:
        pass
