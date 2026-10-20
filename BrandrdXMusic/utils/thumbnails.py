#https://github.com/WCGKING/BrandrdXMusic

import os
from io import BytesIO

import aiohttp
from PIL import Image

from config import YOUTUBE_IMG_URL

_SOURCES = ("maxresdefault", "sddefault", "hqdefault", "mqdefault")
_MIN_WIDTH = 300
_BAR_LIMIT = 24


def _trim_bars(image):
    width, height = image.size
    bar = int(height * 0.125)
    if bar < 1:
        return image, False
    top = image.crop((0, 0, width, bar)).convert("L").getextrema()[1]
    bottom = image.crop((0, height - bar, width, height)).convert("L").getextrema()[1]
    if top < _BAR_LIMIT and bottom < _BAR_LIMIT:
        return image.crop((0, bar, width, height - bar)), True
    return image, False


async def _fetch(session, videoid, name):
    url = f"https://i.ytimg.com/vi/{videoid}/{name}.jpg"
    try:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            raw = await resp.read()
    except Exception:
        return None
    try:
        image = Image.open(BytesIO(raw))
        image.load()
    except Exception:
        return None
    if image.width < _MIN_WIDTH:
        return None
    return raw, image


async def get_thumb(videoid):
    path = f"cache/{videoid}.jpg"
    if os.path.isfile(path) and os.path.getsize(path) > 0:
        return path
    try:
        os.makedirs("cache", exist_ok=True)
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for name in _SOURCES:
                got = await _fetch(session, videoid, name)
                if not got:
                    continue
                raw, image = got
                image, trimmed = _trim_bars(image)
                if trimmed:
                    image.convert("RGB").save(path, "JPEG", quality=95)
                else:
                    with open(path, "wb") as f:
                        f.write(raw)
                return path
    except Exception:
        pass
    return YOUTUBE_IMG_URL
