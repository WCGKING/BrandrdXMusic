import os
import random
import html
import asyncio
from datetime import datetime, timedelta

from telegraph import upload_file
from pyrogram.enums import ButtonStyle
from PIL import Image, ImageDraw, ImageFont
from pyrogram import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType, ParseMode

# BOT FILE NAME
from BrandrdXMusic import app as app
from BrandrdXMusic.mongo.couples_db import _get_image, get_couple


POLICE = [
    [
        InlineKeyboardButton(
            text="🥀 ᴍʏ ᴄᴜᴛᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ 🥀",
            url="https://t.me/BRANDED_PAID_CC",
            style=ButtonStyle.DANGER,
        ),
    ],
]


def dt():
    now = datetime.now()
    return [
        now.strftime("%d/%m/%Y %H:%M"),
        now.strftime("%d/%m/%Y"),
    ]


def dt_tom():
    return (
        datetime.now() + timedelta(days=1)
    ).strftime("%d/%m/%Y")


def get_font(size, bold=False):
    """Load a readable font with a fallback."""
    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]

    for font_path in fonts:
        try:
            return ImageFont.truetype(font_path, size)
        except OSError:
            continue

    return ImageFont.load_default()


def fit_font(draw, text, max_width, size, bold=True):
    """Fit text inside a maximum width."""
    while size > 12:
        font = get_font(size, bold)
        bbox = draw.textbbox((0, 0), text, font=font)

        if bbox[2] - bbox[0] <= max_width:
            return font

        size -= 2

    return get_font(size, bold)


def draw_centered_text(draw, center_x, center_y, text, font, fill):
    """Draw text using its visual center."""
    draw.text(
        (center_x, center_y),
        text,
        font=font,
        fill=fill,
        anchor="mm",
    )


