import requests

from supermag.query import SupermagParams
from supermag.queryutils import StationParam
from supermag.queryutils import IntervalParam

from cloud import cloudutils

import boto3

from datetime import datetime, timedelta


if __name__=="__main__":

# Define the span of years and months: 1981-2015 are available.
    years = list(range(1981,1982))
    months = list(range(1,13))

# Define the storage bucket and folder in S3.
    s3bucketName = 'lanlytics/gmd'

# Set the proxy information for LANL and create an s3 client.
    cloudutils.setproxy('proxyout.lanl.gov:8080')
    s3 = boto3.resource('s3')

# Instatiate the parameter classes.
    sparam = StationParam()
    iparam = IntervalParam()

# Set up the station block sizes.
    stations = sparam.stations
    ns = len(stations)
    ind = list(range(0, ns, 100))
    ind.append(ns)


# Loop over years.
    for y in years:

        for m in months:
            startdate = datetime(day=1,month=m,year=y)
            start = startdate.isoformat()+'.000Z'
            print('start='+start)

            y2=y
            m2=m+1
            if m==12:
                m2=1
                y2=y+1
            enddate = datetime(day=1,month=m2,year=y2)
            interval = iparam.createIntervalString(startdate,enddate)
            print('interval='+interval)









