import json
import os
from groq import Groq

client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)


def lambda_handler(event, context):

    body = json.loads(event["body"])

    injury_text = body["text"]

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

Return JSON only with these fields:
- injury_name
- body_area
- symptoms
- possible_causes

Injury description:
{injury_text}
"""
            }
        ],
        temperature=0
    )

    return {
        "statusCode": 200,
        "body": response.choices[0].message.content
    }