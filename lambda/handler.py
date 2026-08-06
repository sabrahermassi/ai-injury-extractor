import json
import boto3
import os
from datetime import datetime, timezone
import uuid
from groq import Groq


# DynamoDB setup
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(
    os.environ["DYNAMODB_TABLE"]
)


# GROQ setup
client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)


def lambda_handler(event, context):

    print("Lambda started")

    try:
        body = json.loads(event["body"])

        injury_text = body["text"]

        print("Received text:", injury_text)


        # Call GROQ
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You extract structured information from injury descriptions. Return JSON only."
                },
                {
                    "role": "user",
                    "content": f"""
Analyze this injury description and extract structured information.

Return ONLY valid JSON.
Do not use markdown.
Do not wrap the JSON in ```.

Schema:

{{
    "injury_name": "",
    "body_area": "",
    "symptoms": [],
    "possible_causes": []
}}

Injury description:

{injury_text}
"""
                }
            ],
            temperature=0
        )


        # Convert GROQ response to dictionary
        extracted_data = json.loads(
            response.choices[0].message.content
        )

        print("Extracted data:", extracted_data)


        # Prepare DynamoDB item
        item = {
            "userId": "test-user-001",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "entryId": str(uuid.uuid4()),

            "rawText": injury_text,

            "extractedData": extracted_data
        }


        print("Saving item:", item)


        # Save to DynamoDB
        dynamodb_response = table.put_item(
            Item=item
        )


        print(
            "DynamoDB response:",
            dynamodb_response
        )


        return {
            "statusCode": 200,
            "body": json.dumps(extracted_data)
        }


    except Exception as e:

        print("ERROR:", str(e))

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }