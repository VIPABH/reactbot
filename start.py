from telethon.tl.functions.messages import GetMessagesViewsRequest, SendReactionRequest
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import MessageEntityCustomEmoji
from telethon.tl.types import ChannelParticipantAdmin
from telethon.errors import UserNotParticipantError
from telethon.tl.types import ReactionEmoji
from telethon.tl.types import Channel
from datetime import datetime
from zoneinfo import ZoneInfo
from io import BytesIO
from helpers import *
# from client import *
import asyncio, random, re
wfffp = 1910015590
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")
ABH = TelegramClient(
    "REACTBOT",
    api_id,
    api_hash,
    connection=connection.ConnectionTcpFull,
    sequential_updates=False,
    auto_reconnect=True,
    connection_retries=None
).start(bot_token=bot_token)
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
info = create('data.json')
def save_data():
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        return False
@ABH.on(events.NewMessage)
async def _(e):
    if e.text == 'ارسل1':
        return await e.reply(str(info[str(e.sender_id)]))
    elif e.text == 'ارسل2':
        return await e.reply(str(session[e.sender_id]))
    elif e.text == 'ارسل3':
        await ABH1.send_message(wfffp, '.')
        return await e.reply(f'{len(clients)} {len(ABHS)}')
    await is_user(e)
    await _filter(e)
@ABH.on(events.CallbackQuery)
async def _(e):
    await is_user(e)
back = [Button.inline('الرجوع', data='back', style=blue, icon=5352759161945867747)]
def buttons(e):
    id = str(e.sender_id)
    if id not in info or not info[id].values():
        b = [
            Button.inline('اضف قناة', data='add_channle', style=green, icon=5222040745665379997), 
            Button.inline('رياكت', data='react', style=green, icon=5884106131822875141), 
        ]
    else:
        b = [
            Button.inline('اضف قناة', data='add_channle', style=blue, icon=5222040745665379997),
            Button.inline('حذف قناة', data='del_channle', style=red, icon=5408832111773757273),
            Button.inline('القنوات المضافة', data='list_channles', style=blue, icon=6323116093724428158),
            Button.inline('الاعدادات', data='settings', style=green, icon=5258096772776991776),
            Button.inline('رياكت', data='react', style=green, icon=5884106131822875141)
            ]
    return chunk_list(b)
session = {}
@ABH.on(events.NewMessage(pattern=r'^/start$'))
async def start(e):
    await send(e, f'اهلا عزيزي ( {await ment(e)} ) اني بوت مال رياكشن وظيفتي اضيفلك رياكشنات ومشاهدات لقناتك', buttons=buttons(e))
    session[e.sender_id] = {}
@ABH.on(events.CallbackQuery(pattern=b'^(add_channle|del_channle|list_channles|settings|back|react)$'))
async def start_callback(e):
    id = e.sender_id
    if not session.get(id):
        session[e.sender_id] = {}
    data = e.data.decode('utf-8')
    if data == 'back':
        return await e.edit('تفضل الازرار كدامك', buttons=buttons(e))
    elif data == 'del_channle':
        if not info.get(str(id)):return await e.edit('ماعندك قنوات مضافة', buttons=back)
        ids = [int(id) for id in info[str(id)]]
        chats = await ABH.get_entity(ids)
        b = [Button.inline(chat.title, data=f'delete:{chat.id}', style=red, icon=5258130763148172425) for chat in chats]
        button = chunk_list(b)
        button.append(back)
        return await e.edit('اختر قناة لحذفها', buttons=button)
    elif data == 'list_channles':
        if not info.get(str(id)):return await e.edit('ماعندك قنوات مضافة', buttons=back)
        ids = [int(id) for id in info[str(id)]]
        chats = await ABH.get_entity(ids)
        b = []
        text = 'قنواتك المضافة🗒️:'
        for num, chat in enumerate(chats, start=1):
            b.append(Button.inline(chat.title, data=f'channle:{chat.id}', style=green, icon=5258096772776991776))
            url=f'https://t.me/{chat.username}' if chat.username else f'https://t.me/c/{str(chat.id).replace("-100", "")}/1'
            text += f"""
            - القناة {ordinal_arabic_female(num) if ordinal_arabic_female(num) else num} - ( [{chat.title}]({url}) ) - ( `{chat.id}` )"""
        button = chunk_list(b)
        button.append(back)
        return await e.edit(text, buttons=button)
    elif data == "settings":
        if not info.get(str(id)):return await e.edit('ماعندك قنوات مضافة', buttons=back)
        ids = [int(id) for id in info[str(id)]]
        chats = await ABH.get_entity(ids)
        b = [Button.inline(chat.title, data=f'channle:{chat.id}', style=green, icon=5258096772776991776) for chat in chats]
        button = chunk_list(b)
        button.append(back)
        return await e.edit('اختر قناة لتعديل اعداداتها', buttons=button)
    elif data == 'add_channle':
        session[id] = {"step": data, 'chat': None}
        await e.edit('ارسل الان الايدي او اليوزر', buttons=back)
    elif data == 'react':
        session[id] = {"step": data, 'chat': None}
        return await e.reply('ارسل الان رابط رسالة', buttons=back)
