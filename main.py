import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from bot import Bot
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1002507596910

if __name__ == "__main__":
    Bot().run()
