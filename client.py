from telethon import events, TelegramClient, connection
import asyncio, os, redis, subprocess
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
wfffp = 1910015590
Max = 15
ABH = TelegramClient(
    "REACTBOT",
    api_id,
    api_hash,
    connection=connection.ConnectionTcpFull,
    sequential_updates=False,
    auto_reconnect=True,
    connection_retries=None
).start(bot_token=bot_token)
r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")
clients = {}
sessions = [f'code{num}' for num in range(1, Max+1)]
for i, session in enumerate(sessions, start=1):
    api_id_i = os.getenv(f"API_ID{i}")
    api_hash_i = os.getenv(f"API_HASH{i}")
    if api_id_i and api_hash_i:
        clients[session] = TelegramClient(session, int(api_id_i), api_hash_i).start()
        print(f"{session} is working!")
    else:
        print(f"Skipping {session} due to missing environment variables.")
ABHS = [clients.get(session) for session in sessions]
