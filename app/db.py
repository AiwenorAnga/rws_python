"""
DB definitions.
"""
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

engine = create_engine('postgresql://app:app@localhost/app')
session: Union[Session, scoped_session] = scoped_session(sessionmaker(bind=engine))

def create_empty_db():    
    from app.model import Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
