import asyncio
import os
import redis
from telethon import events, TelegramClient, connection
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")
wfffp = 1910015590
REACTBOT = TelegramClient(
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
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
clients = {}
for i in range(1, 15):
    api_id_i = os.getenv(f"API_ID{i}")
    api_hash_i = os.getenv(f"API_HASH{i}")
    if api_id_i and api_hash_i:
        print(f"Starting code{i}...")
        clients[f'code{i}'] = TelegramClient(f'code{i}', int(api_id_i), api_hash_i).start()
        print(f"{f'code{i}'} is working!")
    else:
        print(f"Skipping code{i} due to missing environment variables.")
ABH1 = clients.get("code1")
ABH2 = clients.get("code2")
ABH3 = clients.get("code3")
ABH4 = clients.get("code4")
ABH5 = clients.get("code5")
ABH6 = clients.get("code6")
ABH7 = clients.get("code7")
ABH8 = clients.get("code8")
ABH9 = clients.get("code9")
ABH10 = clients.get("code10")
ABH11 = clients.get("code11")
ABH12 = clients.get("code12")
ABH13 = clients.get("code13")
ABH14 = clients.get("code14")
ABH15 = clients.get("code15")
ABHS = [ABH1, ABH2, ABH3, ABH4, ABH5, ABH6, ABH7, ABH8, ABH9, ABH10, ABH11, ABH12, ABH13, ABH14, ABH15]
