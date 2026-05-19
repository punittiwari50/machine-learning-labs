# 01-tokenizers-text: High-Level Mind Map + Code-Level Coverage

## Mind Map

- 01-tokenizers-text
  - A. Foundations and Conceptual Framing
    - Tokenization concept map
      - End-to-end flow: raw text -> normalization -> tokenization -> IDs -> model inputs
      - Real-time use: support message routing by keyword-intent mapping
      - Startup rules: stable preprocessing order and reproducible vocab mapping
    - Why tokenization matters
      - Accuracy impact: better lexical coverage and lower OOV behavior
      - Latency impact: token count and tokenizer complexity affect p95
      - Cost impact: token budget drives model compute and memory usage

  - B. Certification and Interview Alignment
    - Certification-aligned topic mapping (NCA-GENL / NCP-GENL context)
      - Concept -> business value -> tokenizer/API selection
    - Interview and certification prep cells
      - Short-answer interview prompts
      - MCQ-style certification checks
      - Scenario decision questions with model answer sheet
    - Enterprise assessment flow
      - Timed mock assessment
      - Scoring rubric
      - Case-study drill sheet

  - C. Enterprise Use-Case Design Layer
    - Use-case map
      - Customer support routing
      - KYC NER and compliance extraction
      - Retrieval indexing and query-time parity
      - Long-document QA under fixed context windows
      - Mobile/on-device inference constraints
    - KPI suggestions and decision checkpoints
      - Coverage ratio
      - OOV rate
      - Latency (p95)
      - Retrieval relevance stability
      - Token budget adherence

  - D. TensorFlow Text Practical Learning Path (Basic -> Advanced)
    - Cell A: Normalize -> tokenize -> vocab lookup
      - tf_text.case_fold_utf8
      - tf_text.WhitespaceTokenizer
      - tf.lookup.StaticVocabularyTable
      - Ragged token-to-id conversion
    - Cell B: Pair input packing for transformer workloads
      - Query/context tokenization
      - Budget-aware trimming with Waterfall policy
      - CLS/SEP insertion and token-type construction
      - Padding and mask generation
    - Cell C: Long-document chunking + KPI snapshot
      - Sequence chunking with window and stride logic
      - Chunk padding masks
      - Throughput-oriented summary metrics
    - Cell D: Certification/interview API decision drill
      - API-by-scenario comparisons and expected choices

  - E. Tokenizers: Direct API Demonstrations
    - Segmentation tokenizers
      - tf_text.WhitespaceTokenizer
      - tf_text.UnicodeScriptTokenizer
      - tf_text.PhraseTokenizer
      - tf_text.StateBasedSentenceBreaker
    - Low-level tokenizers
      - tf_text.ByteSplitter
      - tf_text.UnicodeCharTokenizer
    - Subword tokenizers
      - tf_text.BertTokenizer
      - tf_text.FastBertTokenizer
      - tf_text.WordpieceTokenizer
      - tf_text.FastWordpieceTokenizer
      - tf_text.SentencepieceTokenizer
      - tf_text.FastSentencepieceTokenizer
    - Specialized tokenizers
      - tf_text.SplitMergeTokenizer
      - tf_text.SplitMergeFromLogitsTokenizer
      - tf_text.HubModuleTokenizer (guarded by dependency/network checks)

  - F. Text Processing Utilities and Sequence Ops
    - Trimmers
      - tf_text.ShrinkLongestTrimmer
      - tf_text.RoundRobinTrimmer
      - tf_text.WaterfallTrimmer
    - Splitting and shape utilities
      - tf_text.RegexSplitter
      - tf_text.regex_split
      - tf_text.wordshape
    - Input shaping utilities
      - tf_text.pad_model_inputs
      - tf.text.trim_model_inputs
      - tf_text.sliding_window
      - tf_text.concatenate_segments
    - UTF-8 normalization and casing
      - tf_text.normalize_utf8 (NFC, NFKC forms)
      - tf_text.case_fold_utf8
      - tf_text.coerce_to_structurally_valid_utf8

  - G. Advanced Feature Engineering and Structured NLP Ops
    - Sentence breaking and segmentation section
    - Item selector and sequence selection section
      - tf_text.FirstNItemSelector
      - tf_text.LastNItemSelector
    - Span operations and NER support section
    - N-gram feature extraction section
      - tf_text.ngrams with Reduction.MEAN
      - tf_text.ngrams with Reduction.SUM
    - MLM masking section
      - token selection strategy and mask position logic
    - Model input preparation section
      - segment packing, type IDs, attention masks
    - Fast model building for TFLite section
      - deployment-oriented tokenizer path decisions

  - H. Concept Maps, Playbooks, and Operational Guidance
    - ML concept map for tokenization in production systems
    - Practical use-case playbook
    - Full API reference summary section
    - Special tokens reference section
      - [PAD], [UNK], [CLS], [SEP], [MASK]
    - Performance optimization tips section
    - Do/Don't section with code examples
    - Tips and tricks section with explicit examples

## Code-Level Inventory (Explicit)

- Tokenizers demonstrated in code
  - tf_text.WhitespaceTokenizer
  - tf_text.UnicodeScriptTokenizer
  - tf_text.PhraseTokenizer
  - tf_text.ByteSplitter
  - tf_text.StateBasedSentenceBreaker
  - tf_text.BertTokenizer
  - tf_text.FastBertTokenizer
  - tf_text.FastWordpieceTokenizer
  - tf_text.FastSentencepieceTokenizer
  - tf_text.SentencepieceTokenizer
  - tf_text.SplitMergeTokenizer
  - tf_text.SplitMergeFromLogitsTokenizer
  - tf_text.UnicodeCharTokenizer
  - tf_text.WordpieceTokenizer
  - tf_text.HubModuleTokenizer

- Text utilities demonstrated in code
  - tf_text.ShrinkLongestTrimmer
  - tf_text.RoundRobinTrimmer
  - tf_text.WaterfallTrimmer
  - tf_text.RegexSplitter
  - tf_text.regex_split
  - tf_text.pad_model_inputs
  - tf.text.trim_model_inputs
  - tf_text.sliding_window
  - tf_text.wordshape
  - tf_text.normalize_utf8
  - tf_text.case_fold_utf8
  - tf_text.coerce_to_structurally_valid_utf8
  - tf_text.ngrams
  - tf_text.concatenate_segments
  - tf_text.FirstNItemSelector
  - tf_text.LastNItemSelector

- Additional advanced tf_text ops shown in notebook
  - tf_text.greedy_constrained_sequence
  - tf_text.max_spanning_tree

- Core TensorFlow structures and preparation patterns
  - RaggedTensor token pipelines
  - StaticVocabularyTable lookups for token-id mapping
  - Segment IDs / type IDs creation for paired inputs
  - Attention mask generation from padded inputs
  - Sliding-window chunk masks for long-document processing
  - OOV-safe vocabulary usage and detokenization checks

## Practical Reading Order

- Read conceptual and certification sections first to understand decisions.
- Run tokenizer API sections second to compare outputs token-by-token.
- Run utilities and advanced sections third to prepare model-ready inputs.
- Use playbook and optimization sections last for enterprise rollout decisions.
