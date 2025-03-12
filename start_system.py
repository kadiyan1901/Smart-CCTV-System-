#script to start both telegram bot,erb server and video capture and alert system simuntaneously 
import subprocess
import time

# Paths to your scripts
telegram_bot_script = "telegram_bot.py"
video_capture_script = "video_capture.py"
flask_app_script = "app.py"

def start_telegram_bot():
    return subprocess.Popen(['python', telegram_bot_script])

def start_video_capture():
    return subprocess.Popen(['python', video_capture_script])

def start_flask_server():
    return subprocess.Popen(['python', flask_app_script])

def main():
    # Start Telegram bot
    bot_process = start_telegram_bot()
    time.sleep(2)  # Give the bot some time to start

    # Start video capture
    video_process = start_video_capture()
    time.sleep(2)  # Give video capture some time to start

    # Start Flask web server
    flask_process = start_flask_server()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        bot_process.terminate()
        video_process.terminate()
        flask_process.terminate()

if __name__ == "__main__":
    main()

