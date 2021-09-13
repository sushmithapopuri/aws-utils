import boto3
import pandas as pd

client = boto3.client('glue')

response = client.get_job_runs(
    JobName='JobName',
    MaxResults=200
)
print(response)
df = pd.DataFrame(response['JobRuns'])
print(df.info())
print(df.head())
print(df)