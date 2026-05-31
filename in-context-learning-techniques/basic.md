# Basic In-Context Learning Techniques

## 1. Zero-Shot Prompting

- Provide only the task instruction, no examples.
- Relies on the model's pretraining and instruction-following behavior.

When to use:
- Fast baseline for a new task.
- Low token budget environments.

Pros:
- Lowest prompt cost.
- Easiest to operationalize.

Cons:
- Less stable output quality on specialized tasks.

Enterprise usage example:
- Classify incoming support tickets into coarse categories with a short routing prompt.

## 2. One-Shot Prompting

- Provide one demonstration example in the prompt.
- Helps define expected output style and format.

When to use:
- Tasks where output format is critical.
- Need quick quality improvement over zero-shot.

Pros:
- Better format consistency.
- Small token overhead.

Cons:
- Sensitive to the quality of the single example.

Enterprise usage example:
- Generate standardized executive summaries by showing one approved summary template.

## 3. Few-Shot Prompting

- Provide multiple input-output examples before the target query.
- Teaches local patterns and decision boundaries in prompt context.

When to use:
- Domain-specific formatting or labeling.
- Ambiguous instructions that benefit from examples.

Pros:
- Typically strong quality gains.
- More controllable behavior.

Cons:
- Higher token cost and latency.

Enterprise usage example:
- Extract invoice fields with 3-5 representative examples across vendor formats.

## 4. Structured Prompting

- Constrain the model with explicit sections, delimiters, and schema hints.
- Example: role, instructions, constraints, context, output schema.

When to use:
- Production workflows requiring parseable output.
- Integrations with downstream services.

Pros:
- Reduced format drift.
- Easier validation and retry logic.

Cons:
- Requires careful prompt design and testing.

Enterprise usage example:
- Produce JSON incident reports consumed by SIEM and ticketing systems.

## 5. Retrieval-Augmented In-Context Prompting (RAG-lite)

- Add relevant documents/snippets directly into prompt context.
- The model reasons over provided facts rather than only parametric memory.

When to use:
- Knowledge changes frequently.
- Need source-grounded responses.

Pros:
- Improved factuality on domain content.
- Lower hallucination risk when retrieval quality is high.

Cons:
- Retrieval quality is a hard dependency.
- Prompt can grow quickly with long documents.

Enterprise usage example:
- Answer policy questions using the latest internal compliance documents retrieved at query time.

## 6. Output Constraint Techniques

- Force output shape with schemas, strict instructions, and examples.
- Use explicit failure handling instructions when required fields are missing.

When to use:
- API-first workflows and automations.
- High reliability extraction tasks.

Pros:
- Higher machine-readability.
- Better operational robustness.

Cons:
- Over-constrained prompts can reduce reasoning flexibility.

Enterprise usage example:
- Contract clause extraction into fixed fields for legal review dashboards.
