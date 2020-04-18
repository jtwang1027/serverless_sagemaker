import boto3, os, datetime
#from sagemaker.model import Model

def lambda_handler(event, context):
    sm = boto3.client('sagemaker')
    
    date_appended=str(datetime.datetime.today()).replace(' ', '-').replace(':', '-').rsplit('.')[0]
    
    
    #transform job from best autopilot pipeline
    tfj=sm.describe_transform_job(TransformJobName='200413-bac-dpp1-rpb-1-ccde820d5f7b48438a9b53c6dab88e670e9da5e9f')
    
    
    #setting raw data source, and output path for transformed data
    tfj['TransformInput']['DataSource']['S3DataSource']['S3Uri']=os.environ['raw_data_s3_location']
    tfj['TransformOutput']['S3OutputPath']=os.environ['transformed_data_s3_location']
    tfj['TransformResources']={'InstanceType': os.environ['instance_type'],
                        'InstanceCount': int(os.environ['instance_count'])}
    
    
    print(tfj['TransformResources'])
    
    print('transform job starting:')
    
    tf_resp=sm.create_transform_job(
        
    #transform job name needs to be unique
    TransformJobName= 'boto3-dpp1-transformer'+ date_appended, 
        ModelName= tfj['ModelName'],
        TransformInput=tfj['TransformInput'],
        TransformOutput=tfj['TransformOutput'], 
        TransformResources= tfj['TransformResources']   
        )
    
    print(tf_resp)
    print('transform job completed:')
    
    

    if tf_resp: #if transform job is completed
        '''   if statement: this will prevent the training job from starting prematurely
    if the dir hasn't been created, you need the if statement, or else the interpreter
    will check if train/validation dir exists'''
    
    ##create new training job
    
        training_job_name = os.environ['old_training_job_name']
    
        sm = boto3.client('sagemaker')
        job = sm.describe_training_job(TrainingJobName=training_job_name)
    
        training_job_prefix = os.environ['training_job_prefix']
        training_job_name = training_job_prefix + date_appended
        
        
        #define input data for training job , same as output from batch transform job
        #batch transform preprocesses+ separates data into train + validation folders for the training model
        
        job['InputDataConfig'][0]['DataSource']['S3DataSource']['S3Uri']= os.environ['transformed_data_s3_location']+ 'train'
        job['InputDataConfig'][1]['DataSource']['S3DataSource']['S3Uri']= os.environ['transformed_data_s3_location'] +'validation'
        
        #output training job into same parent dir
        job['OutputDataConfig']['S3OutputPath']=os.environ['transformed_data_s3_location']+'training_job'
        
        
        #instance specification
        job['ResourceConfig']['InstanceType'] = os.environ['instance_type']
        job['ResourceConfig']['InstanceCount'] = int(os.environ['instance_count'])
        
        #spot training
        job['EnableManagedSpotTraining']= bool(os.environ['spot_training'])
        job['StoppingCondition']= { "MaxRuntimeInSeconds": 3500,"MaxWaitTimeInSeconds": 3500}
        
        
    
        print("Starting training job %s" % training_job_name)
        
        #you can't rewrite MetricDefinitions when specifying new job, so drop it 
        job['AlgorithmSpecification'].pop('MetricDefinitions',None)
    
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
        print('training job completed')
        
        
        ###creating model from new training job
        '''training_job_name='lambda-retrain2020-04-17-22-05-06'
        
        #grab configs from training job to feed into creating new model
        newtj=sm.describe_training_job(TrainingJobName=training_job_name)
        print(newtj['ModelArtifacts']['S3ModelArtifacts'])
        
        Model(
            name=newtj['TrainingJobName'],
            model_data=newtj['ModelArtifacts']['S3ModelArtifacts'],
            image=newtj['AlgorithmSpecification']['TrainingImage'],
            role= newtj['RoleArn'])'''
        
        
















