import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
# import datetime
# from datetime import date, datetime

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    # book = relationship("Book", back_populates="publisher")

    def __str__(self):
        return f'{self.id}: {self.name}'

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    # publisher = relationship(Publisher, back_populates="book")
    publisher = relationship(Publisher, backref="book")

    def __str__(self):
        return f'{self.id}: {self.title}'

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    # stock = relationship("Stock", back_populates="shop")

    def __str__(self):
        return f'{self.id}: {self.name}'

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    # book = relationship("Book", back_populates="stock")
    # shop = relationship("Shop", back_populates="stock")
    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

    def __str__(self):
        return f'{self.id}: {self.book_id}: {self.shop_id}'

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    sale_date = sq.Column(sq.String(length=40), nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    # stock = relationship("Stock", back_populates="sale")
    stock = relationship(Stock, backref="sale")

    def __str__(self):
        return f'{self.id}: {self.price}: {self.sale_date}: {self.stock_id}'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


DSN = "postgresql://postgres:bazadannykh@localhost:5432/publishers_db"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    # создание объектов
    pushkin = Publisher(name="Пушкин")
    lermontov = Publisher(name="Лермонтов")
    tolstoy = Publisher(name="Толстой")

    book1 = Book(title="Капитанская дочка", publisher=pushkin)
    book2 = Book(title="Евгений Онегин", publisher=pushkin)
    book3 = Book(title="Пиковая дама", publisher=pushkin)
    book4 = Book(title="Герой нашего времени", publisher=lermontov)
    book5 = Book(title="Мцыри", publisher=lermontov)
    book6 = Book(title="Кавказский пленник", publisher=lermontov)
    book7 = Book(title="Война и мир", publisher=tolstoy)
    book8 = Book(title="Анна Каренина", publisher=tolstoy)
    book9 = Book(title="Филипок", publisher=tolstoy)

    bukvoed = Shop(name="Буквоед")
    labirint = Shop(name="Лабиринт")
    knizdom = Shop(name="Книжный дом")
    chitgor = Shop(name="Читай-город")

    stock1 = Stock(book=book1, shop=bukvoed, count=6)
    stock2 = Stock(book=book1, shop=labirint, count=4)
    stock3 = Stock(book=book3, shop=labirint, count=1)
    stock4 = Stock(book=book7, shop=chitgor, count=20)
    stock5 = Stock(book=book7, shop=knizdom, count=25)
    stock6 = Stock(book=book7, shop=bukvoed, count=26)
    stock7 = Stock(book=book9, shop=bukvoed, count=27)
    stock8 = Stock(book=book8, shop=labirint, count=5)
    stock9 = Stock(book=book4, shop=chitgor, count=9)

    sale1 = Sale(price=900, sale_date="25-03-2024", stock=stock2, count=4)
    sale2 = Sale(price=650, sale_date="14-04-2024", stock=stock1, count=6)
    sale3 = Sale(price=1101, sale_date="16-05-2024", stock=stock4, count=2)
    sale4 = Sale(price=1102, sale_date="20-05-2024", stock=stock5, count=3)
    sale5 = Sale(price=1103, sale_date="28-05-2024", stock=stock4, count=5)
    sale6 = Sale(price=1200, sale_date="01-06-2024", stock=stock7, count=7)
    sale7 = Sale(price=1200, sale_date="01-06-2024", stock=stock8, count=7)
    sale8 = Sale(price=1102, sale_date="02-06-2024", stock=stock9, count=1)

    session.add_all([pushkin, lermontov, tolstoy, book1, book2, book3, book4, book5, book6, book7, book8, book9,
                     bukvoed, labirint, knizdom, chitgor, stock1, stock2, stock3, stock4, sale1, sale2, sale1])
    session.commit()  # фиксируем изменения

    autor = input("Введите имя автора: ")

    subq0 = session.query(Book).join(Publisher.book).filter(Publisher.name == autor)
    for s in subq0.all():
        query_list = []
        # query_list.append(s.title)
        # print(query_list)
        # print(s)
        subq_stock = session.query(Stock).join(Book.stock).filter(Stock.book_id == s.id)
        for s_st in subq_stock.all():
            # query_list.append(s.title)
            # print(s_st)
            subq_shop = session.query(Shop).join(Stock.shop).filter(Shop.id == s_st.shop_id)
            for s_sh in subq_shop.all():
                # query_list.append(s_sh.name)
                # print(query_list)
                subq_sale = session.query(Sale).join(Stock.sale).filter(Sale.stock_id == s_st.id)
                for s_sa in subq_sale.all():
                    # print(s_sa)
                    query_list.append(s.title)
                    query_list.append(s_sh.name)
                    query_list.append(s_sa.price)
                    query_list.append(s_sa.sale_date)
                    print(' | '.join(map(str, query_list)))
                    query_list = []