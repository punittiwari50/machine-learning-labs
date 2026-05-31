# Code Generation Documentation Standard

## Purpose
Ensure generated code and markdown are clear, practical, and easy to review.

## Required for Generated Code
1. Add concise code-level comments on non-obvious logic.
2. Explain assumptions near critical sections.
3. Label validation, retry, and fallback blocks clearly.

## Required for Generated Markdown
1. Add concept markup sections with direct, on-point explanation.
2. Keep language simple and learner-friendly.
3. Include 3-5 real-time enterprise use cases.
4. For each use case, include:
- business context
- ML function
- deployment concern
- validation signal

## Realtime Use-Case Pattern
- Use Case Name
- Problem in production
- ML solution behavior
- Delivery/CICD risk
- Validation and rollback signal

## Example Use Cases
1. Fraud scoring in payment gateway.
2. Ticket urgency classification in support operations.
3. Forecasting demand spikes in retail supply chain.
4. OCR document classification in compliance workflow.
5. Personalized ranking in recommendation service.

## Quality Rule
No vague comments, no generic use cases, and no missing validation signal.
