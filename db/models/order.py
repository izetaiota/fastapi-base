from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from db.models import Base


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
