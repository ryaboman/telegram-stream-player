from aiogram import Bot
from aiogram.types import Message
from core.keyboards.inline import manage_player


async def get_class_text(message: Message, bot: Bot):
    await message.answer(f'done')

async def get_start(message: Message, bot: Bot):

    await message.answer(f'Привет <b>{message.from_user.first_name}</b>. '
                         f'Я Бот для управления плеером трансляции.')

    await message.answer('Выберите действие', reply_markup=manage_player)




