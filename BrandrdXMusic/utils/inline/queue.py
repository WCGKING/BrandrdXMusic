#https://github.com/WCGKING/BrandrdXMusic

from typing import Union
from BrandrdXMusic import app
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

COLORS = (ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER)

def queue_markup(
    _,
    DURATION,
    CPLAY,
    videoid,
    played: Union[bool, int] = None,
    dur: Union[bool, int] = None,
):
    not_dur = [
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
                style=COLORS[0],
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=COLORS[2],
            ),
        ]
    ]
    dur = [
        [
            InlineKeyboardButton(
                text=_["QU_B_2"].format(played, dur),
                callback_data="GetTimer",
                style=COLORS[0],
            )
        ],
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
                style=COLORS[1],
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=COLORS[2],
            ),
        ],
    ]
    upl = InlineKeyboardMarkup(not_dur if DURATION == "Unknown" else dur)
    return upl


def queue_back_markup(_, CPLAY):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"queue_back_timer {CPLAY}",
                    style=COLORS[0],
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=COLORS[2],
                ),
            ]
        ]
    )
    return upl


def aq_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"ADMIN Resume|{chat_id}",
                style=COLORS[1],
            ),
            InlineKeyboardButton(
                text="⏸️",
                callback_data=f"ADMIN Pause|{chat_id}",
                style=COLORS[0],
            ),
            InlineKeyboardButton(
                text="⏭️",
                callback_data=f"ADMIN Skip|{chat_id}",
                style=COLORS[1],
            ),
            InlineKeyboardButton(
                text="⏹️",
                callback_data=f"ADMIN Stop|{chat_id}",
                style=COLORS[2],
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=COLORS[2],
            )
        ],
    ]
    return buttons



def queuemarkup(_, vidid, chat_id):

    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_5"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=COLORS[1],
            ),
        ],
        [
            InlineKeyboardButton(
                text="ᴘᴀᴜsᴇ",
                callback_data=f"ADMIN Pause|{chat_id}",
                style=COLORS[0],
            ),
            InlineKeyboardButton(
                text="sᴛᴏᴘ",
                callback_data=f"ADMIN Stop|{chat_id}",
                style=COLORS[2],
            ),
            InlineKeyboardButton(
                text="sᴋɪᴘ",
                callback_data=f"ADMIN Skip|{chat_id}",
                style=COLORS[1],
            ),
        ],
        [
            InlineKeyboardButton(
                text="ʀᴇsᴜᴍ",
                callback_data=f"ADMIN Resume|{chat_id}",
                style=COLORS[1],
            ),
            InlineKeyboardButton(
                text="ʀᴇᴘʟᴀ",
                callback_data=f"ADMIN Replay|{chat_id}",
                style=COLORS[0],
            ),
        ],
        [
            InlineKeyboardButton(
                text="๏ ᴍᴏʀᴇ ๏",
                url="https://t.me/BRANDED_PAID_CC",
                style=COLORS[0],
            ),
        ],
    ]

    return buttons
