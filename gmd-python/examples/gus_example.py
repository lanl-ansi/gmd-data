import pytz
import requests
from datetime import datetime, timedelta
from magneto.dbsettings import *
from sqlalchemy import Column, DateTime, String, Integer, \
                       MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

Base = declarative_base()

class Nomination(Base):
    __tablename__ = 'nominations'
    metadata = MetaData(schema='gas')
    schema = 'gas'
    id = Column(Integer, primary_key=True)
    location = Column(String)
    scheduled_quantity = Column(Integer)
    design_capacity = Column(Integer)
    operating_capacity = Column(Integer)
    units = Column(String)
    date = Column(DateTime)
    desc = Column(String)
    cycle = Column(String)


def parse_date(date, date_format, time_zone):
    local = pytz.timezone('US/{}'.format(time_zone))
    naive = datetime.strptime(date, date_format)
    local_dt = local.localize(naive)
    utc = local_dt.astimezone(pytz.utc)
    return utc


def parse_int(num):
    if isinstance(num, str):
        return int(num.replace(',', ''))
    else:
        return int(num)


def scrape_iroquois():
    url = 'https://iol1.iroquois.com/infopost/classes/ip/capacity/OperationallyAvailableData.php'
    search_date = (datetime.now() - timedelta(days=1)).strftime('%m/%d/%Y')
    cycles = ['Timely', 'Evening', 'Intraday1', 'Intraday2', 'Intraday3']
    nominations = []
    for cycle in cycles:
        params = {'type': 'report', 'SearchDate': search_date, 
                'OACycleDesc': cycle, 'OALocation': 'All'}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        nominations.extend([Nomination(location=nom['Loc Name'],
                                  units = nom['Meas Basis Desc'],
                                  scheduled_quantity=parse_int(nom['Total Scheduled Quantity']),
                                  operating_capacity=parse_int(nom['Operating Capacity']),
                                  design_capacity=parse_int(nom['Design Capacity']),
                                  date = parse_date('{} {}'.format(nom['Posting Date'], nom['Posting Time']), 
                                                    '%m/%d/%Y %H:%M:%S %p', 
                                                    'Eastern'),
                                  desc = nom['Flow Ind Desc'],
                                  cycle = cycle)
                       for nom in resp_json])
    print('Nominations: {}'.format(len(nominations)))
    return nominations


def scrape_algonquin():
    print('scrape algonquin')
    url = 'https://rtba.spectraenergy.com/InformationalPosting/Default.aspx?bu=AG&Type=OA'
    resp = requests.post(url, data=algonquin_body())
    resp_json = resp.json()
    nominations = [Nomination(endpoint=nom['endpoint'],
                              mmbtu=nom['amount'],
                              date = datetime(nom['date']),
                              type = nom['type']) 
                   for nom in resp_json]
    return nominations


def insert_nominations():
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(USER, PASSWORD, HOST, PORT, DATABASE))
    print(Base.metadata)
    Nomination.metadata.create_all(engine)
    #engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    nominations = scrape_iroquois()
    try:
        session.bulk_save_objects(nominations)
        session.commit()
        print('Data added to DB')
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()

if __name__ == '__main__':
    insert_nominations()
