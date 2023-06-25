import uuid as uuid
from sqlalchemy import Table, String, Integer, Column, Text, DateTime, Boolean, create_engine, BLOB, ForeignKey, JSON
from datetime import datetime

from sqlalchemy.orm import declarative_base, sessionmaker

from config_reader import config

Base = declarative_base()
metadata = Base.metadata


class Addresses(Base):
    __tablename__ = 't_addresses'
    id = Column(Integer(), primary_key=True)
    stellar_address = Column(String(32), nullable=False)
    account_id = Column(String(56), nullable=False)
    memo = Column(String(32), nullable=True)
    add_dt = Column(DateTime(), default=datetime.now)
    updated_dt = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Transactions(Base):
    __tablename__ = 't_transactions'
    hash = Column('hash', String(64), primary_key=True)
    description = Column('description', Text(4000), nullable=False)
    body = Column('body', Text(12000), nullable=False)
    add_dt = Column('add_dt', DateTime(), default=datetime.now)
    updated_dt = Column('updated_dt', DateTime(), default=datetime.now, onupdate=datetime.now)
    uuid = Column('uuid', String(32), default=uuid.uuid4().hex)
    json = Column('json', Text(), nullable=True)
    state = Column('state', Integer(), default=0)  # 0-new 1-need_sent 2-was_send


class Signers(Base):
    __tablename__ = 't_signers'
    id = Column('id', Integer(), primary_key=True)
    username = Column('username', String(32), nullable=False)
    public_key = Column('public_key', String(56), nullable=False)
    signature_hint = Column('signature_hint', String(8), nullable=False)
    add_dt = Column('add_dt', DateTime(), default=datetime.now)


class Signatures(Base):
    __tablename__ = 't_signatures'
    id = Column('id', Integer(), primary_key=True)
    signature_xdr = Column('signature_xdr', String(100), nullable=False)
    transaction_hash = Column('transaction_hash', String(64), ForeignKey('t_transactions.hash'))
    signer_id = Column('signer_id', Integer(), ForeignKey('t_signers.id'))
    add_dt = Column('add_dt', DateTime(), default=datetime.now)
    Column('updated_dt', DateTime(), default=datetime.now, onupdate=datetime.now)


if __name__ == '__main__':
    pass
    engine = create_engine(config.db_dns, pool_pre_ping=True)
    db_pool = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
