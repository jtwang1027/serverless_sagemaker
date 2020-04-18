# AWS AutoML model generation with scheduled retraining via AWS Cloudwatch and Lambda

**add Schematic here**

## AutoML (Autopilot)
Autopilot helps create classification and regression models without explicitly and defining feature types. Autopilot comes up with several "candidates pipelines", which consist of a data preprocessing step (with train-test split) and an inference model. After, hyperparameter optimization is run on each pipeline (>200 training job) aimed at minimizing the objective function (in this case validation rmse). For this case, I used the BACE dataset to predict drug pIC50, a quantiative metric of drug inhibition on the enzyme Bace1 enzyme [(link)](http://moleculenet.ai/datasets-1). 

add youtube link

In the video, I demonstrate how to use Autopilot using the AWS Sagemaker Studio, but the functionality can also be access via the low-level boto3 API [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.create_auto_ml_job), and allows you to specify other parameters (such as objective function, max number of candidates, max training job time).

### Configuration notes for inputting data into autopilot  
The data file needs to be a csv in s3. The csv file needs to have a header with column names, which you will use to specify the target column. Missing values are handled via various imputation methods in the preprocessing step. 

### Autopilot experiment output in Sagemaker Studio
When the Autopilot experiment has concluded, the preprocessing (transform) job, training jobs, and hyperparameter tuning can be view inside jupyter notebook. 
![image](https://user-images.githubusercontent.com/46359281/79669499-ed4d7300-8189-11ea-8d99-609f234edb0a.png)
In addition, there are 2 attached notebooks: 1) data exploration notebook (descriptive statistics on each feature) and 2) candidate generation notebook. The candidate generation notebook gives you complete code to rerun the entire analysis, and gives you insight into all the configurations used at each step, including details on each candidate pipeline. For example, you can see the methods used for imputating missing data, scaling features, and model use for training. These all have links to the source code.
![image](https://user-images.githubusercontent.com/46359281/79669603-aad86600-818a-11ea-924a-5bf68e9d9926.png)

### Autopilot pipeline setup and deployment
At the end of Autopilot, you will have a best *training job* from the hyperparameter tuning. This training job needs to not only be converted into a Sagemaker model, but also needs to be linked to the preprocessing/batch transform job that it accepted data from. This can be done in the *candidate generation notebook*, which has code cells for creating a data pipeline, which essentially links the preprocessing job + training job. This can also be done in the Sagemaker console (Create a model with 2 containers), but make sure you transfer all the environment variables from each job, and also add env variables recommmended in the candidate generation notebook. For example, my models needed the filetypes to be specified for the "transformer" (data preprocessing step) and estimator (xgboost model): 
![image](https://user-images.githubusercontent.com/46359281/79669916-29360780-818d-11ea-9b55-2bc08ce2fb50.png)


## Setting up Cloudwatch and Lambda
![image](https://user-images.githubusercontent.com/46359281/79670316-f7727000-818f-11ea-9def-befb14167245.png)
AWS Lambda functions let you run serverless applications with automatic scaling when triggered. These functions can also be triggered by a wide array of events. For example, you can add an HTTP API to directly trigger lambda functions. Here, I've used *Cloudwatch* to trigger the lambda function on a scheduled basis for serverless, automated model training. 

### Lambda function for model retraining
The lambda function code can be found in *handler.py* (python 3.6).

- passing artifacts from previous model
- using environment variables as new parameters for new model


### Using Lambda layers to provide python modules

### AWS Autopilot limitations
- requires CSV data
- slow even with small datasets
- typically requires (and defaults to) faster instance types for model training (including preprocessing, model selection, hyperparameter tuning)
- contrast with Ludwig and Google AutoML


### Helpful resources
- [AWS Sagemaker notebooks] (https://github.com/awslabs/amazon-sagemaker-examples) 
- Julien Simon 
- 
