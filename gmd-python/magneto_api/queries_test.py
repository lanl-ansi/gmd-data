from magneto_api.dbconnect import DBConnector
from magneto_api import queries
from magneto_api.queries import *

from datetime import *

if __name__=="__main__":

    # Test a typical filtered query.
    dbconnector = DBConnector()

    stations = get_stations(dbconnector)
    keys = sorted(list(stations.keys()))
    for key in keys:
        station = stations[key]
        print(station.iaga+","+str(station.glon)+","+str(station.glat)+","+station.station_name)

    test_stations = ['AAE'];

    initial_timestamp = datetime(2001,10,2,18,0,0) # "2001-10-02 18:00:00"
    final_timestamp = datetime(2001,10,2,18,1,0)# "2001-10-02 18:01:00"

    minlon=-166.03
    minlat=59.59
    maxlon=-141.90
    maxlat=70.88; # Alaska
    min_coord = Coordinate(minlon,minlat)
    max_coord = Coordinate(maxlon,maxlat)


    filter = MeasurementFilter()
    filter.add_measurement_option(MeasurementOption.E)
    filter.add_station_ids(test_stations)
    filter.set_coordinate_range(min_coord,max_coord)
    filter.set_coordinate_type(CoordinateType.GEOGRAPHIC)
    filter.set_timestamp_range(initial_timestamp,final_timestamp)

    rs = filter_measurements(dbconnector,filter)

    for row in rs:
        print(row)




