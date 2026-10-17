import asyncio
import os
import redis
from telethon import events, TelegramClient, connection
api_id = int(os.getenv("API_ID", 0))
api_hash = os.getenv("API_HASH", "")
bot_token = os.getenv("bot_token", "")
wfffp = 1910015590
MAX = 15
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
bot = TelegramClient("botcode", api_id, api_hash)
mainABH = TelegramClient("wfffp", api_id, api_hash)
clients = {'wfffp': mainABH}
sessions = [f'code{num}' for num in range(1, MAX)]
for i, session in enumerate(sessions, start=1):
    api_id_i = os.getenv(f"API_ID{i}", api_id)
    api_hash_i = os.getenv(f"API_HASH{i}", api_hash)
    if api_id_i and api_hash_i:
        clients[session] = TelegramClient(session, int(api_id_i), api_hash_i)
ABHS = [c for session_name, c in clients.items() if session_name != 'wfffp' and c is not None]
users = {}
async def sync_users():
    """مزامنة معرفات الحسابات المساعدة"""
    users.clear()
    for ABH in ABHS:
        try:
            if not ABH.is_connected():
                await ABH.connect()
            me = await ABH.get_me()
            if me:
                users[me.id] = ABH
        except Exception as e:
            print(f"Error syncing user: {e}")
async def init_clients():
    if not bot.is_connected():
        await bot.start(bot_token=bot_token)
        print("✅ تم تشغيل البوت الأساسي (bot)")
    react_token = os.getenv("REACTBOT_TOKEN") or os.getenv("REACTBOT")
    if react_token and not REACTBOT.is_connected():
        try:
            await REACTBOT.start(bot_token=react_token)
            print("✅ تم تشغيل بوت الريأكشن (REACTBOT)")
        except Exception as e:
            print(f"⚠️ فشل تشغيل REACTBOT: {e}")
    if not mainABH.is_connected():
        await mainABH.start()
        print("✅ تم تشغيل الحساب الرئيسي (wfffp)")
    for session_name, client in clients.items():
        if session_name == 'wfffp':
            continue
        if not client.is_connected():
            try:
                print(f"⏳ جاري بدء تشغيل الحساب: {session_name}...")
                await client.start()
                print(f"✅ تم تشغيل {session_name}")
            except Exception as e:
                print(f"❌ فشل تشغيل {session_name}: {e}")
    await sync_users()
async def main():
    await init_clients()
    all_clients = [bot, REACTBOT, mainABH] + ABHS
    await asyncio.gather(*(client.run_until_disconnected() for client in all_clients if client))
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف السكريبت بواسطة المستخدم.")
