import requests

from supermag.query import SupermagParams
from supermag.queryutils import StationParam, IntervalParam

from datetime import datetime


if __name__=="__main__":

    startdate = datetime(day=1,month=1,year=2000)
    enddate = datetime(day=2,month=1,hour=1,year=2000)

    sparam = StationParam()
    stations = sparam.stations
    ns = len(stations)
    ind = list(range(0,ns,100))
    ind.append(ns)
    print(ind)

    iparam = IntervalParam()
    interval = iparam.createIntervalString(startdate,enddate)
    startparam = startdate.isoformat() + '.000Z'

    filename = './supermag_test.csv'
    newline ='\n'
    header = 'Date_UTC,IAGA,MLT,MLAT,N,E,Z'

    with open(filename, 'wb') as fd:
        fd.write(header.encode())
        fd.write(newline.encode())
        for i in range(0,len(ind)-1):
            print('stations '+str(ind[i])+':'+str(ind[i+1]-1))
            sstations = sparam.createStationString(ind[i],ind[i+1]-1)

            p = SupermagParams(startparam, interval, sstations)
            pdict = p.createParamsDict()

            print("params=" + str(pdict))

            r = requests.get(p.host, proxies=p.proxydict, params=pdict, stream=True)
            print("Status="+str(r.status_code))
            print(dict(r.headers))

            first = True
            for line in r.iter_lines():
                if first:
                    first=False
                else:
                    print(line)
                    fd.write(line)
                    fd.write(newline.encode())
    fd.close()

