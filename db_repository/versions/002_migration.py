from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
novelty = Table('novelty', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String, nullable=False),
    Column('headline', String, nullable=False),
    Column('comments', Integer),
    Column('timestamp', DateTime),
)

novelty = Table('novelty', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String(length=2048), nullable=False),
    Column('headline', String(length=512), nullable=False),
    Column('tags', String(length=100)),
    Column('news_date', DateTime),
    Column('comments_count', Integer),
    Column('last_update', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['novelty'].columns['comments'].drop()
    pre_meta.tables['novelty'].columns['timestamp'].drop()
    post_meta.tables['novelty'].columns['comments_count'].create()
    post_meta.tables['novelty'].columns['last_update'].create()
    post_meta.tables['novelty'].columns['news_date'].create()
    post_meta.tables['novelty'].columns['tags'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['novelty'].columns['comments'].create()
    pre_meta.tables['novelty'].columns['timestamp'].create()
    post_meta.tables['novelty'].columns['comments_count'].drop()
    post_meta.tables['novelty'].columns['last_update'].drop()
    post_meta.tables['novelty'].columns['news_date'].drop()
    post_meta.tables['novelty'].columns['tags'].drop()
