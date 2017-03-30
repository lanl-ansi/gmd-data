from magneto_api.dbconnect import DBConnector
from magneto_api import queries

if __name__=="__main__":

    # Test basic SQL query.
    dbconnector = DBConnector()
    queryString = "select * from magneto.stations"
    rs = queries.query_magneto(dbconnector,queryString)

    for row in rs:
        print(row)

