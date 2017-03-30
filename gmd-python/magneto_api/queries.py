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
    # Note: This query include a shift to SuperMag longitude values in the range [0,360]
	# instead of [-180,180]. The transformation requires adding 360 degrees to longitude.
    minlonc = minlon +360
    maxlonc = maxlon +360

    Station =dbconnector.Station
    stations = {}
    for station in dbconnector.session.query(Station)\
            .filter(and_(Station.glon>=minlonc,Station.glat>=minlat,Station.glon<=maxlonc,Station.glat<=maxlat))\
            .order_by(Station.iaga):
        station.glon = station.glon -360
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
    for s in station_ids:
        station_set.add(s)

    # TODO ..........................................
    # If the coordinate range is not empty query for stations in the coordinate range.
    # Add stations in the range to the set.

    # Create a query based on the station set and append the timestamp range query.

    # Perform the query and return the measurements.


