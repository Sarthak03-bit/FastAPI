from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column , Mapped, relationship


Base = declarative_base()


class Note(Base):
    __tablename__ = "Notes"
    id : Mapped[int]= mapped_column(Integer , primary_key=True, index=True)
    heading: Mapped[str] = mapped_column(String)
    pointers: Mapped[str] = mapped_column(String)

    # foreign key to users.id
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # relationship back to User
    owner: Mapped["User"] = relationship(back_populates="notes")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)

    # 1 user -> many notes
    notes: Mapped[list["Note"]] = relationship(back_populates="owner")

