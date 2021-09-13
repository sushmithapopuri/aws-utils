import boto3
import json
import pandas as pd

client = boto3.client('glue')

def get_glue_details(glue_name):
    try:
        # function = client.get_job(JobName=glue_name)
        function = client.get_job_runs(JobName=glue_name)
        # print(function['JobRuns'][0].keys())
        return function['JobRuns']
    except Exception as e:
        print(e)

jobs = ['JobName']

# with open('jobs.json','w+') as f:
for lmda in jobs:
    # lambda_details.append()
    fn = get_glue_details(lmda)
    print(type(fn))
    df = pd.DataFrame.from_dict(fn)
    df.to_csv('jobs.csv')
        # for k,v in fn.items():
        #     fn[k] = fn[str(v)]
        # f.write(json.dumps(fn))