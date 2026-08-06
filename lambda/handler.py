import json
import boto3
import os
from datetime import datetime, timezone
import uuid
from groq import Groq


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "http://localhost:3000",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST"
}


MAX_TEXT_LENGTH = 5000


# DynamoDB setup
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(
    os.environ["DYNAMODB_TABLE"]
)


# GROQ setup
client = Groq(
    api_key=os.environ["GROQ_API_KEY"],
    timeout=15.0,
    max_retries=0
)


def lambda_handler(event, context):

    print("Lambda started")

    try:
        raw_body = event.get("body") if isinstance(event, dict) else None

        try:
            body = json.loads(raw_body) if isinstance(raw_body, str) else None
        except json.JSONDecodeError:
            body = None

        if (
            not isinstance(body, dict)
            or not isinstance(body.get("text"), str)
            or not body["text"].strip()
            or len(body["text"]) > MAX_TEXT_LENGTH
        ):
            return {
                "statusCode": 400,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "Invalid request body"}),
            }

        injury_text = body["text"]

        print("Processing injury extraction request")


        # Call GROQ
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract structured information from injury descriptions. "
                        "Return JSON only."
                    )
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
    "pain_level": null,
    "symptoms": [],
    "possible_causes": []
}}

Rules:
- Extract pain level as a number if it is mentioned.
- If pain level is not mentioned, return null.
- Keep symptoms as an array of strings.
- Keep possible causes as an array of strings.

Injury description:

{injury_text}
"""
                }
            ],
            temperature=0,
            max_tokens=500
        )


        # Convert GROQ response to dictionary
        extracted_data = json.loads(
            response.choices[0].message.content
        )


        required_fields = [
            "injury_name",
            "body_area",
            "pain_level",
            "symptoms",
            "possible_causes"
        ]


        if not all(field in extracted_data for field in required_fields):
            return {
                "statusCode": 502,
                "headers": CORS_HEADERS,
                "body": json.dumps({
                    "error": "Invalid AI response format"
                })
            }


        print("Extraction completed")


        # Prepare DynamoDB item
        item = {
            "userId": "test-user-001",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "entryId": str(uuid.uuid4()),

            "rawText": injury_text,

            "extractedData": extracted_data
        }


        print("Saving item to DynamoDB")


        # Save to DynamoDB
        table.put_item(
            Item=item
        )


        print("DynamoDB save completed")


        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps(extracted_data)
        }


    except Exception as e:

        print("ERROR:", str(e))

        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({
                "error": "Internal server error"
            })
        }
