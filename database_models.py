from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column 

Base = declarative_base()


class Note(Base):
    __tablename__ = "Notes"
    id = mapped_column(Integer , primary_key=True, index=True)
    heading = mapped_column(String)
    pointers = mapped_column(String)
    