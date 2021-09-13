import boto3

def get_certificate(id):
    client = boto3.client('apigateway')
    cert_list = client.get_client_certificates()
    for cert in cert_list['     ']:
        a = client.get_client_certificate(clientCertificateId = cert['clientCertificateId'])
        print(a)
    # print(cert_list)

get_certificate('123')