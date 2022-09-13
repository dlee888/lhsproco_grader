import boto3
import os

s3 = boto3.resource('s3')
bucket = s3.Bucket(os.getenv('BUCKET_NAME'))


def upload_file(file_name: str, object_name=None):
    '''Upload file to s3'''
    if object_name is None:
        object_name = file_name
    bucket.upload_file(file_name, object_name)


def download_file(file_name: str, object_name=None):
    '''Download file from s3'''
    if object_name is None:
        object_name = file_name
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    bucket.download_file(object_name, file_name)


def upload_folder(folder_name: str):
    '''Upload folder to s3'''
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            upload_file(os.path.join(root, file))


def download_folder(folder_name: str):
    '''Download folder from s3'''
    for obj in bucket.objects.filter(Prefix=folder_name):
        download_file(obj.key)


def sync_all():
    '''Sync all files and folders. Downloads everything from s3'''
    for obj in bucket.objects.all():
        download_file(obj.key)
