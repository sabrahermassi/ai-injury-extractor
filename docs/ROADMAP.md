# Project Roadmap

## MVP Progress

### AI Injury Extraction Pipeline

- [x] Create Lambda function
- [x] Integrate GROQ API for AI extraction
- [x] Create API Gateway REST API
- [x] Configure CORS for frontend communication
- [x] Store extracted injury data in DynamoDB

### Frontend

- [x] Create Next.js frontend
- [x] Connect frontend to API Gateway
- [ ] Build injury extraction user interface
- [ ] Add loading and error states
- [ ] Display extracted injury results

### Injury History

- [ ] Create API endpoint to retrieve injury history
- [ ] Build injury history dashboard
- [ ] Display timeline of injury entries
- [ ] Add injury entry details view

### User Management

- [ ] Add authentication
- [ ] Associate injury entries with authenticated users
- [ ] Replace temporary userId with real user identity

---

## AI Model Reliability (Before Production)

- [ ] Review and update Groq model selection
  - Replace deprecated models (e.g., `llama-3.1-8b-instant`) before retirement
  - Move model configuration to environment variables instead of hardcoding
  - Validate LLM responses against the expected JSON schema
  - Handle model/API failures gracefully

# Future Improvements

## Security Hardening (Before Production)

- [ ] Add authentication and authorization
  - Protect API Gateway endpoints with JWT-based authentication
  - Use an identity provider such as Amazon Cognito or another authentication solution
  - Replace the hardcoded userId with the authenticated user's ID

- [ ] Protect public API endpoints
  - Add API Gateway throttling/rate limiting
  - Evaluate AWS WAF with rate-based rules for production workloads

- [ ] Secure CORS configuration
  - Replace development-only `http://localhost:3000` origin with the production frontend URL
  - Manage allowed origins through Terraform variables

- [ ] Review AWS permissions
  - Apply least-privilege IAM policies
  - Remove unnecessary permissions before production deployment

- [ ] Add Lambda code signing
  - Configure AWS Signer and Lambda code signing configuration
  - Ensure only trusted deployment artifacts can be executed

## Data Model Improvements (Before Production)

- [ ] Replace hardcoded user identity
  - Remove the hardcoded `userId = "test-user-001"` value in Lambda
  - Use the authenticated user's ID from JWT claims (e.g., Amazon Cognito or another identity provider)
  - Ensure each user can only access and create their own injury records

- [ ] Improve DynamoDB record uniqueness
  - Replace the timestamp-only sort key strategy with a unique injury entry identifier
  - Use `entryId` as part of the DynamoDB key design to prevent accidental overwrites
  - Add idempotency protection to prevent duplicate records from retried requests

- [ ] Improve Lambda deployment process
  - Build Lambda packages inside a Lambda-compatible Linux environment
  - Use Docker or CI/CD build pipeline for reproducible artifacts

- [ ] Improve Lambda error handling
  - Catch Groq API failures separately (timeouts, connection errors, rate limits)
  - Return appropriate HTTP status codes (502/503 instead of always returning 500)
  - Avoid exposing internal exception details in API responses
  - Add sanitized error messages for frontend handling

### AI Extraction Improvements

- [ ] Align Lambda output with the full injury schema defined in `docs/lambda-design.md`
  - Add additional fields:
    - injury name
    - body area
    - side
    - cause
    - description
    - status
    - structured symptoms
  - Validate AI responses against the expected schema
  - Evaluate Groq structured outputs / JSON schema support

---

# Developer Experience Improvements

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
