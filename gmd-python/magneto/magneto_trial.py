#import pytz
#import requests
import csv
from datetime import datetime, timedelta
from magneto.dbsettings import *
from sqlalchemy import Column, DateTime, String, Integer, Float, \
                       ForeignKey, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

Base = declarative_base()

# Main measurements table fields:
# Date_UTC,IAGA,MLT,MLAT,N,E,Z,SOURCE
# SuperMAG stations fields:
#IAGA,GLON,GLAT,MLON,MLAT,STATION_NAME

class Station(Base):
    __tablename__ = 'stations'
    iaga = Column(String, primary_key=True)
    glon = Column(Float)
    glat = Column(Float)
    mlon = Column(Float)
    mlat = Column(Float)
    station_name = Column(String)

class Measurement(Base):
    __tablename__ = 'measurements'
    metadata = MetaData(schema='magneto')
    date_utc = Column(DateTime,primary_key=True)
    iaga = Column(String,ForeignKey('stations.iaga'),primary_key=True)
    mlt = Column(Float)
    mlat = Column(Float)
    n = Column(Float)
    e = Column(Float)
    z = Column(Float)
    source = Column(String,nullable=True)

def read_measurements():
    measurementsfile = '../../data/supermag-2000-01-01T00-00-00.csv'
    measurements=[]
    with open(measurementsfile) as f:
        reader = csv.reader(f)
        first = True
        for row in reader:
            if(first):
                first=False
            else:
                measurement = None # Needs implementation ...
                measurements.append(measurement)
    return measurements

def read_stations():
    stationsfile = '../../data/supermag_stations.csv'
    stations = []
    with open(stationsfile) as f:
        reader = csv.reader(f)
        first = True
        for row in reader:
            if(first):
                first=False
            else:
                station = Station(iaga=row[0],glon=float(row[1]),glat=float(row[2]),mlon=float(row[3]),mlat=float(row[4]),
                              station_name=row[5])
                stations.append(station)
    return stations


def insert_stations():
    #engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(USER, PASSWORD, HOST, PORT, DATABASE))
    engine = create_engine('sqlite:///../../data/magneto.db')
    # print(Base.metadata)
    Station.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    stations = read_stations()
    try:
        session.bulk_save_objects(stations)
        session.commit()
        print('Station data added to DB')
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()

# def insert_measurements():
#     #engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(USER, PASSWORD, HOST, PORT, DATABASE))
#     engine = create_engine('sqlite:///../../data/magneto.db')
#     print(Base.metadata)
#     Measurement.metadata.create_all(engine)
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     measurements = read_measurements()
#     try:
#         session.bulk_save_objects(measurements)
#         session.commit()
#         print('Measurement data added to DB')
#     except Exception as e:
#         print(e)
#         session.rollback()
#     finally:
#         session.close()

if __name__ == '__main__':
    insert_stations()
    #insert_measurements()
