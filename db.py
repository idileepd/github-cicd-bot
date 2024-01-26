#ENV STUFF
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from secure import encrypt_data, decrypt_data
import os

db_name = os.getenv("DB_NAME")

DATABASE_URL = f"sqlite:///{db_name}.db"
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    accountId = Column(String, primary_key=True)
    name = Column(String)
    gitToken = Column(String)

class Repository(Base):
    __tablename__ = 'repositories'
    repoId = Column(String, primary_key=True)
    userId = Column(String)

# Create the table
Base.metadata.create_all(bind=engine)

# # Create a session to interact with the database
# Session = sessionmaker(bind=engine)
# session = Session()

# # Insert a new user
# new_user = Account(name="John Doe", age=25)
# session.add(new_user)
# session.commit()

# # Query and print all users
# users = session.query(Account).all()
# for user in users:
#     print(f"User ID: {user.id}, Name: {user.name}, Age: {user.age}")

# # Close the session
# session.close()


#-----
# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


def deleteRecord(id,Cls):
    id_to_delete = session.get(Cls, id)
    
    if id_to_delete:
        session.delete(id_to_delete)
        session.commit()
        print(f"Record with ID {id} has been deleted.")
    else:
        print(f"No Record found with ID {id}.")

deleteRecord("et",Account)

# # Encrypt and insert a new data
# new_data = Account(accountId="et",name="te",gitToken=encrypt_data("secretToke"))
# session.add(new_data)
# session.commit()

# # Query and decrypt the data
# stored_data = session.query(Account).filter_by(accountId="et").first()
# decrypted_data = decrypt_data(stored_data.gitToken)

# print(f"Encrypted Data: {stored_data.gitToken}")
# print(f"Decrypted Data: {decrypted_data}")



# Close the session
session.close()