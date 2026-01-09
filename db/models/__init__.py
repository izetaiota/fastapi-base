from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from db.models.admin_user import AdminUser  # noqa: E402,F401
from db.models.order import Order  # noqa: E402,F401
from db.models.user import User  # noqa: E402,F401
