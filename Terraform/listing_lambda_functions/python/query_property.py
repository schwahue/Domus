import boto3, sys

DYNAMODB_CLIENT = boto3.client("dynamodb", region_name="us-east-1")

def my_init(event):
    if (event == None):
        typeOfProp=sys.argv[1]
    else:
        typeOfProp=event["type_str"]
    if (typeOfProp=="All"):
        return scanTable()
    else:
        return queryIndex(typeOfProp)

def queryIndex(typeOfProp):
    response = DYNAMODB_CLIENT.query(
        TableName="listings",
        IndexName="type_index",
        ExpressionAttributeValues={":type":{"S":typeOfProp}},
        KeyConditionExpression="#type = :type",
        ExpressionAttributeNames={
        "#type": "type"
        }
    )
    print(response["Items"]) # for testing in Cloud9 console
    return response["Items"]

def scanTable():
    response = DYNAMODB_CLIENT.scan(
        TableName="listings"
    )
    print(response["Items"]) # for testing in Cloud9 console
    return response["Items"]


def handler(event, context):
    print("Running as a script in Lambda")
    return my_init(event)

if __name__ == "__main__":
    print("Running as a script in Cloud9")
    my_init(None)
