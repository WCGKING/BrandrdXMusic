import re
import os
import asyncio
import yt_dlp
import logging
from typing import Union

from pyrogram.enums import MessageEntityType
from pyrogram.types import Message


from BrandrdXMusic.utils.downloader import VibeApi
from BrandrdXMusic.utils.formatters import time_to_seconds

logger = logging.getLogger(__name__)


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="

    async def exists(self, link: str, videoid: Union[bool, str] = None) -> bool:
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        url = text[entity.offset:entity.offset + entity.length]
                        return url.split("?si=")[0] if "?si=" in url else url
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            duration_sec = int(time_to_seconds(duration_min)) if duration_min != "None" else 0
        
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None) -> str:
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["title"]
        return "Unknown"

    async def duration(self, link: str, videoid: Union[bool, str] = None) -> str:
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["duration"]
        return "0:00"

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None) -> str:
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["thumbnails"][0]["url"].split("?")[0]
        return ""

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        
        downloaded_file = await VibeApi.download_video(link)
        if downloaded_file:
            return 1, downloaded_file
        
        return await VibeApi.get_video_url(link)

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        
        try:
            plist = await Playlist.get(link)
        except:
            return []

        videos = plist.get("videos") or []
        ids = []
        for data in videos[:limit]:
            if data and data.get("id"):
                ids.append(data["id"])
        return ids

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            track_details = {
                "title": result["title"],
                "link": result["link"],
                "vidid": result["id"],
                "duration_min": result["duration"],
                "thumb": result["thumbnails"][0]["url"].split("?")[0],
            }
            return track_details, result["id"]
        return None, None

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        
        cookie_file = VibeApi.get_cookie_file()
        if not cookie_file:
            return [], link
        
        ytdl_opts = {"quiet": True, "cookiefile": cookie_file}
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            
            for fmt in r["formats"]:
                if "dash" in str(fmt.get("format", "")).lower():
                    continue
                
                required_keys = ["format", "filesize", "format_id", "ext", "format_note"]
                if all(k in fmt for k in required_keys):
                    formats_available.append({
                        "format": fmt["format"],
                        "filesize": fmt["filesize"],
                        "format_id": fmt["format_id"],
                        "ext": fmt["ext"],
                        "format_note": fmt["format_note"],
                        "yturl": link,
                    })
        
        return formats_available, link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        
        data = result[query_type]
        return (
            data["title"],
            data["duration"],
            data["thumbnails"][0]["url"].split("?")[0],
            data["id"]
        )

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> tuple:
        if videoid:
            link = self.base + link
        
        is_video = bool(video or songvideo)
        is_audio = bool(songaudio or not video)
        
        try:
            if is_video:
                file_path = await VibeApi.download_video(link)
                if file_path:
                    return file_path, True
            elif is_audio:
                file_path = await VibeApi.download_song(link)
                if file_path:
                    return file_path, True
        except Exception as e:
            logger.error(f"Download failed: {e}")
        
        cookie_file = VibeApi.get_cookie_file()
        if not cookie_file:
            logger.error("No cookies found")
            return None, False
        
        loop = asyncio.get_running_loop()
        
        def _ytdlp_download():
            if is_video:
                ydl_opts = {
                    "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                    "outtmpl": "downloads/%(id)s.%(ext)s",
                    "geo_bypass": True,
                    "quiet": True,
                    "cookiefile": cookie_file,
                    "no_warnings": True,
                }
            else:
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": "downloads/%(id)s.%(ext)s",
                    "geo_bypass": True,
                    "quiet": True,
                    "cookiefile": cookie_file,
                    "no_warnings": True,
                }
            
            x = yt_dlp.YoutubeDL(ydl_opts)
            info = x.extract_info(link, False)
            file_path = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            
            if not os.path.exists(file_path):
                x.download([link])
            
            return file_path
        
        try:
            file_path = await loop.run_in_executor(None, _ytdlp_download)
            return file_path, True
        except Exception as e:
            logger.error(f"Fallback failed: {e}")
            return None, False
