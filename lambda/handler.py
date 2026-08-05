import json


def lambda_handler(event, context):

    body = json.loads(event["body"])

    injury_text = body["text"]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Lambda is working",
            "received_text": injury_text
        })
    }