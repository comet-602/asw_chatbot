'''
用boto3 操作s3

創造客戶端
使用客戶端上傳object
使用客戶端下載object
使用客戶端刪除object

'''

import boto3
s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIAR4NDUH53GWDLQFNM',
    aws_secret_access_key='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'
)

# # 使用客戶端上傳object
# # boto3 upload object to s3 bucket
# # google ~
# # response = s3_client.upload_file(file_name, bucket, object_name)
# response = s3_client.upload_file('Pipfile', 'iii-tutorial-v2', 'student21/lbh_is_good')


# # 使用客戶端下載object
# # boto3 download object to s3 bucket
# # google ~
# # s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')
# s3_client.download_file('iii-tutorial-v2', 'student21/lbh_is_good', 'lbh_is_very_good')

# # 使用客戶端刪除object
# # boto3 delete object to s3 bucket
# # google ~
# # s3_client.delete_object(Bucket='examplebucket',Key='objectkey.jpg')
# s3_client.delete_object(Bucket='iii-tutorial-v2',Key='student21/lbh_is_good')


