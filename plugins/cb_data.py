import logging
import os
import time
from pyrogram import Client, filters
from pyrogram.types import ForceReply
from helper.utils import progress_for_pyrogram, convert
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import db
import humanize
from PIL import Image

logging.basicConfig(level=logging.INFO)

@Client.on_callback_query(filters.regex('cancel'))  
async def cancel(bot, update):  
    try:  
        await update.message.delete()  
    except Exception:
        return  

@Client.on_callback_query(filters.regex('rename'))  
async def rename(bot, update):  
    user_id = update.message.chat.id  
    date = update.message.date  
    await update.message.delete()  
    await update.message.reply_text("__𝙿𝚕𝚎𝚊𝚜𝚎 𝙴𝚗𝚝𝚎𝚛 𝙽𝚎𝚠 𝙵𝚒𝚕𝚎𝙽𝚊𝚖𝚎...__",  
    reply_to_message_id=update.message.reply_to_message.id,    
    reply_markup=ForceReply(True))  

@Client.on_callback_query(filters.regex("upload"))  
async def doc(bot, update):  
    type = update.data.split("_")[1]  
    new_name = update.message.text  
    try:
        new_filename = new_name.split(":-")[1].strip()
    except IndexError:
        await update.message.edit("❌ Error: Invalid file name format.")
        return

    # Use absolute path
    file_path = os.path.join(os.getcwd(), 'downloads', new_filename)  
    file = update.message.reply_to_message  
    ms = await update.message.edit("⚠️__**Please wait...**__\n__Downloading file to my server...__")  
    c_time = time.time()  

    try:  
        logging.info(f"Downloading file: {file.file_id}")
        path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=("Downloading file...", ms, c_time))  
        logging.info(f"File downloaded at {path}")
    except Exception as e:  
        await ms.edit(f"❌ Error during download: {e}")  
        return  

    if not os.path.exists(path):
        await ms.edit("❌ Error: File download failed.")
        return

    # Rename file
    splitpath = path.split("/downloads/")
    dow_file_name = os.path.basename(path)  
    old_file_name = path  
    logging.info(f"Renaming file from {old_file_name} to {file_path}")
    os.rename(old_file_name, file_path)

    if not os.path.exists(file_path):
        await ms.edit("❌ Error: Renamed file not found!")
        return

    logging.info(f"File renamed successfully: {file_path}")
    os.chmod(file_path, 0o777)  # Set permissions

    # Metadata extraction
    duration = 0  
    try:  
        metadata = extractMetadata(createParser(file_path))  
        if metadata.has("duration"):  
            duration = metadata.get('duration').seconds  
    except Exception:
        pass  

    user_id = int(update.message.chat.id)   
    ph_path = None   
    media = getattr(file, file.media.value)  
    c_caption = await db.get_caption(update.message.chat.id)  
    c_thumb = await db.get_thumbnail(update.message.chat.id)  

    if c_caption:  
        try:  
            caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size), duration=convert(duration))  
        except Exception as e:  
            await ms.edit(text=f"Your caption Error unexpected keyword ●> ({e})")  
            return  
    else:  
        caption = f"**{new_filename}**"  

    if media.thumbs or c_thumb:  
        if c_thumb:  
            ph_path = await bot.download_media(c_thumb)   
        else:  
            ph_path = await bot.download_media(media.thumbs[0].file_id)  
        Image.open(ph_path).convert("RGB").save(ph_path)  
        img = Image.open(ph_path)  
        img.resize((320, 320))  
        img.save(ph_path, "JPEG")  

    await ms.edit("⚠️__**Please wait...**__\n__Processing file upload....__")  
    c_time = time.time()  

    try:  
        logging.info(f"Sending file: {file_path}")
        if type == "document":  
            await bot.send_document(  
                update.message.chat.id,  
                document=file_path,  
                thumb=ph_path if ph_path else None,   
                caption=caption,   
                progress=progress_for_pyrogram,  
                progress_args=("⚠️__**Please wait...**__\n__Processing file upload....__", ms, c_time))  
        elif type == "video":   
            await bot.send_video(  
                update.message.chat.id,  
                video=file_path,  
                caption=caption,  
                thumb=ph_path if ph_path else None,  
                duration=duration,  
                progress=progress_for_pyrogram,  
                progress_args=("⚠️__**Please wait...**__\n__Processing file upload....__", ms, c_time))  
        elif type == "audio":   
            await bot.send_audio(  
                update.message.chat.id,  
                audio=file_path,  
                caption=caption,  
                thumb=ph_path if ph_path else None,  
                duration=duration,  
                progress=progress_for_pyrogram,  
                progress_args=("⚠️__**Please wait...**__\n__Processing file upload....__", ms, c_time))   
    except Exception as e:   
        await ms.edit(f"❌ Error during upload: {e}")   
        os.remove(file_path)  
        if ph_path:  
            os.remove
