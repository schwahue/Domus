import boto3

client = boto3.client("dynamodb", region_name="us-east-1")

res = client.update_table(
    AttributeDefinitions=[
        {
            "AttributeName": "type",
            "AttributeType": "S"
        },
    ],
    TableName="listings",
    GlobalSecondaryIndexUpdates=[
        {
            'Create': {
                'IndexName': 'type_index',
                'KeySchema': [
                    {
                        'AttributeName': 'type',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            }
        }
    ]
)
