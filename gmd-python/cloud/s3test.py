import boto3
from cloud import utils

if __name__=="__main__":

    utils.setproxy('proxyout.lanl.gov:8080')

    s3 = boto3.resource('s3')

    for b in s3.buckets.all():
        print(b.name)