from telethon import events, TelegramClient, connection
import asyncio, os, redis, subprocess
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
sessions = [f'code{num}' for num in range(1, 16)]
for i, session in enumerate(sessions, start=1):
    api_id_i = os.getenv(f"API_ID{i}")
    api_hash_i = os.getenv(f"API_HASH{i}")
    if api_id_i and api_hash_i:
        print(f"Starting {session}...")
        clients[session] = TelegramClient(session, int(api_id_i), api_hash_i).start()
        print(f"{session} is working!")
    else:
        print(f"Skipping {session} due to missing environment variables.")
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
async def run_cmd(command: str):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().strip(), stderr.decode().strip(), process.returncode
@ABH.on(events.NewMessage(pattern="^(تحديث|up)$", from_users=[1910015590]))
async def update_repo(event):
    try:
        stdout, stderr, code = await run_cmd("git pull")
        if code == 0:
            await event.reply(f" تم تحديث السورس بنجاح\n\n{stdout or 'لا توجد تحديثات'}")
            os.execv(sys.executable, [sys.executable, os.path.abspath("config.py")])
        else:
            await hint(f" حدث خطأ أثناء التحديث:\n\n{stderr}")
    except Exception as e:
        await e.reply(f"⚠️ خطأ غير متوقع:\n\n{e}")
