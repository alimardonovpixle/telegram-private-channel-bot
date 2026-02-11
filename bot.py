import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
SECRET_WORD = os.getenv("SECRET_WORD")

bot = Bot(token=TOKEN)
dp = Dispatcher()

used_users = set()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("🔐 Maxfiy so‘zni kiriting:")

@dp.message()
async def check_secret(message: types.Message):
    user_id = message.from_user.id

    if user_id in used_users:
        await message.answer("❌ Siz allaqachon link olgansiz.")
        return

    if message.text == SECRET_WORD:
        invite = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            member_limit=1,
            expire_date=message.date + 60
        )
        used_users.add(user_id)
        await message.answer(
            f"✅ To‘g‘ri!\n\n🔗 Kanalga kirish linki:\n{invite.invite_link}"
        )
    else:
        await message.answer("❌ Noto‘g‘ri so‘z.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
