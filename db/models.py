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
    reference = relationship("ConversationTable")
class ConversationTable(Base):
    __tablename__ = "conversationTable"
    conversationId = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    request_count = Column(Integer, nullable=False)
    requested_At = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    userId = Column(Integer, ForeignKey("userTable.userId", ondelete="CASCADE"), nullable=False)
    owner = relationship("Users")