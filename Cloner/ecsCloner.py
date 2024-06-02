import boto3

ecs_client = session.get    
existing_task_def_response = ecs_client.describe_task_definition(
    taskDefinition=ecs_task_definition_name,
)
new_task_definition = existing_task_def_response['taskDefinition']
#edit the image tag here
new_task_definition['containerDefinitions'][0]['image'] = yournewimagetagforexample

#drop all the keys from the dict that you can't use as kwargs in the next call. could be explicit here and map things
remove_args=['compatibilities', 'registeredAt', 'registeredBy', 'status', 'revision', 'taskDefinitionArn', 'requiresAttributes' ]
for arg in remove_args:
    new_task_definition.pop(arg)

reg_task_def_response = ecs_client.register_task_definition(
**new_task_definition
)
