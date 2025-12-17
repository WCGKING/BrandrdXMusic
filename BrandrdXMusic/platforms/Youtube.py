import asyncio
import os
import re
from typing import Union, Optional
import httpx

from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from BrandrdXMusic.utils.formatters import time_to_seconds


# API Configuration
API_BASE_URL = "https://youtubify.me"
API_KEY = "773f80726ade410590c486d23db96a62"

# Streaming configuration
ENABLE_STREAMING = True  # Enable streaming URLs for VC (no file size limit)
MAX_DOWNLOAD_SIZE_MB = 48  # Only download files smaller than this (for direct uploads)
STREAM_MODE_DURATION_THRESHOLD = 1200  # 20 minutes - files longer than this will use streaming URLs


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if re.search(self.regex, link):
            return True
        else:
            return False

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset in (None,):
            return None
        return text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            if str(duration_min) == "None":
                duration_sec = 0
            else:
                duration_sec = int(time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
        return title

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            duration = result["duration"]
        return duration

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail

    async def video(self, link: str, videoid: Union[bool, str] = None):
        """Get video stream URL via API"""
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        # Extract video ID
        vid = link.split("v=")[-1].split("&")[0] if "v=" in link else link.split("/")[-1].split("?")[0]
        
        # Return streaming URL for VC playback
        stream_url = f"{API_BASE_URL}/download/video?video_id={vid}&mode=stream&max_res=720&api_key={API_KEY}"
        return 1, stream_url
    
    async def stream_url(self, link: str, videoid: Union[bool, str] = None, video: bool = False) -> Optional[str]:
        """
        Get streaming URL for VC playback (no file download, no size limit).
        
        Args:
            link: YouTube URL or video ID
            videoid: If True, link is just the video ID
            video: If True, return video stream; if False, return audio stream
        
        Returns:
            Streaming URL string that can be used directly by FFmpeg/Telegram VC
        """
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        # Extract video ID
        vid = link.split("v=")[-1].split("&")[0] if "v=" in link else link.split("/")[-1].split("?")[0]
        
        # Build streaming URL (default redirect mode - API redirects to YouTube's URL)
        if video:
            return f"{API_BASE_URL}/download/video?video_id={vid}&max_res=720&api_key={API_KEY}"
        else:
            return f"{API_BASE_URL}/download/audio?video_id={vid}&api_key={API_KEY}"

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        """Playlist support - returns list of video IDs"""
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        
        # Extract playlist ID
        playlist_id = link.split("list=")[-1].split("&")[0] if "list=" in link else ""
        
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(connect=5.0, read=15.0)) as client:
                url = f"{API_BASE_URL}/playlist"
                params = {"playlist_id": playlist_id, "limit": limit, "api_key": API_KEY}
                r = await client.get(url, params=params)
                if r.status_code == 200:
                    data = r.json()
                    return data.get("video_ids", [])
        except Exception:
            pass
        
        return []

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        """Get available formats via API"""
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        # Extract video ID
        vid = link.split("v=")[-1].split("&")[0] if "v=" in link else link.split("/")[-1].split("?")[0]
        
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(connect=5.0, read=10.0)) as client:
                url = f"{API_BASE_URL}/formats"
                params = {"video_id": vid, "api_key": API_KEY}
                r = await client.get(url, params=params)
                if r.status_code == 200:
                    data = r.json()
                    return data.get("formats", []), link
        except Exception:
            pass
        
        return [], link

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        title = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        vidid = result[query_type]["id"]
        thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

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
    ) -> Union[str, tuple]:
        """
        Download audio or video using API.
        
        Returns:
            - For streaming (long videos): Returns streaming URL as string
            - For downloads (short videos): Returns (filepath, True) tuple
        """
        if videoid:
            link = self.base + link
        
        # Extract video ID from link
        vid = link.split("v=")[-1].split("&")[0] if "v=" in link else link.split("/")[-1].split("?")[0]
        
        # Check video duration to decide streaming vs download
        duration_seconds = 0
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
                info_resp = await client.get(
                    f"{API_BASE_URL}/info",
                    params={"video_id": vid, "api_key": API_KEY}
                )
                if info_resp.status_code == 200:
                    info_data = info_resp.json()
                    duration_str = info_data.get("duration", "0:0")
                    # Parse duration
                    parts = duration_str.split(":")
                    if len(parts) == 3:
                        duration_seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                    elif len(parts) == 2:
                        duration_seconds = int(parts[0]) * 60 + int(parts[1])
                    else:
                        duration_seconds = int(parts[0])
        except Exception as e:
            print(f"Failed to get duration: {e}")
        
        # For long videos (>20 min), return streaming URL instead of downloading
        if ENABLE_STREAMING and duration_seconds > STREAM_MODE_DURATION_THRESHOLD:
            # Return streaming URL for VC playback
            # Use redirect mode (default) which gives YouTube's direct URL - works with FFmpeg
            if video:
                stream_url = f"{API_BASE_URL}/download/video?video_id={vid}&max_res=720&api_key={API_KEY}"
            else:
                stream_url = f"{API_BASE_URL}/download/audio?video_id={vid}&api_key={API_KEY}"
            
            print(f"Using streaming URL for long video ({duration_seconds}s): {stream_url}")
            return stream_url  # Return URL directly for streaming
        
        # For short videos, download as before
        # Use API for downloads
        async def api_download_audio():
            """Download audio using the API"""
            try:
                async with httpx.AsyncClient(
                    timeout=httpx.Timeout(connect=10.0, read=600.0, write=600.0, pool=10.0),
                    follow_redirects=True
                ) as client:
                    url = f"{API_BASE_URL}/download/audio"
                    params = {
                        "video_id": vid,
                        "mode": "download",
                        "no_redirect": "1",
                        "api_key": API_KEY
                    }
                    
                    # Get filename first
                    info_resp = await client.get(f"{API_BASE_URL}/info", params={"video_id": vid, "api_key": API_KEY})
                    if info_resp.status_code == 200:
                        info_data = info_resp.json()
                        file_title = info_data.get("title", vid)
                    else:
                        file_title = vid
                    
                    # Sanitize filename
                    safe_title = re.sub(r'[<>:"/\\|?*]', '', file_title)[:100]
                    filepath = f"downloads/{safe_title}.mp3"
                    
                    # Download file
                    async with client.stream("GET", url, params=params) as r:
                        if r.status_code != 200:
                            raise Exception(f"API returned {r.status_code}")
                        
                        os.makedirs("downloads", exist_ok=True)
                        with open(filepath, "wb") as f:
                            async for chunk in r.aiter_bytes(chunk_size=1024 * 128):
                                if chunk:
                                    f.write(chunk)
                    
                    return filepath
            except Exception as e:
                print(f"API audio download failed: {e}")
                return None
        
        async def api_download_video():
            """Download video using the API"""
            try:
                async with httpx.AsyncClient(
                    timeout=httpx.Timeout(connect=10.0, read=600.0, write=600.0, pool=10.0),
                    follow_redirects=True
                ) as client:
                    url = f"{API_BASE_URL}/download/video"
                    params = {
                        "video_id": vid,
                        "mode": "download",
                        "no_redirect": "1",
                        "max_res": "720",
                        "api_key": API_KEY
                    }
                    
                    # Get filename first
                    info_resp = await client.get(f"{API_BASE_URL}/info", params={"video_id": vid, "api_key": API_KEY})
                    if info_resp.status_code == 200:
                        info_data = info_resp.json()
                        file_title = info_data.get("title", vid)
                    else:
                        file_title = vid
                    
                    # Sanitize filename
                    safe_title = re.sub(r'[<>:"/\\|?*]', '', file_title)[:100]
                    filepath = f"downloads/{safe_title}.mp4"
                    
                    # Download file
                    async with client.stream("GET", url, params=params) as r:
                        if r.status_code != 200:
                            raise Exception(f"API returned {r.status_code}")
                        
                        os.makedirs("downloads", exist_ok=True)
                        with open(filepath, "wb") as f:
                            async for chunk in r.aiter_bytes(chunk_size=1024 * 128):
                                if chunk:
                                    f.write(chunk)
                    
                    return filepath
            except Exception as e:
                print(f"API video download failed: {e}")
                return None

        # Handle special song download cases (custom format_id)
        if songvideo or songaudio:
            # For custom format downloads, fall back to video/audio download
            if songvideo:
                downloaded_file = await api_download_video()
                if downloaded_file:
                    fpath = f"downloads/{title}.mp4" if title else downloaded_file
                    if downloaded_file != fpath and os.path.exists(downloaded_file):
                        os.rename(downloaded_file, fpath)
                    return fpath
            else:  # songaudio
                downloaded_file = await api_download_audio()
                if downloaded_file:
                    fpath = f"downloads/{title}.mp3" if title else downloaded_file
                    if downloaded_file != fpath and os.path.exists(downloaded_file):
                        os.rename(downloaded_file, fpath)
                    return fpath
            return None
        
        # Standard video or audio download
        if video:
            # Download video
            downloaded_file = await api_download_video()
            if downloaded_file and os.path.exists(downloaded_file):
                return downloaded_file, True
            return None, True
        else:
            # Download audio
            downloaded_file = await api_download_audio()
            if downloaded_file and os.path.exists(downloaded_file):
                return downloaded_file, True
            return None, True
