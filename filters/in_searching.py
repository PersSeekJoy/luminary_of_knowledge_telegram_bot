from aiogram.filters import BaseFilter
from aiogram.types import Message
from services import read_states


class InSearching(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        states = read_states()
        return states[message.from_user.id]['in_searching']
