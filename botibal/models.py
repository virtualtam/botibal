"""Database models"""
# pylint: disable=invalid-name,too-few-public-methods
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Question(Base):
    """Quizz question model"""

    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    text = Column(Text)

    answers = relationship(
        'Answer',
        back_populates='question',
        cascade='all, delete, delete-orphan',
    )


class Answer(Base):
    """Quizz answer model"""

    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    question_id = Column(Integer, ForeignKey('question.id'))

    question = relationship('Question', back_populates='answers')


class Taunt(Base):
    """Taunt model"""

    __tablename__ = 'taunt'

    id = Column(Integer, primary_key=True)
    nick = Column(Text)
    text = Column(Text)
    aggro = Column(Integer, default=5)
