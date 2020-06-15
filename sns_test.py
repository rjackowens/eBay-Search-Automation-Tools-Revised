import boto3
from config import phone_number

def send_text_message(message_body):
    """Send text message via SNS"""

    sns = boto3.client("sns", region_name="us-east-1")
    response = sns.publish(
        PhoneNumber=phone_number,
        Message=message_body
        )
    return response

# send_text_message("Jack is cool")
