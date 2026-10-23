import asyncio
import os
from telethon import TelegramClient, connection
import redis
from start import *
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
wfffp = 1910015590

# 1. إعداد متغيرات البوت الأساسي
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

ABH = TelegramClient(
    "REACTBOT",
    api_id,
    api_hash,
    connection=connection.ConnectionTcpFull,
    sequential_updates=False,
    auto_reconnect=True,
    connection_retries=None,
)

# 2. إعداد الجلسات الـ 15 وتخزينها في القاموس
clients = {}
for i in range(1, 16):
    session = f"code{i}"
    api_id_i = os.getenv(f"API_ID{i}")
    api_hash_i = os.getenv(f"API_HASH{i}")

    if api_id_i and api_hash_i:
      clients[session] = TelegramClient(session, int(api_id_i), api_hash_i)
    else:
      print(f"Skipping {session} due to missing environment variables.")

# 3. تشغيل البوت وجميع الجلسات معاً دفعة واحدة عبر الحدث العام (Event Loop)
loop = asyncio.get_event_loop()

async def _start_all():
    tasks = [ABH.start(bot_token=bot_token)]
    for client in clients.values():
        tasks.append(client.start())
    
    print("Launching all clients concurrently...")
    await asyncio.gather(*tasks)
    print("All clients are up and running!")

loop.run_until_complete(_start_all())

# 4. تعيين المتغيرات الفردية مباشرة عالمياً كما طلبت
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

ABHS = [
    ABH1, ABH2, ABH3, ABH4, ABH5, 
    ABH6, ABH7, ABH8, ABH9, ABH10, 
    ABH11, ABH12, ABH13, ABH14, ABH15
]

# 5. إبقاء البوت وجميع الجلسات متصلة للعمل بشكل دائم
all_active_clients = list(clients.values()) + [ABH]
loop.run_until_complete(
    asyncio.gather(*(client.run_until_disconnected() for client in all_active_clients if client))
)
