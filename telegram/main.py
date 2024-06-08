import asyncio

from aiogram import F, Bot
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, PreCheckoutQuery, LabeledPrice, InputMediaPhoto

from config import dp, bot
from filters import CheckSub
from keyboards import start_buttons, categorys_inline, subcategorys_inline, products_inline, cart_inline, change_cart_inline, empty_cart_inline, faq_inline
from settings import PAGINATION_ROW, PAGINATION_WORD_ROW, PROVIDER_TOKEN
from database import get_categorys, get_subcategorys, get_products, exist_order
import database as db
import google_client as gclient


@dp.message(CommandStart(), CheckSub())
async def start(message: Message, bot: Bot, command: CommandObject):
    await menu(message, bot)


@dp.callback_query(
    lambda call:
    call.data.startswith('menu')
)
async def menu(message: CallbackQuery | Message, bot: Bot):
    try:
        await message.message.answer(
            'Я тестовый бот для заказа товаров. Выберите нужную опцию:',
            reply_markup=start_buttons()
        )
        await message.answer()
    except AttributeError:
        await message.answer(
            'Я тестовый бот для заказа товаров. Выберите нужную опцию:',
            reply_markup=start_buttons()
        )


@dp.callback_query(
    lambda call:
    call.data.startswith('faq')
)
async def faq(callback: CallbackQuery, bot: Bot):
    page = 0
    faq_id = None
    data = callback.data.split(',')
    if len(data) > 1:
        page = int(data[1].split(':')[1])
    if 'faq:' in callback.data:
        faq_id = int(data[0].split(':')[1])
    if faq_id:
        answer, question = await db.get_answer(faq_id)
        text = f'Ответ на вопрос "{question}":\n{answer}'
    else:
        text = 'Часто задаваемые вопросы:'
    faq_list = await db.get_faq(PAGINATION_ROW, page)
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=faq_inline(faq_list, page+1)
    )
    await callback.answer()


@dp.callback_query(
    lambda call:
    call.data == 'cat' or
    call.data.startswith("cat_page:")
)
async def catalog(callback: CallbackQuery, bot: Bot):
    page = 0
    if 'page' in callback.data:
        page = int(callback.data.split(':')[1])
    categorys = await get_categorys(PAGINATION_ROW, PAGINATION_WORD_ROW, page)
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text='Выберите интересующую категорию',
        reply_markup=categorys_inline(categorys, page+1)
    )
    await callback.answer()


@dp.callback_query(
    lambda call:
    call.data.startswith("cat:")
)
async def subcatalog(callback: CallbackQuery, bot: Bot):
    page = 0
    data = callback.data.split(',')
    if len(data) > 2:
        page = int(data[1].split(':')[1])
    category = int(data[0].split(':')[1])
    subcategorys = await get_subcategorys(
        category,
        PAGINATION_ROW,
        PAGINATION_WORD_ROW,
        page
    )
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text='Выберите интересующую категорию',
        reply_markup=subcategorys_inline(category, subcategorys, page+1)
    )
    await callback.answer()


@dp.callback_query(
    lambda call:
    call.data.startswith("sub:")
)
async def products(callback: CallbackQuery, bot: Bot):
    page = 0
    amount = 1
    data = callback.data.split(',')
    if len(data) > 2:
        page = int(data[2].split(':')[1])
    if len(data) > 3:
        amount = int(data[3].split(':')[1])
    category = int(data[1].split(':')[1])
    subcat = int(data[0].split(':')[1])
    products = await get_products(
        subcat,
        page
    )
    if callback.message.photo:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(media=FSInputFile(
                f'backend/static/media/{products[0][3]}'),
                caption='*Описание*:\n' + products[0][2],
                parse_mode="Markdown"),
            reply_markup=products_inline(
                products, category, subcat, page+1, amount),
        )
    else:
        await bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=FSInputFile(f'backend/static/media/{products[0][3]}'),
            caption='*Описание*:\n' + products[0][2],
            reply_markup=products_inline(
                products, category, subcat, page+1, amount),
            parse_mode="Markdown"
        )
    await callback.answer()


@dp.callback_query(
    lambda call:
    call.data.startswith("incart:")
)
async def change_cart(callback: CallbackQuery, bot: Bot):
    data = callback.data.split(',')
    product = int(data[3].split(':')[1])
    category = int(data[2].split(':')[1])
    subcat = int(data[1].split(':')[1])
    amount = int(data[0].split(':')[1])
    username = callback.from_user.username
    if not await exist_order(username):
        await db.create_order(username)
    await db.add_incart(username, product, amount)
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text='Хотите продолжить покупки или перейти в корзину?',
        reply_markup=cart_inline(product, subcat, category)
    )
    await callback.answer()


@dp.callback_query(
    lambda call:
    call.data.startswith("cart")
)
async def cart(callback: CallbackQuery, bot: Bot):
    username = callback.from_user.username
    data = callback.data.split(',')
    if len(data) > 1:
        del_item = int(data[1].split(':')[1])
        await db.delete_fromcart(username, del_item)
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
            reply_markup=change_cart_inline(cart[0])
        )
    else:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text='Корзина пуста!',
            reply_markup=empty_cart_inline()
        )
    await callback.answer()


@dp.callback_query(
    lambda call:
    call.data.startswith("buy")
)
async def order(callback: CallbackQuery, bot: Bot):
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
        reply_markup=start_buttons()
    )


@dp.callback_query(F.data == "none")
async def none_func(callback: CallbackQuery):
    await callback.answer()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
