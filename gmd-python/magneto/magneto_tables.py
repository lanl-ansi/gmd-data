import csv
from datetime import datetime, timedelta
from magneto import dbsettings
from sqlalchemy import Column, DateTime, String, Integer, Float, \
                       ForeignKey, MetaData, create_engine, Table

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

Base = declarative_base()

# Main measurements table fields:
# Date_UTC,IAGA,MLT,MLAT,N,E,Z,SOURCE
# SuperMAG stations fields:
#IAGA,GLON,GLAT,MLON,MLAT,STATION_NAME

engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(dbsettings.write_user,dbsettings.write_user_passwd,
                                                            dbsettings.host, dbsettings.port, dbsettings.db))
#engine = create_engine('sqlite:///../../data/magneto.db')

metadata = MetaData()

stations = Table('stations', metadata,
    Column('iaga', String, primary_key=True),
    Column('glon', Float, nullable=False),
    Column('glat', Float, nullable=False),
    Column('mlon', Float, nullable=False),
    Column('mlat', Float, nullable=False),
    Column('station_name', String, nullable=True),
    schema = 'magneto'
)

measurements = Table('measurements', metadata,
    Column('date_utc', DateTime, primary_key=True),
    Column('iaga', String, ForeignKey("magneto.stations.iaga"), primary_key=True),
    Column('mlt', Float),
    Column('mlat', Float),
    Column('n', Float),
    Column('e', Float),
    Column('z', Float),
    Column('collection', String, primary_key=True),
    schema='magneto'
)

metadata.create_all(engine)