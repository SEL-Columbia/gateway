from sqlalchemy import *
from migrate import *

meta = MetaData()

main_logs = Table('primary_log',
                  meta,
                  Column('created', DateTime))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    meter_time = main_logs.c['created']
    meter_time.alter(name='meter_time')


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    meter_time = main_logs.c['meter_time']
    meter_time.alter(name='created')