from helpers import *
from client import *
info = create('data.json')
@ABH.on(events.NewMessage)
async def _(e):
    await is_user(e)
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
@ABH.on(events.NewMessage(pattern=r'^/start$'))
async def start(e):
    await send(e, f'اهلا عزيزي ( {await ment(e)} ) اني بوت مال رياكشن وظيفتي اضيفلك رياكشنات ومشاهدات لقناتك', buttons=buttons(e))
    session[id] = {}
session = {}
@ABH.on(events.CallbackQuery(pattern=b'^(add_channle|del_channle|channles|settings|back)$'))
async def start_callback(e):
    id = e.sender_id
    data = e.data.decode('utf-8')
    if data == 'back':
        return await e.edit('تفضل الازرار كدامك', buttons=button(e))
    elif data.endswith('_channle'):
        session[id]['step'] = data
        return await e.edit('ارسل الان اليوزر او الايدي او رابط القناة', buttons=back)
    elif data == 'channles':
        if not info.get(str(id)):return await e.edit('ماعندك قنوات مضافة', buttons=back)
        ids = [id for id in info[str(id)]]
        chats = await ABH.get_entity(ids)
        b = []
        text = 'قنواتك المضافة🗒️:'
        for chat in chats:
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
