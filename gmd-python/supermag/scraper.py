import requests

from supermag.query import SupermagParams
from supermag.queryutils import StationParam
from supermag.queryutils import IntervalParam

from cloud import cloudutils

import boto3

from datetime import datetime, timedelta


if __name__=="__main__":

# Define the span of years and months: 1981-2015 are available.
    #years = list(range(1981, 2016))
    years = list(range(1986,1987))
    months = list(range(6,7))
    #months = list(range(1,2))

# Define the storage bucket and folder in S3.
    s3bucketName = 'lanlytics/gmd'

# Set the proxy information for LANL and create an s3 client.
    cloudutils.setproxy('proxyout.lanl.gov:8080')
    #s3 = boto3.resource('s3')
    s3client = boto3.client('s3')

# Instatiate the parameter classes.
    sparam = StationParam()
    iparam = IntervalParam()

# Set up the station block sizes.
    stations = sparam.stations
    ns = len(stations)
    ind = list(range(0, ns, 100))
    ind.append(ns)

    newline = '\n'
    header = 'Date_UTC,IAGA,MLT,MLAT,N,E,Z'
    stations = sparam.stations
    ns = len(stations)
    ind = list(range(0, ns, 100))
    ind.append(ns)
    print(ind)


# Loop over years.
    for y in years:

        for m in months:
            startdate = datetime(day=1,month=m,year=y)
            start = startdate.isoformat()+'.000Z'
            print('start='+start)
            filename = '../tmp.csv'
            storage_name = 'supermag-'+startdate.isoformat()+'.csv'

            y2=y
            m2=m+1
            if m==12:
                m2=1
                y2=y+1
            enddate = datetime(day=1,month=m2,year=y2)
            interval = iparam.createIntervalString(startdate,enddate)
            print('interval='+interval)

            with open(filename, 'wb') as fd:
                fd.write(header.encode())
                fd.write(newline.encode())
                for i in range(0, len(ind) - 1):
                    print('stations ' + str(ind[i]) + ':' + str(ind[i + 1] - 1))
                    sstations = sparam.createStationString(ind[i], ind[i + 1] - 1)

                    p = SupermagParams(start, interval, sstations)
                    pdict = p.createParamsDict()
                    print("params=" + str(pdict))

                    r = requests.get(p.host, proxies=p.proxydict, params=pdict, stream=True)
                    print("Status=" + str(r.status_code))
                    print(dict(r.headers))

                    first = True
                    for line in r.iter_lines():
                        if first:
                            first = False
                        else:
                            #print(line)
                            fd.write(line)
                            fd.write(newline.encode())
                fd.close()
                print(filename+' written to local storage.')
                s3client.upload_file('../tmp.csv', 'lanlytics', 'gmd/'+storage_name)
                print(storage_name+' written to s3.')











