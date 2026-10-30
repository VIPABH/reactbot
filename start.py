from telethon.tl.functions.messages import GetMessagesViewsRequest, SendReactionRequest
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import MessageEntityCustomEmoji
from telethon.tl.types import ChannelParticipantAdmin
from telethon.errors import UserNotParticipantError
from telethon.tl.types import ReactionEmoji
from telethon.utils import get_peer_id
from telethon.tl.types import Channel
import asyncio, random, re, os, time
from datetime import datetime
from zoneinfo import ZoneInfo
from io import BytesIO
from helpers import *
from client import *
info = create('data.json')
chat_info = create('chat_info.json')
def save_data(all=None):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=4)
    if all:
        with open('chat_info.json', 'w', encoding='utf-8') as f:
            json.dump(chat_info, f, ensure_ascii=False, indent=4)
send_msg = {}
@ABH.on(events.NewMessage)
async def _(e):
    await is_chat_in(e)
    await is_user(e)
    await _filter(e)
@ABH.on(events.CallbackQuery)
async def _(e):
    await is_user(e)
    if not _me:
        me = await ABH.get_me()
        _me.append(me)
    else:
        me = _me[0]
    key = f"banned_users:{me.id}"
    user_id = e.sender_id
    if r.sismember(key, user_id):
        await e.reply('عذرا صديقي انت محظور من البوت \n تفضل راسل المطور لرفع الحظر @k_4x1')
        raise events.StopPropagation
async def banned_user(e):
    step = ban_and_unban.get(e.sender_id, None)
    if step in ('ban_user', 'un_ban_user'):
        text = e.text.strip()
        target = None
        if text.isdigit():
            target = int(text)
        elif text.startswith(('@', 'https://t.me/')):
            target = text            
        if not target:
            return await e.reply('⚠️ عذراً، يرجى إرسال أيدي المستخدم أو يوزره بشكل صحيح.', buttons=back_to_button)
        try:
            user = await ABH.get_entity(target)
        except Exception:
            return await e.reply('❌ عذراً، لم أتمكن من العثور على حساب هذا المستخدم.')
        if not _me:
            me = await ABH.get_me()
            _me.append(me)
        else:
            me = _me[0]
        key = f"banned_users:{me.id}"
        user_id = user.id
        ban_and_unban.pop(e.sender_id, None)
        if step == "ban_user":
            r.sadd(key, user_id)
            return await e.reply(f'✅ تم حظر ( {await ment(user)} ) بنجاح.')
        else:
            r.srem(key, user_id)
            return await e.reply(f'✅ تم إلغاء حظر ( {await ment(user)} ) بنجاح.')
async def is_chat_in(e):
    chat_id = str(e.chat_id)
    if chat_id in chat_info:
        id = chat_info[chat_id]
        isuser = await is_user(e, id=id, callable=True)
        if not isuser:
            react_list = info[str(id)][chat_id].get('react', [])
            return await react(e, chat=chat_id, emojis=react_list)
        current_time = time.time()
        if id not in send_msg or (current_time - send_msg[id]) >= 300:
            send_msg[id] = current_time
            text = f'عذرا صديقي الخدمه متوقفة \n حته تستفاد من خدمه التفاعلات لازم تكون مشترك على طول بالقنوات 🌚'
            photo_file = None
            chat = await ABH.get_entity(e.chat_id)
            if chat.photo:
                photo_bytes = await ABH.download_profile_photo(chat, file=bytes)
                if photo_bytes:
                    photo_file = BytesIO(photo_bytes)
                    photo_file.name = "photo.jpg"
            if photo_file:
                await ABH.send_file(id, file=photo_file, caption=text, buttons=not_isuser)
            else:
                await ABH.send_message(id, message=text, buttons=not_isuser)
            raise events.StopPropagation
@ABH.on(events.CallbackQuery)
async def _(e):
    await is_user(e)
