from pyrogram import *
import yt_dlp
from . import *
from pyrogram import Client, filters
from pytgcalls import StreamType
from pytgcalls.types.input_stream import *
from pytgcalls.types.input_stream.quality import *


# Audio Stream
@on_message("play", allow_stan=True)
async def audio_stream(client, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    audio = (
        (replied.audio or replied.voice or
        replied.video or replied.document)
        if replied else None
    )
    m = await eor(message, "**🔄 Processing ...**")
    try:
        if audio:
            await m.edit("**📥 Downloading ...**")
            file = await replied.download()
        else:
            if len(message.command) < 2:
                 return await m.edit("**🤖 Give Some Query ...**")
            text = message.text.split(None, 1)[1]
            if "?si=" in text:
                query = text.split("?si")[0]
            else:
                query = text
            await m.edit("**🔍 Searching ...**")
            search = get_youtube_video(query)
            stream = search[0]
            file = await get_youtube_stream(stream)
        await m.edit("**🔄 Processing ...**")
        check = db.get(chat_id)
        if not check:
            await call.join_group_call(
                chat_id,
                AudioPiped(
                    file,
                    HighQualityAudio(),
                ),
                stream_type=StreamType().pulse_stream
            )
            await put_que(chat_id, file, "Audio")
            await m.edit("**🥳 Streaming Started!**")
            await m.delete()
        else:
            pos = await put_que(chat_id, file, "Audio")
            await m.edit(f"**😋 Added To Queue #{pos}**")
            await m.delete()
    except Exception as e:
        await m.edit(f"**Error:** `{e}`")

  
# Video Stream
@on_message("vplay", allow_stan=True)
async def video_stream(client, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    video = (
        (replied.audio or replied.voice or
        replied.video or replied.document)
        if replied else None
    )
    m = await eor(message, "**🔄 Processing ...**")
    try:
        if video:
            await m.edit("**📥 Downloading ...**")
            file = await replied.download()
        else:
            if len(message.command) < 2:
                 return await m.edit("**🤖 Give Some Query ...**")
            text = message.text.split(None, 1)[1]
            if "?si=" in text:
                query = text.split("?si")[0]
            else:
                query = text
            await m.edit("**🔍 Searching ...**")
            search = get_youtube_video(query)
            stream = search[0]
            file = await get_youtube_stream(stream)
        await m.edit("**🔄 Processing ...**")
        check = db.get(chat_id)
        if not check:
            await call.join_group_call(
                chat_id,
                AudioVideoPiped(
                    file,
                    HighQualityAudio(),
                    HighQualityVideo(),
                ),
                stream_type=StreamType().pulse_stream
            )
            await put_que(chat_id, file, "Video")
            await m.edit("**🥳 Streaming Started!**")
            await message.delete()
        else:
            pos = await put_que(chat_id, file, "Video")
            await m.edit(f"**😋 Added To Queue #{pos}**")
            await m.delete()
    except Exception as e:
        await m.edit(f"**Error:** `{e}`")


# Pause Stream
@on_message("pause", allow_stan=True)
async def pause_stream(client, message):
    chat_id = message.chat.id
    try:
        check = db.get(chat_id)
        if check:
            await call.pause_stream(chat_id)
            return await eor(message, "**Stream Paused !**")
        else:
            return await eor(message, "**Nothing Playing !**")
    except Exception as e:
        await eor(message, f"**Error:** `{e}`")


# Resume Stream
@on_message("resume", allow_stan=True)
async def resume_streams(client, message):
    chat_id = message.chat.id
    try:
        check = db.get(chat_id)
        if check:
            await call.resume_stream(chat_id)
            return await eor(message, "**Stream Resumed !**")
        else:
            return await eor(message, "**Nothing Playing !**")
    except Exception as e:
        await eor(message, f"**Error:** `{e}`")
        
        
# Skip To Next Stream
@on_message("skip", allow_stan=True)
async def change_streams(client, message):
    chat_id = message.chat.id
    try:
        check = db.get(chat_id)
        if check:
            que = db[chat_id]
            que.pop(0)
            if len(que) == 0:
                await call.leave_group_call(chat_id)
                return await eor(message, "Empty Queue !")
            else:
                file = check[0]["file"]
                type = check[0]["type"]
                if type == "Audio":
                    stream = AudioPiped(
                        file,
                        HighQualityAudio(),
                    )
                elif type == "Video":
                    stream = AudioVideoPiped(
                        file,
                        HighQualityAudio(),
                        HighQualityVideo(),
                    )
                await call.change_stream(chat_id, stream)
                return await eor(message, "🥳 Skipped !")
        else:
            return await eor(message, "**Nothing Playing ...**")
    except Exception as e:
        await eor(message, f"**Error:** `{e}`")


# Stop/End Stream
@on_message("end", allow_stan=True)
async def leave_streams(client, message):
    chat_id = message.chat.id
    try:
        check = db.get(chat_id)
        if check:
            db.pop(chat_id)
            await call.leave_group_call(chat_id)
            return await eor(message, "**Stream Stopped !**")
        else:
            return await eor(message, "**Nothing Playing !**")
    except Exception as e:
        await eor(message, f"**Error:** `{e}`")