@ABH.on(events.CallbackQuery(pattern=b'^(delete|channle|react_count|setreact|view_count)'))
async def _(e):
    data = e.data.decode('utf-8')
    arg, chat = data.split(':')
    id = str(e.sender_id)
    if not id in info:return await e.edit('عذرا بس انت ماعندك قنوات حاليا', buttons=back)
    if not chat in info[id]:return await e.edit('عذرا بس القناة هاي مو مضافة', buttons=back)
    if arg == 'delete':
        del info[id][chat]
        save_data()
        return await e.edit('تم حذف القناة ب نجاح', buttons=back)
    elif arg == 'channle':
        button = [
            [Button.inline('تحديد التفاعلات', data=f'setreact:{chat}', style=green, icon=5226513232549664618)],
            [Button.inline('عدد المشاهدات', data=f'view_count:{chat}', style=green, icon=5226513232549664618),
            Button.inline('عدد التفاعلات', data=f'react_count:{chat}', style=green, icon=5226513232549664618)]
        ]
        button.append(back)
        await e.edit('اختر ما تريد تحديده', buttons=button)
    elif arg in ('view_count', 'react_count'):
        session[e.sender_id] = {"step": arg, 'chat': chat}
        caption = 'ارسل الان العدد'
        caption+=f'\nالعدد الحالي ( {info[id][chat].get(arg)} )' if info[id][chat].get(arg) else '...'
        return await e.edit(caption, buttons=back)
    elif arg == 'setreact':
        session[e.sender_id] = {"step": arg, 'chat': chat}
        caption = 'ارسل الان الايموجيات المراد وضعها\n'
        if 'react' in info[id][chat]:
            caption+=f'الرياكت الحالي ( {', '.join(info[id][chat]['react'])} )'
        return await e.edit(caption, buttons=back)
