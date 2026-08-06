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
