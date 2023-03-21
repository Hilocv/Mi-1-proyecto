from pyrogram import Client, filters
from config import *
from folder import create_folder
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import os
import requests
import math
import shutil
import zipfile
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
#funcion_seven
def compress_files(file_numbers, part_size):
    files = os.listdir('descarga')
    if not files:
        return "🚨 No hay archivos en la carpeta de descarga 🚨"
    if not file_numbers:
        return "🤔 Debes especificar el número de al menos un archivo que deseas comprimir"
    for file_number in file_numbers:
        try:
            index = int(file_number) - 1
            file_name = sorted(files)[index]
            file_path = f"descarga/{file_name}"
            file_size = os.path.getsize(file_path)
            parts = math.ceil(file_size / (part_size * 1024 * 1024))
            with open(file_path, 'rb') as f_in:
                for part in range(parts):
                    part_path = f"descarga/{file_name}.part{part+1}"
                    with open(part_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out, part_size * 1024 * 1024)
            compressed_file_name = f"{file_name}.zip"
            with zipfile.ZipFile(compressed_file_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for part in range(parts):
                    part_path = f"descarga/{file_name}.part{part+1}"
                    zip_file.write(part_path)
                    os.remove(part_path)
            return f"✅ Archivo {file_name} comprimido y dividido en {parts} partes de {part_size} MB ✅"
        except (ValueError, IndexError):
            return f"😰 No se pudo comprimir el archivo {file_number}: número de archivo no válido"

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
#Comprimir

@bot.on_message(filters.command('seven'))
def compress_and_split_files(client, message):
    file_numbers = message.text.split(' ')[1:-1]
    part_size = int(message.text.split(' ')[-1])
    result = compress_files(file_numbers, part_size)
    bot.send_message(chat_id=message.chat.id, text=result)
    

   #listar archivos
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
        bot.send_message(message.chat.id,"🔥 ¡Todos los archivos han sido eliminados de la carpeta de descarga! 🔥")
    
#ELIMINAR
@bot.on_message(filters.command('delete'))
def delete_file(bot, message):
    files = os.listdir('descarga')
    if not files:
        bot.send_message(message.chat.id,"💢 Carpeta vacía💢")
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

#Command help
@bot.on_message(filters.command('help'))
def cmd_help(bot,message):
    bot.send_message(message.chat.id,HELP)
    
    
#Command InlineKeyboardMarkup [Button]
REPORT_MESSAGE = '🚦REPORTAR_FALLA🚦'
REPORT_MESSAGE_BUTTONS = [
  [InlineKeyboardButton('👤ADMIN',url='https://t.me/nautaii'),
  InlineKeyboardButton('🏵️CHANEL',url='https://t.me/nautidev')
  ],
  [
  InlineKeyboardButton('🗂️Data',url='https://t.me/database'),
  InlineKeyboardButton('🤔Otro',url='https://t.me/otros')
  ]
  ]
@bot.on_message(filters.command('report'))
def cmd_report(bot,message):
    text = REPORT_MESSAGE
    reply_markup = InlineKeyboardMarkup(REPORT_MESSAGE_BUTTONS)
    message.reply(
      text=text,
      reply_markup=reply_markup,
      disable_web_page_preview=True
      )
      

#Command to get user ID
@bot.on_message(filters.command('id'))
def cmd_id(bot, message):
    bot.send_message(message.chat.id, f'Tu ID es: <code>{message.chat.id}</code>')
    
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
