#import pytz
#import requests
import csv
from datetime import datetime, timedelta
from magneto import dbsettings
from sqlalchemy import Column, DateTime, String, Integer, Float, \
                       ForeignKey, MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

# Main measurements table fields:
# Date_UTC,IAGA,MLT,MLAT,N,E,Z,SOURCE
# SuperMAG stations fields:
#IAGA,GLON,GLAT,MLON,MLAT,STATION_NAME


def insert_stations():
    Base = automap_base()

    #engine = create_engine('sqlite:///../../data/magneto.db')
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(dbsettings.write_user, dbsettings.write_user_passwd,
                                                                dbsettings.host, dbsettings.port, dbsettings.db))
    Base.prepare(engine, schema='magneto', reflect=True)

    Station = Base.classes.stations

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

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        session.bulk_save_objects(stations)
        session.commit()
        print('Station data added to DB')
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    print ("Reading and storing stations.")
    insert_stations()
