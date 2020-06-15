import boto3
from botocore.exceptions import ClientError

def create_table(table_name=None):
    """Creates new DynamoDB table

    Args:
        table_name: Name of new DynamoDB table. Cannot contain spaces.

    """

    dynamo_db = boto3.resource("dynamodb")

    try:
        table = dynamo_db.create_table(
            TableName=table_name.replace(" ", ""),
            KeySchema=[
                {
                    'AttributeName': 'title',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

    except ClientError as e:
        if e.response['Error']['Code'] == "ResourceInUseException":
            print("Table already exists")

    else:
        return table

print(create_table(table_name="Jaeger LeCoultre"))
