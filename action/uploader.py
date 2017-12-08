import boto3
import os
import datetime

from action.env_getter import getVariable

def uploadImageUser(file_image):
    s3 = boto3.client('s3')
    fileName = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '.jpg'

    output = os.path.join("/tmp/", fileName)
    with open(output, "wb") as file:
        file.write(file_image.read())

    print(file_image)
    s3BucketPath = getVariable('s3BucketPath')
    s3BucketName = getVariable('s3BucketName')
    filePathS3 = fileName
    completePath = s3BucketPath + filePathS3
    s3.upload_file('/tmp/' + fileName, s3BucketName, filePathS3)

    return completePath