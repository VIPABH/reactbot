import asyncio, uvloop, traceback, logging
from client import *
from start import *
class TelegramLogsHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            err_entry = self.format(record)
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(send_error(err_entry, source="سجل النظام (Logging)"))
            except:
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
            f"⏰ **الوقت:** `{datetime.datetime.now(baghdad_tz).strftime('%H:%M:%S')}`\n"
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
async def shutdown(loop):
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
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
async def start_everything():
    loop = asyncio.get_running_loop()
    loop.set_exception_handler(handle_async_exception)
    await ABH.start(bot_token=bot_token)
    await ABH.run_until_disconnected()
    print('bot is running')
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start_everything())
    except KeyboardInterrupt:
        print("\nتم إيقاف البوت يدوياً.")
    except Exception:
        print(traceback.format_exc())
    finally:
        loop.close()
