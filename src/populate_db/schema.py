from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship

# ORM Class Definitions
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)
    address = Column(JSON)
    date_of_birth = Column(Date)
    created_at = Column(DateTime)
    orders = relationship("Order", back_populates="user")


class Inventory(Base):
    __tablename__ = 'inventory'

    product_name = Column(String, primary_key=True)
    available_quantity = Column(Integer)
    unit_price = Column(Numeric)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_date = Column(DateTime)
    status = Column(String)
    total = Column(Numeric)
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_name = Column(String, ForeignKey('inventory.product_name'))
    requested_quantity = Column(Integer)
    unit_price = Column(Numeric)
    order = relationship("Order", back_populates="items")
    inventory = relationship("Inventory")