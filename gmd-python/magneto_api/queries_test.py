from magneto_api.dbconnect import DBConnector
from magneto_api import queries
from magneto_api.queries import *

from datetime import *

if __name__=="__main__":

    # Test basic SQL query.
    dbconnector = DBConnector()
    # queryString = "select * from magneto.stations"
    # rs = queries.query_magneto(dbconnector,queryString)
    #
    # for row in rs:
    #     print(row)

    # test_stations = [\
		# 	"A02","A03","A04","A05","A06","A07",\
		# 	"A08","A09","A10","A11"]
    test_stations = ['AAE'];

    initial_timestamp = datetime(2001,10,2,18,0,0) # "2001-10-02 18:00:00"
    final_timestamp = datetime(2001,10,2,18,1,0)# "2001-10-02 18:01:00"

    minlon=-166.03
    minlat=59.59
    maxlon=-141.90
    maxlat=70.88; # Alaska
    min_coord = queries.Coordinate(minlon,minlat)
    max_coord = queries.Coordinate(maxlon,maxlat)


    filter = MeasurementFilter()
    filter.add_station_ids(test_stations)
    filter.set_coordinate_range(min_coord,max_coord)
    filter.set_timestamp_range(initial_timestamp,final_timestamp)

    rs = filter_measurements(dbconnector,filter)

    for row in rs:
        print(row)




