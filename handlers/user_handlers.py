from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from random import choice
from lexicon import LEXICON
from services import google_search, read_states, write_states, separator, SITES, read_facts
from states import null_state
from keyboards import menu_keyboard, create_pagination_keyboard, categories_keyboard, create_facts_pagination_keyboard
from database import ALL_FACTS
from filters import InSearching

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    states = read_states()
    if message.from_user.id not in states:
        states[message.from_user.id] = null_state
    await message.answer(LEXICON[message.text])
    write_states(states)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/menu"
# и отправлять пользователю 2 инлайн-кнопки, чтобы выбрать, что он хочет сделать
@router.message(Command(commands='menu'))
async def process_menu_command(message: Message):
    await message.answer(
        text=LEXICON[message.text],
        reply_markup=menu_keyboard
    )


@router.message(Command(commands='random_fact'))
async def process_random_command(message: Message):
    await message.answer(
        text=choice(ALL_FACTS)
    )


# Этот хэндлер будет срабатывать на инлайн-кнопку, чтобы перейти к поиску"
@router.callback_query(F.data == 'search_menu_button')
async def process_search_button_pressed(callback: CallbackQuery):
    states = read_states()
    states[callback.from_user.id]['in_searching'] = True
    await callback.message.edit_text(
        text=LEXICON['search']
    )
    write_states(states)


@router.message(InSearching())
async def process_search(message: Message):
    states = read_states()
    
    # Выполняем поиск
    search_result = google_search(search_term=message.text, sites=SITES, num_results=100)
    
    # Если результаты есть, разделяем их на страницы
    if search_result:
        states[message.from_user.id]['search'] = separator(search_result)
        states[message.from_user.id]['page_number'] = 1  # Устанавливаем начальную страницу
        
        # Формируем текст для текущей страницы
        current_page = states[message.from_user.id]['search'][states[message.from_user.id]['page_number']]
        text = '\n\n'.join([f'<a href="{list(item.keys())[0]}">{list(item.values())[0]}</a>' for item in current_page])
    else:
        text = 'Ничего найти не удалось'
    
    # Отправляем результат пользователю
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            '<<',
            'menu_button',
            '>>'
        ),
        parse_mode="HTML"  # Указываем, что текст содержит HTML-разметку
    )
    
    # Выходим из режима поиска
    states[message.from_user.id]['in_searching'] = False
    write_states(states)


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
@router.callback_query(F.data == '>>')
async def process_forward_press(callback: CallbackQuery):
    states = read_states()
    if states[callback.from_user.id]['page_number'] < len(states[callback.from_user.id]['search']):
        states[callback.from_user.id]['page_number'] += 1
    else:
        states[callback.from_user.id]['page_number'] = 1

    current_page = states[callback.from_user.id]['search'][str(states[callback.from_user.id]['page_number'])]
    text = '\n\n'.join([f'<a href="{list(item.keys())[0]}">{list(item.values())[0]}</a>' for item in current_page])
    if not text:
        text = 'Ничего найти не удалось'
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            '<<',
            'menu_button',
            '>>'
        )
    )
    await callback.answer()
    write_states(states)


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
@router.callback_query(F.data == '<<')
async def process_backward_press(callback: CallbackQuery):
    states = read_states()
    if states[callback.from_user.id]['page_number'] > 1:
        states[callback.from_user.id]['page_number'] -= 1
    else:
        states[callback.from_user.id]['page_number'] = len(states[callback.from_user.id]['search'])

    current_page = states[callback.from_user.id]['search'][str(states[callback.from_user.id]['page_number'])]
    text = '\n\n'.join([f'<a href="{list(item.keys())[0]}">{list(item.values())[0]}</a>' for item in current_page])
    if not text:
        text = 'Ничего найти не удалось'
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            '<<',
            'menu_button',
            '>>'
        )
    )
    await callback.answer()
    write_states(states)



