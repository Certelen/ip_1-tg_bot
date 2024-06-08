import asyncio

from aiogram import F, Bot
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import (Message, CallbackQuery, FSInputFile,
                           PreCheckoutQuery, LabeledPrice, InputMediaPhoto)

from config import dp, bot
from filters import CheckSub
from settings import PAGINATION_ROW, PAGINATION_WORD_ROW, PROVIDER_TOKEN
import keyboards as kb
import database as db
import google_client as gclient


async def split_callback(data: list) -> dict:
    data = data.split(',')
    data_dict = dict()
    for arg in data:
        arg = arg.split(':')
        data_dict[arg[0]] = arg[1]
    return data_dict


@dp.message(CommandStart(), CheckSub())
async def start(message: Message, bot: Bot, command: CommandObject):
    await menu(message, bot)


@dp.callback_query(
    lambda call:
    call.data.startswith('menu')
)
async def menu(message: CallbackQuery | Message, bot: Bot):
    try:
        await bot.edit_message_text(
            chat_id=message.message.chat.id,
            message_id=message.message.message_id,
            text='Я тестовый бот для заказа товаров. Выберите нужную опцию:',
            reply_markup=kb.start_buttons()
        )
        await message.answer()
    except AttributeError:
        await message.answer(
            'Я тестовый бот для заказа товаров. Выберите нужную опцию:',
            reply_markup=kb.start_buttons()
        )


@dp.callback_query(
    lambda call:
    call.data.startswith('faq')
)
async def faq(callback: CallbackQuery, bot: Bot):
    call_data = await split_callback(callback.data)
    faq_id = call_data['faq']
    page = int(call_data['page'])
    if call_data['faq'] != 'none':
        answer, question = await db.get_answer(faq_id)
        text = f'Ответ на вопрос "{question}":\n{answer}'
    else:
        text = 'Часто задаваемые вопросы:'
    faq_list = await db.get_faq(PAGINATION_ROW, page)
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=kb.faq_inline(faq_list, page+1)
    )
    await callback.answer()


@dp.callback_query(
    lambda call:
    call.data.startswith('cat:none') or
    call.data.startswith("cat_page:")
)
async def catalog(callback: CallbackQuery, bot: Bot):
    call_data = await split_callback(callback.data)
    if 'page' in call_data:
        page = int(call_data['page'])
    else:
        page = int(call_data['cat_page'])
    categorys = await db.get_categorys(
        PAGINATION_ROW,
        PAGINATION_WORD_ROW,
        page
    )
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text='Выберите интересующую категорию',
        reply_markup=kb.categorys_inline(categorys, page+1)
    )
    await callback.answer()


@dp.callback_query(
    lambda call:
    call.data.startswith("cat:")
)
async def subcatalog(callback: CallbackQuery, bot: Bot):
    call_data = await split_callback(callback.data)
    page = int(call_data['page'])
    category = int(call_data['cat'])
    subcategorys = await db.get_subcategorys(
        category,
        PAGINATION_ROW,
        PAGINATION_WORD_ROW,
        page
    )
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text='Выберите интересующую категорию',
        reply_markup=kb.subcategorys_inline(category, subcategorys, page+1)
    )
    await callback.answer()


@dp.callback_query(
    lambda call:
    call.data.startswith("sub:")
)
async def products(callback: CallbackQuery, bot: Bot):
    call_data = await split_callback(callback.data)
    category = int(call_data['cat'])
    subcat = int(call_data['sub'])
    page = int(call_data['prod_page'])
    amount = int(call_data['amount'])
    products = await db.get_products(
        subcat,
        page
    )
    if not products:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text='В данной подкатегории нет товаров.',
            reply_markup=kb.empty_cart_inline()
        )
    else:
        if callback.message.photo:
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=InputMediaPhoto(media=FSInputFile(
                    f'static/media/{products[0][3]}'),
                    caption='*Описание*:\n' + products[0][2],
                    parse_mode="Markdown"),
                reply_markup=kb.products_inline(
                    products, category, subcat, page+1, amount),
            )
        else:
            await bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id
            )
            await bot.send_photo(
                chat_id=callback.message.chat.id,
                photo=FSInputFile(f'static/media/{products[0][3]}'),
                caption='*Описание*:\n' + products[0][2],
                reply_markup=kb.products_inline(
                    products, category, subcat, page+1, amount),
                parse_mode="Markdown"
            )
    await callback.answer()


