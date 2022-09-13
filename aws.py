import boto3
import os

s3 = boto3.resource('s3')
bucket = s3.Bucket(os.getenv('BUCKET_NAME'))


def upload_file(file_name, object_name=None):
    if object_name is None:
        object_name = file_name
    bucket.upload_file(file_name, object_name)


def download_file(file_name, object_name=None):
    if object_name is None:
        object_name = file_name
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    bucket.download_file(object_name, file_name)


def upload_folder(folder_name):
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            upload_file(os.path.join(root, file))


def download_folder(folder_name):
    for obj in bucket.objects.filter(Prefix=folder_name):
        download_file(obj.key)


def sync_all():
    for obj in bucket.objects.all():
        download_file(obj.key)
