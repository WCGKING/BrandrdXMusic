import sys

from pyrogram import Client

import config

from ..logging import LOGGER

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_name=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_name=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_name=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_name=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_name=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info(f"😁𝐋𝐨𝐚𝐝𝐢𝐧𝐠 𝐘𝐨𝐮𝐫 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭...")
        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("TG_FRIENDSS")
                await self.one.join_chat("VIP_CREATORS")
                await self.one.join_chat("THE_VIP_BOY")
                await self.one.join_chat("THE_VIP_BOY_OP")
            except:
                pass
            assistants.append(1)
            get_me = await self.one.get_me()
            self.one.username = get_me.username
            self.one.id = get_me.id
            self.one.mention = get_me.mention
            assistantids.append(get_me.id)
            if get_me.last_name:
                self.one.name = (
                    get_me.first_name + " " + get_me.last_name
                )
            else:
                self.one.name = get_me.first_name
            LOGGER(__name__).info(
                f"🥀𝐂𝐡𝐚𝐥𝐨 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐜𝐞 𝐁𝐡𝐢 𝐃𝐨𝐧𝐞, 𝐍𝐚𝐦𝐞:- {self.one.name}"
            )
            try:
                await self.one.send_message(
                    config.LOG_GROUP_ID, f"**╔═══❰𝐖𝐄𝐋𝐂𝐎𝐌𝐄❱═══❍⊱❁۪۪**\n**║**\n**║┣⪼🥀𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝🎉**\n**║**\n**║┣⪼🏓𝐈𝐝:- {self.one.id}**\n**║**\n**║┣⪼💛𝐔-𝐍:- @{self.one.username}**\n**║ **\n**║┣⪼💖𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨𝐫 𝐔𝐬𝐢𝐧𝐠😍**\n**║**\n**╚══════════════❍⊱❁**"
                )
            except:
                LOGGER(__name__).error(
                    f"🤬𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 𝐈𝐬 𝐍𝐨𝐭 𝐀𝐝𝐦𝐢𝐧 𝐈𝐧 𝐘𝐨𝐮𝐫 𝐋𝐨𝐠𝐠𝐞𝐫 𝐆𝐫𝐨𝐮𝐩, 𝐆𝐨 𝐀𝐧𝐝 𝐌𝐚𝐤𝐞 𝐀𝐝𝐦𝐢𝐧 𝐓𝐡𝐞𝐧 𝐁𝐨𝐭 𝐖𝐢𝐥𝐥 𝐖𝐨𝐫𝐤😑"
                )
                
        if config.STRING2:
            await self.two.start()
            try:
                await self.two.join_chat("tg_friendss")
                await self.two.join_chat("vip_creators")
                await self.two.join_chat("THE_VIP_BOY")
                await self.two.join_chat("THE_VIP_BOY_OP")
            except:
                pass
            assistants.append(2)
            get_me = await self.two.get_me()
            self.two.username = get_me.username
            self.two.id = get_me.id
            self.two.mention = get_me.mention
            assistantids.append(get_me.id)
            if get_me.last_name:
                self.two.name = (
                    get_me.first_name + " " + get_me.last_name
                )
            else:
                self.two.name = get_me.first_name
            try:
                await self.two.send_message(
                    config.LOG_GROUP_ID, f"**» {config.MUSIC_BOT_NAME} ᴀssɪsᴛᴀɴᴛ ᴛᴡᴏ sᴛᴀʀᴛᴇᴅ :**\n\n✨ ɪᴅ : `{self.two.id}`\n❄ ɴᴀᴍᴇ : {self.two.name}\n💫 ᴜsᴇʀɴᴀᴍᴇ : @{self.two.username}"
                )
            except:
                LOGGER(__name__).error(
                    f"Assistant Account 2 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin ! "
                )
                
            LOGGER(__name__).info(
                f"🥀𝐂𝐡𝐚𝐥𝐨 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐜𝐞 2 𝐁𝐡𝐢 𝐃𝐨𝐧𝐞, 𝐍𝐚𝐦𝐞:- {self.two.name}"
            )
        if config.STRING3:
            await self.three.start()
            try:
                await self.three.join_chat("tg_friendss")
                await self.three.join_chat("vip_creators")
                await self.three.join_chat("THE_VIP_BOY")
                await self.three.join_chat("THE_VIP_BOY_OP")
            except:
                pass
            assistants.append(3)
            get_me = await self.three.get_me()
            self.three.username = get_me.username
            self.three.id = get_me.id
            self.three.mention = get_me.mention
            assistantids.append(get_me.id)
            if get_me.last_name:
                self.three.name = (
                    get_me.first_name + " " + get_me.last_name
                )
            else:
                self.three.name = get_me.first_name
            try:
                await self.three.send_message(
                    config.LOG_GROUP_ID, f"**» {config.MUSIC_BOT_NAME} ᴀssɪsᴛᴀɴᴛ ᴛʜʀᴇᴇ sᴛᴀʀᴛᴇᴅ :**\n\n✨ ɪᴅ : `{self.three.id}`\n❄ ɴᴀᴍᴇ : {self.three.name}\n💫 ᴜsᴇʀɴᴀᴍᴇ : @{self.three.username}"
                )
            except:
                LOGGER(__name__).error(
                    f"Assistant Account 3 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin ! "
                )
                
            LOGGER(__name__).info(
                f"Assistant Three Started as {self.three.name}"
            )
        if config.STRING4:
            await self.four.start()
            try:
                await self.four.join_chat("tg_friendss")
                await self.four.join_chat("vip_creators")
                await self.four.join_chat("THE_VIP_BOY")
                await self.four.join_chat("THE_VIP_BOY_OP")
            except:
                pass
            assistants.append(4)
            get_me = await self.four.get_me()
            self.four.username = get_me.username
            self.four.id = get_me.id
            self.four.mention = get_me.mention
            assistantids.append(get_me.id)
            if get_me.last_name:
                self.four.name = (
                    get_me.first_name + " " + get_me.last_name
                )
            else:
                self.four.name = get_me.first_name
            try:
                await self.four.send_message(
                    config.LOG_GROUP_ID, f"**» {config.MUSIC_BOT_NAME} ᴀssɪsᴛᴀɴᴛ ғᴏᴜʀ sᴛᴀʀᴛᴇᴅ :**\n\n✨ ɪᴅ : `{self.four.id}`\n❄ ɴᴀᴍᴇ : {self.four.name}\n💫 ᴜsᴇʀɴᴀᴍᴇ : @{self.four.username}"
                )
            except:
                LOGGER(__name__).error(
                    f"Assistant Account 4 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin ! "
                )
                
            LOGGER(__name__).info(
                f"Assistant Four Started as {self.four.name}"
            )
        if config.STRING5:
            await self.five.start()
            try:
                await self.five.join_chat("tg_friendss")
                await self.five.join_chat("vip_creators")
                await self.five.join_chat("THE_VIP_BOY")
            except:
                pass
            assistants.append(5)
            get_me = await self.five.get_me()
            self.five.username = get_me.username
            self.five.id = get_me.id
            self.five.mention = get_me.mention
            assistantids.append(get_me.id)
            if get_me.last_name:
                self.five.name = (
                    get_me.first_name + " " + get_me.last_name
                )
            else:
                self.five.name = get_me.first_name
            try:
                await self.five.send_message(
                    config.LOG_GROUP_ID, f"**» {config.MUSIC_BOT_NAME} ᴀssɪsᴛᴀɴᴛ ғɪᴠᴇ sᴛᴀʀᴛᴇᴅ :**\n\n✨ ɪᴅ : `{self.five.id}`\n❄ ɴᴀᴍᴇ : {self.five.name}\n💫 ᴜsᴇʀɴᴀᴍᴇ : @{self.five.username}"
                )
            except:
                LOGGER(__name__).error(
                    f"Assistant Account 5 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin ! "
                )
                
            LOGGER(__name__).info(
                f"Assistant Five Started as {self.five.name}"
            )
             
