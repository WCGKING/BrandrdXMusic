import asyncio
import os
import wave
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from ntgcalls import TelegramServerError
from pytgcalls import PyTgCalls, filters
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types import (
    AudioQuality,
    ChatUpdate,
    GroupCallConfig,
    MediaStream,
    StreamEnded,
    Update,
    VideoQuality,
)

import config
from BrandrdXMusic import LOGGER, YouTube, app
from BrandrdXMusic.misc import db
from BrandrdXMusic.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_active_chat,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from BrandrdXMusic.utils.exceptions import AssistantErr
from BrandrdXMusic.utils.formatters import check_duration, seconds_to_min, speed_converter
from BrandrdXMusic.utils.inline.play import stream_markup
from BrandrdXMusic.utils.stream.autoclear import auto_clean
from BrandrdXMusic.utils.thumbnails import get_thumb
from strings import get_string

autoend = {}
counter = {}

AUDIO_QUALITY = AudioQuality.HIGH
VIDEO_QUALITY = VideoQuality.SD_360p


def _audio_stream(path, ffmpeg_parameters=None):
    return MediaStream(
        path,
        audio_parameters=AUDIO_QUALITY,
        video_flags=MediaStream.Flags.IGNORE,
        ffmpeg_parameters=ffmpeg_parameters,
    )


def _video_stream(path, ffmpeg_parameters=None):
    return MediaStream(
        path,
        audio_parameters=AUDIO_QUALITY,
        video_parameters=VIDEO_QUALITY,
        ffmpeg_parameters=ffmpeg_parameters,
    )


async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


PLACEHOLDER_SECONDS = 120
_video_placeholder_lock = asyncio.Lock()


