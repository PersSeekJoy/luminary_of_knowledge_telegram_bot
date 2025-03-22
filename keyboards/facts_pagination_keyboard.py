from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_facts_pagination_keyboard(fact_number) -> InlineKeyboardMarkup:
    button1 = InlineKeyboardButton(
        text='<<<',
        callback_data='<<<'
        )
    button2 = InlineKeyboardButton(
        text=fact_number,
        callback_data='search_menu_button'
        )
    button3 = InlineKeyboardButton(
        text='>>>',
        callback_data='>>>'
        )
    button4 = InlineKeyboardButton(
        text='Категории',
        callback_data='facts_menu_button'
        )

    menu_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [button1, button2, button3],
            [button4]
        ]
    )

    return menu_keyboard
