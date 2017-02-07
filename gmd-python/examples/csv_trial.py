import csv
stationsfile = '../../data/supermag_stations.csv'
measurementsfile = '../../data/supermag-2000-01-01T00-00-00.csv'

if __name__=='__main__':
    with open(stationsfile) as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
    f.close()

    with open(measurementsfile) as f:
        reader = csv.reader(f)
        for i in range(0,20):
            row = reader.__next__()
            print(row)
    f.close()
