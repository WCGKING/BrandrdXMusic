import requests
from pyrogram import filters

from BrandrdXMusic import app


@app.on_message(filters.command(["ig", "instagram", "reel"]))
async def download_instagram_video(client, message):
    if len(message.command) < 2:
        await message.reply_text(
            "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ Iɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ"
        )
        return
    a = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
    url = message.text.split()[1]
    api_url = (
        f"https://nodejs-1xn1lcfy3-jobians.vercel.app/v2/downloader/instagram?url={url}"
    )

    response = requests.get(api_url)
    data = response.json()

    if data["status"]:
        video_url = data["data"][0]["url"]
        await a.delete()
        await client.send_video(message.chat.id, video_url)
    else:
        await a.edit("Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʀᴇᴇʟ")


__MODULE__ = "Iɴsᴛᴀɢʀᴀᴍ"
__HELP__ = """/reel [ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ ᴜʀʟ] - Tᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ʀᴇᴇʟ ʙʏ ʙᴏᴛ
/ig [ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ ᴜʀʟ] - Tᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ʀᴇᴇʟ ʙʏ ʙᴏᴛ
/instagram [ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ ᴜʀʟ] - Tᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ʀᴇᴇʟ ʙʏ ʙᴏᴛ
"""
