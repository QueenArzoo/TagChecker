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
                     
               
               
@tagcheck.on_message(filters.incoming & filters.command(['start', 'start@{BOT_USERNAME}']))
def _start(client, message):
    update_channel = UPDATES_CHANNEL
    if update_channel:
        try:
            user = client.get_chat_member(update_channel, message.chat.id)
            if user.status == "kicked":
               client.send_message(
                   chat_id=message.chat.id,
                   text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/DarkXForce).",
                   parse_mode="markdown",
                   disable_web_page_preview=True
               )
               return
        except UserNotParticipant:
            client.send_message(
                chat_id=message.chat.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Join Updates Channel", url=f"https://t.me/DarkXForce")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            client.send_message(message.chat.id,
                text="**👋🏻 Hey [{}](tg://user?id={})**\n__Fuck You**".format(message.from_user.first_name, message.from_user.id),
	        reply_markup=InlineKeyboardMarkup(
                    [
                        [   
                           InlineKeyboardButton("Updates Channel", url="https://t.me/DarkXForce"),
                           InlineKeyboardButton("Support Group", url="https://t.me/DarkXForce")
                      ],
                     [
                           InlineKeyboardButton("🧑‍💻Devloper🧑‍💻", url="https://t.me/DarkXForce")
                     ]
                 ]
             ),
        parse_mode="markdown",
        reply_to_message_id=message.message_id
        )
            return
    client.send_message(message.chat.id,
        text="**👋🏻 Hey [{}](tg://user?id={})**\n__Fuck You  **".format(message.from_user.first_name, message.from_user.id),
	reply_markup=InlineKeyboardMarkup(
            [
		[
                    InlineKeyboardButton("Updates Channel", url="https://t.me/DarkXForce"),
                    InlineKeyboardButton("Support Group", url="https://t.me/DarkXForce")
                ],
                [
                    InlineKeyboardButton("🧑‍💻Devloper🧑‍💻", url="https://t.me/DarkXForce")	
                ]
            ]
        ),
        parse_mode="markdown",
        reply_to_message_id=message.message_id
        )
   
   
   
tagcheck.run()