back = [Button.inline('الرجوع', data='back', style=blue, icon=5352759161945867747)]
def buttons(e):
    id = str(e.sender_id)
    iid = e.sender_id
    formatted_date = datetime.now().strftime("%Y %m %d")
    if formatted_date not in limit:
        limit[formatted_date] = {}
    if iid not in limit[formatted_date]:
        limit[formatted_date][iid] = 3
    tries = limit[formatted_date][iid]
    if id not in info or not info[id].values():
        b = [
            Button.inline('اضف قناة', data='add_channle', style=green, icon=5222040745665379997)]
        if tries > 0:
            b.append(Button.inline(f'رياكت ( 3\\{tries} )', data='react', style=green, icon=5884106131822875141))
    else:
        b = [
            Button.inline('اضف قناة', data='add_channle', style=blue, icon=5222040745665379997),
            Button.inline('حذف قناة', data='del_channle', style=red, icon=5408832111773757273),
            Button.inline('القنوات المضافة', data='list_channles', style=blue, icon=6323116093724428158),
            Button.inline('الاعدادات', data='settings', style=green, icon=5258096772776991776),
            ]
        if tries > 0:
            b.append(Button.inline(f'رياكت ( 3\\{tries} )', data='react', style=green, icon=5884106131822875141))
    return chunk_list(b)
session = {}
wfffp_button =[
    Button.inline('عدد المستخدمين', data='users_count', style=blue, icon=5305355874187880345),
    Button.inline('المستخدمين', data='users', style=blue, icon=5305355874187880345),
    Button.inline('المحظورين', data='banned_users', style=blue, icon=5305355874187880345),
    Button.inline('حظر شخص', data='ban_user', style=red, icon=5305355874187880345),
    Button.inline('الغاء حظر شخص', data='un_ban_user', style=green, icon=5305355874187880345),
]
chunked_button = chunk_list(wfffp_button)
chunked_button.append(back)
back_to_button = [Button.inline('ارجع للازرار', data='back_button', style=red, icon=5305355874187880345)]
@ABH.on(events.NewMessage(pattern=r'^/start'))
async def start(e):
    if e.sender_id == wfffp:return await send(e, 'اهلا عزيزي ابن هاشم , شنو تحب تسوي', buttons=chunked_button)
    await send(e, f'اهلا عزيزي ( {await ment(e)} ) اني بوت مال رياكشن وظيفتي اضيفلك رياكشنات ومشاهدات لقناتك', buttons=buttons(e))
    session[e.sender_id] = {}
ban_and_unban = {}
_me = []
@ABH.on(events.CallbackQuery(pattern=b'^(users_count|banned_users|ban_user|un_ban_user|back_button|users)$'))
async def wfffp_callback(e):
    if e.sender_id != wfffp:return
    data = e.data.decode('utf-8')
    if not _me:
        me = await ABH.get_me()
        _me.append(me)
    else:
        me = _me[0]
    key = f"users:{me.id}"
    users_count = r.scard(key)
    if data == 'users_count':return await e.edit(f'عدد مستخدمين البوت هو ( {users_count} )', buttons=back_to_button)
    elif data == "banned_users":
        if not r.smembers(f"banned_users:{me.id}"):return await e.edit('ماكو مستخدمين محظورين', buttons=back_to_button)
        mention = [f"{num}- ( {await ment(id)} ) - ( `{id}` )" for num, id in enumerate(r.smembers(f"banned_users:{me.id}"), start=1)]
        await e.edit(f"المستخدمين المحظورين:\n {'\n'.join(mention)}", buttons=back_to_button)
    elif data == "users":
        mention = [f"{num}- ( {await ment(id)} ) - ( `{id}` )" for num, id in enumerate(r.smembers(f"users:{me.id}"), start=1)]
        await e.edit(f"المستخدمين:\n {'\n'.join(mention)}", buttons=back_to_button)
    elif data == 'back_button':await e.edit('تفضل ابنل الهاش', buttons=chunked_button)
    else:
        ban_and_unban[e.sender_id] = data
        await e.edit('ارسل الان ايدي او يوزر المستخدم', buttons=back_to_button)
@ABH.on(events.CallbackQuery(pattern=b'^(add_channle|del_channle|list_channles|settings|back|react)$'))
async def start_callback(e):
    id = e.sender_id
    if not session.get(id):
        session[e.sender_id] = {}
    data = e.data.decode('utf-8')
    if data == 'back':
        if session.get(id):
            del session[id]
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
            text += f"\n{num} - ( [{chat.title}]({url}) ) - ( `{chat.id}` )"
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
        formatted_date = datetime.now().strftime("%Y %m %d")
        if formatted_date not in limit:
            limit[formatted_date] = {}
        if id not in limit[formatted_date]:
            limit[formatted_date][id] = 3
        tries = limit[formatted_date][id]
        if tries <= 0:
            return await e.edit('عذرا محاولاتك انتهت حاول مجددا غدا', buttons=back)
        session[id] = {"step": data, 'chat': None}
        return await e.edit('ارسل الان رابط رسالة \n يسمح لك ب 3 رياكتات يوميا وبعدها يتطلب من الاننتظار لليوم التالي', buttons=back)
