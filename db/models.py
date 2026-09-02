from sqlalchemy.orm import relationship

from .connection import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
class Users(Base):
    __tablename__ = "userTable"
    userId = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_At = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    reference = relationship("Conversations")
class Conversations(Base):
    __tablename__ = "conversationTable"
    conversationId = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    request_count = Column(Integer, nullable=False)
    requested_At = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    userId = Column(Integer, ForeignKey("userTable.userId", ondelete="CASCADE"), nullable=False)
    owner = relationship("Users")
    reference = relationship("Messages")

class Messages(Base):
    __tablename__ = "messageTable"
    messageId = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    role = Column(String, nullable=False)
    content = Column(String)
    generatedAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    conversationId = Column(Integer, ForeignKey("conversationTable.conversationId", ondelete="CASCADE"), nullable=False)
    owner = relationship("Conversations")