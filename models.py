from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy import create_engine, Column, String, Text

from secure import Secure
from database import Base


class Account(Base):
    __tablename__ = "accounts"
    accountId = Column(String, primary_key=True)
    name = Column(String)
    gitToken = Column(String)

    def get_json(self):
        return {
            "accountId": self.accountId,
            "name": self.name,
            "gitToken": Secure.decrypt(self.gitToken),
        }


class Repository(Base):
    __tablename__ = "repos"
    repoId = Column(String, primary_key=True)
    accountId = Column(String)

    preStartScript = Column(Text)
    startScript = Column(Text)

    checkoutLogs = Column(Text)
    preStartLogs = Column(Text)
    startLogs = Column(Text)
    allLogs = Column(Text)

    env = Column(Text)

    def get_json(self):
        return {
            "repoId": self.repoId,
            "accountId": self.accountId,
            "preStartScript": self.preStartScript,
            "startScript": self.startScript,
            "checkoutLogs": self.checkoutLogs,
            "preStartLogs": self.preStartLogs,
            "startLogs": self.startLogs,
            "allLogs": self.allLogs,
        }
