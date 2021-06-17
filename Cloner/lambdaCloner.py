import os
import boto3
import requests


args = ['Runtime','Role','Handler','Description','Timeout','MemorySize','Publish','VpcConfig','PackageType','DeadLetterConfig','Environment','KMSKeyArn','TracingConfig','Tags','Layers','FileSystemConfigs','ImageConfig','CodeSigningConfigArn']
lambda_client = boto3.client('lambda')
s3 = boto3.resource('s3')

# Creates s3 bucket tofacilitate code copy
def get_s3_bucket():
    s3.create_bucket(Bucket = 'lambda-code-py')
    print('default bucket created')
    return 'lambda-code-py'

#Fetches the details of lambda that are to be cloned
def get_lambda_details(lambda_name):
    try:
        function = lambda_client.get_function(FunctionName=lambda_name)
        return function
    except Exception as e:
        print(e)

#Upload the code of reference lambda to S3 bucket
def upload_code_to_s3(url,bucket_name,key_name):
    try:
        response = requests.get(url,stream = True)
        response = s3.Bucket(bucket_name).put_object(Key = key_name,Body = response.raw.read())
    except Exception as e:
        print(e)

# Creates a new lambda basis reference
def create_lambda(lambda_details,lambda_name,s3bucket):
    try:
        config= {}
        config['FunctionName'] = lambda_name
        upload_code_to_s3(lambda_details['Code']['Location'],s3bucket,'{}.zip'.format(lambda_name))
        config['Code'] = {'S3Bucket':s3bucket,'S3Key':'{}.zip'.format(lambda_name)}
        print(lambda_details['Configuration'].keys())
        for arg in  [arg for arg in args if arg in lambda_details['Configuration'].keys()]:
            config[arg] = lambda_details['Configuration'][arg]
        del config['VpcConfig']['VpcId']
        print(config)
        response = lambda_client.create_function(**config)
        return response
    except Exception as e:
        print(e)

#Destroys the code copy and the S3 Bucket post cloning
def clean_code_copy(bucket_name,lambda_name):
    bucket = s3.Bucket(bucket_name)
    s3.Object(bucket_name,'{}.zip'.format(lambda_name)).delete()
    if bucket_name == 'lambda-code-py':
        bucket.delete()
        print('default bucket deleted')
        

def clone_lambda(reference,clone_name,bucket_name = None):
    if not clone_name:
        clone_name = '{}_tmp'.format(reference)
    if not bucket_name:
        bucket_name = get_s3_bucket()
    details = get_lambda_details(reference)
    # print(details)
    cloned_lambda= create_lambda(details,clone_name,bucket_name) 
    print(cloned_lambda)
    # clean_code_copy(bucket_name,clone_name)

#Main Function
if __name__ == '__main__':
    clone_lambda('old_lambda','new_lambda')
