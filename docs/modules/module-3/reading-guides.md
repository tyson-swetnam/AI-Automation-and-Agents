---
title: Module 3 Reading Guides
description: Reading guides with guiding questions for the five chapters of Module 3 on memory architectures and retrieval-augmented generation.
type: Reading Guide
tags:
- module-3
- student-facing
- reading-guide
- memory
- rag
- langchain
- chroma
- ragas
module: 3
status: stable
stale_after: '2027-09-01T00:00:00Z'
generated:
  by: process:scripts/migrate_wiki.py
  at: '2026-09-08T00:00:00Z'
sources:
- id: wiki-v2
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-3.2-Addendum
  title: 'AI Automation and Agents v2 wiki: Module-3.2-Addendum'
  author: Carlos Lizárraga-Celaya; Michelle Yung
  last_modified: '2026-08-12T15:56:29-07:00'
authorship:
  created: '2026-07-23'
  contributors:
  - C. Lizárraga
wiki_page: Module-3.2-Addendum
---
# Module 3 Reading Guides

These reading guides accompany the assigned sources for each chapter of Module 3. Work through the guiding questions as you read — they focus your attention on the concepts the chapter lessons, labs, and quizzes will assess. Complete the extraction tasks embedded in each guide before moving to the next chapter.

## Reading Guide 1 — Chapter 1: Parametric vs. Non-Parametric Memory { #reading-guide-1 }

**Sources covered:**

- Lewis, P., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *NeurIPS 2020*. *(Abstract + Sections 1–2)*
- Bommasani, R., et al. (2021). On the opportunities and risks of foundation models. *arXiv:2108.07258*. *(Section 2.1 only)*
- Video 1: "What is Retrieval-Augmented Generation (RAG)?" — IBM Technology (~6 min)

**Estimated study time:** ~12 minutes (Lewis et al.) + ~8 minutes (Bommasani et al. Section 2.1) + ~6 minutes (video)

**Chapter connection:** These sources establish the foundational distinction that motivates every subsequent topic in Module 3. Read them in order: Bommasani et al. first for the theoretical framing, then Lewis et al. for the architectural solution, then the video as a synthesis check.

### Overview

Bommasani et al. (2021) articulate the fundamental constraint of foundation models: the knowledge encoded in model parameters during training is static — it cannot be updated without retraining, cannot be attributed to specific sources, and cannot incorporate information that postdates the training cutoff. This constraint is not incidental; it is structural, arising from how gradient-descent-based training encodes information into billions of parameter weights. Lewis et al. (2020) introduced Retrieval-Augmented Generation (RAG) as a principled architectural solution: by coupling a parametric generative model with a non-parametric retrieval index, the system can ground its generation in dynamically retrieved, externally verifiable, and continuously updatable evidence.

This distinction — parametric vs. non-parametric memory — is the conceptual backbone of Module 3. Every subsequent design decision (pipeline stage, memory type, chunking strategy, retrieval method) is an engineering response to the fundamental properties and limitations of each memory class.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **Parametric memory** | Knowledge encoded in model weights during training; fixed at training time, inaccessible to external inspection or update without retraining |
| **Non-parametric memory** | Knowledge stored in an external index or database; retrievable at inference time, updatable without model retraining, attributable to specific source documents |
| **Foundation model** | A large model trained on broad data that can be adapted to a wide range of downstream tasks (Bommasani et al., 2021) |
| **Training cutoff** | The date beyond which a model's parametric knowledge does not extend; information published after this date is not in the model's weights |
| **Knowledge-intensive NLP task** | A task (question answering, fact verification, document-grounded dialogue) whose correct completion requires access to specific factual knowledge that may not be reliably encoded in parametric memory |
| **Hallucination** | A generated output that is fluent and plausible but factually incorrect or unsupported by the retrieved context — a characteristic failure mode of parametric-only generation |
| **RAG** | Retrieval-Augmented Generation — an architecture that combines a parametric generative model with a non-parametric retrieval component, grounding generation in retrieved evidence |
| **Retrieval index** | The external data structure (typically a vector store) that stores document representations and supports semantic similarity search at inference time |
| **Inference time** | The moment when a trained model processes an input and generates an output — distinct from training time, when model weights are updated |
| **Grounding** | Constraining a generative model's output to be consistent with and attributable to specific retrieved source documents |

