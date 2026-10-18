from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import MessageEntityCustomEmoji
from telethon.tl.types import ChannelParticipantAdmin
from telethon.errors import UserNotParticipantError
from telethon.tl.types import Channel
from datetime import datetime
from helpers import *
from client import *
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
    await is_user(e)
    await _filter(e)
@ABH.on(events.CallbackQuery)
async def _(e):
    await is_user(e)
back = [Button.inline('الرجوع', data='back', style=blue, icon=5352759161945867747)]
def buttons(e):
    if str(e.sender_id) not in info:
        b = [Button.inline('اضف قناة', data='add_channle', style=green, icon=5222040745665379997)]
    else:
        b = [
            Button.inline('اضف قناة', data='add_channle', style=blue, icon=5222040745665379997),
            Button.inline('حذف قناة', data='del_channle', style=red, icon=5408832111773757273),
            Button.inline('القنوات المضافة', data='channles', style=blue, icon=6323116093724428158),
            Button.inline('الاعدادات', data='settings', style=green, icon=5258096772776991776),
            ]
    return chunk_list(b)
session = {}
@ABH.on(events.NewMessage(pattern=r'^/start$'))
async def start(e):
    await send(e, f'اهلا عزيزي ( {await ment(e)} ) اني بوت مال رياكشن وظيفتي اضيفلك رياكشنات ومشاهدات لقناتك', buttons=buttons(e))
    session[e.sender_id] = {}
@ABH.on(events.CallbackQuery(pattern=b'^(add_channle|del_channle|channles|settings|back)$'))
async def start_callback(e):
    id = e.sender_id
    if not session.get(id):
        session[e.sender_id] = {}
    data = e.data.decode('utf-8')
    if data == 'back':
        return await e.edit('تفضل الازرار كدامك', buttons=buttons(e))
    elif data.endswith('_channle'):
        session[id]['step'] = data
        return await e.edit('ارسل الان اليوزر او الايدي او رابط القناة', buttons=back)
    elif data == 'channles':
        if not info.get(str(id)):return await e.edit('ماعندك قنوات مضافة', buttons=back)
        ids = [int(id) for id in info[str(id)]]
        chats = await ABH.get_entity(ids)
        b = []
        text = 'قنواتك المضافة🗒️:'
        for num, chat in enumerate(chats, start=1):
            b.append(Button.url(chat.title, url=f'https://t.me/{chat.username}' if chat.username else f'https://t.me/c/{str(chat.id).replace("-100", "")}/1'))
            text+=f"""
        القناة {ordinal_arabic_female(num) or num2words(num, lang='ar')} - 
        {f'( [{chat.title}](https://t.me/{chat.username}) )' if chat and chat.username else chat.title} 
        - (`{chat.id}`)"""
        button = chunk_list(b)
        return await e.edit(text, buttons=button)
    elif data == "settings":
        if not info.get(str(id)):return await e.edit('ماعندك قنوات مضافة', buttons=back)
        ids = [id for id in info[str(id)]]
        chats = await ABH.get_entity(ids)
        b = [Buttons.inline(chat.title, data=f'channle:{chat.id}') for chat in chats]
        return await e.edit('اختر قناة لتعديل اعداداتها', buttons=b)
async def _filter(e):
    text = e.text
    id = e.sender_id
    sid = str(e.sender_id)
    if id not in session:return 
    step = session.get(id).get('step')
    if text == '/start':return
    if step in ('add_channle', 'del_channle'):
        target = None
        if text.startswith(('https://t.me/', '@')):
            target = text
        elif text.isdigit():
            target = int(text)
        else:
            return await e.reply('ادخل يوزر او ايدي او رابط صالح!', button=back)
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
            return await e.reply('تم تجاهل الاضافة')
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
        if step == 'add_channle':
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
            photo_file = None
            if chat.photo:
                photo_bytes = await ABH.download_profile_photo(chat, file=bytes)
                if photo_bytes:
                    photo_file = BytesIO(photo_bytes)
                    photo_file.name = "photo.jpg"
            if photo_file:
                return await e.reply('تم اضافة القناة ب نجاح', file=photo_file)
            return await e.reply('تم اضافة القناة ب نجاح')
