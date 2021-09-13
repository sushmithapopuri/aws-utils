import boto3
import json

args = ['Runtime','Role','Handler','Description','Timeout','MemorySize','Publish','VpcConfig','PackageType','DeadLetterConfig','Environment','KMSKeyArn','TracingConfig','Tags','FileSystemConfigs','ImageConfig','CodeSigningConfigArn']
lambda_client = boto3.client('lambda')
s3 = boto3.resource('s3')

def get_lambda_details(lambda_name):
    rej_list = []
    try:
        function = lambda_client.get_function(FunctionName=lambda_name)
        # print (function)
        return function,rej_list
    except Exception as e:
        print(e)
        rej_list.append(lambda_name)
        return {},rej_list

# lambda_details = []
lambdas = ['lambdaName']

# with open('lambdas.json','w+') as f:
#     for lmda in lambdas:
#         # lambda_details.append()
#         fn,rej = get_lambda_details(lmda)
#         f.write(json.dumps(fn, default=lambda o: o.__dict__, sort_keys=True, indent=2))

fn,rej = get_lambda_details(lambdas[0])
print(json.dumps(fn, default=lambda o: o.__dict__, sort_keys=True, indent=2))
print(rej)
