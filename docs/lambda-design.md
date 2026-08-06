# Lambda Function Design

## Overview

The AI Injury Extractor uses AWS Lambda as the serverless backend processing layer.

The Lambda function is responsible for receiving user injury text, sending it to the Groq API for structured extraction, storing the result in DynamoDB, and returning a response to the client.

---

## Lambda Function

### Function Name

`extractInjuryEntry`

### Purpose

Convert unstructured injury journal text into structured injury data using an LLM.

Example input:

> "I hurt my left knee doing squats two weeks ago. Pain is 6/10."

Example output:

```json
{
  "name": "Knee injury",
  "bodyArea": "knee",
  "side": "left",
  "cause": "squats",
  "description": "Pain after training",
  "status": "active",
  "symptoms": {
    "painLevel": 6,
    "location": "knee",
    "notes": "Pain during exercise"
  }
}
```

---

# High-Level Flow

```
User
 |
 | Injury description
 ↓
API Gateway
 |
 ↓
Lambda (extractInjuryEntry)
 |
 |-- Validate input
 |
 |-- Call Groq API
 |
 |-- Parse AI response
 |
 |-- Store data
 ↓
DynamoDB
 |
 ↓
Return response
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

Invalid requests return an error response.

Example:

```json
{
  "error": "Missing injury text"
}
```

---

## 3. Call Groq API

Lambda sends the user's text to Groq API with instructions to extract structured injury information.

The LLM is responsible for converting unstructured text into structured JSON.

Required fields:

- name
- bodyArea
- side
- cause
- description
- status
- symptoms

---

## 4. Save Data to DynamoDB

Lambda stores the extracted information together with the original user text.

Example:

```json
{
  "userId": "user123",
  "timestamp": "2026-08-04T10:30:00Z",
  "rawText": "I hurt my left knee...",
  "injury": {},
  "symptoms": {},
  "createdAt": "2026-08-04T10:30:00Z"
}
```

---

## 5. Return Response

Lambda returns a success response to the frontend.

Example:

```json
{
  "message": "Entry extracted successfully",
  "data": {
    "bodyArea": "knee",
    "status": "active"
  }
}
```

---

# Required AWS Permissions

The Lambda execution role will require:

## DynamoDB

Permission:

```
dynamodb:PutItem
```

Purpose:

Store extracted injury entries.

---

## CloudWatch Logs

Permissions:

```
logs:CreateLogGroup
logs:CreateLogStream
logs:PutLogEvents
```

Purpose:

Enable application logging and debugging.

---

## Groq API Access

The Groq API key will be provided through environment variables.

Example:

```text
GROQ_API_KEY
```

The key will not be stored in source code.

---

# MVP Design Decision

The MVP uses a single Lambda function:

```
extractInjuryEntry
```

It handles:

- Request processing
- AI extraction
- Database storage
- Response generation

Future improvements could split responsibilities into separate functions for:

- AI processing
- Data processing
- Analytics
- Background jobs

---

# Current Architecture

```
Frontend
    |
    ↓
API Gateway
    |
    ↓
AWS Lambda
    |
    ├── Groq API
    |
    ↓
DynamoDB
```
