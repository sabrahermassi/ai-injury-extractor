# Project Roadmap

## Completed Features

### AI Injury Extraction Pipeline

- [x] Create Lambda function
- [x] Integrate GROQ API for AI extraction
- [x] Create API Gateway REST API
- [x] Configure CORS for frontend communication
- [x] Store extracted injury data in DynamoDB

### Frontend

- [x] Create Next.js frontend
- [x] Connect frontend to API Gateway
- [x] Build injury extraction user interface
- [x] Add loading and error states
- [x] Display extracted injury results

### Injury History

- [x] Add GET /injuries API endpoint
- [x] Retrieve saved injury entries from DynamoDB
- [x] Display injury history entries
- [x] Create reusable injury history cards

## Future Improvements

## AI Model Reliability

- [ ] Review and update Groq model selection
  - Replace deprecated models before retirement
  - Move model configuration to environment variables instead of hardcoding
  - Validate LLM responses against the expected JSON schema
  - Handle model/API failures gracefully

---

## Data & API Improvements

- [ ] Improve DynamoDB record design
  - Review partition key and sort key strategy
  - Add stronger uniqueness guarantees
  - Prevent duplicate entries from retries

- [ ] Improve Lambda error handling
  - Handle Groq API failures separately
  - Return appropriate HTTP status codes
  - Avoid exposing internal exceptions
  - Add sanitized error messages for frontend handling

---

## AI Extraction Improvements

- [ ] Expand injury extraction schema
  - Add additional fields:
    - injury name
    - body area
    - side
    - cause
    - description
    - status
    - structured symptoms

- [ ] Validate AI responses against the expected schema
- [ ] Evaluate Groq structured outputs / JSON schema support

---

## Developer Experience Improvements

- [ ] Automate Lambda deployment workflow
  - Automate building `function.zip`
  - Simplify deployment scripts
  - Ensure dependencies are packaged correctly

- [ ] Add automated tests
  - Lambda unit tests
  - API integration tests
  - Frontend component tests

- [ ] Add monitoring and observability
  - CloudWatch logging improvements
  - Error tracking
  - Usage metrics
