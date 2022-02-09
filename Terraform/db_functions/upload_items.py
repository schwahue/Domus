
import boto3

DDB_RESOURCE = boto3.resource("dynamodb", region_name="us-east-1")

table = DDB_RESOURCE.Table("listings")

table.put_item(
   Item={
        "address": "Yishun Ave 2 Block 166",
        "type": "HDB",
        "district": "Yishun"
    }
)

table.put_item(
   Item={
        "address": "40 Springside Link",
        "type": "HDB",
        "district": "Upper Thomson"
    }
)
