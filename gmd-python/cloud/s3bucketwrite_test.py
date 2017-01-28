
import boto3

from cloud import cloudutils

if __name__=='__main__':

    cloudutils.setproxy('proxyout.lanl.gov:8080')

    # Open s3 and write the test CSV file into the GMD bucket.
    s3_client = boto3.client('s3')

    # Upload the file to S3
    s3_client.upload_file('../supermag/supermag_test.csv', 'lanlytics', 'gmd/supermag.csv')
