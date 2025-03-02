from sqlalchemy.orm import mapped_column, Mapped

from database.connection import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(nullable=False)