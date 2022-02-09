import boto3
from boto3.dynamodb.conditions import Key, Attr

DOB_RESOURCE = boto3.resource("dynamodb", region_name="us-east-1")

address = "40 Springside Link"
table = DOB_RESOURCE.Table("listings")

response = table.query(
    KeyConditionExpression=Key("address").eq(address),
    ProjectionExpression="district"
)

items = response['Items']
print(items)