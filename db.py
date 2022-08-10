import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.types import Integer, String
from sqlalchemy import Column, ForeignKey, text
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

# Creating DB engine
engine = create_engine(
    url='postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'.format(
        db_user=os.environ.get("DB_USER", 'app'),
        db_password=os.environ.get("DB_PASSWORD", '123qwe'),
        db_host=os.environ.get("DB_HOST", 'localhost'),
        db_port=os.environ.get("DB_PORT", 5432),
        db_name=os.environ.get("DB_NAME", 'users')
    )
)

# In the most general sense, the Session establishes all conversations with the database and represents a “holding zone”
# for all the objects which you’ve loaded or associated with it during its lifespan.

# The Session begins in a mostly stateless form. Once queries are issued or other objects are persisted with it,
# it requests a connection resource from an Engine that is associated with the Session, and then establishes
# a transaction on that connection. This transaction remains in effect until the Session is instructed to commit or
# roll back the transaction.

# The purpose of sessionmaker is to provide a factory for Session objects with a fixed configuration.
session_factory = sessionmaker(engine)

Base = declarative_base(bind=engine)


# TODO: Визуализация таблиц
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, comment='User ID')
    first_name = Column(String, comment="User's first name")
    last_name = Column(String, comment="User's last name")
    email = Column(String, comment="User's email")
    group_id = Column(Integer, ForeignKey('user_group.id'))
    password = Column(String, comment='Password as is')

    def __str__(self):
        return f"User: {self.first_name} {self.last_name}"

    def __repr__(self):
        return self.__str__()


class UserGroup(Base):
    __tablename__ = 'user_group'

    id = Column(Integer, primary_key=True, comment='Group ID')
    name = Column(String, comment="Group name")
    users = relationship("User")

    def __str__(self):
        return f'{self.name} group'.capitalize()

    def __repr__(self):
        return self.__str__()


# Creating tables
Base.metadata.create_all()
