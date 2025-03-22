from aiogram import Router
from aiogram.types import Message
from lexicon import LEXICON
from services import read_states, write_states

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def send_echo(message: Message):
    states = read_states()
    states[message.from_user.id]['nonsense_couner'] += 1
    # ----- Пасхалки -----
    if states[message.from_user.id]['nonsense_couner'] == 100:
        await message.answer('''100 раз!
Ты сейчас серьёзно!?
Тебе заняться что ли нечем!?
Зачем 100 раз что попало сюда писать?''')
    elif states[message.from_user.id]['nonsense_couner'] == 1000:
        await message.answer('''Ну да, кто и что тебя остановит...
Подумаешь всего лишь 1000 бесполезных сообщений...
Ладно, я понял, что с тобой бесполезно.
                             
Всё, надоело, делай что хочешь.''')
    elif states[message.from_user.id]['nonsense_couner'] == 10000:
        await message.answer('''Обалдеть ты настойчивый!
Мне кажется мы с тобой найдём общий язык, можешь написать сюда: @nikita_olh''')
    # -----          -----
    else:
        await message.answer(LEXICON['unknown_command'])
    write_states(states)
