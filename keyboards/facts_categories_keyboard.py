from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon import LEXICON

category_button1 = InlineKeyboardButton(
    text=LEXICON['stars'],
    callback_data='stars_button'
    )
category_button2 = InlineKeyboardButton(
    text=LEXICON['planets'],
    callback_data='planets_button'
    )
category_button3 = InlineKeyboardButton(
    text=LEXICON['galaxies'],
    callback_data='galaxies_button'
    )
category_button4 = InlineKeyboardButton(
    text=LEXICON['menu_button'],
    callback_data='menu_button'
    )

categories_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [category_button1],
        [category_button2],
        [category_button3],
        [category_button4]
    ]
)
