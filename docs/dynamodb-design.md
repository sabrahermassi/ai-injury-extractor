# DynamoDB Schema Design

## Overview

The AI Injury Extractor uses DynamoDB as the storage layer for extracted injury journal entries.

The goal is to store user-provided text together with structured information extracted by the LLM (Gemini API).

The MVP focuses on:

- Injury information
- Symptoms
- Related events (e.g., physiotherapy visit, medical consultation)
- AI-extracted structured data

---

## Table Design

### Table Name

`InjuryEntries`

---

## Primary Key Design

DynamoDB uses a composite primary key:

| Key           | Name        | Purpose                                               |
| ------------- | ----------- | ----------------------------------------------------- |
| Partition Key | `userId`    | Groups all entries belonging to one user              |
| Sort Key      | `timestamp` | Allows chronological ordering and querying of entries |

Example:

```
userId                 timestamp
-------------------------------------------
user123                2026-08-01T10:00:00Z
user123                2026-08-03T15:30:00Z
user123                2026-08-04T09:15:00Z
```

This design allows efficient queries such as:

- Get all injury entries for a user
- Retrieve entries within a date range
- Display an injury timeline

---

## Example DynamoDB Item

```json
{
  "userId": "user123",
  "timestamp": "2026-08-04T10:30:00Z",

  "rawText": "I hurt my left knee doing squats two weeks ago. Pain is 6/10. Went to physio yesterday.",

  "injury": {
    "bodyArea": "knee",
    "side": "left",
    "cause": "squats",
    "description": "pain after training"
  },

  "symptoms": {
    "painLevel": 6,
    "location": "knee",
    "duration": "2 weeks"
  },

  "event": {
    "type": "physiotherapy",
    "date": "2026-08-03",
    "notes": "initial assessment"
  }
}
```

---

## Design Decisions

### Single-table approach

For the MVP, injury data is stored as a single DynamoDB item instead of creating multiple tables.

Reason:

- Faster development
- Fits DynamoDB access patterns
- Reduces complexity
- Suitable for an MVP

A relational database model (like PostgreSQL/Prisma) may separate:

- Injury
- Symptoms
- Treatments
- Medical visits
- Timeline events

However, DynamoDB is designed around access patterns rather than normalized relationships.

---

## Future Improvements

Possible future additions:

- Separate entities for analytics pipelines
- DynamoDB Streams for event processing
- Export data to S3 for Athena queries
- AI-generated tags for trend analysis
- Vector embeddings for RAG search

---

## Current MVP Flow

```
User text input
        |
        v
Gemini API
        |
        v
Structured injury data
        |
        v
DynamoDB InjuryEntries table
```