emoji = [
    "🤣", "❤️", "👍", "👎", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😡", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊",
    "🤡", "🥱", "☺️", "😍", "🐳", "❤️‍🔥", "🌚", "🌭", "😙", "💯", "⚡️", "🍌", "🏆", "😡", "😘", "🙊", "😎", "👾", "🤷‍♂️",
    "🤷‍♀️", "🤷", "☃️", "🗿", "🆒", "💘", "🙈", "😇", "😨", "🤝", "✍️", "🤗", "🫡", "🎅", "🎄", "😴", "😭", "🤓", "👻",
    "👨‍💻", "👀", "🎃", "🙈", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈"]
def extract_channel_and_msg(text):
    pattern = r'https://t\.me/(?!c/)([a-zA-Z0-9_]+)(?:/(\d+))?'
    match = re.search(pattern, text)
    if match:
        channel_username = match.group(1)
        message_id = match.group(2) if match.group(2) else None
        return channel_username, message_id
    return None
async def react(event, chat=None, id=None, emojis=None):
    if not event.is_channel or not event.message or not event.message.post:
        return [0, 0]
    chat_id = chat if chat else event.chat_id
    msg_id = id if id else event.message.id
    status = [0, 0]    
    for ABH in ABHS:
        if not ABH:
            continue
        try:
            peer = await ABH.get_entity(chat_id)
            try:
                await ABH(GetMessagesViewsRequest(
                    peer=peer,
                    id=[msg_id],
                    increment=True
                ))
            except Exception:
                pass            
            emoji = random.choice(emojis) if emojis else random.choice(['❤️', '🕊', '🌚'])
            await ABH(SendReactionRequest(
                peer=peer,
                msg_id=msg_id,
                reaction=[ReactionEmoji(emoticon=emoji)],
                big=False
            ))
            status[0] += 1
        except Exception:
            status[1] += 1
        await asyncio.sleep(1)
    return status
async def _filter(e):
    text = e.text
    id = e.sender_id
    sid = str(e.sender_id)
    if text == '/start':return
    step = session[id]['step']
    chat_id = session.get(id).get('chat')
    if step == 'add_channle':
        target = None
        if text.startswith(('https://t.me/', '@')):
            target = text
        elif text.isdigit():
            target = int(text)
        else:
            return await e.reply('ادخل يوزر او ايدي او رابط صالح!', buttons=back)
        if not target:return await e.reply(f'عذرا بس ماكدرت اوصل معلومات ( {target} )')
        chat = await ABH.get_entity(target)        
        if not isinstance(chat, Channel) or not chat.broadcast:
            return await e.reply('صديقي اتفقنه تضيف قناة مو شيء اخر!', buttons=back)
        chan_key = str(chat.id)
        if not isinstance(info.get(sid), dict):
            info[sid] = {}
        if step == 'del_channle':
            if session.get(id):
                del session[id]
            return await e.reply('تم تجاهل الاضافة', buttons=back)
        if chan_key in info[sid]:
            return await e.reply('عذرا بس القناة هاي ضايفها انت من قبل', buttons=back)
        try:
            bot_user = await ABH.get_me()
            participant = await ABH(GetParticipantRequest(
                channel=chat,
                participant=bot_user.id
            ))
            is_admin = isinstance(participant.participant, ChannelParticipantAdmin)
            if not is_admin:
                return await e.reply("البوت مو مشرف! ارفعه مشرف بالاول وعيد المحاولة", buttons=back)
        except UserNotParticipantError:
            return await e.reply("❌ البوت غير موجود في القناة! يرجى إضافته ورفعه مشرفاً أولاً.", buttons=back)
        owner = await get_channel_owner(chat)
        participants = await ABH.get_participants(chat, limit=0)
        current_time = datetime.now(ZoneInfo("Asia/Baghdad")).strftime("%Y-%m-%d %H:%M:%S")
        info[sid][chat.id] = {
            'name': chat.title,
            'owner': owner.id,
            'added_by': e.sender_id,
            'count': participants.total,
            'text': text,
            'time': current_time,
            }
        save_data()
        caption = f'**تم اضافة القناة بنجاح🌚**\nاسم القناة: ( {chat.title} )\nايدي القناة: ( `{chat.id}` )\n مالك القناة: ( {await ment(owner)} )\n ايديه: ( `{owner.id}` )\n عدد مشتركين القناة: ( `{participants.total}` )'
        url=f'https://t.me/{chat.username}' if chat.username else f'https://t.me/c/{str(chat.id).replace("-100", "")}/1'
        caption+=f'\nالرابط ( [{chat.title}]({url}) )'
        b = [Button.url(chat.title, url=url, style=blue, icon=5465374681915727405)]
        button = [b, back]
        del session[id]
        photo_file = None
        if chat.photo:
            photo_bytes = await ABH.download_profile_photo(chat, file=bytes)
            if photo_bytes:
                photo_file = BytesIO(photo_bytes)
                photo_file.name = "photo.jpg"
        if photo_file:
            return await e.reply(caption, file=photo_file, buttons=button)
        return await e.reply(caption, buttons=button)
    elif step == 'setreact':
        if not text:return await e.reply('يرجى ارسال نص صالح', buttons=back)
        valid_emojis = []
        uninvailde = set()
        for t in text.split():
            for char in t:
                if char in emoji:
                    valid_emojis.append(char)
                else:
                    uninvailde.add(t)
        caption = f'**النص المدخل** ( `{text}` )\n'
        if valid_emojis:
            caption+= f'تم اضافة ( {', '.join(valid_emojis)} )\n'
        if uninvailde:
            caption+=f'تم تخطي ( {', '.join(uninvailde)} )\n'
        if not valid_emojis:return await e.reply('لم يتم ارسال ايموجي صالح', buttons=back)
        info[sid][chat_id]['react'] = valid_emojis
        save_data()
        del session[id]
        return await e.reply(caption, buttons=back)
    elif step in ('react_count', 'view_count'):
        if not text.isdigit():
            return await e.reply('ارسل رقم صالح!', buttons=back)
        num = int(text)
        if num < 1 or num > 15:return await e.reply('عذرا صديقي بس العدد لازم يكون بين (1-15 )', buttons=back)
        info[sid][chat_id][step] = num
        save_data()
        if id in session:
            del session[id]
        label = "التفاعلات" if step == 'react_count' else "المشاهدات"
        return await e.reply(f'تم تحديد عدد {label} المطلوبة ( `{text}` )', buttons=back)
    elif step == 'react':
        if not text.startswith('https://t.me/'):return await e.reply('ارسل رابط صالح!', buttons=back)
        chat, id = extract_channel_and_msg(text)
        if not chat or not id:return await e.reply('الرابط غير كامل!', buttons=back)
        status_msg = await e.reply(f'تم عمل الرياكت ب نجاح\n نجح')
        status = await react(e, chat=chat, id=id)
        return await status_msg.edit(
            f"✅ **اكتملت العملية بنجاح**\n\n"
            f"👥 الحسابات المشاركة: `{status[0]}`\n"
            f"🔥 التفاعلات الناجحة: `{status[1]}`\n"
            f"📍 الهدف: `{chat}`")
ABH.run_until_disconnected()
