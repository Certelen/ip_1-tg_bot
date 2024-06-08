from aiogram import types

from settings import PAGINATION_ROW, PAGINATION_WORD_ROW


def next_page_exist(
    obj_list: list,
    pag_x: int = 1,
    pag_y: int = PAGINATION_ROW,
    next_page: bool = False
) -> bool:
    if len(obj_list) > pag_y*pag_x:
        obj_list = obj_list[:pag_y*pag_x]
        next_page = True
    return next_page


def start_buttons() -> types.InlineKeyboardMarkup:
    """Клавиатура после старта"""
    buttons = [[
        types.InlineKeyboardButton(
            text='Каталог', callback_data='cat:none,page:0'
        ),
        types.InlineKeyboardButton(
            text='Корзина', callback_data='cart:none,del:none'
        ),
        types.InlineKeyboardButton(
            text='FAQ', callback_data='faq:none,page:0'
        )
    ]]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def faq_inline(obj_list: list, page: int = 0) -> types.InlineKeyboardMarkup:
    """Клавиатура популярных вопросов"""
    buttons = []
    buttons_row = []
    for index_row in range(len(obj_list)):
        quituestion = obj_list[index_row]
        buttons_row.append(
            types.InlineKeyboardButton(
                callback_data=f'faq:{str(quituestion[0])},page:{page-1}',
                text=quituestion[1]
            )
        )
    buttons.append(buttons_row)

    prew_text = '---' if page == 1 else 'Предыдущая страница'
    prew_call = 'none' if page == 1 else f'faq:none,page:{page-2}'
    next_text = '---' if not next_page_exist(
        obj_list
    ) else 'Следующая страница'
    next_call = 'none' if not next_page_exist(
        obj_list
    ) else f'faq:none,page:{page}'

    buttons.append([
        types.InlineKeyboardButton(
            text=prew_text,
            callback_data=prew_call,
        ),
        types.InlineKeyboardButton(
            text=f'<{str(page)}>',
            callback_data='none'
        ),
        types.InlineKeyboardButton(
            text=next_text,
            callback_data=next_call,
        )
    ])
    buttons.append([
        types.InlineKeyboardButton(
            text='На главную',
            callback_data='menu'
        )
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def categorys_inline(
    obj_list: list, page: int = 0
) -> types.InlineKeyboardMarkup:
    """Клавиатура категорий"""
    buttons = []
    buttons_row = []
    for index_row in range(len(obj_list)):
        if index_row % PAGINATION_WORD_ROW == 0:
            buttons.append(buttons_row)
            buttons_row = []
        category = obj_list[index_row]
        buttons_row.append(
            types.InlineKeyboardButton(
                callback_data=f'cat:{str(category[0])},page:0',
                text=category[1]
            )
        )
    buttons.append(buttons_row)

    prew_text = '---' if page == 1 else 'Страница ' + str(page-1)
    prew_call = 'none' if page == 1 else 'cat_page:' + str(page-2)
    next_text = '---' if not next_page_exist(
        obj_list, PAGINATION_WORD_ROW
    ) else 'Страница ' + str(page+1)
    next_call = 'none' if not next_page_exist(
        obj_list, PAGINATION_WORD_ROW
    ) else 'cat_page:' + str(page)

    buttons.append([
        types.InlineKeyboardButton(
            text=prew_text,
            callback_data=prew_call,
        ),
        types.InlineKeyboardButton(
            text=f'<{str(page)}>',
            callback_data='none'
        ),
        types.InlineKeyboardButton(
            text=next_text,
            callback_data=next_call,
        )
    ])
    buttons.append([
        types.InlineKeyboardButton(
            text='Вернуться на главную',
            callback_data='menu')
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def subcategorys_inline(
    cat_id: int, obj_list: list, page: int = 0
) -> types.InlineKeyboardMarkup:
    """Клавиатура подкатегорий"""
    buttons = []
    buttons_row = []
    for index_row in range(len(obj_list)):
        if index_row % PAGINATION_WORD_ROW == 0:
            buttons.append(buttons_row)
            buttons_row = []
        obj = obj_list[index_row]
        buttons_row.append(
            types.InlineKeyboardButton(
                callback_data=(
                    f'sub:{str(obj[0])},'
                    f'cat:{cat_id},'
                    'prod_page:0,'
                    'amount:1'
                ), text=obj[1]
            )
        )
    buttons.append(buttons_row)

    prew_text = '---' if page == 1 else 'Страница ' + str(page-1)
    prew_call = 'none' if page == 1 else f'cat:{cat_id},page:{str(page-2)}'
    next_text = '---' if not next_page_exist(
        obj_list, PAGINATION_WORD_ROW
    ) else 'Страница ' + str(page+1)
    next_call = 'none' if not next_page_exist(
        obj_list, PAGINATION_WORD_ROW
    ) else f'cat:{cat_id},page:{str(page)}'

    buttons.append([
        types.InlineKeyboardButton(
            text=prew_text,
            callback_data=prew_call,
        ),
        types.InlineKeyboardButton(
            text=f'<{str(page)}>',
            callback_data='none'
        ),
        types.InlineKeyboardButton(
            text=next_text,
            callback_data=next_call,
        )
    ])
    buttons.append([
        types.InlineKeyboardButton(
            text='Вернуться на главную',
            callback_data='menu')
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def products_inline(
    obj_list: list, sub_id: int, cat_id: int, page: int = 0, amount: int = 1
) -> types.InlineKeyboardMarkup:
    """Клавиатура товаров"""
    buttons = []
    prod_price = obj_list[0][4]
    prew_text = '---' if page == 1 else 'Предыдущий товар'
    prew_call = (
        f'sub:{sub_id},'
        f'cat:{cat_id},'
        f'prod_page:{str(page-2)},'
        'amount:1' if page == 1 else 'none')
    next_text = '---' if not next_page_exist(
        obj_list, PAGINATION_WORD_ROW
    ) else 'Следующий товар'
    next_call = (
        f'sub:{sub_id},'
        f'cat:{cat_id},'
        f'prod_page:{str(page)},'
        'amount:1' if not next_page_exist(
            obj_list, PAGINATION_WORD_ROW
        ) else 'none')
    buttons.append([
        types.InlineKeyboardButton(
            text=prew_text,
            callback_data=prew_call,
        ),
        types.InlineKeyboardButton(
            text=f'Цена: {prod_price}',
            callback_data='none'
        ),
        types.InlineKeyboardButton(
            text=next_text,
            callback_data=next_call,
        )
    ])
    prew_text = '-1' if amount > 1 else '---'
    prew_call = (
        f'sub:{sub_id},'
        f'cat:{cat_id},'
        f'prod_page:{str(page-1)},'
        f'amount:{amount - 1}' if amount > 1 else 'none')
    buttons.append([
        types.InlineKeyboardButton(
            text=prew_text,
            callback_data=prew_call
        ),
        types.InlineKeyboardButton(
            text=f'Добавить:{amount} шт',
            callback_data=(
                f'incart:{amount},'
                f'sub:{sub_id},'
                f'cat:{cat_id},'
                f'prod_page:{str(page)}')
        ),
        types.InlineKeyboardButton(
            text='+1',
            callback_data=(
                f'sub:{sub_id},'
                f'cat:{cat_id},'
                f'prod_page:{str(page-1)},'
                f'amount:{amount + 1}')
        ),
    ])
    buttons.append([
        types.InlineKeyboardButton(
            text='Вернуться на главную',
            callback_data='menu')
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def cart_inline(
    prod_id: int, sub_id: int, cat_id: int
) -> types.InlineKeyboardMarkup:
    """Клавиатура после добавления товара в корзину"""
    buttons = []
    buttons.append([
        types.InlineKeyboardButton(
            text='Продолжить',
            callback_data=(
                f'sub:{sub_id},'
                f'cat:{cat_id},'
                f'prod_page:{prod_id-1},'
                'amount:1')
        ),
        types.InlineKeyboardButton(
            text='В корзину',
            callback_data='cart:none,del:none'
        )
    ])
    buttons.append([
        types.InlineKeyboardButton(
            text='Вернуться на главную',
            callback_data='menu')
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def change_cart_inline(obj_list: list) -> types.InlineKeyboardMarkup:
    """Клавиатура удаления товара из корзины"""
    buttons = []
    for obj in obj_list:
        buttons.append([
            types.InlineKeyboardButton(
                text=f'Удалить {obj[1]} из корзины',
                callback_data=f'cart:none,del:{obj[0]}'
            )
        ])
    buttons.append([
        types.InlineKeyboardButton(
            text='К оплате',
            callback_data='buy'
        )
    ])
    buttons.append([
        types.InlineKeyboardButton(
            text='Вернуться на главную',
            callback_data='menu')
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def empty_cart_inline() -> types.InlineKeyboardMarkup:
    """Клавиатура при пустой корзине"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(
            text='К покупкам',
            callback_data='cat:none,page:0'
        )], [
            types.InlineKeyboardButton(
                text='Вернуться на главную',
                callback_data='menu')
        ]]
    )
