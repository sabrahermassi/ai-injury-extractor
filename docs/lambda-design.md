# Lambda Function Design

## Overview

The AI Injury Extractor uses AWS Lambda as the serverless backend processing layer.

The Lambda function receives injury descriptions from the frontend, uses the Groq API to extract structured injury information, stores entries in DynamoDB, and returns responses to the client.

---

## Integration Note

This repository focuses on the AI extraction service and serverless infrastructure.

Authentication, user management, and full injury tracking workflows are handled by the consuming application.

---

# Lambda Function

## Function Name

`injury-extractor`

## Purpose

Convert unstructured injury journal text into structured injury data using an LLM.

Example input:

> "I hurt my left knee doing squats two weeks ago. Pain is 6/10."

Example output:

```json
{
  "injury_name": "Knee injury",
  "body_area": "left knee",
  "pain_level": 6,
  "symptoms": ["pain during exercise"],
  "possible_causes": ["squats"]
}
```

---

# High-Level Flow

```text
Frontend
 |
 | POST /extract
 ↓
API Gateway
 |
 ↓
Lambda
 |
 |-- Validate input
 |
 |-- Call Groq API
 |
 |-- Parse AI response
 |
 |-- Store injury entry
 ↓
DynamoDB


Frontend
 |
 | GET /injuries
 ↓
API Gateway
 |
 ↓
Lambda
 |
 |-- Retrieve injury history
 ↓
DynamoDB
 |
 ↓
Return injury history
```

---

# Lambda Processing Steps

## 1. Receive Request

The Lambda function receives an HTTP request from API Gateway.

Example request:

```json
{
  "text": "I hurt my left knee doing squats two weeks ago. Pain is 6/10."
}
```

---

## 2. Validate Input

Before processing:

- Check that injury text exists
- Check that the input is not empty
- Validate request format
- Enforce maximum input length

Invalid requests return an error response.

Example:

```json
{
  "error": "Invalid request body"
}
```

---

## 3. Call Groq API

Lambda sends the injury description to Groq with instructions to extract structured information.

The LLM converts unstructured text into JSON.

Required fields:

- `injury_name`
- `body_area`
- `pain_level`
- `symptoms`
- `possible_causes`

Example:

```json
{
  "injury_name": "Knee injury",
  "body_area": "left knee",
  "pain_level": 6,
  "symptoms": ["pain during exercise"],
  "possible_causes": ["squats"]
}
```

---

## 4. Store Data in DynamoDB

Lambda stores the extracted injury information together with the original text.

Example DynamoDB item:

```json
{
  "userId": "test-user-001",
  "timestamp": "2026-08-04T10:30:00Z",
  "entryId": "uuid",
  "rawText": "I hurt my left knee...",
  "extractedData": {
    "injury_name": "Knee injury",
    "body_area": "left knee",
    "pain_level": 6,
    "symptoms": ["pain during exercise"],
    "possible_causes": ["squats"]
  }
}
```

---

## 5. Retrieve Injury History

The Lambda also supports retrieving previously stored injury entries.

Request:

```text
GET /injuries
```

The function reads stored entries from DynamoDB and returns the injury history list.

---

## 6. Return Response

For extraction requests, Lambda returns the structured injury data.

Example:

```json
{
  "injury_name": "Knee injury",
  "body_area": "left knee",
  "pain_level": 6,
  "symptoms": [],
  "possible_causes": []
}
```

For history requests, Lambda returns saved injury entries.

---

# Required AWS Permissions

The Lambda execution role requires the following permissions.

## DynamoDB

Permissions:

```text
dynamodb:PutItem
dynamodb:Scan
```

Purpose:

- Store extracted injury entries
- Retrieve injury history during development

Note:

The current `/injuries` endpoint uses DynamoDB Scan for MVP demonstration purposes only. Since authentication and user identity management are handled by the consuming application, production implementations should replace Scan with Query operations using an authenticated userId.

Before production use:

- Add authentication and authorization
- Extract user identity from JWT claims
- Replace Scan with Query(userId)
- Apply least-privilege IAM permissions

---

## CloudWatch Logs

Permissions:

```text
logs:CreateLogGroup
logs:CreateLogStream
logs:PutLogEvents
```

Purpose:

Enable application logging and debugging.

---

## Groq API Access

The Groq API key is provided through environment variables.

Example:

```text
GROQ_API_KEY
```

The key is never stored directly in source code.

---

# MVP Design Decision

The MVP uses a single Lambda function:

```text
injury-extractor
```

It handles:

- HTTP request processing
- Input validation
- AI extraction
- DynamoDB storage
- Injury history retrieval
- Response generation

Future improvements could split responsibilities into separate functions for:

- AI processing
- Data processing
- Analytics
- Background jobs

---

# Current Architecture

```text
Frontend
    |
    ↓
API Gateway
    |
    ↓
AWS Lambda
    |
    ├── Groq API
    |      (AI extraction)
    |
    └── DynamoDB
           (Storage + History)
```
