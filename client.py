from telethon import events, TelegramClient, connection
import asyncio, os, redis
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
wfffp = 1910015590
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
async def start_client(client, name, is_bot=False, token=None):
    try:
        if is_bot:
            await client.start(bot_token=token)
        else:
            await client.start()
        print(f"✅ تم تشغيل {name}")
    except Exception as e:
        print(f"❌ فشل تشغيل {name}: {e}")
async def main():
    global ABH1, ABH2, ABH3, ABH4, ABH5, ABH6, ABH7, ABH8, ABH9, ABH10, ABH11, ABH12, ABH13, ABH14, ABH15, ABHS
    start_tasks = [start_client(ABH, "البوت الأساسي (ABH)", is_bot=True, token=bot_token)]
    for i in range(1, 16):
        api_id_i = os.getenv(f"API_ID{i}")
        api_hash_i = os.getenv(f"API_HASH{i}")
        if api_id_i and api_hash_i:
            client = TelegramClient(
                f'code{i}',
                int(api_id_i),
                api_hash_i,
                connection=connection.ConnectionTcpFull,
                sequential_updates=False,
                auto_reconnect=True,
                connection_retries=None
            )
            clients[f'code{i}'] = client
            start_tasks.append(start_client(client, f'code{i}'))
        else:
            print(f"⚠️ تخطي code{i} لعدم توفر المتغيرات.")
    await asyncio.gather(*start_tasks)
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
    all_clients = [ABH] + [c for c in ABHS if c is not None]
    await asyncio.gather(*(client.run_until_disconnected() for client in all_clients))
all_clients = [ABH] + [c for c in ABHS if c is not None]
