import boto3

def get_certificate(id):
    try:
        client = boto3.client('apigateway')
        cert_list = client.get_client_certificates()
        for cert in cert_list['items']:
            a = client.get_client_certificate(clientCertificateId = cert['clientCertificateId'])
            print(a)
        # print(cert_list)
    except Exception as e:
        print(e)

def get_layer(arn):
    try:
        client = boto3.client('lambda')
        response = client.get_layer_version_by_arn(Arn = arn)
        return response
    except Exception as e:
        print(e)

def get_lambda(lambda_name):
    try:
        client = boto3.client('lambda')
        function = client.get_function(FunctionName=lambda_name)
        return function
    except Exception as e:
        print(e)
#get_certificate('123')
# get_layer('layerName')
# get_lambda('LambdaName')