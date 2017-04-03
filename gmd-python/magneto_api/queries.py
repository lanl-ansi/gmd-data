from datetime import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import and_


class SchemaDescription:
    table_names = ["stations", "measurements"]
    station_fields = {"iaga":"character","glon":"double","glat":"double","mlon":"double",\
                      "mlat":"double","station_name":"character"}
    measurement_fields = {"date_utc":"timestamp","iaga":"character","mlt":"double","mlat":"double",\
                          "n":"double","e":"double","z":"double","collection":"character"}

class CoordinateType:
    GEOGRAPHIC = 0
    MAGNETIC = 1

class Coordinate:
    def __init__(self,x,y):
        self.x = x
        self.y = y

# Timestamp range is given in python datetime.datetime instances.
class MeasurementFilter:
    def __init__(self):
        self.station_ids = []
        self.timestamp_range = []
        self.coordinate_range = []
        self.coordinate_type = CoordinateType.GEOGRAPHIC

    def add_station_ids(self,station_ids):
        for id in station_ids:
            self.station_ids.append(id)

    def set_timestamp_range(self,min_timestamp,max_timestamp):
        self.timestamp_range = []
        self.timestamp_range.append(min_timestamp)
        self.timestamp_range.append(max_timestamp)

    def set_coordinate_range(self,mincoord,maxcoord):
        self.coordinate_range = []
        self.coordinate_range.append(mincoord)
        self.coordinate_range.append(maxcoord)

    def set_coordinate_type(self,coordtype):
        self.coordinate_type = coordtype


def get_station_field_names():
    return list(SchemaDescription.station_fields.keys())

def get_station_field_types():
    return list(SchemaDescription.station_fields.values())

def get_measurement_field_names():
    return list(SchemaDescription.measurement_fields.keys())

def get_measurement_field_types():
    return list(SchemaDescription.measurement_fields.values())

def query_magneto(dbconnector, queryString):
    conn = dbconnector.engine.connect()
    rs = conn.execute(queryString)
    return rs

def get_stations(dbconnector):
    Station =dbconnector.Station
    stations = {}
    for station in dbconnector.session.query(Station).order_by(Station.iaga):
        stations[station.iaga] = station
    return stations

def get_stations_by_geocoords(dbconnector,minlon,minlat,maxlon,maxlat):
    Station =dbconnector.Station
    stations = {}
    for station in dbconnector.session.query(Station)\
            .filter(and_(Station.glon>=minlon,Station.glat>=minlat,Station.glon<=maxlon,Station.glat<=maxlat))\
            .order_by(Station.iaga):
        station.glon = station.glon
        stations[station.iaga] = station
    return stations

def get_stations_by_magcoords(dbconnector,minlon,minlat,maxlon,maxlat):
    # Do these longitudes require a shift?
    Station =dbconnector.Station
    stations = {}
    for station in dbconnector.session.query(Station)\
            .filter(and_(Station.mlon>=minlon,Station.mlat>=minlat,Station.mlon<=maxlon,Station.mlat<=maxlat))\
            .order_by(Station.iaga):
        stations[station.iaga] = station
    return stations

def filter_measurements(dbconnector,filter):
    station_ids = filter.station_ids
    timestamp_range = filter.timestamp_range
    coordinate_range = filter.coordinate_range
    coordinate_type = filter.coordinate_type

    # Station ID set.
    station_set = set()

    # Add existing station IDs to the set.
    for station_id in station_ids:
        station_set.add(station_id)

    stations = None
    # If the coordinate range is not empty, query for stations in the coordinate range.
    if len(coordinate_range)>0:
        minlon = coordinate_range[0].x
        minlat = coordinate_range[0].y
        maxlon = coordinate_range[1].x
        maxlat = coordinate_range[1].y
        if coordinate_type == CoordinateType.GEOGRAPHIC:
            # Use geographic coordinates.
            stations = get_stations_by_geocoords(dbconnector,minlon,minlat,maxlon,maxlat)
        if coordinate_type == CoordinateType.MAGNETIC:
            # Use magnetic coordinates.
            stations = get_stations_by_magcoords(dbconnector,minlon,minlat,maxlon,maxlat)
    # Add stations in the range to the set.
    if stations!=None:
        key_list = stations.keys()
        for key in key_list:
            station_set.add(key)

    # Create a string-based query,filter based on the station set.
    query_string = "select * from magneto.measurements where "
    station_id_list = list(station_set)
    # If there are stations to be named.
    if len(station_id_list)>0:
        query_string = query_string+ "iaga = any(array['"+station_id_list[0]
        for i in range(1,len(station_id_list)):
            query_string = query_string+"','" + station_id_list[i]
        query_string = query_string+"'])"

    #Append the timestamp range if any.
    if len(timestamp_range)>0:

        query_string = query_string+" and "
        query_string = query_string+ "date_utc >= '" + str(timestamp_range[0]) \
                + "' and date_utc <= '" + str(timestamp_range[1]) + "'"

    # Perform the query and return the measurements.
    query_string = query_string + " order by date_utc"
    rs = query_magneto(dbconnector,query_string)
    return rs