### Guiding Questions

#### Section A — Bommasani et al. (2021): Section 2.1 — Parametric vs. Non-Parametric Knowledge

1. Bommasani et al. distinguish parametric knowledge (encoded in model weights) from non-parametric knowledge (stored externally). What is the precise technical meaning of "encoded in weights"? Why does this encoding mechanism make parametric knowledge difficult to inspect, attribute, or update?

2. The report characterizes foundation model capabilities as "emergent" from scale. What does this imply about the relationship between a model's training data distribution and its parametric knowledge? What categories of knowledge are most likely to be reliably encoded, and which are most likely to be unreliably encoded or absent?

3. Bommasani et al. identify the "long tail" of specialized knowledge as a particular limitation of parametric memory. In a professional deployment context — healthcare, law, finance, education — give two specific examples of long-tail knowledge that would be essential for a high-quality agent but is unlikely to be reliably encoded in a general-purpose foundation model's parameters.

4. What organizational property makes non-parametric memory especially valuable in enterprise AI deployment? Specifically, what would it take to update a parametric model when an organization's internal policy changes, and how does RAG eliminate that cost?

#### Section B — Lewis et al. (2020): Abstract + Sections 1–2

5. Lewis et al. define RAG formally as a combination of two components. Name both components precisely and describe what each contributes to the system's overall capability.

6. The paper identifies "knowledge-intensive NLP tasks" as the target problem class for RAG. What properties make a task "knowledge-intensive"? Give one example of a task that qualifies and one that does not, with a justification for each.

7. Lewis et al. describe RAG as a model that "jointly reasons over parametric and non-parametric memory." What does "jointly" mean in this context? Why is joint reasoning more powerful than either component alone?

8. The original RAG architecture uses a dense passage retriever (DPR) for the retrieval component. What is the functional role of the retriever in the system, and what property of the query-document relationship does it exploit to find relevant passages?

9. Lewis et al. contrast RAG with parametric-only models and with "retrieve-then-read" pipelines. What distinguishes RAG from a simple retrieve-then-read approach? What does the "augmented generation" component add that simple retrieval does not provide?

#### Section C — IBM Technology Video: "What is RAG?"

10. After watching the video, identify one concept from Lewis et al. that the video explains accurately and one that it simplifies in a potentially misleading way. Justify your assessment with reference to the original paper.

11. The video uses an analogy to explain RAG to a non-technical audience. Evaluate the analogy: what does it capture well about the parametric/non-parametric distinction, and what does it fail to convey about the engineering complexity of the retrieval component?

### Critical Thinking Prompts

- A colleague argues: "Since LLMs will eventually be retrained more frequently, the parametric/non-parametric distinction will become less important." Evaluate this claim using the concepts from Bommasani et al. What categories of knowledge would remain non-parametric even with daily retraining?

- The shift from parametric-only to RAG-augmented generation introduces a new failure mode: retrieval failure (the system retrieves irrelevant or no relevant documents). How does this failure mode differ from hallucination in parametric-only systems? What new evaluation responsibilities does it place on the practitioner?

## Reading Guide 2 — Chapter 2: The Six-Stage RAG Pipeline — Architecture, Design Decisions, and Downstream Consequences { #reading-guide-2 }

**Sources covered:**

- Lewis, P., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *NeurIPS 2020*. *(Re-read: focus on the two-component architecture)*
- Gao, Y., et al. (2023). Retrieval-augmented generation for large language models: A survey. *arXiv:2312.10997*. *(Sections 1–3)*
- LangChain Documentation: Document Loaders, Text Splitters, Vector Stores, and the LangChain Expression Language (LCEL) runnables that compose them
- Video 2: "RAG Explained For Beginners" — KodeKloud (~10 min)

**Estimated study time:** ~15 minutes (Gao et al. Sections 1–3) + ~15 minutes (LangChain docs) + ~10 minutes (video)

