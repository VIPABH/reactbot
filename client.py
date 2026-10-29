from telethon import events, TelegramClient, connection
import asyncio, os, redis, subprocess
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
wfffp = 1910015590
Max = 16
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
clients = {}
sessions = [f'code{num}' for num in range(1, Max+1)]
async def start_single_client(session, api_id_i, api_hash_i):
    try:
        client = TelegramClient(
            session, 
            int(api_id_i), 
            api_hash_i,
            connection=connection.ConnectionTcpFull,
            sequential_updates=False,
            auto_reconnect=True,
            connection_retries=None
        )
        await client.start()
        return session, client
    except Exception as e:
        print(f"Skipping {session} due to error: {e}")
        return session, None
async def main_init():
    await ABH.start(bot_token=bot_token)
    tasks = []
    for i, session in enumerate(sessions, start=1):
        api_id_i = os.getenv(f"API_ID{i}")
        api_hash_i = os.getenv(f"API_HASH{i}")
        if api_id_i and api_hash_i:
            tasks.append(start_single_client(session, api_id_i, api_hash_i))
        else:
            print(f"Skipping {session} due to missing environment variables.")
    if tasks:
        results = await asyncio.gather(*tasks)
        for session, client in results:
            if client:
                clients[session] = client
    global ABHS
    ABHS = [clients.get(session) for session in sessions if clients.get(session)]
    print(f"تم تشغيل {len(ABHS)} حساب بنجاح!")
