from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column , Mapped

Base = declarative_base()


class Note(Base):
    __tablename__ = "Notes"
    id : Mapped[int]= mapped_column(Integer , primary_key=True, index=True)
    heading: Mapped[str] = mapped_column(String)
    pointers: Mapped[str] = mapped_column(String)
    