def _silence_path():
    path = os.path.abspath(os.path.join("cache", "silence.wav"))
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with wave.open(path, "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(1)
            f.setframerate(8000)
            f.writeframes(b"\x80" * 8000 * PLACEHOLDER_SECONDS)
    return path


async def _silence_video_path():
    path = os.path.abspath(os.path.join("cache", "silence.mp4"))
    if os.path.isfile(path) and os.path.getsize(path) > 0:
        return path
    async with _video_placeholder_lock:
        if os.path.isfile(path) and os.path.getsize(path) > 0:
            return path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=black:s=320x180:r=15",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=8000:cl=mono",
            "-t",
            str(PLACEHOLDER_SECONDS),
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-shortest",
            "-f",
            "mp4",
            tmp,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.communicate()
        if proc.returncode != 0 or not os.path.isfile(tmp) or os.path.getsize(tmp) == 0:
            if os.path.isfile(tmp):
                os.remove(tmp)
            raise RuntimeError("Silent video placeholder generation failed")
        os.replace(tmp, path)
    return path


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="BrandrdXMusic1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(self.userbot1, cache_duration=100)

        self.userbot2 = Client(
            name="BrandrdXMusic2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )
        self.two = PyTgCalls(self.userbot2, cache_duration=100)

        self.userbot3 = Client(
            name="BrandrdXMusic3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )
        self.three = PyTgCalls(self.userbot3, cache_duration=100)

        self.userbot4 = Client(
            name="BrandrdXMusic4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
        )
        self.four = PyTgCalls(self.userbot4, cache_duration=100)

        self.userbot5 = Client(
            name="BrandrdXMusic5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
        )
        self.five = PyTgCalls(self.userbot5, cache_duration=100)

        self._prejoin_tasks = {}
        self._prejoin_video = {}
        self._chat_locks = {}

    def chat_lock(self, chat_id: int):
        lock = self._chat_locks.get(chat_id)
        if lock is None:
            lock = asyncio.Lock()
            self._chat_locks[chat_id] = lock
        return lock

    async def _assistant_join(self, assistant, chat_id: int, stream, _):
        try:
            await assistant.play(
                chat_id, stream, config=GroupCallConfig(auto_start=False)
            )
        except NoActiveGroupCall:
            LOGGER(__name__).error("_assistant_join: unhandled exception", exc_info=True)
            raise AssistantErr(_["call_8"])
        except TelegramServerError:
            LOGGER(__name__).error("_assistant_join: unhandled exception", exc_info=True)
            raise AssistantErr(_["call_10"])

    async def _run_prejoin(self, chat_id: int, video: bool = False):
        assistant = await group_assistant(self, chat_id)
        _ = get_string(await get_lang(chat_id))
        used_video = False
        if video:
            try:
                path = await _silence_video_path()
                stream = _video_stream(path)
                used_video = True
            except Exception:
                LOGGER(__name__).error("_run_prejoin: unhandled exception", exc_info=True)
                stream = _audio_stream(_silence_path())
        else:
            stream = _audio_stream(_silence_path())
        self._prejoin_video[chat_id] = used_video
        await self._assistant_join(assistant, chat_id, stream, _)

    async def prejoin_start(self, chat_id: int, video: bool = False) -> bool:
        async with self.chat_lock(chat_id):
            if chat_id in self._prejoin_tasks or await is_active_chat(chat_id):
                return False
            task = asyncio.create_task(self._run_prejoin(chat_id, video))
            self._prejoin_tasks[chat_id] = task
            return True

    async def await_prejoin(self, chat_id: int):
        task = self._prejoin_tasks.get(chat_id)
        if task is not None:
            await asyncio.shield(task)

    async def prejoin_settle(self, chat_id: int):
        async with self.chat_lock(chat_id):
            task = self._prejoin_tasks.pop(chat_id, None)
            self._prejoin_video.pop(chat_id, None)
            if task is None:
                return
            try:
                await asyncio.shield(task)
            except Exception:
                LOGGER(__name__).warning("prejoin_settle: unhandled exception", exc_info=True)
                return
            try:
                assistant = await group_assistant(self, chat_id)
                await assistant.leave_call(chat_id)
            except Exception:
                LOGGER(__name__).warning("prejoin_settle: unhandled exception", exc_info=True)
                pass

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_call(chat_id)
        except Exception:
            LOGGER(__name__).warning("stop_stream: unhandled exception", exc_info=True)
            pass

    async def stop_stream_force(self, chat_id: int):
        assistants = [
            (config.STRING1, self.one),
            (config.STRING2, self.two),
            (config.STRING3, self.three),
            (config.STRING4, self.four),
            (config.STRING5, self.five),
        ]

        for session, assistant in assistants:
            if session:
                try:
                    await assistant.leave_call(chat_id)
                except Exception:
                    LOGGER(__name__).warning("stop_stream_force: unhandled exception", exc_info=True)
                    pass

        try:
            await _clear_(chat_id)
        except Exception:
            LOGGER(__name__).warning("stop_stream_force: unhandled exception", exc_info=True)
            pass

    async def speedup_stream(self, chat_id: int, file_path, speed, playing):
        assistant = await group_assistant(self, chat_id)

        if str(speed) != "1.0":
            base = os.path.basename(file_path)
            chatdir = os.path.join(os.getcwd(), "playback", str(speed))
            os.makedirs(chatdir, exist_ok=True)
            out = os.path.join(chatdir, base)

            if not os.path.isfile(out):
                speed_values = {
                    "0.5": 2.0,
                    "0.75": 1.35,
                    "1.5": 0.68,
                    "2.0": 0.5,
                }
                vs = speed_values.get(str(speed), 1.0)

                proc = await asyncio.create_subprocess_shell(
                    cmd=(
                        "ffmpeg -y "
                        f'-i "{file_path}" '
                        "-filter:v "
                        f"setpts={vs}*PTS "
                        "-filter:a "
                        f"atempo={speed} "
                        f'"{out}"'
                    ),
                    stdin=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await proc.communicate()
                if proc.returncode != 0 or not os.path.isfile(out):
                    raise AssistantErr("Could not create the speed-adjusted audio.")
        else:
            out = file_path

        dur = await asyncio.get_event_loop().run_in_executor(
            None, check_duration, out
        )
        dur = int(dur)
        played, con_seconds = speed_converter(playing[0]["played"], speed)
        duration = seconds_to_min(dur)

        ffmpeg_parameters = f"-ss {played} -to {duration}"
        stream = (
            _video_stream(out, ffmpeg_parameters=ffmpeg_parameters)
            if playing[0]["streamtype"] == "video"
            else _audio_stream(out, ffmpeg_parameters=ffmpeg_parameters)
        )

        if str(db[chat_id][0]["file"]) == str(file_path):
            await assistant.play(chat_id, stream)
        else:
            raise AssistantErr("Umm")

        if str(db[chat_id][0]["file"]) == str(file_path):
            exis = playing[0].get("old_dur")
            if not exis:
                db[chat_id][0]["old_dur"] = db[chat_id][0]["dur"]
                db[chat_id][0]["old_second"] = db[chat_id][0]["seconds"]

            db[chat_id][0]["played"] = con_seconds
            db[chat_id][0]["dur"] = duration
            db[chat_id][0]["seconds"] = dur
            db[chat_id][0]["speed_path"] = out
            db[chat_id][0]["speed"] = speed

    async def force_stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)

        try:
            check = db.get(chat_id)
            if check:
                check.pop(0)
        except Exception:
            LOGGER(__name__).warning("force_stop_stream: unhandled exception", exc_info=True)
            pass

        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)

        try:
            await assistant.leave_call(chat_id)
        except Exception:
            LOGGER(__name__).warning("force_stop_stream: unhandled exception", exc_info=True)
            pass

    async def skip_stream(
        self,
        chat_id: int,
        link: str,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)

        if video:
            stream = _video_stream(link)
        else:
            stream = _audio_stream(link)

        await assistant.play(chat_id, stream)

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        assistant = await group_assistant(self, chat_id)

        ffmpeg_parameters = f"-ss {to_seek} -to {duration}"
        stream = (
            _video_stream(file_path, ffmpeg_parameters=ffmpeg_parameters)
            if mode == "video"
            else _audio_stream(file_path, ffmpeg_parameters=ffmpeg_parameters)
        )

        await assistant.play(chat_id, stream)

    async def stream_call(self, link):
        assistant = await group_assistant(self, config.LOGGER_ID)
        await assistant.play(
            config.LOGGER_ID,
            _video_stream(link),
            config=GroupCallConfig(auto_start=False),
        )
        await asyncio.sleep(0.2)
        await assistant.leave_call(config.LOGGER_ID)

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        language = await get_lang(chat_id)
        _ = get_string(language)

        if video:
            stream = _video_stream(link)
        else:
            stream = _audio_stream(link)

        async with self.chat_lock(chat_id):
            joined = False
            task = self._prejoin_tasks.pop(chat_id, None)
            if task is not None:
                try:
                    await asyncio.shield(task)
                    prejoin_was_video = self._prejoin_video.pop(chat_id, False)
                    if bool(video) == prejoin_was_video:
                        try:
                            await assistant.play(chat_id, stream)
                            joined = True
                        except Exception:
                            LOGGER(__name__).error("join_call: unhandled exception", exc_info=True)
                            try:
                                await assistant.leave_call(chat_id)
                            except Exception:
                                LOGGER(__name__).warning("join_call: unhandled exception", exc_info=True)
                                pass
                    else:
                        try:
                            await assistant.leave_call(chat_id)
                        except Exception:
                            LOGGER(__name__).warning("join_call: unhandled exception", exc_info=True)
                            pass
                except Exception:
                    LOGGER(__name__).error("join_call: unhandled exception", exc_info=True)
                    self._prejoin_video.pop(chat_id, None)
            if not joined:
                await self._assistant_join(assistant, chat_id, stream, _)

        await add_active_chat(chat_id)
        await music_on(chat_id)

        if video:
            await add_active_video_chat(chat_id)

        if await is_autoend():
            counter[chat_id] = {}
            users = len(await assistant.get_participants(chat_id))
            if users == 1:
                autoend[chat_id] = datetime.now() + timedelta(minutes=1)

    async def change_stream(self, client, chat_id):
        check = db.get(chat_id)
        popped = None
        if not check:
            return
        loop = await get_loop(chat_id)

        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop = loop - 1
                await set_loop(chat_id, loop)

            await auto_clean(popped)

            if not check:
                await _clear_(chat_id)
                return await client.leave_call(chat_id)

        except Exception:
            LOGGER(__name__).error("change_stream: unhandled exception", exc_info=True)
            try:
                await _clear_(chat_id)
                return await client.leave_call(chat_id)
            except Exception:
                LOGGER(__name__).warning("change_stream: unhandled exception", exc_info=True)
                return

        else:
            queued = check[0]["file"]
            language = await get_lang(chat_id)
            _ = get_string(language)

            title = check[0]["title"].title()
            user = check[0]["by"]
            original_chat_id = check[0]["chat_id"]
            streamtype = check[0]["streamtype"]
            videoid = check[0]["vidid"]

            if videoid and videoid not in ("telegram", "soundcloud"):
                record_played(chat_id, videoid)

            db[chat_id][0]["played"] = 0

            exis = check[0].get("old_dur")
            if exis:
                db[chat_id][0]["dur"] = exis
                db[chat_id][0]["seconds"] = check[0]["old_second"]
                db[chat_id][0]["speed_path"] = None
                db[chat_id][0]["speed"] = 1.0

            video = str(streamtype) == "video"

            if "live_" in queued:
                n, link = await YouTube.video(videoid, True)

                if n == 0:
                    return await app.send_message(
                        original_chat_id, text=_["call_6"]
                    )

                stream = (
                    _video_stream(link) if video else _audio_stream(link)
                )

                try:
                    await client.play(chat_id, stream)
                except Exception:
                    LOGGER(__name__).error("change_stream: unhandled exception", exc_info=True)
                    return await app.send_message(
                        original_chat_id, text=_["call_6"]
                    )

                img = await get_thumb(videoid)
                button = stream_markup(_, videoid, chat_id)

                run = await app.send_photo(
                    chat_id=original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        title[:23],
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"

            elif "vid_" in queued:
                mystic = await app.send_message(
                    original_chat_id, _["call_7"]
                )

                try:
                    file_path, direct = await YouTube.download(
                        videoid,
                        mystic,
                        videoid=True,
                        video=video,
                    )
                except Exception:
                    LOGGER(__name__).error("change_stream: unhandled exception", exc_info=True)
                    return await mystic.edit_text(
                        _["call_6"], disable_web_page_preview=True
                    )

                stream = (
                    _video_stream(file_path) if video else _audio_stream(file_path)
                )

                try:
                    await client.play(chat_id, stream)
                except Exception:
                    LOGGER(__name__).error("change_stream: unhandled exception", exc_info=True)
                    return await app.send_message(
                        original_chat_id, text=_["call_6"]
                    )

                img = await get_thumb(videoid)
                button = stream_markup(_, videoid, chat_id)
                await mystic.delete()

                run = await app.send_photo(
                    chat_id=original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        title[:23],
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"

            elif "index_" in queued:
                stream = (
                    _video_stream(videoid) if video else _audio_stream(videoid)
                )

                try:
                    await client.play(chat_id, stream)
                except Exception:
                    LOGGER(__name__).error("change_stream: unhandled exception", exc_info=True)
                    return await app.send_message(
                        original_chat_id, text=_["call_6"]
                    )

                button = stream_markup(_, videoid, chat_id)

                run = await app.send_photo(
                    chat_id=original_chat_id,
                    photo=config.STREAM_IMG_URL,
                    caption=_["stream_2"].format(user),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"

            else:
                stream = (
                    _video_stream(queued) if video else _audio_stream(queued)
                )

                try:
                    await client.play(chat_id, stream)
                except Exception:
                    LOGGER(__name__).error("change_stream: unhandled exception", exc_info=True)
                    return await app.send_message(
                        original_chat_id, text=_["call_6"]
                    )

                if videoid == "telegram":
                    button = stream_markup(_, videoid, chat_id)

                    run = await app.send_photo(
                        chat_id=original_chat_id,
                        photo=(
                            config.TELEGRAM_AUDIO_URL
                            if str(streamtype) == "audio"
                            else config.TELEGRAM_VIDEO_URL
                        ),
                        caption=_["stream_1"].format(
                            config.SUPPORT_GROUP,
                            title[:23],
                            check[0]["dur"],
                            user,
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"

                elif videoid == "soundcloud":
                    button = stream_markup(_, videoid, chat_id)

                    run = await app.send_photo(
                        chat_id=original_chat_id,
                        photo=config.SOUNCLOUD_IMG_URL,
                        caption=_["stream_1"].format(
                            config.SUPPORT_GROUP,
                            title[:23],
                            check[0]["dur"],
                            user,
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"

                else:
                    img = await get_thumb(videoid)
                    button = stream_markup(_, videoid, chat_id)

                    run = await app.send_photo(
                        chat_id=original_chat_id,
                        photo=img,
                        caption=_["stream_1"].format(
                            f"https://t.me/{app.username}?start=info_{videoid}",
                            title[:23],
                            check[0]["dur"],
                            user,
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "stream"

    async def ping(self):
        pings = []

        if config.STRING1:
            pings.append(self.one.ping)
        if config.STRING2:
            pings.append(self.two.ping)
        if config.STRING3:
            pings.append(self.three.ping)
        if config.STRING4:
            pings.append(self.four.ping)
        if config.STRING5:
            pings.append(self.five.ping)

        if not pings:
            return "0"

        return str(round(sum(pings) / len(pings), 3))

async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Client...\n")

        if config.STRING1:
            await self.one.start()
        if config.STRING2:
            await self.two.start()
        if config.STRING3:
            await self.three.start()
        if config.STRING4:
            await self.four.start()
        if config.STRING5:
            await self.five.start()

    async def decorators(self):
        clients = [self.one, self.two, self.three, self.four, self.five]

        async def stream_services_handler(_, update: Update):
            await self.stop_stream(update.chat_id)

        async def stream_end_handler(client, update: StreamEnded):
            if update.chat_id in self._prejoin_tasks:
                return
            await self.change_stream(client, update.chat_id)

        

Hotty = Call()