@dp.callback_query(
    lambda call:
    call.data.startswith("incart:")
)
async def change_cart(callback: CallbackQuery, bot: Bot):
    call_data = await split_callback(callback.data)
    category = int(call_data['cat'])
    subcat = int(call_data['sub'])
    amount = int(call_data['incart'])
    product = int(call_data['prod_page'])
    username = callback.from_user.username

    await db.exist_or_create_order(username)
    await db.add_incart(username, product, amount)
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text='Хотите продолжить покупки или перейти в корзину?',
        reply_markup=kb.cart_inline(product, subcat, category)
    )
    await callback.answer()


@dp.callback_query(
    lambda call:
    call.data.startswith("cart")
)
async def cart(callback: CallbackQuery, bot: Bot):
    """Корзина из главной и удаление товаров"""
    username = callback.from_user.username
    call_data = await split_callback(callback.data)
    del_item = call_data['del']
    if del_item != 'none':
        await db.delete_fromcart(username, int(del_item))
    await db.exist_or_create_order(username)
    cart = await db.get_cart(username)
    if cart:
        text = 'В корзине:\n'
        for item in cart[0]:
            text += f'{item[1]} - {item[2]} шт\n'
        text += f'Общая цена:{cart[1]}'
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=text,
            reply_markup=kb.change_cart_inline(cart[0])
        )
    else:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text='Корзина пуста!',
            reply_markup=kb.empty_cart_inline()
        )
    await callback.answer()


@dp.callback_query(
    lambda call:
    call.data.startswith("buy")
)
async def order(callback: CallbackQuery, bot: Bot):
    """Отправка запроса на оплату"""
    username = callback.from_user.username
    order = await db.get_cart(username)
    prices = []
    for product in order[0]:
        prices.append(
            LabeledPrice(
                label=f'{product[1]} - {product[2]} шт',
                amount=product[2] * product[3] * 100
            )
        )
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title='Окно оплаты заказа',
        description='Здесь Вы можете оплатить заказ.',
        payload='Payment through a bot',
        provider_token=PROVIDER_TOKEN,
        currency='rub',
        prices=prices,
        start_parameter='Test_bot_ip',
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True,
        need_email=True,
        request_timeout=10
    )
    await callback.answer()


@dp.pre_checkout_query()
async def pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery,
    bot: Bot
):
    """После подтверждение оплаты, но перед самим фактом оплаты"""
    await bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True
    )


@dp.message(F.successful_payment)
async def succesfull_payment(
        message: Message,
        bot: Bot
):
    """Сообщение об успешной оплате заказа."""
    username = message.from_user.username
    payment_id = message.successful_payment.provider_payment_charge_id
    info = message.successful_payment.order_info

    products = await db.get_cart(username)
    order_info = await db.close_order(username, payment_id, info)
    await gclient.spreadsheets_update_value(products, order_info)

    msg = (
        'Ваш заказ общей стоимостью: '
        f'{message.successful_payment.total_amount // 100} '
        f'{message.successful_payment.currency}. успешно оплачен!'
        f'\r\nСпасибо, что выбираете нас!'
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text=msg,
        reply_markup=kb.start_buttons()
    )


@dp.callback_query(F.data == "none")
async def none_func(callback: CallbackQuery):
    """Отработка нажатия 'пустых' клавиш"""
    await callback.answer()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
