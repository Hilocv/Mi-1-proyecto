from pyrogram import Client, filters
from config import *
import os
import requests
import math
import shutil

bot = Client(
    "My bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# DOWNLOADS
@bot.on_message(filters.document | filters.video | filters.audio | filters.photo)
def download_files(client, message):
    file_type = message.document or message.video or message.audio or message.photo
    file_path = f"descarga/{file_type.file_name}"
    message.download(file_path)
    bot.send_message(chat_id=message.chat.id, text=f"📥Archivo {file_type.file_name} descargado📥")

# Command to upload a file
@bot.on_message(filters.command('up'))
def cmd_upload(bot, message):
    files = os.listdir('descarga')
    if not files:
        bot.send_message(chat_id=message.chat.id, text="💢 No hay archivos en la carpeta de descarga 💢")
        return
    file_numbers = message.text.split(' ')[1:]
    if not file_numbers:
        bot.send_message(chat_id=message.chat.id, text="🤔 Debes especificar el número de al menos un archivo que deseas subir")
        return
    for file_number in file_numbers:
        try:
            index = int(file_number) - 1
            file_path = f"descarga/{files[index]}"
            bot.send_chat_action(chat_id=message.chat.id, action="upload_document")
            bot.send_document(chat_id=message.chat.id, document=file_path)
            bot.send_message(chat_id=message.chat.id, text=f"📤Archivo {files[index]} enviado📤")
            os.remove(file_path)
        except (ValueError, IndexError):
            bot.send_message(chat_id=message.chat.id, text=f"💢 Archivo {file_number} no encontrado 💢")

bot.run()
