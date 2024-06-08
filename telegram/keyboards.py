from aiogram import types

from settings import PAGINATION_ROW, PAGINATION_WORD_ROW


def start_buttons():
    """Клавиатура после старта"""
    buttons = [[
        types.InlineKeyboardButton(
            text='Каталог', callback_data='cat'
        ),
        types.InlineKeyboardButton(
            text='Корзина', callback_data='cart'
        ),
        types.InlineKeyboardButton(
            text='FAQ', callback_data='faq'
        )
    ]]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def faq_inline(obj_list, page=0):
    buttons = []
    buttons_row = []
    next_page = False
    max_page = PAGINATION_ROW
    if len(obj_list) > max_page:
        obj_list = obj_list[:max_page]
        next_page = True
    for index_row in range(len(obj_list)):
        quituestion = obj_list[index_row]
        buttons_row.append(
            types.InlineKeyboardButton(
                callback_data=f'faq:{str(quituestion[0])},page:{page-1}',
                text=quituestion[1]
            )
        )
    buttons.append(buttons_row)

    if page == 1:
        prew_button = types.InlineKeyboardButton(
            text='Первая страница',
            callback_data='none'
        )
    else:
        prew_button = types.InlineKeyboardButton(
            text='Страница ' + str(page-1),
            callback_data=f'faq,page:{page-2}',
        )
    if not next_page:
        next_button = types.InlineKeyboardButton(
            text='Последняя страница', callback_data='none'
        )
    else:
        next_button = types.InlineKeyboardButton(
            text='Страница ' + str(page+1),
            callback_data=f'faq,page:{page}',
        )
    buttons.append([
        prew_button,
        types.InlineKeyboardButton(
            text='Текущая страница: ' + str(page),
            callback_data='none'
        ),
        next_button
    ])
    buttons.append([
        types.InlineKeyboardButton(
            text='На главную',
            callback_data='menu'
        )
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def categorys_inline(categorys_list, page=0):
    buttons = []
    buttons_row = []
    next_page = False
    max_page = PAGINATION_ROW*PAGINATION_WORD_ROW
    if len(categorys_list) > max_page:
        categorys_list = categorys_list[:max_page]
        next_page = True
    for index_row in range(len(categorys_list)):
        if index_row % PAGINATION_WORD_ROW == 0:
            buttons.append(buttons_row)
            buttons_row = []
        category = categorys_list[index_row]
        buttons_row.append(
            types.InlineKeyboardButton(
                callback_data='cat:' + str(category[0]), text=category[1]
            )
        )
    buttons.append(buttons_row)

    if page == 1:
        prew_button = types.InlineKeyboardButton(
            text='Первая страница',
            callback_data='none'
        )
    else:
        prew_button = types.InlineKeyboardButton(
            text='Страница ' + str(page-1),
            callback_data='cat_page:' + str(page-2)
        )
    if not next_page:
        next_button = types.InlineKeyboardButton(
            text='Последняя страница', callback_data='none'
        )
    else:
        next_button = types.InlineKeyboardButton(
            text='Страница ' + str(page+1),
            callback_data='cat_page:' + str(page)
        )
    buttons.append([
        prew_button,
        types.InlineKeyboardButton(
            text='Текущая страница: ' + str(page),
            callback_data='none'
        ),
        next_button
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def subcategorys_inline(cat_id, obj_list, page=0):
    buttons = []
    buttons_row = []
    next_page = False
    max_page = PAGINATION_ROW*PAGINATION_WORD_ROW
    if len(obj_list) > max_page:
        obj_list = obj_list[:max_page]
        next_page = True
    for index_row in range(len(obj_list)):
        if index_row % PAGINATION_WORD_ROW == 0:
            buttons.append(buttons_row)
            buttons_row = []
        obj = obj_list[index_row]
        buttons_row.append(
            types.InlineKeyboardButton(
                callback_data=f'sub:{str(obj[0])},cat:{cat_id}', text=obj[1]
            )
        )
    buttons.append(buttons_row)

    if page == 1:
        prew_button = types.InlineKeyboardButton(
            text='Первая страница',
            callback_data='none'
        )
    else:
        prew_button = types.InlineKeyboardButton(
            text='Страница ' + str(page-1),
            callback_data=f'cat:{cat_id},sub_page:{str(page-2)}'
        )
    if not next_page:
        next_button = types.InlineKeyboardButton(
            text='Последняя страница', callback_data='none'
        )
    else:
        next_button = types.InlineKeyboardButton(
            text='Страница ' + str(page+1),
            callback_data=f'cat:{cat_id},sub_page:{str(page)}'
        )
    buttons.append([
        prew_button,
        types.InlineKeyboardButton(
            text='Текущая страница: ' + str(page),
            callback_data='none'
        ),
        next_button
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def products_inline(obj_list, sub_id, cat_id, page=0, amount=1):
    buttons = []
    max_page = 1
    next_page = False
    if len(obj_list) > max_page:
        obj_list = obj_list[:max_page]
        next_page = True
    prod_id = obj_list[0][0]
    prod_price = obj_list[0][4]
    if page == 1:
        prew_button = types.InlineKeyboardButton(
            text='---',
            callback_data='none'
        )
    else:
        prew_button = types.InlineKeyboardButton(
            text='Предыдущий товар',
            callback_data=f'sub:{sub_id},cat:{cat_id},prod_page:{str(page-2)}'
        )
    if not next_page:
        next_button = types.InlineKeyboardButton(
            text='---', callback_data='none'
        )
    else:
        next_button = types.InlineKeyboardButton(
            text='Следующий товар',
            callback_data=f'sub:{sub_id},cat:{cat_id},prod_page:{str(page)}'
        )
    buttons.append([
        prew_button,
        types.InlineKeyboardButton(
            text=f'Цена: {prod_price}',
            callback_data='none'
        ),
        next_button
    ])
    if amount > 1:
        minus_amount = types.InlineKeyboardButton(
            text='-1',
            callback_data=f'sub:{sub_id},cat:{cat_id},prod_page:{str(page-1)},amount:{amount - 1}'
        )
    else:
        minus_amount = types.InlineKeyboardButton(
            text='---', callback_data='none'
        )
    buttons.append([
        minus_amount,
        types.InlineKeyboardButton(
            text=f'В корзину: {amount} шт',
            callback_data=f'incart:{amount},sub:{sub_id},cat:{cat_id},prod_page:{str(page)}'
        ),
        types.InlineKeyboardButton(
            text='+1',
            callback_data=f'sub:{sub_id},cat:{cat_id},prod_page:{str(page-1)},amount:{amount + 1}'
        ),
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def cart_inline(prod_id, sub_id, cat_id):
    buttons = []
    buttons.append([
        types.InlineKeyboardButton(
            text='Продолжить',
            callback_data=f'sub:{sub_id},cat:{cat_id},prod_page:{str(prod_id-1)}'
        ),
        types.InlineKeyboardButton(
            text='В корзину',
            callback_data='cart'
        )
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def change_cart_inline(obj_list):
    buttons = []
    for obj in obj_list:
        buttons.append([
            types.InlineKeyboardButton(
                text=f'Удалить {obj[1]} из корзины',
                callback_data=f'cart,del:{obj[0]}'
            )
        ])
    buttons.append([
        types.InlineKeyboardButton(
            text='К оплате',
            callback_data='buy'
        )
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def empty_cart_inline():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(
            text='К покупкам',
            callback_data='cat'
        )]]
    )
