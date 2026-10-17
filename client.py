from telethon import events, TelegramClient, connection
import os, redis
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
REACTBOT = TelegramClient(
    "REACTBOT",
    api_id,
    api_hash,
    connection=connection.ConnectionTcpFull,
    sequential_updates=False,
    auto_reconnect=True,
    connection_retries=None)
r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True)
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")
wfffp = 1910015590
bot = TelegramClient("botcode", api_id, api_hash)
mainABH = TelegramClient("wfffp", api_id, api_hash)
clients = {'wfffp': mainABH}
MAX = 1
sessions = [f'code{num}' for num in range(1, MAX + 1)]
for i, session in enumerate(sessions, start=1):
    api_id_i = os.getenv(f"API_ID{i}")
    api_hash_i = os.getenv(f"API_HASH{i}")
    if api_id_i and api_hash_i:
        clients[session] = TelegramClient(session, int(api_id_i), api_hash_i)
ABH1 = clients.get("code1")
ABH2 = clients.get("code2")
ABHS = [c for session_name, c in clients.items() if session_name != 'wfffp' and c is not None]
users = {}
async def sync_users():
    users.clear()
    for ABH in ABHS:
        me = await ABH.get_me()
        if me:
            users[me.id] = ABH
async def init_clients():
    if not bot.is_connected():
        await bot.start(bot_token=bot_token)
    react_token = os.getenv("REACTBOT")
    if react_token and not REACTBOT.is_connected():
        await REACTBOT.start(bot_token=react_token)
    if not mainABH.is_connected():
        await mainABH.start()
    for session_name, client in clients.items():
        if session_name == 'wfffp':
            continue
        if not client.is_connected():
            print(f"Starting {session_name}...")
            await client.start()
    await sync_users()
