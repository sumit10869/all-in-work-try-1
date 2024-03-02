import os
from config import Config
from pyrogram import Client, idle
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from pyrogram.raw import functions
from datetime import datetime
import time

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "log.txt", maxBytes=5000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)

# Auth Users
AUTH_USERS = [int(chat) for chat in Config.AUTH_USERS.split(",") if chat != '']

# Prefixes
prefixes = ["/", "~", "?", "!"]

if __name__ == "__main__":
    bot = Client(
        "StarkBot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=20,
        plugins=dict(root="plugins"),
        workers=50
    )

    async def sync_time():
        local_time = int(time.time())
        server_time = int((await bot.send(functions.Ping(ping_id=0))).ping_id)
        time_difference = server_time - local_time
        time_offset = int(time_difference / 2)
        return time_offset

    async def main():
        try:
            await bot.start()
            bot_info = await bot.get_me()
            LOGGER.info(f"<--- @{bot_info.username} Started (c) STARKBOT --->")

            while True:
                time_offset = await sync_time()
                LOGGER.info(f"Time offset with server: {time_offset} seconds")
                await asyncio.sleep(300)  # sleep for 5 minutes

        finally:
            await bot.stop()
            LOGGER.info(f"<---Bot Stopped--->")

    # Explicitly create and set the event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
