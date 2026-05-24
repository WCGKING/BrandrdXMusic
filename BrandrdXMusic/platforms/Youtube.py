# YouTube.py

import asyncio
from yt_dlp import YoutubeDL

ytdl_opts = {
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0",
}

class YouTube:
    def __init__(self):
        self.ytdl = YoutubeDL(ytdl_opts)

    async def search(self, query: str):
        """
        Search YouTube and return first result
        """

        loop = asyncio.get_event_loop()

        data = await loop.run_in_executor(
            None,
            lambda: self.ytdl.extract_info(
                f"ytsearch1:{query}",
                download=False
            )
        )

        if not data or "entries" not in data:
            return None

        result = data["entries"][0]

        return {
            "title": result.get("title"),
            "duration": result.get("duration"),
            "thumbnail": result.get("thumbnail"),
            "url": result.get("webpage_url"),
            "stream_url": result.get("url"),
            "id": result.get("id"),
        }

    async def download(self, url: str):
        """
        Extract stream/download info from YouTube URL
        """

        loop = asyncio.get_event_loop()

        data = await loop.run_in_executor(
            None,
            lambda: self.ytdl.extract_info(
                url,
                download=False
            )
        )

        return {
            "title": data.get("title"),
            "duration": data.get("duration"),
            "thumbnail": data.get("thumbnail"),
            "url": data.get("webpage_url"),
            "stream_url": data.get("url"),
            "id": data.get("id"),
        }


# Example usage
# yt = YouTube()
# song = await yt.search("Alan Walker Faded")
# print(song)
