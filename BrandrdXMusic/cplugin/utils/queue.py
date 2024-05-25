from BrandrdXMusic.misc import clonedb


async def put(
    chat_id,
    title,
    duration,
    videoid,
    file_path,
    ruser,
    user_id,
):
    put_f = {
        "title": title,
        "duration": duration,
        "file_path": file_path,
        "videoid": videoid,
        "req": ruser,
        "user_id": user_id,
    }
    get = clonedb.get(chat_id)
    if get:
        clonedb[chat_id].append(put_f)
    else:
        clonedb[chat_id] = []
        clonedb[chat_id].append(put_f)
