
from pyrogram import Client, filters
from config import *
from folder import create_folder
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
            file_name = sorted(files)[index]
            file_path = f"descarga/{file_name}"
            bot.send_document(chat_id=message.chat.id, document=file_path)
        except (ValueError, IndexError):
            bot.send_message(chat_id=message.chat.id, text=f"😰 No se pudo subir el archivo {file_number}: número de archivo no válido")

# create_folder
@bot.on_message(filters.command("create_folder"))
def cmd_create_folder(client, message):
    folder_name = " ".join(message.command[1:])
    create_folder(folder_name)
    bot.send_message(message.chat.id, f"The folder '{folder_name}' has been created!")

# listar archivos
@bot.on_message(filters.command('list'))
def list_files(client, message):
    files = os.listdir('descarga')
    if not files:
        bot.send_message(chat_id=message.chat.id, text="🚨No hay archivos en la carpeta de descarga🚨")
        return
    file_details = ""
    for index, file_name in enumerate(sorted(files), start=1):
        file_path = f"descarga/{file_name}"
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        file_details += f"{index}. {file_name} ({file_size:.2f} MB)\n"
    bot.send_message(chat_id=message.chat.id, text=file_details, disable_web_page_preview=True)

# delete files
@bot.on_message(filters.command('delete'))
def delete_files(client, message):
    files = os.listdir('descarga')
    if not files:
        bot.send_message(chat_id=message.chat.id, text="🤷‍♂️ No hay archivos en la carpeta de descarga 🤷‍♂️")
        return
    file_numbers = message.text.split(' ')[1:]
    if not file_numbers:
        bot.send_message(chat_id=message.chat.id, text="🤔 Debes especificar el número de al menos un archivo que deseas eliminar")
        return
    for file_number in file_numbers:
        try:
            index = int(file_number) - 1
            file_name = sorted(files)[index]
            file_path = f"descarga/{file_name}"
            os.remove(file_path)
            bot.send_message(chat_id=message.chat.id, text=f"🗑️ Archivo {file_name} eliminado 🗑️")
        except (ValueError, IndexError):
            bot.send_message(chat_id=message.chat.id, text=f"😰 No se pudo eliminar el archivo {file_number}: número de archivo no válido")

bot.run()
