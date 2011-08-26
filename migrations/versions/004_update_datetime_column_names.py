from sqlalchemy import *
from migrate import *

meta = MetaData()



def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    pass

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