@router.callback_query(F.data == 'menu_button')
async def process_menu_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON['/menu'],
        reply_markup=menu_keyboard
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на инлайн-кнопку, чтобы перейти к фактам
@router.callback_query(F.data == 'facts_menu_button')
async def process_facts_button_pressed(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON['facts'],
        reply_markup=categories_keyboard
    )


@router.callback_query(F.data == 'stars_button')
async def process_stars_button_pressed(callback: CallbackQuery):
    states = read_states()
    facts = read_facts('Звёзды')
    states[callback.from_user.id]['actiive_category'] = 'stars'
    fact_number = states[callback.from_user.id][f"{states[callback.from_user.id]['actiive_category']}_fact_number"] + 1
    await callback.message.edit_text(
        text=facts[states[callback.from_user.id]['stars_fact_number']],
        reply_markup=create_facts_pagination_keyboard(f'{fact_number}')
    )
    write_states(states)


@router.callback_query(F.data == 'planets_button')
async def process_planets_button_pressed(callback: CallbackQuery):
    states = read_states()
    facts = read_facts('Планеты')
    states[callback.from_user.id]['actiive_category'] = 'planets'
    fact_number = states[callback.from_user.id][f"{states[callback.from_user.id]['actiive_category']}_fact_number"] + 1
    await callback.message.edit_text(
        text=facts[states[callback.from_user.id]['planets_fact_number']],
        reply_markup=create_facts_pagination_keyboard(f'{fact_number}')
    )
    write_states(states)


@router.callback_query(F.data == 'galaxies_button')
async def process_stars_button_pressed(callback: CallbackQuery):
    states = read_states()
    facts = read_facts('Галактики')
    states[callback.from_user.id]['actiive_category'] = 'galaxies'
    fact_number = states[callback.from_user.id][f"{states[callback.from_user.id]['actiive_category']}_fact_number"] + 1
    await callback.message.edit_text(
        text=facts[states[callback.from_user.id]['galaxies_fact_number']],
        reply_markup=create_facts_pagination_keyboard(f'{fact_number}')
    )
    write_states(states)


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
@router.callback_query(F.data == '>>>')
async def process_forward_fact_press(callback: CallbackQuery):
    states = read_states()
    facts = read_facts(states[callback.from_user.id]["actiive_category"])
    if states[callback.from_user.id][f'{states[callback.from_user.id]["actiive_category"]}_fact_number'] + 1 < len(facts):
        states[callback.from_user.id][f'{states[callback.from_user.id]["actiive_category"]}_fact_number'] += 1
    else:
        states[callback.from_user.id][f'{states[callback.from_user.id]["actiive_category"]}_fact_number'] = 0
    text = facts[states[callback.from_user.id][f'{states[callback.from_user.id]["actiive_category"]}_fact_number']]
    fact_number = states[callback.from_user.id][f"{states[callback.from_user.id]['actiive_category']}_fact_number"] + 1
    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=create_facts_pagination_keyboard(f'{fact_number}')
        )
    except TelegramBadRequest:
        pass

    await callback.answer()
    write_states(states)


@router.callback_query(F.data == '<<<')
async def process_backward_fact_press(callback: CallbackQuery):
    states = read_states()
    facts = read_facts(states[callback.from_user.id]["actiive_category"])
    if states[callback.from_user.id][f'{states[callback.from_user.id]["actiive_category"]}_fact_number'] + 1 > 1:
        states[callback.from_user.id][f'{states[callback.from_user.id]["actiive_category"]}_fact_number'] -= 1
    else:
        states[callback.from_user.id][f'{states[callback.from_user.id]["actiive_category"]}_fact_number'] = len(facts) - 1
    text = facts[states[callback.from_user.id][f'{states[callback.from_user.id]["actiive_category"]}_fact_number']]
    fact_number = states[callback.from_user.id][f"{states[callback.from_user.id]['actiive_category']}_fact_number"] + 1
    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=create_facts_pagination_keyboard(f'{fact_number}')
        )
    except TelegramBadRequest:
        pass

    await callback.answer()
    write_states(states)
