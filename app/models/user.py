from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import false, true

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(index=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(server_default=true())
    is_superuser: Mapped[bool] = mapped_column(server_default=false())
    weight: Mapped[float] = mapped_column(nullable=True)

    def __repr__(self):
        return f"<User(full_name={self.full_name}, email={self.email})>"
