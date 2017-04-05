# Presumes that the stations and measurements tables have been instantiated, and that the stations table is populated.
import sys
sys.path.append('.')

from cloud import cloudutils

import boto3

from  datetime import datetime

from magneto.dbsettings_RESTRICTED import *

from magneto import magneto_measurements


if __name__=="__main__":
    # Define the storage bucket and folder in S3.
    s3bucketName = 'lanlytics/gmd'

    # Set the LANL flag: True for LANL False for AWS.
    LANL = False

    # Set the proxy information for LANL.
    if LANL:
        cloudutils.setproxy('proxyout.lanl.gov:8080')

    # Obtain an s3 client
    s3client = boto3.client('s3')

    # Obtain an s3 resource
    s3 = boto3.resource('s3')


    # List all the files in the bucket.
    bucket = s3.Bucket('lanlytics')
    objects = bucket.objects.filter(Prefix='gmd/supermag-200')
    filelist = []
    for object in objects:
        print(object.key)
        filelist.append(object.key)
    print(str(len(filelist))+' file objects to import.')

    # Get the start time.
    t1 = datetime.now()
    print('start:'+str(t1))

    # Configure the database uri:
    db_uri='postgresql://{}:{}@{}:{}/{}'.format(write_user, write_user_passwd, host, port, db)

    for file in filelist:
        # Download the file to tmp.csv
        bucket.download_file(file,'tmp.csv')

        # Add the records to the database.
        print('Importing downloaded measurements file '+file+' to database.')
        magneto_measurements.insert_measurements('tmp.csv',db_uri)

    # Get the end time and the delta.
    t2 = datetime.now()
    print('start:'+str(t1)+', end:'+str(t2)+', interval:'+str(t2-t1))






