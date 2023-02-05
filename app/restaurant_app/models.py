from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class RestaurantMenu(Base):
    __tablename__ = "RestaurantMenu"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(2048), nullable=False)
    sub_menu = relationship("RestaurantSubMenu", back_populates="menu")


menus = RestaurantMenu.__table__


class RestaurantSubMenu(Base):
    __tablename__ = "RestaurantSubMenu"
    id = Column(Integer, primary_key=True)
    menu_id = Column(
        Integer, ForeignKey("RestaurantMenu.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(255), nullable=False)
    description = Column(String(2048), nullable=False)
    menu = relationship("RestaurantMenu", back_populates="sub_menu")
    dish = relationship("RestaurantDish", back_populates="sub_menu")


sub_menus = RestaurantSubMenu.__table__


class RestaurantDish(Base):
    __tablename__ = "RestaurantDish"
    id = Column(Integer, primary_key=True)
    sub_menu_id = Column(
        Integer, ForeignKey("RestaurantSubMenu.id", ondelete="CASCADE"), nullable=False
    )
    price = Column(
        Float(precision=2, asdecimal=True, decimal_return_scale=2), nullable=False
    )
    title = Column(String(255), nullable=False)
    description = Column(String(2048), nullable=False)
    sub_menu = relationship("RestaurantSubMenu", back_populates="dish")


dish = RestaurantDish.__table__
