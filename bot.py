import random
import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.events import StopPropagation
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []
aykhan_tag = []
#tektag
@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global aykhan_tag
  aykhan_tag.remove(event.chat_id)

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("Salam **{usr.first_name}**.\n\nMən sizin əvəzinizdən qruplarnızda istifadəçiləri tağ edə bilərəm.\n\nHaqqımda daha ətraflı məlumat əldə etmək üçün /help əmrinə toxunun.",
                    buttons=(
                      [Button.url('🌟 Məni Qrupa Sal', 'https://t.me/OldTaggerBot?startgroup=a'),
                      Button.url('👨‍💻 Sahibim', 'https://t.me/muellime')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Old Tagger Bot'un Kömək Menyusu**\n\nƏmr: /all \n  Bu əmri, başqalarını bəhs etmək istədiyiniz mətinlə birlikdə istifadə edə bilərsiniz. \n`Məsələn: /all Sabahınız xeyir!`  \nBu əmri yanıt olaraq istifadə edə bilərsiniz. hər hansə bir mesaj Bot, yanıtlanan ilətiyə istifadəçiləri etiketləyəcək.\n /tagadmin \nYalnız adminləri tag edəcəkdir. \n /tektag \nTək-tək tag edəcəkdir.\n /etag /nEmojilernən tag edəcəkdir."
  await event.reply(helptext,
                    buttons=(
                      [Button.url('🌟 Məni Qrupa əlavə et', 'https://t.me/OldTaggerBot?startgroup=a'),
                      Button.url('🧑‍💻 Sahibim', 'https://t.me/muellime')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Bu əmr qruplarda və kanallarda işlədilə bilər.!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Yalnız adminlər bu əmrdən isdifadə  edə bilər!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Köhnə mesajlar üçün userləri tağ edə bilmərəm! (bu mesaj məni qrupa əlavə etməmişdən qabaq yazılıb)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Mənə bir arqument ver!__")
  else:
    return await event.respond("__Bir mesajı yanıtlayın və ya başqalarını tag etmək üçün mənə bir mətin verin!__")
    
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Tağ uğurlu şəkildə dayandırıldı ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Tağ uğurlu şəkildə dayandırıldı ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


@client.on(events.NewMessage(pattern="^/tektag ?(.*)"))
async def tektag(event):
  global aykhan_tag
  if event.is_private:
    return await event.respond(f"Bura qrup deyil")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"Yalnız Adminlər Tağ Edə Bilər")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Köhnə mesajları görə bilmirəm! (bu mesaj məni qrupa əlavə etməmişdən qabaq yazılıb)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Tağ mesajı yazmadın!__")
  else:
    return await event.respond("__Tağ etmək üçün bir mesajı yanıtlayın və ya bir mətn yazın!__")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "❄️ Tək-Tək Tağ Başladı\n⏱️ İnterval - 2 saniyə",
                    buttons=(
                      [
                      Button.inline(f"dayandır", data="cancel")
                      ]
                    )
                  ) 
    aykhan_tag.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in aykhan_tag:
        await event.respond("⛔ Tək Tək Tağ Prosesi Dayandırıldı",
                    buttons=(
                      [
                      Button.inline(f"yenidən", data="yenidən")
                      ]
                    )
                  )
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, f"{usrtxt} {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

#########################


@client.on(events.NewMessage(pattern=lambda x: "/tagadmin" in x.lower(), incoming=True))
async def tag_admin(event):
    chat = await event.get_input_chat()
    text = "Tagging admins"
    async for x in event.client.iter_participants(chat, 100, filter=ChannelParticipantsAdmins):
        text += f" \n [{x.first_name}](tg://user?id={x.id})"
    if event.reply_to_msg_id:
        await event.client.send_message(event.chat_id, text, reply_to=event.reply_to_msg_id)
    else:
        await event.reply(text)
    raise StopPropagation

def main():
  bot.start(bot_token=TOKEN)
  bot.run_until_disconnected()



anlik_calisan = []

tekli_calisan = []


@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global emoji_calisan
  anlik_calisan.remove(event.chat_id)


emoji = " ❤️ 🧡 💛 💚 💙 💜 🖤 🤍 🤎 🙂 🙃 😉 😌 😍 🥰 😘 😗 😙 😚 😋 😛 😝 😜 🤪 🤨 🧐 🤓 😎 🤩 🥳 😏 😒 " \
        "😞 😔 😟 😕 🙁 😣 😖 😫 😩 🥺 😢 😭 😤 😠 😡  🤯 😳 🥵 🥶 😱 😨 😰 😥 😓 🤗 🤔 🤭 🤫 🤥 😶 😐 😑 😬 🙄 " \
        "😯 😦 😧 😮 😲 🥱 😴 🤤 😪 😵 🤐 🥴 🤢 🤮 🤧 😷 🤒 🤕 🤑 🤠 😈 👿 👹 👺 🤡  👻 💀 👽 👾 🤖 🎃 😺 😸 😹 " \
        "😻 😼 😽 🙀 😿 😾".split(" ")


@client.on(events.NewMessage(pattern="^/etag ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("**Bu əmr qruplar ve kanallar üçün etibarlıdır❗**")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("**Bu Əmri yalnız adminlər işlədə bilər〽️**")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("**bu mesaj məni qrupa əlavə etməmişdən qabaq yazılıb**")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("Tağ eləmək üçün səbəb yoxdur❗️")
  else:
    return await event.respond("**Tağ Prossesinə Başlamaq Üçün Səbəb Yazın...!**")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{random.choice(emoji)}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("** Tağ prosesi uğurla  dayandırıldı❌**")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{random.choice(emoji)}](tg://user?id={usr.id}) "
      if event.chat_id not in emoji_calisan:
        await event.respond("Tağ prosesi uğurla  dayandırıldı❌\n\n**Burada sizin reklamınız ola bilər @muellime**❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/tag ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("Bu əmr qruplar ve kanallar üçün etibarlıdır❗️**")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("**Bu əmri yalnız adminlər işlədə bilər〽️**")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("Əvvəlki Mesajlara Cavab Verməyin")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("Başlamaq üçün səbəb yaz❗️")
  else:
    return await event.respond("Tağ Prossesinə Başlamaq Üçün Səbəb Yazın")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"👥 - [{usr.first_name}](tg://user?id={usr.id}) \n"
      if event.chat_id not in anlik_calisan:
        await event.respond("Tağ prosesi uğurla  dayandırıldı❌\n\n**Burada sizin reklamınız ola bilər @muellime**❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
 

print(">> Bot işləyir narahat olma 🚀 məlumat almaq üçün @muellime yazın <<")
client.run_until_disconnected()
run_until_disconnected()
