from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from aiogram import types

import datetime

from settings import SQLALCHEMY_DATABASE_URL


class PreBase:
    id: Mapped[int] = mapped_column(primary_key=True)


Base = declarative_base(cls=PreBase)


class Channel(Base):
    __tablename__ = 'subscribes_channel'
    name: Mapped[str]
    tg_id: Mapped[str]
    tg_link: Mapped[str]


class Category(Base):
    __tablename__ = 'products_category'
    name: Mapped[str]


class SubCategory(Base):
    __tablename__ = 'products_subcategory'
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    name: Mapped[str]


class Product(Base):
    __tablename__ = 'products_product'
    sub_category_id: Mapped[int] = mapped_column(ForeignKey("subcategory.id"))
    name: Mapped[str]
    description: Mapped[str]
    image: Mapped[str]
    price: Mapped[int]


class Order(Base):
    __tablename__ = 'orders_order'
    user: Mapped[str]
    phone: Mapped[str]
    mail: Mapped[str]
    adress: Mapped[str]
    amount: Mapped[int]
    payment: Mapped[str]
    close: Mapped[bool]
    close_data: Mapped[datetime.datetime]


class ProductOrder(Base):
    __tablename__ = 'orders_productorder'
    product_id: Mapped[int] = mapped_column(ForeignKey("products_product.id"))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders_order.id"))
    quantity: Mapped[int]


class FAQ(Base):
    __tablename__ = 'subscribes_faq'
    quituestion: Mapped[str]
    answer: Mapped[str]


engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_channels() -> list:
    """Получение каналов и групп"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(Channel))
            result = [[chat.tg_id, chat.tg_link, chat.name]
                      for chat in result.scalars().all()]
            return result


async def get_faq(pag_y: int, page: int = 0) -> list:
    """Получение вопросов"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            q = select(FAQ).offset(
                page * pag_y
            ).limit(pag_y + 1)
            result = await session.execute(q)
            result = [[one_qu.id, one_qu.quituestion]
                      for one_qu in result.scalars().all()]
            return result


async def get_answer(faq_id: int | str) -> tuple:
    """Получение ответов на вопросы"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            q = select(FAQ).where(FAQ.id == int(faq_id))
            result = await session.execute(q)
            result = result.scalars().first()
            return result.answer, result.quituestion


async def get_categorys(pag_y: int, pag_x: int, page: int = 0) -> list:
    """Получение категорий"""
    obj_amount = pag_y * pag_x
    async with AsyncSessionLocal() as session:
        async with session.begin():
            q = select(Category).offset(
                page * obj_amount
            ).limit(obj_amount + 1)
            result = await session.execute(q)
            result = [[category.id, category.name]
                      for category in result.scalars()]
            return result


async def get_subcategorys(
    category: int, pag_y: int, pag_x: int, page: int = 0
) -> list:
    """Получение подкатегорий"""
    obj_amount = pag_y * pag_x
    async with AsyncSessionLocal() as session:
        async with session.begin():
            q = select(SubCategory).where(
                SubCategory.category_id == category
            ).offset(
                page * obj_amount
            ).limit(obj_amount + 1)
            result = await session.execute(q)
            result = [[subcategory.id, subcategory.name]
                      for subcategory in result.scalars()]
            return result


async def get_products(subcategory: int, page: int = 0) -> list:
    """Получение товаров"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            q = select(Product).where(
                Product.sub_category_id == subcategory
            ).offset(
                page
            ).limit(2)
            result = await session.execute(q)
            result = [
                [product.id, product.name, product.description,
                 product.image, product.price]
                for product in result.scalars()]
            return result


async def exist_or_create_order(user: str) -> list:
    """Если у пользователя нет корзины - создать"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            q = select(Order).where(
                (Order.user == user) &
                (Order.close == False)  # noqa
            )
            order = await session.execute(q)
            if not order.scalars().first():
                session.add(Order(user=user, amount=0, close=False))


async def add_incart(user: str, product_id: int, amount: int) -> list:
    """Добавление товара в корзину"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            q = select(Order).where(
                (Order.user == user) &
                (Order.close == False)  # noqa
            )
            order = await session.execute(q)
            order = order.scalars().first()
            q = select(Product).where(
                Product.id == product_id
            )
            product = await session.execute(q)
            product = product.scalars().first()
            q = select(ProductOrder).where(
                (ProductOrder.product_id == product_id) &
                (ProductOrder.order_id == order.id)
            )
            productorder = await session.execute(q)
            productorder = productorder.scalars().first()
            if productorder:
                productorder.quantity += amount
            else:
                session.add_all([
                    ProductOrder(
                        product_id=product_id,
                        order_id=order.id,
                        quantity=amount
                    )
                ])
            print(amount, product.price)
            order.amount += amount*product.price
            await session.commit()


async def delete_fromcart(user: str, product_id: str) -> list:
    """Удаление товара из корзины"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            q = select(Order).where(
                (Order.user == user) &
                (Order.close == False)  # noqa
            )
            order = await session.execute(q)
            order = order.scalars().first()
            q = select(Product).where(
                Product.id == product_id
            )
            product = await session.execute(q)
            product = product.scalars().first()
            q = select(ProductOrder).where(
                (ProductOrder.product_id == product_id) &
                (ProductOrder.order_id == order.id)
            )
            productorder = await session.execute(q)
            productorder = productorder.scalars().first()
            order.amount -= productorder.quantity*product.price
            await session.delete(productorder)
            await session.commit()


async def get_cart(user: str) -> list:
    """Получение корзины"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            q = select(Order).where(
                (Order.user == user) &
                (Order.close == False)  # noqa
            )
            order = await session.execute(q)
            order = order.scalars().first()
            q = select(ProductOrder).where(
                ProductOrder.order_id == order.id
            )
            productorders = await session.execute(q)
            productorders = productorders.scalars().all()
            return_list = [[]]
            if productorders:
                for productorder in productorders:
                    q = select(Product).where(
                        productorder.product_id == Product.id
                    )
                    product = await session.execute(q)
                    product = product.scalars().first()
                    return_list[0].append(
                        [product.id, product.name, productorder.quantity,
                         product.price])
                return_list.append(order.amount)
                return return_list
            else:
                return False


async def close_order(
    user: str, pay_id: int, info: types.SuccessfulPayment
) -> tuple:
    """Закрытие заказа"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            q = select(Order).where(
                (Order.user == user) &
                (Order.close == False)  # noqa
            )
            adress_info = info.shipping_address
            adress_text = (
                f'{adress_info.country_code},'
                f'{adress_info.state},'
                f'{adress_info.city},'
                f'{adress_info.post_code},'
                f'{adress_info.street_line1},'
                f'{adress_info.street_line2}'
            )
            order = await session.execute(q)
            order = order.scalars().first()
            order.phone = info.phone_number
            order.mail = info.email
            order.adress = adress_text
            order.payment = pay_id
            order.close_data = datetime.date.today()
            order.close = True
            return_tuple = (order.id, order.user, order.phone,
                            order.mail, order.adress)
            await session.commit()
            return return_tuple