@ABH.on(events.CallbackQuery(pattern=b'^(delete|channle|react_count|setreact|view_count)'))
async def _(e):
    data = e.data.decode('utf-8')
    arg, chat = data.split(':')
    if not chat.startswith('-100'):
        chat = '-100'+chat
    id = str(e.sender_id)
    if not id in info:return await e.edit('عذرا بس انت ماعندك قنوات حاليا', buttons=back)
    if not chat in info[id]:return await e.edit('عذرا بس القناة هاي مو مضافة', buttons=back)
    if arg == 'delete':
        del info[id][chat]
        del chat_info[chat]
        save_data(all=True)
        return await e.edit('تم حذف القناة ب نجاح', buttons=back)
    elif arg == 'channle':
        button = [
            [Button.inline('تحديد التفاعلات', data=f'setreact:{chat}', style=green, icon=5226513232549664618)],
            [Button.inline('عدد المشاهدات', data=f'view_count:{chat}', style=green, icon=5226513232549664618),
            Button.inline('عدد التفاعلات', data=f'react_count:{chat}', style=green, icon=5226513232549664618)]
        ]
        button.append([Button.inline('حذف القناة', data=f'delete:{chat}', style=red, icon=5258130763148172425)])
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
def extract_channel_and_msg(text):
    pattern = r'https://t\.me/(?!c/)([a-zA-Z0-9_]+)(?:/(\d+))?'
    match = re.search(pattern, text)
    if match:
        channel_username = match.group(1)
        message_id = match.group(2) if match.group(2) else None
        return channel_username, message_id
    return None
