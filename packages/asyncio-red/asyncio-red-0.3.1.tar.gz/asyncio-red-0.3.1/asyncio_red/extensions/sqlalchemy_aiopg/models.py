from sqlalchemy import Table, MetaData, Column, BigInteger, String, Float, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, JSON

meta = MetaData()


RedIncomingEvent = Table(
    'red_incoming_event', meta,

    Column('id', BigInteger, primary_key=True),
    Column('type', String(length=254), index=True),
    Column('source', String(length=254), index=True),
    Column('uuid', UUID, index=True),
    Column('created_at', Float),
    Column('received_at', Float),
    Column('payload', JSON)
)


RedIncomingEventResult = Table(
    'red_incoming_event_result', meta,

    Column('id', BigInteger, primary_key=True),
    Column('red_incoming_event_id', ForeignKey('red_incoming_event.id')),
    Column('error', String(length=500)),
    Column('finished_at', Float)
)
