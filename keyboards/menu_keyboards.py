from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon import LEXICON

button1 = InlineKeyboardButton(
    text=LEXICON['facts_button'],
    callback_data='facts_menu_button'
    )
button2 = InlineKeyboardButton(
    text=LEXICON['search_button'],
    callback_data='search_menu_button'
    )

menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [button1],
        [button2]
    ]
)
