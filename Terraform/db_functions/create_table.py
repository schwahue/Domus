
import boto3
DDB_RESOURCE = boto3.resource("dynamodb", region_name="us-east-1")

DDB_RESOURCE.create_table(
    TableName="listings",
    KeySchema=[
        {
            "AttributeName": "address",
            "KeyType": "HASH"
        }
    ],
    AttributeDefinitions=[
        {
            "AttributeName": "address",
            "AttributeType": "S"
        }
    ],
    ProvisionedThroughput={
        "ReadCapacityUnits": 1,
        "WriteCapacityUnits": 1
    }
)