emoji = [
    "🤣", "❤️", "👍", "👎", "🔥", "🥰", "👏", "😁", "🤯", "😱", "🤬", "😡", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊",
    "🤡", "🥱", "😍", "🐳", "❤️‍🔥", "🌚", "🌭", "💯", "⚡️", "🍌", "🏆", "😡", "😘", "🙊", "😎", "👾", "🤷‍♂️",
    "🤷‍♀️", "🤷", "☃️", "🗿", "🆒", "💘", "🙈", "😇", "😨", "🤝", "✍️", "🤗", "🫡", "🎅", "🎄", "😴", "😭", "🤓", "👻",
    "👨‍💻", "👀", "🎃", "🙈", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈"]
async def react(event, chat=None, id=None, emojis=None):
    chat_id = chat if chat else str(event.chat_id)
    msg_id = id if id else event.message.id
    status = [0, 0, set()]
    views = 0
    reacts = 0
    id = str(chat_info[chat_id])
    rdb = info[id][chat_id].get('react_count', Max)
    vdb = info[id][chat_id].get('view_count', Max)
    for ABH in ABHS:
        try:
            peer = await ABH.get_input_entity(int(chat_id))
        except Exception:
            peer = await ABH.get_entity(int(chat_id))
        if not views >= vdb:
            await ABH(GetMessagesViewsRequest(
                peer=peer,
                id=[int(msg_id)],
                increment=True 
            ))
            views += 1
        if not reacts >= rdb:
            emoji = random.choice(list(emojis)) if emojis else random.choice(['❤️', '🕊', '🌚'])
            try:
                await ABH(SendReactionRequest(
                    peer=peer,
                    msg_id=int(msg_id),
                    reaction=[ReactionEmoji(emoticon=emoji)],
                    big=False
                ))
                reacts += 1
                status[0] += 1
                await asyncio.sleep(0.3)
            except Exception as e:
                status[1] += 1
                if 'Invalid reaction provided' in str(e):
                    status[2].add(emoji)
    return status
async def random_react(event, chat=None, id=None, emojis=None):
    chat_id = chat if chat else event.chat_id
    msg_id = id if id else event.message.id
    status = [0, 0, set()]
    formatted_date = datetime.now().strftime("%Y %m %d")
    if formatted_date not in limit:
        limit[formatted_date] = {}
    if event.sender_id not in limit[formatted_date]:
        limit[formatted_date][event.sender_id] = 3
    for ABH in ABHS:
        try:
            peer = await ABH.get_input_entity(int(chat_id))
        except Exception:
            peer = await ABH.get_entity(int(chat_id))
        await ABH(GetMessagesViewsRequest(
            peer=peer,
            id=[int(msg_id)],
            increment=True 
        ))
        emoji = random.choice(emojis) if emojis else random.choice(['❤️', '🕊', '🌚'])
        try:
            await ABH(SendReactionRequest(
                peer=peer,
                msg_id=int(msg_id),
                reaction=[ReactionEmoji(emoticon=emoji)],
                big=False
            ))
            status[0] += 1
            await asyncio.sleep(0.3)
        except Exception as e:
            status[1] += 1
            if 'Invalid reaction provided' in str(e):
                status[2].add(emoji)
    if status[0]>status[1]:
        limit[formatted_date][event.sender_id] -= 1
    return status
limit = {}
async def _filter(e):
    if not e.is_private:return
    text = e.text
    id = e.sender_id
    sid = str(e.sender_id)
    formatted_date = datetime.now().strftime("%Y %m %d")
    if text == '/start':return
    if id not in session:return
    step = session[id].get('step')
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
        if not chan_key.startswith('-100'):
            chan_key = '-100'+chan_key
        if not isinstance(info.get(sid), dict):
            info[sid] = {}
        if step == 'del_channle':
            if session.get(id):
                del session[id]
            return await e.reply('تم تجاهل الاضافة', buttons=back)
        if chan_key in info[sid]:
            return await e.reply('عذرا بس القناة هاي ضايفها انت من قبل', buttons=back)
        if chan_key in chat_info and int(chat_info[chan_key]) != e.sender_id:return await e.reply(f'عذرا بس هاي القناة مضافة من ( {await ment(int(chat_info[chan_key]))} )')
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
        info[sid][chan_key] = {
            'name': chat.title,
            'owner': owner.id,
            'added_by': e.sender_id,
            'count': participants.total,
            'text': text,
            'time': current_time,
            'react_count': Max,
            'view_count': Max,
            }
        chat_info[chan_key] = id
        save_data(all=True)
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
        if num < 1 or num > Max:return await e.reply(f'عذرا صديقي بس العدد لازم يكون بين (1-{Max} )', buttons=back)
        info[sid][chat_id][step] = num
        save_data()
        if id in session:
            del session[id]
        label = "التفاعلات" if step == 'react_count' else "المشاهدات"
        return await e.reply(f'تم تحديد عدد {label} المطلوبة ( `{text}` )', buttons=back)
    elif step == 'react':
        if not text.startswith('https://t.me/'):return await e.reply('ارسل رابط صالح!', buttons=back)
        chat, mid = extract_channel_and_msg(text)
        if not chat or not mid:return await e.reply('الرابط غير كامل!', buttons=back)
        if 'temp' not in session[id]:
            session[id]['temp'] = {}
        session[id]['step'] = 'setemoji'
        session[id]['temp']['chat'] = chat
        session[id]['temp']['id'] = mid
        chat_entity = await ABH.get_entity(chat)
        if not chat:return await e.reply('عذرا بس القناة غير موجودة')
        await try_forward(e, chat=int(chat) if chat.isdigit() else chat, id=mid, to=e.sender_id)
        return await e.reply('ارسل الان التفاعلات المطلوبة')
    elif step == 'setemoji':
        valid_emojis = []
        uninvailde = []
        for t in text.split():
            for char in t:
                if char in emoji:
                    valid_emojis.append(char)
        status_msg = await e.reply('يجري عمل الرياكت...')
        chat = session[id]['temp']['chat']
        mid = session[id]['temp']['id']
        chat_entity = await ABH.get_entity(chat)
        chat_id = get_peer_id(chat_entity)
        status = await random_react(e, chat=chat_id, id=mid, emojis=valid_emojis)
        caption = f"""
✅ **اكتملت العملية بنجاح**\n
📍 اليوزر: ( `{chat}` )
👥 الحسابات المشاركة: ( `{len(ABHS)}` )
🔥 التفاعلات الناجحة: ( `{status[0]}` )
"""
        if status[1]>0:
            caption+= f'\n❌ التفاعلات الفاشلة: ( `{status[1]}` )'
        if status[2]:
            caption+= f'\n❌ ايموجيات مقفولة في القناة: ( {'و '.join(status[2])} )'
        if status[0]>0:
            limit[formatted_date][id] -= 1
        if 'temp' in session.get(id, {}):
            del session[id]['temp']
        del session[id]
        return await status_msg.edit(caption)
ABH.run_until_disconnected()
