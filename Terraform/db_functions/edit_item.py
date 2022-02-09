import boto3

DDB_RESOURCE = boto3.resource("dynamodb", region_name="us-east-1")

table = DDB_RESOURCE.Table("listings")

address = "40 Springside Link"

table.update_item(
    Key={
        'address': address
    },
    UpdateExpression="set #type = :t",
    ExpressionAttributeValues={
        ":t": "Condominium"
    },
    ExpressionAttributeNames={
        "#type": "type"
    },
    ReturnValues="UPDATED_NEW"
)
