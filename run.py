import asyncio
import uvloop
import traceback
import logging
import datetime
import os
from telethon import TelegramClient, connection
from start import *
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
clients = {}
ABH1 = ABH2 = ABH3 = ABH4 = ABH5 = ABH6 = ABH7 = ABH8 = ABH9 = ABH10 = ABH11 = ABH12 = ABH13 = ABH14 = ABH15 = None
ABHS = []
all_clients = []
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
class TelegramLogsHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            err_entry = self.format(record)
            try:
                loop = asyncio.get_running_loop()
                if loop.is_running():
                    loop.create_task(send_error(err_entry, source="سجل النظام (Logging)"))
            except RuntimeError:
                pass
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        TelegramLogsHandler()
    ]
)
logger = logging.getLogger(__name__)
async def send_error(error_text, source="غير معروف"):
    if not error_text or "send_message" in error_text or "send_error" in error_text:
        return
    try:
        clean_error = str(error_text).strip()[:3500]        
        if not clean_error:
            clean_error = "لا يوجد تفاصيل نصية للخطأ."
        report = (
            f"⚠️ **تنبيه: خطأ تقني مكتشف**\n"
            f"__________________________\n\n"
            f"🔍 **المصدر:** `{source}`\n"
            f"__________________________\n\n"
            f"⏰ **الوقت:** `{datetime.datetime.now().strftime('%H:%M:%S')}`\n"
            f"__________________________\n\n"
            f"💻 **التفاصيل:**\n"
            f"```python\n{clean_error}\n```\n"
            f"__________________________"
        )         
        await ABH.send_message(wfffp, report)
    except Exception as e:
        try:
            await ABH.send_message(wfffp, f"خطأ خام من {source}:\n\n{error_text[:3800]}")
        except:
            print(f"❌ فشل الإرسال النهائي تماماً: {e}")
def handle_async_exception(loop, context):
    exception = context.get("exception")
    if exception:
        err_text = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
    else:
        err_text = f"Asyncio Message: {context['message']}"    
    if loop.is_running():
        loop.create_task(send_error(err_text, source="محرك الأحداث (Asyncio)"))
    else:
        print(f"Loop closed. Critical Error: {err_text}")
async def start_client_task(client, name, is_bot=False, token=None):
    try:
        if is_bot:
            await client.start(bot_token=token)
        else:
            await client.start()
        print(f"✅ تم تشغيل {name}")
    except Exception as e:
        print(f"❌ فشل تشغيل {name}: {e}")
async def start_everything():
    global ABH1, ABH2, ABH3, ABH4, ABH5, ABH6, ABH7, ABH8, ABH9, ABH10, ABH11, ABH12, ABH13, ABH14, ABH15, ABHS, all_clients
    loop = asyncio.get_running_loop()
    loop.set_exception_handler(handle_async_exception)
    start_tasks = [start_client_task(ABH, "البوت الأساسي (ABH)", is_bot=True, token=bot_token)]
    active_clients_dict = {}
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
            active_clients_dict[f'code{i}'] = client
            start_tasks.append(start_client_task(client, f'code{i}'))
        else:
            print(f"⚠️ تخطي code{i} لعدم توفر المتغيرات.")
    await asyncio.gather(*start_tasks)
    clients.update(active_clients_dict)
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
def run_bot():
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("Loop is closed")
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)    
    if loop.is_running():
        loop.create_task(start_everything())
    else:
        try:
            loop.run_until_complete(start_everything())
        except KeyboardInterrupt:
            print("\nتم إيقاف البوت يدوياً.")
        except Exception:
            print(traceback.format_exc())
        finally:
            try:
                loop.close()
            except:
                pass
if __name__ == "__main__":
    run_bot()
