from aiogram import types
from aiogram.filters import BaseFilter
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from database import get_channels
from config import bot
from settings import ADMIN_ID


class CheckSub(BaseFilter):
    async def __call__(self, message: types.Message):
        chats = await get_channels()
        sub_buttons = list()
        for chat in chats:
            try:
                user_channel_status = await bot.get_chat_member(
                    chat_id=chat[0],
                    user_id=message.from_user.id
                )
            except TelegramBadRequest:
                text = f'Меня нет в чате или он указан неверно - id: {chat[0]}'
                await bot.send_message(chat_id=ADMIN_ID, text=text)
            except TelegramForbiddenError:
                text = f'Меня выкинули из этого чата - id: {chat[0]}'
                await bot.send_message(chat_id=ADMIN_ID, text=text)
            if user_channel_status.status == ChatMemberStatus.LEFT:
                sub_buttons.append(
                    [types.InlineKeyboardButton(url=chat[1], text=chat[2])]
                )
        else:
            if len(sub_buttons) == 0:
                return True
            markup = types.InlineKeyboardMarkup(
                inline_keyboard=sub_buttons
            )
            await bot.send_message(
                chat_id=message.from_user.id,
                text='Подпишитесь на телеграмм каналы:',
                reply_markup=markup
            )
