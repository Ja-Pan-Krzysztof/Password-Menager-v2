from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

from .connection import Connection


Base = declarative_base()


class Owner(Base):
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    key_base64 = Column(String(64), nullable=False)
    key_hex = Column(String(64), nullable=False)
    uuid4 = Column(String(255), nullable=False)

    def __init__(self, username, password, key_base64, key_hex, uuid4):
        self.username = username
        self.password = password
        self.key_base64 = key_base64
        self.key_hex = key_hex
        self.uuid4 = uuid4


    def __repr__(self):
        return f'<User {self.username}>'


class Passwords(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    login = Column(String(255), nullable=False)
    site = Column(String(255), nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f'<Data {self.login} {self.password}>'


def build():
    """Create all table"""
    conn = Connection()
    engine = conn.conn()

    return Base.metadata.create_all(bind=engine)
