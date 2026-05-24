import asyncio
import os
import re
from typing import Optional

import aiohttp
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython import VideosSearch, Playlist

from BrandrdXMusic import LOGGER
from BrandrdXMusic.utils.formatters import time_to_seconds

API_URL = "https://shrutibots.site"
DOWNLOAD_DIR = "downloads"


async def _download_file(url: str, file_path: str) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return None

                with open(file_path, "wb") as f:
                    async for chunk in response.content.iter_chunked(16384):
                        f.write(chunk)

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return file_path

    except Exception as e:
        LOGGER.error(f"Download file error: {e}", exc_info=True)

    return None


async def download_media(link: str, media_type: str) -> Optional[str]:
    try:
        video_id = (
            link.split("v=")[-1].split("&")[0]
            if "v=" in link
            else link
        )

        if not video_id:
            return None

        ext = "mp3" if media_type == "audio" else "mp4"

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        file_path = os.path.join(
            DOWNLOAD_DIR,
            f"{video_id}.{ext}"
        )

        if os.path.exists(file_path):
            return file_path

        async with aiohttp.ClientSession() as session:
            params = {
                "url": video_id,
                "type": media_type
            }

            async with session.get(
                f"{API_URL}/download",
                params=params,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:

                if response.status != 200:
                    LOGGER.error(f"API returned {response.status}")
                    return None

                data = await response.json()

                token = data.get("download_token")

                if not token:
                    LOGGER.error("No download token received")
                    return None

                stream_url = (
                    f"{API_URL}/stream/"
                    f"{video_id}?type={media_type}&token={token}"
                )

                return await _download_file(stream_url, file_path)

    except Exception as e:
        LOGGER.error(f"download_media error: {e}", exc_info=True)
        return None


async def download_song(link: str):
    return await download_media(link, "audio")


async def download_video(link: str):
    return await download_media(link, "video")


class YouTubeAPI:
    def init(self):
        self.base = "https://www.youtube.com/watch?v="
        self.listbase = "https://youtube.com/playlist?list="
        self.regex = r"(?:youtube\.com|youtu\.be)"

    async def exists(self, link: str, videoid=None):
        if videoid:
            link = self.base + link

        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message):
        messages = [message_1]

        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        for message in messages:

            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[
                            entity.offset:
                            entity.offset + entity.length
                        ]

            if message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url

        return None

    async def _search(self, query: str):
        try:
            results = VideosSearch(query, limit=1)

data = await results.next()

            if not data.get("result"):
                return None

            return data["result"][0]

        except Exception as e:
            LOGGER.error(f"YouTube search error: {e}", exc_info=True)
            return None

    async def details(self, link: str, videoid=None):
        if videoid:
            link = self.base + link

        result = await self._search(link)

        if not result:
            return None

        title = result.get("title")
        duration_min = result.get("duration")
        vidid = result.get("id")

        thumbs = result.get("thumbnails") or []
        thumbnail = thumbs[0]["url"].split("?")[0] if thumbs else None

        duration_sec = (
            int(time_to_seconds(duration_min))
            if duration_min
            else 0
        )

        return (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        )

    async def title(self, link: str, videoid=None):
        if videoid:
            link = self.base + link

        result = await self._search(link)

        return result.get("title") if result else None

    async def duration(self, link: str, videoid=None):
        if videoid:
            link = self.base + link

        result = await self._search(link)

        return result.get("duration") if result else None

    async def thumbnail(self, link: str, videoid=None):
        if videoid:
            link = self.base + link

        result = await self._search(link)

        if not result:
            return None

        thumbs = result.get("thumbnails") or []

        if not thumbs:
            return None

        return thumbs[0]["url"].split("?")[0]

    async def video(self, link: str, videoid=None):
        try:
            if videoid:
                link = self.base + link

            file = await download_video(link)

            if not file:
                return 0, "Video download failed"

            return 1, file

        except Exception as e:
            LOGGER.error(f"Video error: {e}", exc_info=True)
            return 0, str(e)

    async def playlist(self, link, limit, user_id, videoid=None):
        try:
            if videoid:
                link = self.listbase + link

            plist = Playlist.get(link)

            videos = plist.get("videos") or []

            ids = []

            for video in videos[:limit]:
                vid = video.get("id")

                if vid:
                    ids.append(vid)

            return ids

        except Exception as e:
            LOGGER.error(f"Playlist error: {e}", exc_info=True)
            return []

    async def track(self, link: str, videoid=None):
        if videoid:
            link = self.base + link

        result = await self._search(link)

        if not result:
            return None, None

        return {
            "title": result.get("title"),
            "link": result.get("link"),
            "vidid": result.get("id"),
            "duration_min": result.get("duration"),
            "thumb": (
                result.get("thumbnails")[0]["url"].split("?")[0]
                if result.get("thumbnails")
                else None
            ),
        }, result.get("id")

    async def formats(self, link: str, videoid=None):
        try:
            if videoid:
                link = self.base + link

            ydl_opts = {"quiet": True}

            ydl = yt_dlp.YoutubeDL(ydl_opts)

            data = await asyncio.to_thread(
                ydl.extract_info,
                link,
                False
            )

            formats_available = []

            for fmt in data.get("formats", []):

                if "dash" in str(fmt.get("format", "")).lower():
                    continue

formats_available.append(
                    {
                        "format": fmt.get("format"),
                        "filesize": fmt.get("filesize"),
                        "format_id": fmt.get("format_id"),
                        "ext": fmt.get("ext"),
                        "format_note": fmt.get("format_note"),
                        "yturl": link,
                    }
                )

            return formats_available, link

        except Exception as e:
            LOGGER.error(f"Formats error: {e}", exc_info=True)
            return [], link

    async def download(
        self,
        link: str,
        mystic=None,
        video=None,
        videoid=None,
        **kwargs
    ):
        try:
            if videoid:
                link = self.base + link

            file = (
                await download_video(link)
                if video
                else await download_song(link)
            )

            if not file:
                return None, False

            return file, True

        except Exception as e:
            LOGGER.error(f"Download error: {e}", exc_info=True)
            return None, False
