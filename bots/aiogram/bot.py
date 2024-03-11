# Importasi modul yang diperlukan
import asyncio
import os
import sys

from aiogram import types
from aiogram.types import ContentType

from bots.aiogram.client import dp, bot
from bots.aiogram.info import client_name
from bots.aiogram.message import MessageSession, FetchTarget
from core.builtins import PrivateAssets, Url
from core.parser.message import parser
from core.types import MsgInfo, Session
from core.utils.bot import load_prompt, init_async
from core.utils.info import Info

# Mengatur aset pribadi
PrivateAssets.set(os.path.abspath(os.path.dirname(__file__) + '/assets'))

# Menonaktifkan mm di Url
Url.disable_mm = True

# Mendefinisikan handler pesan
@dp.message()
async def msg_handler(message: types.Message):
    # Mendefinisikan target_id dan reply_id
    target_id = f'Telegram|{message.chat.type}|{message.chat.id}'
    reply_id = None

    # Memeriksa apakah pesan adalah balasan
    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    # Membuat MessageSession
    msg = MessageSession(
        MsgInfo(
            target_id=target_id,
            sender_id=f'Telegram|User|{message.from_user.id}',
            target_from=f'Telegram|{message.chat.type}',
            sender_from='Telegram|User',
            sender_name=message.from_user.username,
            client_name=client_name,
            message_id=message.message_id,
            reply_id=reply_id
        ),
        Session(
            message=message,
            target=message.chat.id,
            sender=message.from_user.id
        )
    )

    # Mem-parsing pesan
    await parser(msg)

# Mendefinisikan fungsi on_startup
async def on_startup(dispatcher):
    # Menginisialisasi dan memuat prompt
    await init_async()
    await load_prompt(FetchTarget)

# Memeriksa apakah 'subprocess' ada di sys.argv
if 'subprocess' in sys.argv:
    Info.subprocess = True

# Mendaftarkan startup
dp.startup.register(on_startup)

# Memulai polling
asyncio.run(dp.start_polling(bot))
