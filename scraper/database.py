## Ref: https://github.com/stgrmks/jobCrawler/blob/master/crawler/db/db.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

## sql config
mysql_config = {
    'host': 'localhost',
    'port': 4001,
    'user': 'root',
    'pw': '',
    'db': 'jobsdb'
}

class jobs(Base):
    __tablename__ = 'jobs'
    id = Column(String(250), primary_key=True)
    date = Column(String(250))
    title = Column(String(250))
    company = Column(String(250))
    description = Column(String(10000))
    url = Column(String(5000))

def connect_and_create():
    user = mysql_config['user']
    host = mysql_config['host']
    port = mysql_config['port']
    pw = mysql_config['pw']
    db = mysql_config['db']
    engine = create_engine('mysql://{}:{}@{}:{}/{}'.format(user, pw, host, port, db))
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(bind=engine)
    return engine, session

def commit(session, entry):
    session.add(entry)
    session.commit()
    return