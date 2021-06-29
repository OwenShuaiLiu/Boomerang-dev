import boto3
from boto3.s3.transfer import S3Transfer
import os
import json


credentials = { 
    'aws_access_key_id': "AKIAJHBPS7RSRXDE5YZA",
    'aws_secret_access_key': "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"
}

BUCKET_NAME = 'brand-product-image'
FILE_PATH = "./data/images/cal-shirt/"

# get name of the iamges
arr = os.listdir('./data/images/cal-shirt')
print(arr)


client = boto3.client('s3', 'us-west-2', **credentials)
transfer = S3Transfer(client)

mimetype = 'image/jpeg' # you can programmatically get mimetype using the `mimetypes` module

# upload the image and return a url
def image_upload(FILE_NAME, BUCKET_NAME, KEY):
    transfer.upload_file(FILE_NAME, BUCKET_NAME, KEY,
                        extra_args={'ACL': 'public-read', "ContentType": mimetype})
    file_url = '%s/%s/%s' % (client.meta.endpoint_url, BUCKET_NAME, KEY)

    return file_url


#upload all iamges and return a list of url
img_url_list = []
for key in arr:
    url_temp = {}
    file_name = FILE_PATH + key
    img_url = image_upload(file_name, BUCKET_NAME, key)
    url_temp["src"] = str(img_url)
    img_url_list.append(url_temp)

img_url_list = json.dumps(img_url_list)
print(img_url_list)

