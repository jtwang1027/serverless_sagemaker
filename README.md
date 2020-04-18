# AWS AutoML model generation with scheduled retraining via AWS Cloudwatch and Lambda

**add Schematic here**

## AutoML (Autopilot)
Autopilot helps create classification and regression models without explicitly and defining feature types. Autopilot comes up with several "candidates pipelines", which consist of a data preprocessing step (with train-test split) and an inference model. After, hyperparameter optimization is run on each pipeline (>200 training job) aimed at minimizing the objective function (in this case validation rmse). For this case, I used the BACE dataset to predict drug pIC50, a quantiative metric of drug inhibition on the enzyme Bace1 enzyme [(link)](http://moleculenet.ai/datasets-1). 

add youtube link

In the video, I demonstrate how to use Autopilot using the AWS Sagemaker Studio, but the functionality can also be access via the low-level boto3 API [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.create_auto_ml_job), and allows you to specify other parameters (such as objective function, max number of candidates, max training job time).

### Configuration notes for inputting data into autopilot  
The data file needs to be a csv in s3. The csv file needs to have a header with column names, which you will use to specify the target column. Missing values are handled via various imputation methods in the preprocessing step. 

### Data pipeline
When the Autopilot experiment has concluded, the preprocessing (transform) job, training jobs, and hyperparameter tuning can be view inside jupyter notebook. 
![image](https://user-images.githubusercontent.com/46359281/79669499-ed4d7300-8189-11ea-8d99-609f234edb0a.png)

- selecting best model, model creation, deployment / batch transformation

## Setting up Cloudwatch and Lambda

### Lambda function breakdown
- handler event notification
- passing artifacts from previous model
- using environment variables as new parameters for new model

### Cloudwatch timer for triggering lambda function


### AWS Autopilot limitations
- requires CSV data
- slow even with small datasets
- typically requires (and defaults to) faster instance types for model training (including preprocessing, model selection, hyperparameter tuning)
- contrast with Ludwig and Google AutoML


### Helpful resources
- [AWS Sagemaker notebooks] (https://github.com/awslabs/amazon-sagemaker-examples) 
- Julien Simon 
- 
