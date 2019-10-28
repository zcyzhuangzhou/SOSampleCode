import traceback
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, MetaData, ForeignKey, DateTime, Index, Boolean, func, Table, \
    SmallInteger, Float, or_, and_, engine
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db.engine_factory import EngineFactory

Base = declarative_base()


class Post(Base):
    __tablename__ = 'post_java'
    Id = Column(Integer, primary_key=True, nullable=False, index=True)
    PostTypeId = Column(Integer, nullable=False)
    AcceptedAnswerId = Column(Integer, nullable=True, index=True)
    ParentId = Column(Integer, nullable=True)
    Score = Column(Integer, nullable=False)
    ViewCount = Column(Integer, nullable=True)
    Body = Column(LONGTEXT(charset='utf8mb4'), nullable=False, index=True)
    OwnerUserId = Column(Integer, nullable=False)
    LastEditorUserId = Column(Integer, nullable=True)
    LastEditDate = Column(LONGTEXT(), nullable=True)
    LastActivityDate = Column(LONGTEXT(), nullable=False)
    Title = Column(LONGTEXT(), nullable=True)
    Tags = Column(LONGTEXT(), nullable=True)
    AnswerCount = Column(Integer, nullable=False)
    CommentCount = Column(Integer, nullable=False)
    FavoriteCount = Column(Integer, nullable=False)
    CreationDate = Column(LONGTEXT(), nullable=False)

    __table_args__ = (Index('search_API_post_index', Id, AcceptedAnswerId, Title, Body), {
        "mysql_charset": "utf8mb4",
    })

    def __init__(self, Id, AcceptedAnswerId, Score, Title, Tags):
        self.Id = Id
        self.AcceptedAnswerId = AcceptedAnswerId
        self.Score = Score
        self.Title = Title
        self.Tags = Tags

    def create(self, session, autocommit=True):
        session.add(self)
        if autocommit:
            session.commit()
        return self

    @staticmethod
    def get_by_id(session, Id):
        try:
            return session.query(Post).filter_by(Id=Id).first()
        except Exception:
            traceback.print_exc()
            return None

    @staticmethod
    def get_by_apiname_title(session, API_name):
        try:
            return session.query(Post).filter(Post.Title.like('%' + API_name + '%')).first()
        except Exception:
            traceback.print_exc()
            return None

    @staticmethod
    def get_by_apiname_body(session, API_name):
        try:
            return session.query(Post).filter(Post.Body.like('%' + API_name + '%')).first()
        except Exception:
            traceback.print_exc()
            return None


class PostHtmlText(Base):
    __tablename__ = 'body_html_text_clean_java'
    Id = Column(Integer, primary_key=True, nullable=False, index=True)
    Question = Column(LONGTEXT(charset='utf8mb4'), nullable=False, index=True)
    AcceptedAnswer = Column(LONGTEXT(charset='utf8mb4'), nullable=False, index=True)
    Score = Column(Integer, nullable=False)
    Title = Column(LONGTEXT(), nullable=True)
    Tags = Column(LONGTEXT(), nullable=True)
    Body_Question = Column(LONGTEXT(), nullable=False)
    Body_AcceptedAnswer = Column(LONGTEXT(), nullable=False)
    Code_Question = Column(LONGTEXT(), nullable=True)
    Code_AcceptedAnswer = Column(LONGTEXT(), nullable=True)
    Url_Question = Column(LONGTEXT(), nullable=True)
    Url_AcceptedAnswer = Column(LONGTEXT(), nullable=True)

    __table_args__ = (Index('index', Id, Question, AcceptedAnswer), {
        "mysql_charset": "utf8mb4",
    })

    def __init__(self, Id, Question, AcceptedAnswer, Score, Title, Tags, Body_Question, Body_AcceptedAnswer,
                 Code_Question, Code_AcceptedAnswer, Url_Question, Url_AcceptedAnswer):
        self.Id = Id
        self.Question = Question
        self.AcceptedAnswer = AcceptedAnswer
        self.Score = Score
        self.Title = Title
        self.Tags = Tags
        self.Body_Question = Body_Question
        self.Body_AcceptedAnswer = Body_AcceptedAnswer
        self.Code_Question = Code_Question
        self.Code_AcceptedAnswer = Code_AcceptedAnswer
        self.Url_Question = Url_Question
        self.Url_AcceptedAnswer = Url_AcceptedAnswer

    def create(self, session, autocommit=True):
        session.add(self)
        if autocommit:
            session.commit()
        return self

    @staticmethod
    def get_by_id(session, Id):
        try:
            return session.query(PostHtmlText).filter_by(Id=Id).first()
        except Exception:
            traceback.print_exc()
            return None

    @staticmethod
    def get_by_apiname(session, API_name):
        try:
            return session.query(PostHtmlText).filter(or_(PostHtmlText.Title.like('%' + API_name + '%'),
                                                          PostHtmlText.Question.like('%' + API_name + '%'),
                                                          PostHtmlText.AcceptedAnswer.like('%' + API_name + '%'))).all()
            # return session.execute(
            #     '''select * from stackoverflow.body_html_text_clean_java
            #     where instr(Title, 'java.lang.StringBuilder') > 0
            #     or instr(Question, 'java.lang.StringBuilder') > 0
            #     or instr(AcceptedAnswer, 'java.lang.StringBuilder') > 0;''')
            # return session.execute(
            #     '''select * from stackoverflow.body_html_text_clean_java
            #     where LOCATE('java.lang.StringBuilder', Title) > 0
            #     or LOCATE('java.lang.StringBuilder', Question) > 0
            #     or LOCATE('java.lang.StringBuilder', AcceptedAnswer) > 0;''')
            # return session.execute(
            #     '''select * from stackoverflow.body_html_text_clean_java
            #     where POSITION('java.lang.StringBuilder' in Title)
            #     or POSITION('java.lang.StringBuilder' in Question)
            #     or POSITION('java.lang.StringBuilder' in AcceptedAnswer);''')
            # return session.execute(
            #     '''select * from stackoverflow.body_html_text_clean_java
            #     where match(stackoverflow.body_html_text_clean_java.Title,
            #     stackoverflow.body_html_text_clean_java.Question,
            #     stackoverflow.body_html_text_clean_java.AcceptedAnswer) against('java.lang.StringBuilder');''')
        except Exception:
            traceback.print_exc()
            return None

    @staticmethod
    def add_all_data(session, data):
        session.add_all(data)
        session.commit()

    @staticmethod
    def delete_by_id(session, Id):
        session.delete(session.query(PostHtmlText).filter_by(Id=Id).first())
        session.commit()


if __name__ == "__main__":
    engine = EngineFactory.create_engine_by_schema_name("stackoverflow")
    metadata = MetaData(bind=engine)
    # delete all table

    # Base.metadata.drop_all(bind=engine)

    # create the table
    Base.metadata.create_all(bind=engine)
