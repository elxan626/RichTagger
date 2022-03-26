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
elxan_tag = []
#tektag
@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global elxan_tag
  elxan_tag.remove(event.chat_id)

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("Salam 👋\n\nMən sizin əvəzinizdən qruplarnızda istifadəçiləri tag edə bilərəm.\n\nHaqqımda daha ətraflı məlumat əldə etmək üçün /help əmrinə toxunun.",
                    buttons=(
                      [Button.url('🌟 Məni Qrupa Sal', 'https://t.me/RichTaggerBot?startgroup=a')],
                      [Button.url('🛠 Support', 'https://t.me/SOQrup'),
                      Button.url('📣 Rəsmi Kanal', 'https://t.me/ledyplaylist')],
                      [Button.url('👨‍💻 Sahibim', 'https://t.me/ruzgar_alican')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Rich Tagger Bot'un Kömək Menyusu**\n\nƏmrlər:\n/all <səbəb> - 5-li tag edəcəkdir. \n/tagadmin <səbəb> - Yalnız adminləri tag edəcəkdir. \n/tektag <səbəb> - Tək-tək tag edəcəkdir.\n/etag <səbəb> - Emojilər ilə tag edəcəkdir."
  await event.reply(helptext,
                    buttons=(
                      [Button.url('🌟 Məni Qrupa Sal', 'https://t.me/RichTaggerBot?startgroup=a')],
                      [Button.url('🛠 Support', 'https://t.me/SOQrup'),
                      Button.url('📣 Rəsmi Kanal', 'https://t.me/ledyplaylist')],
                      [Button.url('👨‍💻 Sahibim', 'https://t.me/ruzgar_alican')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__**Bu əmr yalnız qruplarda və kanallarda işlədilə bilər**❗__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__**Yalnız adminlər bu əmrdən isdifadə edə bilər**❗__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__**Köhnə mesajlar üçün userləri tag edə bilmərəm ❗ (bu mesaj məni qrupa əlavə etməmişdən qabaq yazılıb)**__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__**Mənə bir arqument ver**❗__")
  else:
    return await event.respond("__**Bir mesajı yanıtlayın və ya başqalarını tag etmək üçün mənə bir mətin verin**❗__")
    
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("**Tag uğurlu şəkildə dayandırıldı** ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n{msg}")
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
        await event.respond("**Tag uğurlu şəkildə dayandırıldı** ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


@client.on(events.NewMessage(pattern="^/tektag ?(.*)"))
async def tektag(event):
  global elxan_tag
  if event.is_private:
    return await event.respond(f"**Bura Qrup Deyil❗**")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"**Yalnız Adminlər Tag Edə Bilər**❗")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__**Köhnə mesajları görə bilmirəm❗ (bu mesaj məni qrupa əlavə etməmişdən qabaq yazılıb**)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__**Tag üçün mesajı yazmadın**❗__")
  else:
    return await event.respond("__**Tag etmək üçün bir mesajı yanıtlayın və ya bir mətn yazın**❗__")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "❄️ **Tək-Tək Tag Başladı**\n⏱️ İnterval - 2 saniyə",
                    buttons=(
                      [
                      Button.inline(f"dayandır", data="cancel")
                      ]
                    )
                  ) 
    elxan_tag.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in elxan_tag:
        await event.respond("**⛔ Tək Tək Tag Prosesi Dayandırıldı**",
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
    text = "Adminlər Tag Olunur"
    async for x in event.client.iter_participants(chat, 100, filter=ChannelParticipantsAdmins):
        text += f" \n 👤 [{x.first_name}](tg://user?id={x.id})"
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
    return await event.respond("**Bu əmr qruplar və kanallar üçün etibarlıdır**❗")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("**Bu Əmri yalnız adminlər işlədə bilər 〽️**")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("**bu mesaj məni qrupa əlavə etməmişdən qabaq yazılıb**")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("**Tag eləmək üçün səbəb yoxdur**❗")
  else:
    return await event.respond("**Tag Prossesinə Başlamaq Üçün Səbəb Yazın**❗")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{random.choice(emoji)}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("**Tag prosesi uğurla dayandırıldı** ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n{msg}")
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
        await event.respond("Tag prosesi uğurla  dayandırıldı** ❌")
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
    return await event.respond("**Bu əmr qruplar və kanallar üçün etibarlıdır**❗")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("**Bu əmri yalnız adminlər işlədə bilər 〽️**")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("Əvvəlki Mesajlara Cavab Verməyin")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("**Tag eləmək üçün səbəb yoxdur**❗")
  else:
    return await event.respond("**Tag Prossesinə Başlamaq Üçün Səbəb Yazın**❗")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"👤 [{usr.first_name}](tg://user?id={usr.id}) \n"
      if event.chat_id not in anlik_calisan:
        await event.respond("**Tag prosesi uğurla dayandırıldı** ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
 

print(">> Bot işləyir narahat olma 🚀 məlumat almaq üçün @tenha055 yazın <<")
client.run_until_disconnected()
run_until_disconnected()
