from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, CallbackContext
import json
import os
import subprocess

bot_token = '7732922339:AAHJsfwOnDWcs-Z5Eu1UqDbT3uq5are9izk'
bot = Bot(token=bot_token)

system_state_file = 'system_state.json'
monitoring_hours_file = 'monitoring_hours.json'
video_capture_process = None

def read_system_state():
    try:
        with open(system_state_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'armed': False}

def write_system_state(state):
    with open(system_state_file, 'w') as file:
        json.dump(state, file)

def read_monitoring_hours():
    try:
        with open(monitoring_hours_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'start': '21:00', 'end': '06:00'}

def write_monitoring_hours(hours):
    with open(monitoring_hours_file, 'w') as file:
        json.dump(hours, file)

def start_video_capture():
    global video_capture_process
    video_capture_process = subprocess.Popen(['python', 'video_capture.py'])

def stop_video_capture():
    global video_capture_process
    if video_capture_process:
        video_capture_process.terminate()
        video_capture_process = None

async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    await update.message.reply_text(f'Welcome to Smart CCTV Alert System! Your chat ID is {chat_id}')

async def arm_system(update: Update, context: CallbackContext):
    state = read_system_state()
    state['armed'] = True
    write_system_state(state)
    start_video_capture()
    await update.message.reply_text('System armed and video capture started.')

async def disarm_system(update: Update, context: CallbackContext):
    state = read_system_state()
    state['armed'] = False
    write_system_state(state)
    stop_video_capture()
    await update.message.reply_text('System disarmed and video capture stopped.')

async def set_hours(update: Update, context: CallbackContext):
    try:
        _, start, end = update.message.text.split()
        monitoring_hours = {'start': start, 'end': end}
        write_monitoring_hours(monitoring_hours)
        await update.message.reply_text(f'Successfully set monitoring hours to {start} - {end}')
    except ValueError:
        await update.message.reply_text('Usage: /sethours <start> <end> (e.g., /sethours 21:00 06:00)')

async def get_hours(update: Update, context: CallbackContext):
    monitoring_hours = read_monitoring_hours()
    start = monitoring_hours['start']
    end = monitoring_hours['end']
    await update.message.reply_text(f'Current monitoring hours: {start} - {end}')

application = Application.builder().token(bot_token).build()
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('arm', arm_system))
application.add_handler(CommandHandler('disarm', disarm_system))
application.add_handler(CommandHandler('sethours', set_hours))
application.add_handler(CommandHandler('gethours', get_hours))

application.run_polling()







