import boto3

LAMBDA_CLIENT = boto3.client("lambda")

result = LAMBDA_CLIENT.create_function(
    Code={"S3Bucket": "cpassignment1","S3Key": "website_api_code.zip"},
    Description="Amazing property website",
    FunctionName="PropertySearch",
    Handler="query_property.handler",
    MemorySize=128,
    Publish=True,
    Role="arn:aws:iam::176285793019:role/LabRole",
   	Runtime="python3.7",
   	Timeout=30
)
print(result)