import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date

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
    title = sq.Column(sq.String(length=40), nullable=False)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    # publisher = relationship(Publisher, back_populates="book")
    publisher = relationship(Publisher, backref="book")

    def __str__(self):
        return f'{self.id}: {self.title}: {self.publisher_id}'

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    logo = sq.Column(sq.String(length=40), unique=True)

    # stock = relationship("Stock", back_populates="shop")

    def __str__(self):
        return f'{self.id}: {self.logo}'

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
    sale_date = sq.Column(sq.Date, nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    # stock = relationship("Stock", back_populates="sale")
    stock = relationship(Stock, backref="sale")

    def __str__(self):
        return f'{self.id}: {self.price}: {self.sale_date}: {self.stock_id}'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def get_booksales(var):
    qq = session.query(Stock.shop_id, Shop.logo, Book.title, Publisher.id, Publisher.name, Sale.price, Sale.sale_date
                       ).join(Shop).join(Book).join(Publisher).join(Sale).subquery()
    if var.isdigit():
        qqq = session.query(qq).filter(qq.c.id == var)
    else:
        qqq = session.query(qq).filter(qq.c.name == var)
    column1 = '  Название книги'
    column2 = '  Магазин'
    column3 = '  Цена'
    column4 = '  Дата'
    print(f"{column1: <40}   {column2: <17}   {column3: <8}   {column4}")
    for s in qqq.all():
        # print(s.title, s.logo, s.price, s.sale_date)
        print(f"{s.title: <40} | {s.logo: <17} | {s.price: <8} | {s.sale_date.strftime('%d-%m-%Y')}")


DSN = "postgresql://postgres:bazadannykh@localhost:5432/publishers_db"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    # создание объектов:
    pushkin = Publisher(name="Пушкин")
    blok = Publisher(name="Блок")
    lermontov = Publisher(name="Лермонтов")
    tolstoy = Publisher(name="Толстой")
    session.add_all([pushkin, blok, lermontov, tolstoy])

    book1 = Book(title="Капитанская дочка", publisher=pushkin)
    book2 = Book(title="Евгений Онегин", publisher=pushkin)
    book3 = Book(title="Пиковая дама", publisher=pushkin)
    book4 = Book(title="Герой нашего времени", publisher=lermontov)
    book5 = Book(title="Мцыри", publisher=lermontov)
    book6 = Book(title="Кавказский пленник", publisher=lermontov)
    book7 = Book(title="Война и мир", publisher=tolstoy)
    book8 = Book(title="Анна Каренина", publisher=tolstoy)
    book9 = Book(title="Филипок", publisher=tolstoy)
    session.add_all([book1, book2, book3, book4, book5, book6, book7, book8, book9])

    bukvoed = Shop(logo="Буквоед")
    labirint = Shop(logo="Лабиринт")
    knizdom = Shop(logo="Книжный дом")
    chitgor = Shop(logo="Читай-город")
    kniga = Shop(logo="Книга")
    bookstore = Shop(logo="Букстор")
    session.add_all([bukvoed, labirint, knizdom, chitgor, kniga, bookstore])

    stock1 = Stock(book=book1, shop=bukvoed, count=6)
    stock2 = Stock(book=book1, shop=labirint, count=4)
    stock3 = Stock(book=book3, shop=labirint, count=1)
    stock4 = Stock(book=book7, shop=chitgor, count=20)
    stock5 = Stock(book=book7, shop=knizdom, count=25)
    stock6 = Stock(book=book7, shop=bukvoed, count=26)
    stock7 = Stock(book=book9, shop=bukvoed, count=11)
    stock8 = Stock(book=book8, shop=labirint, count=5)
    stock9 = Stock(book=book4, shop=chitgor, count=9)
    stock10 = Stock(book=book7, shop=labirint, count=28)
    session.add_all([stock1, stock2, stock3, stock4, stock5, stock6, stock7, stock8, stock9, stock10])

    sale1 = Sale(price=900, sale_date=date(2024, 3, 25), stock=stock2, count=4)
    sale2 = Sale(price=650, sale_date=date(2024, 4, 14), stock=stock1, count=6)
    sale3 = Sale(price=1101, sale_date=date(2024, 5,16), stock=stock4, count=2)
    sale4 = Sale(price=1102, sale_date=date(2024, 5, 20), stock=stock5, count=3)
    sale5 = Sale(price=1103, sale_date=date(2024, 5, 28), stock=stock3, count=5)
    sale6 = Sale(price=1200, sale_date=date(2024, 6, 1), stock=stock7, count=7)
    sale7 = Sale(price=1200, sale_date=date(2024, 6, 1), stock=stock8, count=7)
    sale8 = Sale(price=1102, sale_date=date(2024, 6, 2), stock=stock9, count=1)
    session.add_all([sale1, sale2, sale3, sale4, sale5, sale6, sale7, sale8])

    # session.add_all([pushkin, lermontov, tolstoy, book1, book2, book3, book4, book5, book6, book7, book8, book9,
    #                  bukvoed, labirint, knizdom, chitgor, kniga, stock1, stock2, stock3, stock4, stock5, stock6,
    #                  stock7, stock8, stock9, sale1, sale2, sale3, sale4, sale5, sale6, sale7, sale8])
    session.commit()
    autor = input("Введите id или имя автора: ")
    get_booksales(autor)
