from multiprocessing import Pool
import boto3

s3 = boto3.resource('s3')
s3.meta.client.download_file(
    'salk-tm-shared',
    'prefix/hello.txt',
    '/tmp/hello.txt'
)