@app.on_message(filters.command("couples"))
async def ctest(_, message):
    cid = message.chat.id

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "💖 ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs."
        )

    msg = None
    output_file = f"test_{cid}.png"
    p1 = None
    p2 = None

    try:
        # GENERATING MESSAGE
        msg = await message.reply_text(
            "<b>💞 ɢᴇɴᴇʀᴀᴛɪɴɢ ᴄᴏᴜᴘʟᴇs ɪᴍᴀɢᴇ... ✨</b>",
            parse_mode=ParseMode.HTML,
        )

        # GET LIST OF USERS
        list_of_users = []

        async for member in app.get_chat_members(cid, limit=50):
            if not member.user.is_bot:
                list_of_users.append(member.user.id)

        if len(list_of_users) < 2:
            await msg.edit_text(
                "❌ ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴜsᴇʀs ᴛᴏ sᴇʟᴇᴄᴛ ᴀ ᴄᴏᴜᴘʟᴇ."
            )
            return

        # SELECT TWO DIFFERENT USERS
        c1_id, c2_id = random.sample(list_of_users, 2)

        # GET USER INFORMATION
        user1 = await app.get_users(c1_id)
        user2 = await app.get_users(c2_id)

        c1_name = html.escape(user1.first_name or "User")
        c2_name = html.escape(user2.first_name or "User")

        # ACTUAL USERNAMES FOR IMAGE
        c1_username = (
            f"@{user1.username}"
            if user1.username
            else user1.first_name or "User"
        )
        c2_username = (
            f"@{user2.username}"
            if user2.username
            else user2.first_name or "User"
        )

        # DATE FOR IMAGE AND CAPTION
        tomorrow = dt_tom()
        today = datetime.now().strftime("%d/%m/%Y")

        # GET PROFILE PHOTOS
        photo1 = (await app.get_chat(c1_id)).photo
        photo2 = (await app.get_chat(c2_id)).photo

        try:
            if not photo1:
                raise ValueError("First user has no profile photo")

            p1 = await app.download_media(
                photo1.big_file_id,
                file_name="pfp.png",
            )
        except Exception:
            p1 = "BrandrdXMusic/assets/upic.png"

        try:
            if not photo2:
                raise ValueError("Second user has no profile photo")

            p2 = await app.download_media(
                photo2.big_file_id,
                file_name="pfp1.png",
            )
        except Exception:
            p2 = "BrandrdXMusic/assets/upic.png"

        # OPEN IMAGES
        with Image.open(p1) as source:
            img1 = source.convert("RGBA")

        with Image.open(p2) as source:
            img2 = source.convert("RGBA")

        with Image.open(
            "BrandrdXMusic/assets/cppicbranded.jpg"
        ) as source:
            img = source.convert("RGBA")

        # PROFILE PHOTO SIZE AND POSITIONS
        # Coordinates are for the supplied 1536 x 1024 background.
        photo_size = 340

        img1 = img1.resize(
            (photo_size, photo_size),
            Image.Resampling.LANCZOS,
        )
        img2 = img2.resize(
            (photo_size, photo_size),
            Image.Resampling.LANCZOS,
        )

        # CIRCULAR MASK
        mask = Image.new("L", (photo_size, photo_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse(
            (0, 0, photo_size - 1, photo_size - 1),
            fill=255,
        )

        img1.putalpha(mask)
        img2.putalpha(mask.copy())

        # PASTE PROFILE PHOTOS
        img.paste(img1, (235, 316), img1)
        img.paste(img2, (955, 316), img2)

        # DRAW ACTUAL USERNAMES AND DATE ON BACKGROUND
        draw = ImageDraw.Draw(img)

        # ---------------------------------------------
        # FIX 1: REPLACE STATIC @User1 AND @User2 LABELS
        # ---------------------------------------------

        # Cover existing placeholder text within the two labels.
        draw.rounded_rectangle(
            (260, 660, 540, 720),
            radius=24,
            fill=(35, 0, 40, 255),
            outline=(255, 45, 210, 255),
            width=3,
        )

        draw.rounded_rectangle(
            (975, 660, 1275, 720),
            radius=24,
            fill=(0, 15, 45, 255),
            outline=(35, 160, 255, 255),
            width=3,
        )

        # Actual Telegram usernames, or first name if username is absent.
        name1_font = fit_font(
            draw, c1_username, 220, 27, True
        )
        name2_font = fit_font(
            draw, c2_username, 240, 27, True
        )

        draw_centered_text(
            draw,
            400,
            690,
            c1_username,
            name1_font,
            (255, 235, 255, 255),
        )

        draw_centered_text(
            draw,
            1125,
            690,
            c2_username,
            name2_font,
            (235, 245, 255, 255),
        )

        # ---------------------------------------------
        # FIX 2: REPLACE STATIC COUPLE NAMES AT BOTTOM
        # ---------------------------------------------

        # Cover the old @User1 + @User2 = heart text.
        draw.rounded_rectangle(
            (405, 760, 1130, 875),
            radius=25,
            fill=(12, 0, 28, 245),
            outline=(140, 40, 220, 255),
            width=3,
        )

        bottom_font_size = 40
        bottom_font1 = fit_font(
            draw,
            c1_username,
            260,
            bottom_font_size,
            True,
        )
        bottom_font2 = fit_font(
            draw,
            c2_username,
            260,
            bottom_font_size,
            True,
        )

        # Use separate colors for both partners.
        draw_centered_text(
            draw,
            570,
            818,
            c1_username,
            bottom_font1,
            (255, 70, 220, 255),
        )

        draw_centered_text(
            draw,
            755,
            818,
            "+",
            get_font(42, True),
            (255, 255, 255, 255),
        )

        draw_centered_text(
            draw,
            925,
            818,
            c2_username,
            bottom_font2,
            (50, 190, 255, 255),
        )

        # ---------------------------------------------
        # FIX 3: DYNAMIC NEXT COUPLES DATE
        # ---------------------------------------------

        # Cover the old fixed date and date label.
        draw.rounded_rectangle(
            (460, 885, 1080, 970),
            radius=18,
            fill=(10, 0, 30, 245),
        )

        date_label_font = get_font(20, True)
        date_font = get_font(34, True)

        draw_centered_text(
            draw,
            770,
            912,
            "NEXT COUPLES WILL BE SELECTED ON",
            date_label_font,
            (255, 255, 255, 255),
        )

        draw_centered_text(
            draw,
            770,
            950,
            tomorrow,
            date_font,
            (255, 75, 220, 255),
        )

        # SAVE IMAGE
        img.save(output_file, format="PNG")

        # COLOURFUL CAPTION
        TXT = f"""<b><blockquote>
ᴛᴏᴅᴀʏ's sᴇʟᴇᴄᴛᴇᴅ ᴄᴏᴜᴘʟᴇs 🎉
━━━━━━━━━━━━━━━━━━
<a href="tg://openmessage?user_id={c1_id}">{c1_name}</a> 
                           +
<a href="tg://openmessage?user_id={c2_id}">{c2_name}</a> 
━━━━━━━━━━━━━━━━━━
ɴᴇxᴛ ᴄᴏᴜᴘʟᴇs ᴡɪʟʟ ʙᴇ
sᴇʟᴇᴄᴛᴇᴅ ᴏɴ: {tomorrow}
━━━━━━━━━━━━━━━━━━
</blockquote></b>"""

        # SEND COUPLES IMAGE
        await message.reply_photo(
            output_file,
            caption=TXT,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(POLICE),
        )

        # DELETE GENERATING MESSAGE
        try:
            await msg.delete()
        except Exception:
            pass

        msg = None

        # UPLOAD TO TELEGRAPH
        uploaded_files = await asyncio.to_thread(
            upload_file, output_file
        )

        for x in uploaded_files:
            img_url = "https://graph.org/" + x

            couple = {
                "c1_id": c1_id,
                "c2_id": c2_id,
            }

            # Database saving remains disabled, as in your original code.
            # await save_couple(cid, today, couple, img_url)

    except Exception as e:
        print(f"Couples Error: {e}")

        if msg:
            try:
                await msg.edit_text(
                    "❌ ᴄᴏᴜᴘʟᴇs ɪᴍᴀɢᴇ ɢᴇɴᴇʀᴀᴛɪᴏɴ ғᴀɪʟᴇᴅ."
                )
            except Exception:
                pass

    finally:
        # CLEAN UP TEMPORARY FILES
        for path in (
            p1,
            p2,
            output_file,
            "./downloads/pfp.png",
            "./downloads/pfp1.png",
        ):
            try:
                if path and os.path.isfile(path):
                    os.remove(path)
            except Exception:
                pass
