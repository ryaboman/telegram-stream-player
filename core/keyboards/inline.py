from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from core.settings import settings

manage_player = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Воспроизведение',
            callback_data='play_track'
        )
    ],
    [
        InlineKeyboardButton(
            text='Следующая песня',
            callback_data='next_track'
        )
    ],
    [
        InlineKeyboardButton(
            text='Предыдущая песня',
            callback_data='previous_track'
        )
    ],
    [
        InlineKeyboardButton(
            text='Паузка',
            callback_data='pause_track'
        )
    ],
    [
        InlineKeyboardButton(
            text='Стоп',
            callback_data='stop_track'
        )
    ]
])
