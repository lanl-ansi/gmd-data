from magneto import dbsettings
from sqlalchemy import Column, DateTime, String, Integer, Float, \
                       ForeignKey, MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

class DBConnector:
    def __init__(self):
        self.engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(dbsettings.read_user,\
            dbsettings.read_user_passwd,dbsettings.host,\
            dbsettings.port, dbsettings.db))
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base = automap_base()
        Base.prepare(self.engine, schema='magneto', reflect=True)
        self.Station = Base.classes.stations
        self.Measurement = Base.classes.measurements


    def close(self):
        self.session.close()
