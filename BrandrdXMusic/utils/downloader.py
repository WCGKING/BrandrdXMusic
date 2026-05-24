import os
import re
import json
import yt_dlp
import random
import logging
import aiohttp
import asyncio
from typing import Optional


from config import API_URL, API_KEY

logger = logging.getLogger(__name__)


class VibeBots:
    def __init__(self):
        self.download_dir = "downloads"
        os.makedirs(self.download_dir, exist_ok=True)
        self.session = None
        self.download_semaphore = asyncio.Semaphore(5)
        
    async def get_session(self) -> aiohttp.ClientSession:
        if not self.session or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=300, connect=30, sock_read=300)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
    
    def get_cookie_file(self) -> Optional[str]:
        cookie_dir = f"{os.getcwd()}/cookies"
        if not os.path.exists(cookie_dir):
            return None
        cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
        if not cookies_files:
            return None
        return os.path.join(cookie_dir, random.choice(cookies_files))
    
    def extract_video_id(self, link: str) -> str:
        if "youtu.be/" in link:
            return link.split("youtu.be/")[-1].split("?")[0]
        elif "v=" in link:
            return link.split('v=')[-1].split('&')[0]
        elif "shorts/" in link:
            return link.split("shorts/")[-1].split("?")[0]
        return link
    
    async def download_via_api(self, video_id: str, is_video: bool = False, progress_callback: Callable = None) -> Optional[str]:
        endpoint = "video" if is_video else "audio"
        
        extensions = ["mp4", "webm", "mkv"] if is_video else ["mp3", "m4a", "webm", "opus"]
        for ext in extensions:
            file_path = f"{self.download_dir}/{video_id}.{ext}"
            if os.path.exists(file_path):
                return file_path
        
        api_url = f"{BASE_API_URL}/{endpoint}?url={video_id}&api_key={BASE_API_KEY}"
        session = await self.get_session()
        
        for attempt in range(3):
            try:
                async with session.get(api_url) as response:
                    if response.status != 200:
                        if attempt < 2:
                            await asyncio.sleep(2)
                            continue
                        return None
                    
                    content_type = response.headers.get('Content-Type', '').lower()
                    if 'video' in content_type:
                        ext = 'mp4'
                    elif 'audio' in content_type:
                        ext = 'mp3'
                    else:
                        ext = 'mp4' if is_video else 'mp3'
                    
                    file_path = f"{self.download_dir}/{video_id}.{ext}"
                    total_size = int(response.headers.get('Content-Length', 0))
                    
                    downloaded = 0
                    with open(file_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if progress_callback and total_size > 0:
                                    await progress_callback(downloaded, total_size)
                    
                    return file_path
                    
            except asyncio.TimeoutError:
                if attempt == 2:
                    logger.error(f"API timeout for {video_id}")
                    return None
                await asyncio.sleep(2)
            except Exception as e:
                if attempt == 2:
                    logger.error(f"API download failed for {video_id}: {e}")
                    return None
                await asyncio.sleep(2)
        
        return None
    
    async def download_via_cookies(self, link: str, is_video: bool = False) -> Tuple[Optional[str], bool]:
        async with self.download_semaphore:
            cookie_file = self.get_cookie_file()
            if not cookie_file:
                logger.error("No cookies found")
                return None, False
            
            loop = asyncio.get_running_loop()
            
            def _download():
                if is_video:
                    ydl_opts = {
                        "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                        "outtmpl": f"{self.download_dir}/%(id)s.%(ext)s",
                        "geo_bypass": True,
                        "nocheckcertificate": True,
                        "quiet": True,
                        "cookiefile": cookie_file,
                        "no_warnings": True,
                    }
                else:
                    ydl_opts = {
                        "format": "bestaudio/best",
                        "outtmpl": f"{self.download_dir}/%(id)s.%(ext)s",
                        "geo_bypass": True,
                        "nocheckcertificate": True,
                        "quiet": True,
                        "cookiefile": cookie_file,
                        "no_warnings": True,
                    }
                
                x = yt_dlp.YoutubeDL(ydl_opts)
                info = x.extract_info(link, download=False)
                file_path = os.path.join(self.download_dir, f"{info['id']}.{info['ext']}")
                
                if not os.path.exists(file_path):
                    x.download([link])
                
                return file_path
            
            try:
                file_path = await loop.run_in_executor(None, _download)
                return file_path, True
            except Exception as e:
                logger.error(f"Cookie download failed: {e}")
                return None, False
    
    async def download_song(self, link: str, progress_callback: Callable = None) -> Optional[str]:
        video_id = self.extract_video_id(link)
        
        file_path = await self.download_via_api(video_id, is_video=False, progress_callback=progress_callback)
        if file_path:
            return file_path
        
        file_path, _ = await self.download_via_cookies(link, is_video=False)
        return file_path
    
    async def download_video(self, link: str, progress_callback: Callable = None) -> Optional[str]:
        video_id = self.extract_video_id(link)
        
        file_path = await self.download_via_api(video_id, is_video=True, progress_callback=progress_callback)
        if file_path:
            return file_path
        
        file_path, _ = await self.download_via_cookies(link, is_video=True)
        return file_path
    
    async def get_video_url(self, link: str) -> Tuple[int, str]:
        cookie_file = self.get_cookie_file()
        if not cookie_file:
            return 0, "No cookies found"
        
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", cookie_file,
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            f"{link}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        else:
            return 0, stderr.decode()
    
    async def check_file_size(self, link: str) -> Optional[int]:
        cookie_file = self.get_cookie_file()
        if not cookie_file:
            logger.error("No cookies found")
            return None
        
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", cookie_file,
            "-J",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        if proc.returncode != 0:
            logger.error(f"yt-dlp error: {stderr.decode()}")
            return None
        
        try:
            info = json.loads(stdout.decode())
            formats = info.get('formats', [])
            total_size = sum(f.get('filesize', 0) for f in formats)
            return total_size if total_size > 0 else None
        except Exception as e:
            logger.error(f"Failed to parse file size: {e}")
            return None


VibeApi = VibeBots()
