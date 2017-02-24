import csv
from datetime import datetime
from magneto import dbsettings
from sqlalchemy import Column, DateTime, String, Integer, Float, \
                       ForeignKey, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = declarative_base()

# Main measurements table fields:
# Date_UTC,IAGA,MLT,MLAT,N,E,Z,SOURCE
# SuperMAG stations fields:
#IAGA,GLON,GLAT,MLON,MLAT,STATION_NAME

class Measurement(Base):
    __tablename__ = 'measurements'
    date_utc = Column(DateTime,primary_key=True)
    iaga = Column(String,ForeignKey('stations.iaga'),primary_key=True)
    mlt = Column(Float)
    mlat = Column(Float)
    n = Column(Float)
    e = Column(Float)
    z = Column(Float)
    source = Column(String,nullable=True)

def insert_measurements(measurementsfile,db_uri):
    Base = automap_base()

    engine = create_engine(db_uri)

    Base.prepare(engine, schema='magneto', reflect=True)

    Measurement = Base.classes.measurements

    with open(measurementsfile) as f:
        reader = csv.reader(f)
        buffsize = 1000
        count = 0
        total = 0
        first = True
        measurements = []
        for row in reader:
            if(first):
                first=False
            else:
                measurement = Measurement(date_utc=datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S"),iaga=row[1],mlt=float(row[2]),mlat=float(row[3]),
                                                          n=float(row[4]),e=float(row[5]),z=float(row[6]),collection='SuperMAG')
                measurements.append(measurement)
                count += 1
                if (count%buffsize)==0:
                    insert_buffer(measurements,engine)
                    total += count
                    print(str(total) + ' records written.')
                    count = 0
                    measurements = []
        if len(measurements)!=0:
            insert_buffer(measurements,engine)
            total += len(measurements)
            print(str(total) + ' records written.')
        f.close()

def insert_buffer(measurements, engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        session.bulk_save_objects(measurements)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    #db_uri = 'sqlite:///../../data/magneto.db'
    #db_uri='postgresql://{}:{}@{}:{}/{}'.format(dbsettings.write_user, dbsettings.write_user_passwd,
    #                                                            dbsettings.host, dbsettings.port, dbsettings.db)

    print("Reading and storing measurements.")
    dt1 = datetime.now()
    print('start = '+str(dt1))
    #measurementsfile = '../../data/supermag-2000-01-01T00-00-00-abbr.csv'
    db_uri=None
    measurementsfile = None # Will abort with error.
    insert_measurements(measurementsfile,db_uri)
    dt2 = datetime.now()
    print('end = ' + str(dt2))
    print('cpu time = '+str(dt2-dt1))


