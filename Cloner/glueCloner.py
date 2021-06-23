import os
import boto3
import requests

args = ['Description', 'LogUri', 'Role', 'ExecutionProperty', 'Command', 'DefaultArguments', 'NonOverridableArguments', 'Connections', 'MaxRetries', 'Timeout', 'SecurityConfiguration', 'Tags', 'NotificationProperty', 'GlueVersion', 'NumberOfWorkers', 'WorkerType']
client = boto3.client('glue')
s3 = boto3.resource('s3')

#Upload the code of reference lambda to S3 bucket
def upload_code_to_s3(url,clone_name):

    try:
        bucket_name = url.split('/')[2]
        key_name = '/'.join(url.split('/')[3:])
        if not clone_name: 
            clone_name = key_name.replace('.py','_tmp.py')
        source = {'Bucket' : bucket_name, 'Key' : key_name}
        s3.Object(bucket_name,'{}.py'.format(clone_name)).copy_from(CopySource=source)
        return url.replace(key_name,'{}.py'.format(clone_name))
    except Exception as e:
        print(e)

#Fetches the details of glue that are to be cloned
def get_glue_details(glue_name):
    try:
        print(glue_name)
        function = client.get_job(JobName=glue_name)
        print(function)
        return function
    except Exception as e:
        print(e)

# Creates a new glue job basis reference
def create_glue(details,name):
    try:
        config= {}
        config['Name'] = name
        for arg in [arg for arg in args if arg in details['Job'].keys()]:
            config[arg] = details['Job'][arg]
        config['Command']['ScriptLocation'] =upload_code_to_s3(details['Job']['Command']['ScriptLocation'],name) 
        response = client.create_job(**config)
        return response
    except Exception as e:
        print(e)

def clone_glue(reference,clone_name):
    if not clone_name:
        clone_name = '{}_tmp'.format(reference)
    details = get_glue_details(reference)
    cloned_glue= create_glue(details,clone_name) 
    print(cloned_glue)

#Main Function
if __name__ == '__main__':
    clone_glue('Old_Glue_Job','New_Glue_Job')
    # print(response)
