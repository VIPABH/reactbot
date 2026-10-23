from telethon import events, TelegramClient, connection
import asyncio
import os
import redis
import traceback
import logging
import datetime
from start import *
api_id = int(os.getenv("API_ID", 0))
api_hash = os.getenv("API_HASH", "")
bot_token = os.getenv("BOT_TOKEN", "")
wfffp = int(os.getenv("WFFFP", 1910015590))
ABH = TelegramClient(
    "REACTBOT",
    api_id,
    api_hash,
    connection=connection.ConnectionTcpFull,
    sequential_updates=False,
    auto_reconnect=True,
    connection_retries=None
)
r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)
ABH.run_until_disconnected()
