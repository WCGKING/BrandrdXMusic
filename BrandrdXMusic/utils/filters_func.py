from enum import Enum, auto
from BrandrdXMusic import app
from pyrogram.types import InlineKeyboardMarkup, Message
from BrandrdXMusic.utils.msg_types import button_markdown_parser
from BrandrdXMusic.utils.notes_func import NoteFillings
from emojis import decode
from pyrogram.types import Message


async def SendFilterMessage(message: Message, filter_name: str, content: str, text: str, data_type: int):
    
    chat_id = message.chat.id
    message_id = message.id
    text, buttons = button_markdown_parser(text)
    
    text = NoteFillings(message, text)
    reply_markup = None
    if len(buttons) > 0:
        reply_markup = InlineKeyboardMarkup(buttons)
    else:
        reply_markup = None

    if data_type == 1:
        await app.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            reply_to_message_id=message_id
        )

    elif data_type == 2:
        await app.send_sticker(
            chat_id=chat_id,
            sticker=content,
            reply_markup=reply_markup,
            reply_to_message_id=message_id
        )
        
    elif data_type ==3:
        await app.send_animation(
            chat_id=chat_id,
            animation=content,
            reply_markup=reply_markup,
            reply_to_message_id=message_id
        )

    elif data_type == 4:
        await app.send_document(
            chat_id=chat_id,
            document=content,
            caption=text,
            reply_markup=reply_markup,
            reply_to_message_id=message_id
        )

    elif data_type == 5:
        await app.send_photo(
            chat_id=chat_id,
            photo=content,
            caption=text,
            reply_markup=reply_markup,
            reply_to_message_id=message_id
        )
    
    elif data_type == 6:
        await app.send_audio(
            chat_id=chat_id,
            audio=content,
            caption=text,
            reply_markup=reply_markup,
            reply_to_message_id=message_id
        )
    
    elif data_type == 7:
        await app.send_voice(
            chat_id=chat_id,
            voice=content,
            caption=text,
            reply_markup=reply_markup,
            reply_to_message_id=message_id
        )
    
    elif data_type == 8:
        await app.send_video(
            chat_id=chat_id,
            video=content,
            caption=text,
            reply_markup=reply_markup,
            reply_to_message_id=message_id
        )
    
    elif data_type == 9:
        await app.send_video_note(
            chat_id=chat_id,
            video_note=content,
            reply_markup=reply_markup,
            reply_to_message_id=message_id
        )


class FilterMessageTypeMap(Enum):
    text = auto()
    sticker = auto()
    animation= auto()
    document = auto()
    photo = auto()
    audio = auto()
    voice = auto()
    video = auto()
    video_note = auto()

async def GetFIlterMessage(message):
    data_type = None
    content = None
    text = str()

    raw_text = message.text or message.caption
    args = raw_text.split(None, 2)
        
    if len(args) >= 3 and not message.reply_to_message:
        text = message.text.markdown[len(message.command[0]) + len(message.command[1]) + 4 :]
        data_type = FilterMessageTypeMap.text.value

    if (
        message.reply_to_message
        and message.reply_to_message.text
    ):
        if len(args) >= 2:
            text = message.reply_to_message.text.markdown
            data_type = FilterMessageTypeMap.text.value
            
    elif (
        message.reply_to_message
        and message.reply_to_message.sticker
    ):
        content = message.reply_to_message.sticker.file_id
        data_type = FilterMessageTypeMap.sticker.value
    
    elif (
        message.reply_to_message
        and message.reply_to_message.animation
    ):
        content = message.reply_to_message.animation.file_id
        if message.reply_to_message.caption:
            text = message.reply_to_message.caption.markdown
        data_type = FilterMessageTypeMap.animation.value
        
    elif (
        message.reply_to_message
        and message.reply_to_message.document
    ):
        content = message.reply_to_message.document.file_id
        if message.reply_to_message.caption: 
            text = message.reply_to_message.caption.markdown 
        data_type = FilterMessageTypeMap.document.value

    elif (
        message.reply_to_message
        and message.reply_to_message.photo
    ):
        content = message.reply_to_message.photo.file_id
        if message.reply_to_message.caption:
            text = message.reply_to_message.caption.markdown
        data_type = FilterMessageTypeMap.photo.value

    elif (
        message.reply_to_message
        and message.reply_to_message.audio
    ):
        content = message.reply_to_message.audio.file_id
        if message.reply_to_message.caption:
            text = message.reply_to_message.caption.markdown 
        data_type = FilterMessageTypeMap.audio.value

    elif (
        message.reply_to_message
        and message.reply_to_message.voice
    ):
        content = message.reply_to_message.voice.file_id
        if message.reply_to_message.caption:
            text = message.reply_to_message.caption.markdown
        data_type = FilterMessageTypeMap.voice.value

    elif (
        message.reply_to_message
        and message.reply_to_message.video
    ):
        content = message.reply_to_message.video.file_id 
        if message.reply_to_message.caption:
            text = message.reply_to_message.caption.markdown 
        data_type= FilterMessageTypeMap.video.value

    elif (
        message.reply_to_message
        and message.reply_to_message.video_note
    ):
        content = message.reply_to_message.video_note.file_id
        text = None 
        data_type = FilterMessageTypeMap.video_note.value

    return (
        content,
        text,
        data_type
    )

def get_text_reason(message: Message) -> str:
    """This function returns text, and the reason of the user's arguments

    Args:
        message (Message): Message

    Returns:
        [str]: text, reason
    """
    text = decode(message.text)
    index_finder = [x for x in range(len(text)) if text[x] == '"']
    if len(index_finder) >= 2:
        text = text[index_finder[0]+1: index_finder[1]]
        reason = text[index_finder[1] + 2:]
        if not reason:
            reason = None
    else:
        text = message.command[1]
        reason = ' '.join(message.command[2:])
        if not reason:
            reason = None
    
    return (
        text,
        reason
        )
