# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite"
# # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from secure import Secure

Base = declarative_base()

# Tables


class DB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            db_name = os.getenv("DB_NAME")
            DATABASE_URL = f"sqlite:///{db_name}.db"

            # Create Singleton instance
            cls._instance = super(DB, cls).__new__(cls)

            # Create DB Engine
            cls._instance.__engine = create_engine(DATABASE_URL, echo=False)

            # Create the tables
            Base.metadata.create_all(bind=cls._instance.__engine)

            # Create a session to interact with the database
            NewSession: Session = sessionmaker(bind=cls._instance.__engine)
            cls._instance.__session = NewSession()

            # Get the current timestamp (just for testing)
            current_timestamp = datetime.now()
            formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            cls._instance.__timestamp = formatted_timestamp

        return cls._instance

    @staticmethod
    def get_session() -> Session:
        return DB._instance.__session

    @staticmethod
    def get_engine():
        return DB._instance.__engine

    @staticmethod
    def get_timestamp():
        return DB._instance.__timestamp

    @staticmethod
    def close():
        DB._instance.__session.close()
        print("DB Session Connection Close.")

    @staticmethod
    def deleteRecord(id, TableClass):
        session = DB._instance.__session
        item_to_delete = session.get(TableClass, id)
        if item_to_delete:
            session.delete(item_to_delete)
            session.commit()
            print(f"Record with ID {id} has been deleted.")
        else:
            print(f"No Record found with ID {id}.")

    @staticmethod
    def add(data):
        session: Session = DB._instance.__session
        try:
            session.add(data)
            session.commit()
        except Exception as e:
            print("Error adding data to table")
            session.rollback()

    @staticmethod
    def getItemByPk(TableClass, pk):
        session: Session = DB._instance.__session
        return session.get(TableClass, pk)


# initialize the singleton instance
DB()
