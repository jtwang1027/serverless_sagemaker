import boto3, os, datetime

def lambda_handler(event, context):

    training_job_name = os.environ['training_job_name']

    sm = boto3.client('sagemaker')
    job = sm.describe_training_job(TrainingJobName=training_job_name)

    training_job_prefix = os.environ['training_job_prefix']
    training_job_name = training_job_prefix+str(datetime.datetime.today()).replace(' ', '-').replace(':', '-').rsplit('.')[0]
    #job['ResourceConfig']['InstanceType'] = os.environ['instance_type']
    #job['ResourceConfig']['InstanceCount'] = int(os.environ['instance_count'])

    print("Starting training job %s" % training_job_name)
    
    #you can't rewrite MetricDefinitions when specifying new job, so drop it 
    job['AlgorithmSpecification'].pop('MetricDefinitions',None)
    
    if 'VpcConfig' in job:
        
        resp = sm.create_training_job(
            TrainingJobName=training_job_name, AlgorithmSpecification=job['AlgorithmSpecification'], RoleArn=job['RoleArn'],
            InputDataConfig=job['InputDataConfig'], OutputDataConfig=job['OutputDataConfig'],
            ResourceConfig=job['ResourceConfig'],   VpcConfig=job['VpcConfig']
           )
    else:
        # Because VpcConfig cannot be empty like HyperParameters or Tags :-/
        #this is the option that gets used
        resp = sm.create_training_job(
            TrainingJobName=training_job_name, AlgorithmSpecification=job['AlgorithmSpecification'], RoleArn=job['RoleArn'],
            InputDataConfig=job['InputDataConfig'], OutputDataConfig=job['OutputDataConfig'],
            ResourceConfig=job['ResourceConfig'], StoppingCondition=job['StoppingCondition'],
            EnableManagedSpotTraining=job['EnableManagedSpotTraining'],
             HyperParameters=job['HyperParameters'] if 'HyperParameters' in job else {},
            Tags=job['Tags'] if 'Tags' in job else [])

    print(resp)
