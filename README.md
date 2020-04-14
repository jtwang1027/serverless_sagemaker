# AWS AutoML model generation with scheduled retraining via AWS Cloudwatch and Lambda

**add Schematic here**

## AutoML (Autopilot)
### Configuration
- data preprocessing, (must be a dataframe)
- Nan are OK
- save data in s3 bucket
- choose model type 



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
