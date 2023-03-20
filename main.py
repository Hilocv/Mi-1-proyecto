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

#DOWNLOADS
@bot.on_message(filters.document | filters.video | filters.audio | filters.photo)
def download_files(client, message):
    file_type = message.document or message.video or message.audio or message.photo
    file_path = f"descarga/{file_type.file_name}"
    message.download(file_path)
    bot.send_message(chat_id=message.chat.id, text=f"📥Archivo {file_type.file_name} descargado📥")

#Command to upload a file
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
 
 
#Command to compress a file in parts
@bot.on_message(filters.command('seven'))
def cmd_compress(bot, message):
    files = os.listdir('descarga')
    if not files:
        bot.send_message(chat_id=message.chat.id, text="💢 No hay archivos en la carpeta de descarga 💢")
        return
    try:
        file_number = int(message.text.split(' ')[1]) - 1
        file_size_mb = int(message.text.split(' ')[2])
    except (ValueError, IndexError):
        bot.send_message(chat_id=message.chat.id, text="🤔 Debes especificar el número de archivo y el tamaño máximo por parte en megabytes")
        return
    try:
        file_name = sorted(files)[file_number]
        file_path = f"descarga/{file_name}"
        parts_folder = f"descarga/parts"
        if not os.path.exists(parts_folder):
            os.mkdir(parts_folder)
        with open(file_path, "rb") as f:
            file_size = os.path.getsize(file_path)
            num_parts = math.ceil(file_size / (file_size_mb * 1048576))
            for i in range(num_parts):
                part_file_path = f"{parts_folder}/{file_name}.part{i+1}"
                with open(part_file_path, "wb") as p:
                    shutil.copyfileobj(f, p, file_size_mb * 1048576)
                bot.send_document(chat_id=message.chat.id, document=part_file_path)
                os.remove(part_file_path)
    except (ValueError, IndexError):
        bot.send_message(chat_id=message.chat.id, text=f"😰 No se pudo comprimir el archivo {file_number}: número de archivo no válido")           
    
   #listar archivos
@bot.on_message(filters.command('list'))
def list_files(client, message):
    files = os.listdir('descarga')
    if not files:
        client.send_message(chat_id=message.chat.id, text="🚨No hay archivos en la carpeta de descarga🚨")
        return
    file_details = ""
    for index, file_name in enumerate(sorted(files), start=1):
        file_path = f"descarga/{file_name}"
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        file_details += f"{index}. {file_name} ({file_size:.2f} MB)\n"
    bot.send_message(chat_id=message.chat.id, text=f"🗂️ Archivos descargados🗂️:\n{file_details}")

#Command to delete all files
@bot.on_message(filters.command('deleteall'))
def delete_all_files(client, message):
    files = os.listdir('descarga')
    if not files:
        bot.send_message(chat_id=message.chat.id, text="💢 No hay archivos en la carpeta de descarga 💢")
        return
    for file_name in files:
        file_path = f"descarga/{file_name}"
        os.remove(file_path)
    client.send_message(chat_id=message.chat.id, text="🔥 ¡Todos los archivos han sido eliminados de la carpeta de descarga! 🔥")
    
#ELIMINAR
@bot.on_message(filters.command('delete'))
def delete_file(bot, message):
    files = os.listdir('descarga')
    if not files:
        bot.send_message(chat_=message.chat., text="💢 Carpeta vacía💢")
        return
    file_numbers = message.text.split(' ')[1:]
    if not file_numbers:
        bot.send_message(chat_=message.chat.id, text="🤔Debes especificar el número de al menos un archivo que deseas eliminar")
        return
    deleted_files = []
    for file_number in file_numbers:
        try:
            index = int(file_number) - 1
            file_name = sorted(files)[index]
            file_path = f"descarga/{file_name}"
            os.remove(file_path)
            deleted_files.append(file_name)
        except (ValueError, IndexError):
            bot.send_message(chat_id=message.chat.id, text=f"😰No se pudo eliminar el archivo {file_number}: número de archivo no válido")
    if deleted_files:
        bot.send_message(chat_id=message.chat.id, text=f"🔥Archivos eliminados de la carpeta de descarga: {', '.join(deleted_files)}")
    
#Welcome message for new group members
GROUP = 'Python_test45'
WELCOME_MESSAGE = 'Bienvenido al grupo'
@bot.on_message(filters.chat(GROUP) & filters.new_chat_members)
def welcome(client, message):
    message.reply_text(WELCOME_MESSAGE)

#Command start
@bot.on_message(filters.command('start'))
def cmd_start(bot, message):
    bot.send_photo(message.chat.id,'https://telegra.ph/file/de4a6ec485c1ab87b2b47.jpg',caption = STARTED)

#Delete_message
@bot.on_message(filters.private) # solo eliminar los mensajes en chats privados
def delete_message(client, message):
    bot.delete_messages(chat_id=message.chat.id, message_ids=message.message_id)
#Command to get user ID
@bot.on_message(filters.command('id'))
def cmd_id(bot, message):
    bot.send_message(message.chat.id, f'Tu ID es: <code>{message.chat.id}</code>')

#Command help
@bot.on_message(filters.command('help'))
def cmd_help(bot, message):
    message.reply_text(HELP)

#Command to send an audio file
@bot.on_message(filters.command('audio'))
def cmd_audio(bot, message):
    bot.send_audio(message.chat.id, 'CQACAgEAAxkBAAIDxWQXcKeIvk1O4e0U7UfbA7Bb3cYbAAJDDQACCdEwR2yWf2_FmfjOHgQ',caption = 'Toma tu audio')

#Command to send a photo
@bot.on_message(filters.command('foto'))
def cmd_foto(bot, message):
    bot.send_photo(message.chat.id, 'https://telegra.ph/file/da6d4d035e9540e69ae2a.jpg', caption='¡Aquí está tu foto! :)')
    
#Command to send an video file
@bot.on_message(filters.command('video'))
def cmd_video(bot, message):
    bot.send_video(message.chat.id,'BAACAgEAAxkBAAIEdmQXyjMzWeGTOmcdv8b9ytPDT75BAAKVAgACOrxoRBEWux5Hl_RFHgQ',caption = 'Mira q buena peli😇')
    
 #Command to send an document file
@bot.on_message(filters.command('document'))
def cmd_document(bot, message):
    bot.send_document(message.chat.id,'BQACAgEAAxkBAAIEg2QXzAcH-2nE_KwcSOvHkupPsWfIAAL-AgAC6BtBRKPqdwi5XnX2HgQ',caption = 'Archivo pesado😗') 
 
  
 #Command to send an document file
@bot.on_message(filters.command('voice'))
def cmd_voice(bot, message):
    bot.send_voice(message.chat.id,'AwACAgEAAxkBAAIEl2QXzi5DpB_vLSjBFsGbPTy0AAHimQACHgMAAkSowURCtGcjnUxfdx4E',caption = 'Test de audio😁')        
print('Bot running...')
bot.run()