**Chapter connection:** Gao et al. (2023) is the most comprehensive survey of the RAG literature and directly grounds the six-stage pipeline the labs implement. The LangChain documentation provides the component-level implementation vocabulary. Read Gao et al. first; use the LangChain documentation as a reference while completing the pipeline diagram template.

### Overview

Gao et al. (2023) identify three evolutionary RAG paradigms — Naive RAG, Advanced RAG, and Modular RAG — that represent increasing sophistication in pipeline design. However, all three share six functional stages: document ingestion, text splitting (chunking), embedding generation, vector indexing, retrieval, and augmented generation. Understanding these stages at the level of their data flow (what format the data enters and exits each stage) and the design decisions made at each stage is the prerequisite for diagnosing failures, selecting optimization strategies, and evaluating system quality. The LangChain component names that implement each stage provide the engineering vocabulary for the labs.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **Document ingestion** | Stage 1: Loading raw source documents into the pipeline using a document loader (e.g., PyPDFLoader); output is a list of Document objects with content and metadata |
| **Text splitting (chunking)** | Stage 2: Dividing loaded documents into smaller units (chunks) suitable for embedding and retrieval; output is a list of smaller Document objects |
| **Embedding generation** | Stage 3: Converting text chunks into dense numerical vectors using an embedding model; output is a list of fixed-dimension float vectors |
| **Vector indexing** | Stage 4: Storing chunk embeddings in a searchable vector database (e.g., Chroma, FAISS); enables fast semantic similarity search at retrieval time |
| **Retrieval** | Stage 5: Given a query embedding, finding the k most similar chunk embeddings in the vector store; output is a list of k retrieved Document chunks |
| **Augmented generation** | Stage 6: Combining the retrieved chunks with the user query into an augmented prompt and passing it to the LLM; output is a generated answer grounded in the retrieved context |
| **Naive RAG** | The baseline RAG paradigm: sequential, one-pass retrieval and generation with no iterative refinement or query transformation |
| **Advanced RAG** | An extended paradigm adding pre-retrieval (query transformation, routing) and post-retrieval (re-ranking, compression) processing to improve precision |
| **Modular RAG** | The most flexible paradigm: arbitrary composition of specialized retrieval, processing, and generation modules into non-sequential pipelines |
| **Context precision** | A RAG quality dimension: the proportion of retrieved chunks that are actually relevant to the query (signal-to-noise ratio in the retrieved context) |
| **Context recall** | A RAG quality dimension: the proportion of relevant information in the corpus that is successfully retrieved (coverage of the query's information needs) |
| **chunk_overlap** | A parameter in text splitting that specifies the number of characters shared between adjacent chunks, preserving context across chunk boundaries |

### Guiding Questions

#### Section A — Gao et al. (2023): Sections 1–3 — RAG Framework and Pipeline

1. Gao et al. enumerate six stages of the RAG pipeline. List all six in order and describe the data format at the input and output of each stage (e.g., "Stage 2 input: Document objects with raw text; output: smaller Document objects (chunks)"). This data-flow specification is the basis for diagnosing at which stage a pipeline failure originates.

2. The survey distinguishes three RAG paradigms: Naive, Advanced, and Modular. What specific limitations of Naive RAG motivated the development of Advanced RAG? Name at least two concrete failure modes of Naive RAG that Advanced RAG addresses.

3. Gao et al. identify two main retrieval quality dimensions: context precision and context recall. Explain the tension between them. Under what corpus and query conditions would you sacrifice context recall to maximize context precision, and under what conditions would you do the reverse?

4. The survey notes that chunking is "the most consequential single decision in RAG pipeline design." Why does chunking occur before embedding rather than after? What property of embedding models makes it necessary to split documents before encoding them?

5. Gao et al. describe Modular RAG as enabling "arbitrary composition" of modules. What does this flexibility cost in terms of system design complexity and debugging difficulty? Under what organizational conditions is Modular RAG's flexibility worth that cost?

#### Section B — LangChain Documentation: Pipeline Components

6. The LangChain documentation describes PyPDFLoader as a document loader that preserves page-level metadata. Why is metadata preservation at the ingestion stage important for later retrieval optimization (specifically, metadata filtering at Stage 5)?

7. RecursiveCharacterTextSplitter uses a priority list of separators (paragraph breaks, sentence breaks, word breaks) to find split points. What problem does this recursive strategy solve compared to a simple fixed-character-length splitter? What type of document content benefits most from recursive splitting?

8. The lab composes Stage 6 explicitly rather than calling a prebuilt question-answering chain: `RunnableParallel(question=RunnablePassthrough(), source_documents=retriever)` fans the query out to the retriever, and a second step adds the generated `result`. What does the chain's `source_documents` key give you that the answer string alone does not, and why is this output critical for diagnosing faithfulness failures (i.e., identifying when the LLM generates an answer that contradicts or goes beyond the retrieved context)?

9. The vector store's `as_retriever(search_kwargs={'k': 4})` call configures Stage 5 retrieval. What is the effect of increasing k from 4 to 8 on (a) context recall, (b) context precision, and (c) total input tokens to the generation stage?

#### Section C — KodeKloud Video: "RAG Explained For Beginners"

10. The video presents the six pipeline stages with visual diagrams. After watching, complete your pipeline diagram template with: the stage name, the data format in/out, and the LangChain component name for each of the six stages. If any stage is missing from your template after the video, return to the Gao et al. survey and fill the gap before proceeding.

### Critical Thinking Prompts

- Lewis et al.'s original RAG architecture used a single retrieval pass. What does the existence of Advanced RAG's query transformation techniques (e.g., HyDE — Hypothetical Document Embeddings, multi-query retrieval) tell us about the limitations of single-pass retrieval? What specific properties of user queries make them poor inputs for direct embedding-based retrieval?

- The six-stage pipeline treats document ingestion as a one-time offline process and retrieval as an online, per-query process. What organizational workflows would require ingestion to be a continuous, streaming process rather than a batch process? What engineering challenges does continuous ingestion introduce that batch ingestion does not?

## Module 3 — Chapter 3 Reading Guide — Conversational Memory Management

**Assigned:** LangChain Documentation — [`RunnableWithMessageHistory`](https://reference.langchain.com/python/langchain-core/runnables/history/RunnableWithMessageHistory){target=_blank} · [Memory Conceptual Guide](https://docs.langchain.com/oss/javascript/concepts/memory){target=_blank} · LangChain Tutorials — Lesson 8: [Memory & Context Management](https://langchain-tutorials.com/lessons/langchain-essentials/lesson-8){target=_blank}

**Estimated time:** ~40 minutes

### Learning Objectives

By the end of this chapter you should be able to:

1. Explain why LLMs need an explicit memory mechanism for multi-turn conversations.
2. Describe how `RunnableWithMessageHistory` connects a chain to a history store.
3. Compare the four memory patterns (Buffer, Window, Summary, Hybrid) on token cost and fidelity.
4. Select the appropriate memory pattern for a deployment scenario given cost and fidelity constraints.
5. Explain why LangGraph State Schema is preferred for multi-agent and production systems.

### Core Concepts

#### 1. The Memory Problem

LLMs are stateless: each API call receives only the tokens in the current prompt. Without an explicit memory mechanism, every conversation turn starts from scratch. Memory solves this by deciding *what* prior context to include in the prompt and *how* to represent it.

#### 2. How LangChain Implements Memory

LangChain's memory system has three components:

1. **A prompt template with a history slot** — reserves space where prior messages are inserted.
2. **A chain** (`prompt | llm`) — the processing pipeline.
3. **`RunnableWithMessageHistory` wrapper** — connects the chain to a history store, automatically loading prior messages before each call and saving new messages after.

Each conversation gets a unique `session_id`, so one chain can serve many concurrent conversations without mixing histories.

#### 3. The Four Memory Patterns

Each pattern trades off token cost against context fidelity:

**Buffer**

- Stores every message verbatim.
- Token cost grows linearly with each turn.
- Best for: short conversations (&lt;10 turns) where complete fidelity matters (e.g., medical record review, compliance dialogue).

**Window**

- Keeps only the last *k* turns; drops older messages.
- Token cost is stable once the window is full.
- Best for: customer support, coding assistants — where recent context matters most and early turns can be dropped.

**Summary**

- Uses an LLM to compress older messages into a running summary; keeps recent messages verbatim.
- Token cost is low and stable.
- Risk: *semantic drift* — specific details (names, numbers, exact phrasing) may not survive summarization.
- Best for: extended multi-session discussions where key decisions must persist but exact wording doesn't.

**Hybrid (Summary + Buffer)**

- Rolling summary of older turns + verbatim buffer of recent turns.
- Token cost is low to moderate.
- Best for: long, dense conversations (debugging, iterative drafting) needing both recency and long-range context.
- Recommended default for production single-agent applications.

#### 4. Reference Table

| Pattern | Storage | Token Cost | Best Use Case |
|---|---|---|---|
| Buffer | Verbatim transcript | Linear (unbounded) | Short sessions, maximum fidelity required |
| Window | Last *k* turns only | Stable (bounded by *k*) | Recent context sufficient, older turns dispensable |
| Summary | LLM-generated summary | ~Constant | Long sessions, cost-constrained, general context sufficient |
| Hybrid | Summary + recent buffer | Low–moderate | Long dense sessions needing recency + long-range context |

#### 5. Persistent Memory

The four patterns above are ephemeral — history is lost when the process stops. For production, configure a persistent backend (database, file store) so conversation history survives across sessions. The `RunnableWithMessageHistory` wrapper supports pluggable backends for this purpose.

#### 6. LangGraph State Schema (Looking Ahead)

For multi-agent systems (Module 4), LangGraph manages state as a typed, structured graph node rather than a message history. Key advantages:

- **Explicit:** All memory fields are declared in the schema — no implicit state.
- **Testable:** Unit tests can assert on state after each node execution.
- **Auditable:** Full state at each step can be logged and reviewed.

For single-agent applications, `RunnableWithMessageHistory` is sufficient. For multi-agent coordination, LangGraph's structured state is preferred.

### Active Reading Tasks

Complete these before proceeding to the quiz.

**Task A — Reconstruct the Reference Table**
Close this guide and reconstruct the four-row pattern table from memory. Check against Section 4. Any cell you cannot fill is a gap to address.

**Task B — Token Cost Sketch**
For Buffer and Summary: sketch the token-count curve (y-axis: tokens in context; x-axis: turn number) for a 20-turn conversation. Label the shape of each curve (linear vs. bounded).

**Task C — Scenario Classification**
For each scenario, identify the best memory pattern and write a one-sentence justification:

1. A legal assistant that must recall exact clause language from turn 3 in a 7-turn session.
2. A customer support bot handling 10,000 simultaneous sessions of ~15 turns each.
3. A debugging assistant with 40+ turn sessions where the user references decisions from 25 turns ago.
4. A research assistant with daily 10-turn sessions recurring over months.

**Task D — RunnableWithMessageHistory**
In two sentences, explain how `RunnableWithMessageHistory` makes a stateless LLM chain behave as though it has memory. Include the role of `session_id`.

### Key Terms

| Term | Definition |
|---|---|
| Buffer memory | Pattern storing every message verbatim; linear token growth |
| Window memory | Pattern keeping only the last *k* turns; stable cost, drops older context |
| Summary memory | Pattern compressing older turns into an LLM-generated summary; low cost, lossy |
| Hybrid memory | Pattern combining rolling summary of older turns with verbatim recent buffer |
| Semantic drift | Accumulated distortion from lossy summarization — details diverge from what was actually said |
| `RunnableWithMessageHistory` | LangChain wrapper that loads/saves conversation history automatically per `session_id` |
| `session_id` | Unique identifier for a conversation; enables one chain to serve many concurrent sessions |
| Persistent memory | Memory backed by a database or file store that survives across process restarts |
| LangGraph State Schema | Typed structured state for multi-agent systems; explicit, testable, auditable |
| Cost-quality trade-off | The framework for selecting a memory pattern by weighing fidelity against token cost |

---

*Before proceeding to the Chapter 3 Quiz, verify you can reconstruct the reference table (Task A) and complete Task C without consulting the guide.*

---

## Reading Guide 4 — Chapter 4: Retrieval Optimization and Context Window Management { #reading-guide-4 }

**Sources covered:**

- Gao, Y., et al. (2023). Retrieval-augmented generation for large language models: A survey. *arXiv:2312.10997*. *(Section 5 — Advanced RAG patterns)*
- LangChain Expression Language (LCEL) Documentation
- Es, S., et al. (2024). RAGAS: Automated evaluation of retrieval augmented generation. *EACL 2024*. *(Background — for optimization feedback loops)*

**Estimated study time:** ~15 minutes (Gao et al. Section 5) + ~15 minutes (LCEL documentation)

**Chapter connection:** This guide builds directly on Reading Guide 2's six-stage pipeline. Section 5 of Gao et al. describes the Advanced RAG optimizations that extend the baseline Naive RAG pipeline. The LCEL documentation provides the implementation patterns for the optimization experiment in Unit 4.

### Overview

A Naive RAG pipeline makes two implicit assumptions that often fail in practice: (1) that fixed-size chunking produces retrievable units of appropriate granularity for all query types, and (2) that cosine similarity to the query embedding is the optimal criterion for selecting which chunks to inject into the generation context. Advanced RAG optimization systematically relaxes both assumptions. Chunking strategy selection, retrieval method selection (similarity vs. MMR), metadata filtering, re-ranking, and context compression are five complementary optimization levers that together determine context quality — the most important determinant of generation quality.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **Fixed-size chunking** | Splitting documents into chunks of a specified character or token count, regardless of semantic boundaries; simple but may fragment logical units |
| **Semantic chunking** | Splitting documents at natural semantic boundaries (paragraphs, sections, sentences) to preserve coherent units of meaning |
| **Hierarchical chunking** | Maintaining multiple chunk granularities (e.g., parent document + child sentence chunks) and using the child chunks for retrieval while injecting the parent for generation context |
| **Similarity search** | Retrieval by selecting the k chunks whose embeddings have the highest cosine similarity to the query embedding; may return redundant chunks from near-duplicate content |
| **Maximum Marginal Relevance (MMR)** | A retrieval method that balances relevance to the query with diversity among retrieved chunks, reducing redundancy when the corpus contains near-duplicate content |
| **lambda_mult** | The MMR diversity parameter (0–1): λ=1 is pure similarity search; λ=0 is pure diversity maximization; λ=0.5 is equal weighting |
| **Metadata filtering** | A pre-retrieval filter applied to the vector store that restricts retrieval to documents matching specified metadata criteria (e.g., source document, date range, document category) |
| **Re-ranking** | A post-retrieval step that applies a more accurate cross-encoder model to re-score and reorder the initially retrieved chunks before context injection |
| **Context compression (LLMLingua)** | A technique that uses a small LLM to remove query-irrelevant sentences from retrieved chunks before context injection, reducing token cost while preserving information density |
| **Single-variable experimentation** | A scientific control principle: changing one pipeline parameter at a time while holding all others constant, enabling the attribution of performance changes to specific design decisions |
| **Cross-encoder** | A model architecture that jointly encodes the query and a candidate document to produce a relevance score; more accurate than bi-encoder (embedding) retrieval but computationally more expensive |

### Guiding Questions

#### Section A — Gao et al. (2023): Section 5 — Advanced RAG

1. Gao et al. organize Advanced RAG optimizations into pre-retrieval, retrieval, and post-retrieval categories. Give one concrete example of an optimization in each category and explain the specific pipeline stage at which it operates and the failure mode it addresses.

2. The survey describes hierarchical chunking as a strategy for preserving semantic coherence while enabling fine-grained retrieval. Explain the "small-to-retrieve, large-to-read" pattern: what is retrieved, what is injected into the generation context, and why does this separation improve generation quality?

3. MMR introduces a diversity penalty that reduces the weight given to chunks similar to already-retrieved chunks. Under what specific corpus conditions is MMR strictly necessary rather than merely preferable? Identify two types of corpora where MMR would produce measurably better retrieval than similarity search.

4. Metadata filtering operates before retrieval (it restricts the search space), while re-ranking operates after retrieval (it reorders the results). What is the key advantage of pre-retrieval filtering over post-retrieval re-ranking in terms of computational cost? What does post-retrieval re-ranking provide that metadata filtering cannot?

5. Context compression (LLMLingua) introduces an additional LLM call to compress retrieved chunks. What is the specific optimization trade-off? Under what deployment conditions — high token cost, very long documents, query-focused tasks — does context compression deliver a positive ROI?

#### Section B — LCEL Documentation: Implementation Patterns

6. LangChain Expression Language (LCEL) uses a pipe operator (`|`) to compose retrieval and generation components into a chain. What does this composition pattern enable that the older prebuilt chain classes — `RetrievalQA` and its siblings, which packaged retrieve-then-generate into a single preconfigured call and were removed from `langchain` in 1.0 — did not? What specific optimization does LCEL's composability simplify?

7. The LCEL documentation describes `RunnablePassthrough` and `RunnableParallel` as composition primitives. What do these primitives allow a practitioner to do with the retrieved context before it is passed to the generation step? Give one concrete optimization use case for each.

8. The Unit 4 optimization experiment requires running four experimental configurations and measuring mean evaluation score for each. Why does the experiment protocol specify that all four runs must use the same evaluation query set and the same evaluation rubric? What would happen to the validity of the conclusions if different query sets were used for different runs?

### Critical Thinking Prompts

- The chapter lesson states that "chunking is the most consequential single decision in RAG pipeline design." Given that all six optimization levers (chunking, MMR, metadata filtering, re-ranking, context compression, k selection) affect context quality, what evidence would you need to evaluate whether chunking is more consequential than retrieval method selection? How would you design an experiment to test this claim?

- MMR's lambda_mult parameter must be tuned for the specific corpus and query distribution. In a production system where the corpus is continuously updated (new documents added daily), how would you monitor whether the optimal lambda_mult value has shifted? What RAGAS metric would be the leading indicator of a MMR tuning problem?

## Reading Guide 5 — Chapter 5: RAGAS Evaluation — From Subjective Impression to Structured, Reproducible Diagnosis { #reading-guide-5 }

**Sources covered:**

- Es, S., James, J., Anke, L. E., & Schockaert, S. (2024). RAGAS: Automated evaluation of retrieval augmented generation. *EACL 2024*. *(Abstract + Sections 1–2)*
- Gao, Y., et al. (2023). *(Background context on RAG failure modes)*

**Estimated study time:** ~20 minutes (Es et al. full paper preview) + ~10 minutes (Gao et al. failure modes cross-reference)

**Chapter connection:** RAGAS is the evaluation framework applied in Unit 5 and the feedback mechanism that validates the optimization experiments in Unit 4. Read the paper before the lab, not concurrently — understanding what each metric measures enables you to interpret your lab results analytically rather than descriptively.

### Overview

Es et al. (2024) introduced RAGAS to solve a reproducibility and scalability problem in RAG evaluation: human judgment-based assessment is slow, expensive, and inconsistent across evaluators. RAGAS provides four automated metrics that together cover the two critical quality dimensions of a RAG system: the quality of the retrieval (did the system retrieve the right information?) and the quality of the generation (did the LLM use the retrieved information faithfully and relevantly?). The four metrics — faithfulness, answer relevance, context precision, and context recall — form a diagnostic instrument: each metric's score points to a specific pipeline stage as the source of a quality failure.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **Faithfulness** | RAGAS metric measuring whether all claims in the generated answer are supported by the retrieved context; specifically targets hallucination (generation that contradicts or goes beyond the retrieved evidence) |
| **Answer relevance** | RAGAS metric measuring whether the generated answer directly addresses the user's question; targets generation failures where the answer is factually grounded but non-responsive to what was asked |
| **Context precision** | RAGAS metric measuring the proportion of retrieved chunks that are genuinely relevant to the query; targets retrieval failures where the retrieved context contains excessive noise |
| **Context recall** | RAGAS metric measuring the proportion of ground-truth answer information that is present in the retrieved context; requires a reference answer; targets retrieval failures where relevant information is missing from the retrieved set |
| **LLM-as-judge** | The evaluation approach used by RAGAS: a capable LLM evaluates the quality of another LLM's output by scoring it against defined criteria — enabling automated, scalable evaluation without human annotators |
| **Reference answer** | A ground-truth answer to a query, required for computing context recall; produced by human annotation or by an oracle system |
| **Hallucination** | A generated claim not supported by the retrieved context — the failure mode most directly measured by the faithfulness metric |
| **Retrieval failure** | A class of RAG failure where the retrieval stage fails to surface relevant documents, leading to a generation that cannot be grounded in evidence — diagnosed by low context recall |
| **Context overflow** | A failure mode where the retrieved context is so large that it exceeds the LLM's context window or dilutes the relevant information with irrelevant content — diagnosed by low context precision |
| **Diagnostic signature** | The specific pattern of RAGAS metric scores that identifies a particular failure mode; e.g., low faithfulness + high context recall = generation failure (the LLM ignored the retrieved evidence) |

### Guiding Questions

#### Section A — Es et al. (2024): Abstract + Sections 1–2

1. Es et al. identify the primary motivation for RAGAS as the inadequacy of human-judgment-based evaluation for RAG systems. What two properties of RAG evaluation make human judgment specifically inadequate — properties that do not apply equally to evaluating a simple text classification model?

2. The faithfulness metric measures whether all claims in the generated answer are entailed by the retrieved context. What is the mathematical formulation of this metric? Specifically, how does RAGAS operationalize "entailment" in a way that enables automated scoring without human annotators?

3. Answer relevance measures whether the answer addresses the user's question. How does RAGAS quantify this — what is the scoring mechanism? A generated answer can score high on faithfulness (all claims grounded in retrieved context) and low on answer relevance simultaneously. Construct a concrete example of this failure pattern.

4. Context precision measures the signal-to-noise ratio in the retrieved context. What specific pipeline stage (from the six-stage model) is the primary target of context precision optimization? What chunking or retrieval configuration changes would most directly improve a low context precision score?

5. Context recall requires a ground-truth reference answer — unlike the other three metrics. Why does context recall require a reference answer when faithfulness and answer relevance do not? What does context recall measure that the other metrics cannot?

#### Section B — Failure Mode Diagnosis

6. RAGAS metrics map to three RAG failure modes. Complete the following mapping from the chapter lesson:
    - Low faithfulness + high context recall → failure mode: ____ → primary remediation: ____
    - Low context recall + high faithfulness → failure mode: ____ → primary remediation: ____
    - Low context precision + low faithfulness → failure mode: ____ → primary remediation: ____

7. A RAG system produces the following RAGAS scores: faithfulness = 0.92, answer relevance = 0.88, context precision = 0.45, context recall = 0.87. Diagnose the system's primary failure mode and specify which pipeline stage is most likely responsible. Propose one concrete remediation and predict which metric would improve first if the remediation is effective.

8. A different RAG system scores: faithfulness = 0.61, answer relevance = 0.85, context precision = 0.89, context recall = 0.43. Diagnose the failure mode. Is this more likely a retrieval failure or a generation failure? Justify your diagnosis by explaining the causal pathway from pipeline stage to metric score.

9. Es et al. propose using RAGAS as a component of a CI/CD pipeline for continuous RAG quality monitoring. What does this imply about the frequency at which RAGAS evaluations should be run in production? What corpus or pipeline event would trigger an unscheduled evaluation?

### Critical Thinking Prompts

- RAGAS uses an LLM as a judge to evaluate another LLM's outputs. What is the fundamental limitation of this approach? Under what conditions might the judge LLM systematically fail to detect faithfulness violations — and what does this imply about the choice of judge model relative to the generation model?

- The chapter lesson states that RAGAS enables "rapid, reproducible, and actionable evaluation that can be integrated into a CI/CD pipeline." For a RAG system serving a high-stakes domain (medical literature, legal research), is automated RAGAS evaluation sufficient for production monitoring, or does it need to be supplemented by human evaluation? If supplemented, which failure modes most require human judgment?

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-3.2-Addendum){target=_blank} (wiki page last changed 2026-08-12). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-3/reading-guides.md){target=_blank}.</p>
