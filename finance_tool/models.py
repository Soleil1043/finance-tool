from sqlalchemy import (create_engine, Column, Integer, String,
                        Float, Date, ForeignKey, UniqueConstraint)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    id      = Column(Integer, primary_key=True)
    name    = Column(String(50), unique=True, nullable=False)
    budget  = Column(Float, default=0)          # 月度预算
    transactions = relationship('Transaction', back_populates='category')

class Transaction(Base):
    __tablename__ = 'transactions'
    id      = Column(Integer, primary_key=True)
    date    = Column(Date, nullable=False, index=True)
    amount  = Column(Float, nullable=False)
    description = Column(String(200))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category    = relationship('Category')

    __table_args__ = (UniqueConstraint('date', 'amount', 'description'),)

def init_db(db_path='data/finance.db'):
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
