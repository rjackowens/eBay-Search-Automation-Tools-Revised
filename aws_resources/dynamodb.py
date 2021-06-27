import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

dynamo_db = boto3.resource("dynamodb")
# dynamo_table = dynamo_db.Table("ebay_items")


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
            print(f"Table {table_name} already exists")

    else:
        return table


def add_single_item(table="ebay_watches", title=None,
                    price="", time_stamp="",
                    brand="", reference="", metal=""):
    """Adds entry to DynamoDB table"""

    dynamo_table = dynamo_db.Table(table)

    dynamo_table.put_item(

        Item={
            "title": title,
            "price": str(price),
            "date_added": time_stamp,
            "brand": brand,
            "reference": reference,
            "metal": metal
            # "date": date
        }

    )

# add_single_item("ebay_watches", title="Test", price="50", time_stamp="6-26-2021", brand="Test", reference="Test", metal="Gold")


def get_single_item(title, table="ebay_watches"):
    """Retrieves entry from DynamoDB table"""

    dynamo_table = dynamo_db.Table(table)

    try:
        response = dynamo_table.get_item(Key={'title': title})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']

# result = get_single_item("Cartier Tank").get("title")
# print(result)


def get_item_by_attr(_attr="Omega Speedmaster", table="ebay_watches"):
    """Retrieves entry from DynamoDB table matching attribute filter"""

    dynamo_table = dynamo_db.Table(table)

    try:
        response = dynamo_table.query(KeyConditionExpression=Key('title').eq(_attr))
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Items']

# print(get_item_by_attr(_attr="Cartier Tank"))

# if (get_item_by_attr(_attr="Estate 3.00ct Diamond 14k Yellow Gold Omega Style Necklace")) == []:
#     print("not found!")


def get_all_items(table="ebay_watches"):
    """Retrieves all entries from DynamoDB using scan"""

    dynamo_table = dynamo_db.Table(table)

    response = dynamo_table.scan(FilterExpression="attribute_exists(title) AND attribute_exists(price)")
    return response["Items"]

# all_items = get_all_items()

# for x in all_items:
#     print(x)