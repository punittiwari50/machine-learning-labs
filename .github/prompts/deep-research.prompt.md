---
description: "Deep research on any ML or system topic with a structured progression from core fundamentals to enterprise"
agent: agent
argument-hint: "Topic to research deeply"
tools: [read, search, web, edit]
---

You are producing a research package that downstream design work can directly consume.

## Mission

Create a practical, citation-backed study in four tiers: Core, Basic, Advanced, Enterprise.

## Source Rules

- Prefer papers, official documentation, and official repositories.
- Use citation markers for major claims.
- Target at least 10 credible papers when available; explain coverage limits otherwise.
- Include foundational and recent references.

## Required Outputs

Create both files:

- foundation/research/<kebab-case-topic>.md
- foundation/research/<kebab-case-topic>-mindmap.md

Research file must include:

1. Topic framing.
2. Core, Basic, Advanced, Enterprise sections with practical examples.
3. Mini enterprise usage mapping for major concepts.
4. System Design Input handoff section.
5. Sources, paper coverage summary, and recommended learning videos.

Mind map file must include:

- Plain-language summary.
- Mermaid mindmap from Core to Enterprise.
- In-scope use cases and short takeaways.

## Constraints

- Do not run code.
- Stay strictly in-topic.
- Do not include uncited key claims.

## References

- ../instructions/policy.instructions.md
- ../instructions/architecture.instructions.md
- ../agents/docs/code-generation-documentation-standard.md
