from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship

# ORM Class Definitions
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    address = Column(JSON, nullable=False)
    date_of_birth = Column(Date)
    created_at = Column(DateTime)

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, unique=True, nullable=False)
    available_quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric, nullable=False)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), ondelete="CASCADE")
    order_date = Column(DateTime)
    status = Column(String)
    total = Column(Numeric)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), ondelete="CASCADE")
    product_name = Column(String, ForeignKey('inventory.product_name'), ondelete="CASCADE")
    requested_quantity = Column(Integer)
    unit_price = Column(Numeric)
    order = relationship("Order", back_populates="items")
    inventory = relationship("Inventory")