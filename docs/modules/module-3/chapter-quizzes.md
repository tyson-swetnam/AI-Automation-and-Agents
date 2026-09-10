---
title: Module 3 Chapter Quizzes
description: Five self-evaluating five-question chapter quizzes with collapsed answer keys and per-option feedback for Module 3, Memory Architectures and Retrieval-Augmented Generation.
type: Assessment
tags:
- module-3
- student-facing
- quiz
- memory
- rag
- langchain
- chroma
- ragas
- self-assessment
- answer-key
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
# Module 3 Chapter Quizzes

These quizzes are self-evaluating. For each question, select your answer, then read the feedback section immediately below. Feedback is provided for every option — including why incorrect options are wrong — so you can diagnose your reasoning, not just verify your answer.

Each quiz has **5 questions**. Two attempts are permitted; your best score is retained. An 80% threshold (4/5) on the Chapter 2 quiz gates access to Unit 3.

## Chapter 1 Quiz — Parametric vs. Non-Parametric Memory { #chapter-1-quiz }

*Based on Reading Guide 1: Lewis et al. (2020), Bommasani et al. (2021), IBM Technology Video*

### Question 1

Bommasani et al. (2021) describe parametric knowledge as knowledge "encoded in model weights." Which statement most precisely explains why this encoding mechanism makes parametric knowledge difficult to update?

A. Parametric knowledge is stored in a proprietary format that third-party developers cannot access or modify.

B. Updating parametric knowledge requires modifying the weight values distributed across billions of parameters through a retraining process, which is computationally expensive and resets the model's behavior across all tasks — not just the target update.

C. Parametric knowledge is encrypted during training to protect the intellectual property of the training data, making post-hoc modification legally prohibited.

D. Parametric knowledge can only be updated by adding new training examples to the original training dataset, which is typically not retained after the initial training run is complete.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Parametric knowledge is not stored in a localized, addressable location — it is diffusely distributed across the billions of weight values that collectively determine model behavior. Updating a single factual claim requires retraining, which adjusts weights globally via backpropagation. This process: (1) is computationally expensive (potentially millions of dollars in compute for large models); (2) risks "catastrophic forgetting" — degrading performance on tasks not related to the target update; and (3) takes hours to weeks, making it unsuitable for knowledge that changes frequently. This is the structural reason RAG is necessary for dynamic, organization-specific knowledge.

    ❌ **A is incorrect.** The difficulty of updating parametric knowledge is not about access formats or proprietary storage — it is about the distributed, non-addressable nature of weight-based encoding. Open-source models with fully accessible weights face exactly the same update difficulty as proprietary models.

    ❌ **C is incorrect.** Model weights are not encrypted after training; the difficulty is architectural, not legal. Research on model editing (e.g., ROME, MEMIT) specifically attempts to address the difficulty of localized weight updates for open-weight models — the challenge is technical, not a legal access barrier.

    ❌ **D is incorrect** as stated. Fine-tuning (updating model weights on new data) does not require the original training dataset — it can be performed on a small domain-specific dataset. However, fine-tuning still requires compute and still risks the other problems described in option B. The answer captures a real constraint but misidentifies dataset availability as the primary obstacle.

### Question 2

Lewis et al. (2020) describe RAG as a system that "jointly reasons over parametric and non-parametric memory." A legal research assistant uses a RAG system to answer questions about recent case law. Which scenario demonstrates the critical necessity of non-parametric memory for this application?

A. The assistant must answer a question about the general principles of contract law, which are stable and well-represented in the model's training data.

B. The assistant must answer a question about a landmark Supreme Court ruling from 2019 that was widely covered and is therefore likely in the model's training data.

C. The assistant must answer a question about a district court ruling issued three months ago that postdates the model's training cutoff and is contained only in the firm's internal document corpus.

D. The assistant must answer a question requiring multi-step legal reasoning — a capability determined by the model's parametric reasoning ability, not by its memory architecture.

??? success "Show answer and feedback"

    **Correct Answer: C**

    ✅ **C is correct.** This scenario directly demonstrates both limitations that non-parametric memory addresses: (1) the ruling postdates the training cutoff, so it cannot be in the model's parametric memory regardless of how capable the model is; (2) the document is in the firm's internal corpus — proprietary, organization-specific content that would never appear in a general-purpose model's training data even if the model were retrained. The non-parametric retrieval index, built from the firm's document corpus, is the only path to a grounded answer. Without RAG, the model would either produce a hallucinated "ruling" or correctly refuse to answer.

    ❌ **A is incorrect.** General principles of contract law are stable, widely documented, and reliably encoded in any large model's parametric memory. This scenario demonstrates parametric memory working well — it does not motivate the necessity of non-parametric augmentation.

    ❌ **B is incorrect.** A widely covered 2019 ruling is highly likely to be in the training data of most modern large models (which typically have training cutoffs in 2023 or later). Parametric memory alone would handle this query reliably. This scenario does not require non-parametric memory.

    ❌ **D is incorrect.** Multi-step legal reasoning is a capability of the model's parametric reasoning architecture, not a memory architecture issue. The scenario described in D would be the same regardless of whether RAG is used — the retrieval component provides evidence; the generative component performs the reasoning. D confuses reasoning capability with memory architecture.

### Question 3

According to Lewis et al. (2020), RAG combines two distinct components. Which description most precisely identifies both components and their respective contributions?

A. A fine-tuned generative model (which encodes domain-specific knowledge) and a keyword search engine (which retrieves relevant documents by term matching).

B. A parametric generative model (which provides language understanding, reasoning, and generation capability) and a non-parametric retrieval component (which surfaces relevant documents from an external index at inference time to ground the generation).

C. A large language model (which generates responses) and a database (which stores facts that the model cannot memorize during training).

D. A question-answering model (which extracts answers from documents) and a document retriever (which selects which documents to pass to the QA model).

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Lewis et al.'s formal definition of RAG combines: (1) a parametric generative model — a sequence-to-sequence model (in the original paper, BART) that provides language understanding, multi-step reasoning, and fluent text generation from the combined input of the query and retrieved context; and (2) a non-parametric dense retrieval component (DPR — Dense Passage Retriever) that encodes documents and queries as dense vectors and retrieves the most semantically relevant documents at inference time. The non-parametric descriptor is technically precise: the retrieval index stores document representations without encoding them in model parameters, making the knowledge externally verifiable and updatable without retraining.

    ❌ **A is incorrect.** The original RAG architecture does not use a fine-tuned domain-specific generative model (fine-tuning is a separate step, not the architecture). More critically, the retrieval component is a dense semantic retriever (DPR), not a keyword search engine — semantic retrieval operates on learned dense embeddings and finds relevant passages by semantic similarity, not term co-occurrence.

    ❌ **C is incorrect** as a precise description. Describing the retrieval component as a "database that stores facts the model cannot memorize" conflates the function of an external knowledge base with the architectural role of a semantic retrieval index. The retrieval component does not store discrete facts — it stores dense vector representations of document passages and retrieves them by semantic similarity to the query.

    ❌ **D is incorrect.** The extractive QA framing (extract an answer span from a document) describes traditional reading comprehension models, not RAG. RAG is a generative architecture: the generative model produces a synthesized answer using the retrieved documents as grounding context — it does not extract a literal span. This distinction matters: RAG can synthesize information across multiple retrieved passages, which extractive QA cannot.

### Question 4

A healthcare organization deploys an LLM to help clinical staff answer questions about medication dosing. The organization argues that because the LLM was trained on extensive medical literature, non-parametric memory (RAG) is unnecessary. Which argument most effectively challenges this position?

A. LLMs cannot reason about medical information because they lack a medical license and are therefore legally prohibited from making clinical recommendations.

B. Parametric memory cannot reliably encode the organization's formulary, patient-specific contraindications, or protocol updates issued after training cutoff — all of which constitute safety-critical, institution-specific, and dynamic knowledge that is precisely the long tail Bommasani et al. identify as unreliable in parametric memory.

C. LLMs always hallucinate in medical contexts, making them unsuitable for clinical use regardless of whether RAG is added.

D. The LLM's parametric knowledge becomes outdated after six months and therefore requires quarterly retraining, which is cost-prohibitive without a RAG architecture to reduce retraining frequency.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** This argument targets the three specific failure modes of parametric memory that are most consequential in a clinical context: (1) Organization-specific knowledge — the hospital formulary, local protocols, and internal clinical guidelines are proprietary content that was never in the model's training data. (2) Temporal currency — drug approvals, dosing guideline updates, and safety alerts issued after the training cutoff are absent from parametric memory. (3) Patient-specific context — contraindications based on a specific patient's record are dynamic, individual-level knowledge that no general parametric model can encode. These are precisely the "long tail" properties Bommasani et al. identify as unreliable in parametric memory, and they are safety-critical in a clinical setting.

    ❌ **A is incorrect.** Legal prohibition is not an argument about memory architecture — it is a regulatory concern about deployment context. The argument against parametric-only systems must be grounded in the architectural limitation (inability to encode institution-specific, dynamic knowledge), not in licensing requirements.

    ❌ **C is incorrect.** While LLMs can and do hallucinate in medical contexts, the claim that they "always hallucinate" is factually false. High-capability models demonstrate reliable performance on well-represented medical knowledge questions. The challenge is not blanket unreliability but specific failures on long-tail, dynamic, and institution-specific knowledge — precisely what option B addresses.

    ❌ **D is incorrect** in its framing. The six-month figure is arbitrary and not grounded in Bommasani et al. or Lewis et al. The core argument is not primarily about retraining cost reduction (though RAG does reduce that cost) — it is about the structural impossibility of encoding organization-specific and dynamically changing knowledge in parametric weights at any retraining frequency.

### Question 5

The IBM Technology video explains that RAG "grounds" the model's generation in retrieved documents. In the context of Lewis et al.'s architecture, what does grounding technically mean, and why is it valuable?

A. Grounding means the LLM is connected to the internet in real time, enabling it to verify its answers against current web sources before generating a response.

B. Grounding means the generated answer is constrained to be consistent with and attributable to specific retrieved passages, enabling factual verification and reducing the probability of hallucination.

C. Grounding means the LLM's weights are updated based on the retrieved documents before generating the response, incorporating the new knowledge into parametric memory.

D. Grounding means the retrieved documents are summarized and added to the model's parametric knowledge base, providing a continuously updated factual foundation for generation.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Grounding in the RAG context means that the generative model's output is conditioned on the retrieved documents — technically, the retrieved passages are concatenated with the query and passed as input to the generative model, so the model's attention mechanism attends to both the query and the retrieved evidence simultaneously. This architectural conditioning means that a well-functioning RAG system generates answers consistent with the retrieved evidence rather than with potentially stale or confabulated parametric knowledge. Grounding is valuable because it: (1) reduces hallucination (claims not in the training data cannot as easily be generated if relevant evidence is present); (2) enables attribution (answers can be traced to specific source passages); and (3) makes the knowledge basis auditable.

    ❌ **A is incorrect.** Standard RAG architectures do not connect to the internet in real time — the retrieval component queries a pre-built, offline vector index. Real-time web search integration is a separate architectural pattern (sometimes called "search-augmented generation") that is not what Lewis et al. describe.

    ❌ **C is incorrect.** This describes fine-tuning, not RAG. In RAG, the model's weights are never updated during inference — the retrieved documents are provided as input context, not as gradient signals for weight updates. The non-parametric nature of RAG's retrieval component means the knowledge is in the index, not in the weights.

    ❌ **D is incorrect.** This describes a hypothetical continuous learning or knowledge base update architecture, not RAG. In the RAG architecture, retrieved documents are not added to the model's parametric memory — they remain in the external non-parametric index. The model's weights are unchanged at inference time.

## Chapter 2 Quiz — The Six-Stage RAG Pipeline { #chapter-2-quiz }

*Based on Reading Guide 2: Gao et al. (2023), Lewis et al. (2020), LangChain Documentation, KodeKloud Video*

### Question 1

Gao et al. (2023) describe six stages of the RAG pipeline. A practitioner observes that their RAG system consistently retrieves documents that are semantically related to the query but do not contain the specific information needed to answer it. At which pipeline stage is the most likely root cause, and what is the technical explanation?

A. Stage 1 (Document Ingestion) — the document loader failed to extract all text from the source PDFs, leaving relevant content unloaded.

B. Stage 3 (Embedding Generation) — the embedding model is not encoding the semantic content of the documents accurately, producing embeddings that do not capture the relevant information.

C. Stage 2 (Text Splitting / Chunking) — chunks are too large and contain the relevant information mixed with extensive irrelevant content, producing embeddings that represent a blend of topics rather than the specific information the query requires, causing retrieval of thematically related but answer-irrelevant chunks.

D. Stage 6 (Augmented Generation) — the LLM is ignoring the retrieved context and generating answers from parametric memory, making the retrieval quality irrelevant.

??? success "Show answer and feedback"

    **Correct Answer: C**

    ✅ **C is correct.** This symptom — semantically related but answer-irrelevant retrieval — is the characteristic failure mode of oversized chunks. When a chunk is too large, its embedding is a vector average over many sentences and topics. The resulting embedding is semantically similar to many queries about the general topic but is not precisely aligned to any specific query. The retriever selects chunks whose embeddings are closest to the query embedding — but if the chunk embedding blends topically relevant content with irrelevant content, the retrieved chunk may score high on thematic similarity while not containing the specific answer the query requires. Reducing chunk size (so each chunk represents a more atomic unit of information) directly addresses this failure mode.

    ❌ **A is incorrect.** Document ingestion failures typically manifest as missing document sections or entirely absent documents, not as retrieval of semantically related but answer-irrelevant content. If ingestion had failed partially, certain documents would be absent from the index entirely — retrieval would return no results or results from other documents, not topically related but answer-incomplete results.

    ❌ **B is incorrect** as the primary diagnosis. While a poor embedding model can cause retrieval quality problems, modern embedding models (OpenAI text-embedding-3-small, all-MiniLM-L6-v2) are sufficiently capable for most domain corpora. The symptom described — semantically related but not specifically answer-relevant results — is more characteristically explained by chunking granularity (Stage 2) than by embedding model failure (Stage 3).

    ❌ **D is incorrect.** Stage 6 failure (LLM ignoring retrieved context) would manifest as a faithfulness failure — the generated answer contradicts or goes beyond the retrieved context — not as a retrieval quality problem. If the retrieved chunks were answer-relevant but the LLM ignored them, answer quality might still be low, but the diagnosis and remediation would be at Stage 6, not Stage 2.

### Question 2

Gao et al. (2023) distinguish Naive RAG, Advanced RAG, and Modular RAG as three evolutionary paradigms. Which statement correctly identifies a specific limitation of Naive RAG that Advanced RAG addresses?

A. Naive RAG cannot use LLMs for generation — it uses a separate extractive QA component, which Advanced RAG replaces with a generative model.

B. Naive RAG performs a single retrieval pass on the raw user query, which may be poorly formed for embedding-based retrieval; Advanced RAG addresses this with query transformation techniques (e.g., query rewriting, HyDE) that improve the alignment between the query embedding and the relevant document embeddings before retrieval.

C. Naive RAG cannot handle PDF documents as a source format; Advanced RAG introduces PDF parsing capabilities through specialized document loaders.

D. Naive RAG is limited to a single vector store backend; Advanced RAG enables multi-source retrieval across heterogeneous databases, including relational databases and knowledge graphs.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** A fundamental limitation of Naive RAG is that it embeds the user's raw query and retrieves documents based on that embedding. User queries are often underspecified, colloquially phrased, or conceptually distant from the way the relevant information is expressed in the corpus — a phenomenon sometimes called the "query-document vocabulary mismatch." Advanced RAG addresses this with pre-retrieval query transformation techniques: query rewriting (using an LLM to rephrase the query to match corpus terminology), HyDE (generating a hypothetical document the retrieval index would return for the ideal answer, then using that document's embedding for retrieval), and multi-query retrieval (generating multiple query variants and merging the retrieved sets). These techniques systematically improve the alignment between query embedding and relevant document embeddings.

    ❌ **A is incorrect.** Both Naive and Advanced RAG use generative models. The generative component is present in all three RAG paradigms — it is the retrieval strategy and pipeline structure that evolves, not the replacement of extraction with generation.

    ❌ **C is incorrect.** Document format support (PDF, Word, HTML, etc.) is determined by the document loaders used at Stage 1, not by the RAG paradigm. Naive RAG can use PDF loaders; the paradigm distinction is about retrieval and generation strategy, not ingestion format support.

    ❌ **D is incorrect.** Multi-source retrieval across heterogeneous backends is a feature more associated with Modular RAG than with the transition from Naive to Advanced RAG. Advanced RAG's primary improvements over Naive RAG are in query transformation (pre-retrieval) and re-ranking/compression (post-retrieval), not in multi-backend integration.

### Question 3

In the six-stage RAG pipeline, the `chunk_overlap` parameter in the text splitter specifies the number of characters shared between adjacent chunks. What specific problem does chunk overlap address, and what is the engineering trade-off it introduces?

A. Chunk overlap prevents the embedding model from processing identical text twice, reducing computational cost; the trade-off is that overlapping chunks may have slightly different embeddings for the same content, introducing retrieval inconsistency.

B. Chunk overlap preserves contextual continuity across chunk boundaries — ensuring that information that spans two adjacent chunks (e.g., a sentence that begins at the end of one chunk and concludes at the start of the next) is fully represented in at least one chunk; the trade-off is increased total number of chunks and therefore increased vector store storage and indexing cost.

C. Chunk overlap ensures that every chunk has the same semantic density, preventing some chunks from containing only low-information content like headers and whitespace; the trade-off is that overlap increases the average chunk size.

D. Chunk overlap allows the retriever to return overlapping chunks as a single merged context block, reducing the total number of retrieval calls needed; the trade-off is increased latency per retrieval operation.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Without chunk overlap, the splitting algorithm cuts the document at fixed character boundaries regardless of semantic structure. Information that spans a chunk boundary — a sentence, a data value, a clause — may be split such that neither chunk contains the complete information. A reader of either chunk would encounter a fragment. Chunk overlap ensures that the last N characters of one chunk appear at the beginning of the next, so boundary-spanning information is fully represented in at least one chunk. The trade-off is real and quantifiable: with chunk_size=512 and chunk_overlap=50, each overlap region adds approximately 50 characters of duplicated content, increasing the total number of chunks relative to zero-overlap splitting and increasing vector store size and embedding computation proportionally.

    ❌ **A is incorrect.** Chunk overlap does not prevent the embedding model from processing identical text — it explicitly causes the embedding model to process the overlapping characters twice (once as part of each adjacent chunk). The motivation is not computational efficiency; it is information preservation at chunk boundaries.

    ❌ **C is incorrect.** Chunk overlap does not equalize semantic density across chunks. A chunk that begins at a document section header may still contain primarily low-information structural text regardless of overlap. Semantic chunking strategies (which split at natural boundaries) are the appropriate technique for equalizing semantic density — overlap is about boundary continuity, not density normalization.

    ❌ **D is incorrect.** Chunk overlap does not enable the retriever to merge overlapping chunks — the retriever returns individual chunk objects as stored. Overlap affects the content of each stored chunk, not the retrieval mechanism or the merging behavior. The retriever has no awareness of which chunks overlap.

### Question 4

A LangChain RAG chain composes the retriever and the generator with LCEL, so that a single invocation returns both the generated `result` and the `source_documents` the retriever supplied for that query. A practitioner runs a test query and observes that the generated answer contains a specific factual claim that does not appear in any of the returned `source_documents`. What failure mode does this observation most precisely identify?

A. A retrieval failure — the relevant source documents were not retrieved, so the model had no basis for the claim.

B. A faithfulness failure — the LLM generated a claim that is not supported by (and may contradict) the retrieved context, drawing on parametric memory rather than the retrieved evidence.

C. A context precision failure — too many irrelevant documents were retrieved, diluting the relevant context and causing the model to ignore the source documents entirely.

D. A document ingestion failure — the document containing the relevant information was not loaded into the vector store, making retrieval of that information impossible.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Because the chain carries `source_documents` alongside `result`, the output of the retrieval stage can be inspected for the very query that produced the answer. When the practitioner confirms that the factual claim in the generated answer is absent from all returned source documents, they have identified a faithfulness violation: the LLM generated a claim that is not supported by the retrieved context. This is precisely what the RAGAS faithfulness metric measures. The LLM "filled the gap" using parametric memory — a dangerous behavior in any application where answers must be attributable to verified sources. The diagnostic value of keeping the retrieved chunks in the chain's own output is exactly this: it makes faithfulness violations visible without requiring RAGAS instrumentation.

    ❌ **A is incorrect.** A retrieval failure would manifest differently: the source documents returned would be topically unrelated to the query, or no documents would be returned. In this scenario, some documents were retrieved (the practitioner can inspect them), but the generated claim is not in those documents. The retrieval component may have functioned correctly; the generation component is the failure point.

    ❌ **C is incorrect.** Low context precision (too many irrelevant documents diluting the relevant context) could contribute to generation failures, but it would not produce the specific symptom described: a generated claim absent from all source documents. Low precision typically manifests as an incomplete or imprecise answer, not as a generated claim contradicting the retrieved set.

    ❌ **D is incorrect.** An ingestion failure would mean the document is absent from the vector store — it would not appear in retrieved results. The symptom in the question is that source documents were retrieved and inspected, but the LLM's claim is absent from them. This points to a generation failure, not an ingestion failure.

### Question 5

Gao et al. (2023) identify context precision and context recall as the two main retrieval quality dimensions. An organization is building a RAG system for medical literature review, where completeness (not missing any relevant study) is more important than precision (avoiding irrelevant studies). Which configuration change most directly optimizes for this priority, and what is the trade-off?

A. Increase chunk_size from 256 to 512 tokens; this improves context recall because larger chunks contain more information per retrieval unit, but reduces precision because each chunk may contain topically mixed content.

B. Increase k (the number of retrieved chunks) from 4 to 8; this improves context recall by retrieving more candidate passages and thereby reducing the probability of missing a relevant study, but reduces context precision because more retrieved chunks increases the probability of including irrelevant content.

C. Switch from similarity search to MMR retrieval; this improves context recall by retrieving more diverse chunks, and context precision is unaffected because MMR's diversity criterion does not affect relevance scoring.

D. Reduce chunk_overlap from 50 to 0; this improves context recall because non-overlapping chunks cover more unique content per retrieval operation, while precision is maintained because each chunk is a distinct semantic unit.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Increasing k directly addresses context recall: with more retrieved chunks in the context window, the probability that a relevant study's key passage is included in the retrieved set increases. This is the most direct and interpretable lever for improving recall. The trade-off is equally direct: a larger k brings more chunks into the context window, including a higher expected number of irrelevant chunks — degrading context precision and consuming more tokens. For a medical literature review application where missing a relevant study has clinical consequences, this trade-off (more tokens, lower precision, higher recall) is explicitly justified by the application's completeness requirement. This is a canonical example of the recall-precision trade-off appearing as a practical engineering decision.

    ❌ **A is incorrect** as the best answer. Increasing chunk_size does affect the amount of information per retrieved unit, but the relationship between chunk_size and context recall is indirect and corpus-dependent. Larger chunks may improve recall for queries requiring multi-sentence evidence, but they may also reduce recall for queries where the relevant information is a short, specific data point buried in a long passage. Increasing k (B) is the more direct and predictable lever for recall.

    ❌ **C is incorrect.** MMR's diversity criterion improves coverage across distinct topics in the corpus — which can improve recall for multi-faceted queries. However, the claim that "context precision is unaffected" is incorrect: MMR may return chunks that are less similar to the query than the top-k similarity search results, potentially including less relevant content. The relationship between MMR and recall is also corpus-dependent rather than guaranteed. B is the more precise and direct intervention.

    ❌ **D is incorrect.** Reducing chunk_overlap does not reliably improve context recall. Overlap addresses information completeness at chunk boundaries; removing it may cause boundary-spanning information to be lost in some chunks. The relationship between overlap and recall depends on how much relevant information in the corpus happens to span chunk boundaries — it is not a general recall improvement strategy.

## Chapter 3 Quiz — Conversational Memory Management { #chapter-3-quiz }

### Question 1

A clinical documentation agent assists physicians during 8–10 turn patient encounters. Specific drug names, dosages, and contraindication details mentioned in early turns must be recalled exactly in later turns. Which memory pattern is most appropriate?

**A.** Summary — compresses older turns to save tokens while retaining key facts.

**B.** Window — keeps only the last *k* turns, which is sufficient for short sessions.

**C.** Buffer — stores every message verbatim, preserving complete fidelity.

**D.** Hybrid — combines summary with recent buffer, which is the recommended production default.

??? success "Show answer and feedback"

    **Correct answer: C**

    **A** ❌ — Summary memory uses lossy compression. Specific drug names and numerical dosages are precisely the details that may not survive summarization. In a clinical context where any missed detail is a patient safety risk, lossy memory is unacceptable.

    **B** ❌ — Window memory drops messages older than *k* turns. If a contraindication was mentioned in turn 2 and the window is set to k=5, that information is permanently lost by turn 8. The scenario requires recall across the full session.

    **C** ✅ — Buffer stores every message verbatim. Sessions are short (8–10 turns), so token growth will not overflow the context window. Maximum fidelity is required — every clinical detail must be preserved exactly. Both conditions align with Buffer memory.

    **D** ❌ — Hybrid is the recommended default for long, dense conversations. For a short session where complete fidelity is required, Buffer is simpler and provides the same (or better) fidelity without the complexity of managing a summary component.

### Question 2

A coding assistant handles long debugging sessions averaging 40+ turns. The user frequently references decisions made 20–30 turns ago, but also relies heavily on the last few turns of code output. Token cost must remain manageable. Which memory pattern best fits?

**A.** Buffer — ensures nothing is lost across the full session.

**B.** Window (k=5) — keeps the most recent context, which is what matters for debugging.

**C.** Summary — compresses the full session into a bounded summary.

**D.** Hybrid — rolling summary of older turns + verbatim buffer of recent turns.

??? success "Show answer and feedback"

    **Correct answer: D**

    **A** ❌ — Buffer stores all 40+ turns verbatim. At this session length, token cost grows linearly and may approach context window limits — violating the cost constraint.

    **B** ❌ — A window of k=5 discards everything beyond the last 5 turns. The scenario specifies that the user references decisions from 20–30 turns ago — Window memory cannot recall those.

    **C** ❌ — Summary compresses older turns but loses exact code snippets and specific variable names from earlier debugging steps. When the user references a decision from turn 12, the summary may not preserve the precise details needed.

    **D** ✅ — Hybrid keeps a rolling summary of older turns (preserving key decisions at low cost) and a verbatim buffer of recent turns (preserving exact code output). This satisfies both requirements: long-range context and recent fidelity, within a manageable token budget. The lesson identifies this as the recommended default for production.

### Question 3

Which statement correctly describes the role of `RunnableWithMessageHistory` in LangChain's memory architecture?

**A.** It is a memory pattern that compresses conversation history into a summary before passing it to the LLM.

**B.** It is a wrapper that connects a chain to a history store, automatically loading prior messages before each call and saving new messages after.

**C.** It replaces the need for a prompt template by injecting conversation history directly into the LLM's system prompt.

**D.** It is a LangGraph-specific component that manages typed state across graph nodes.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ — `RunnableWithMessageHistory` is not a memory pattern — it is the infrastructure that *implements* memory. Summarization is a specific pattern choice; the wrapper itself is pattern-agnostic.

    **B** ✅ — `RunnableWithMessageHistory` wraps a chain and handles the mechanics of memory: loading stored messages into the prompt before each LLM call, and saving the new exchange afterward. Each conversation is identified by a `session_id`, allowing one chain to serve many concurrent conversations.

    **C** ❌ — A prompt template with a history slot is still required. `RunnableWithMessageHistory` fills that slot with stored messages — it does not replace the template.

    **D** ❌ — This describes LangGraph State Schema, which is a different approach to memory management used for multi-agent systems. `RunnableWithMessageHistory` is a LangChain abstraction for single-agent conversational memory.

### Question 4

A student claims: "Window memory is strictly worse than Hybrid memory because Hybrid includes a buffer for recent turns and also preserves older context via summary." What is the flaw in this reasoning?

**A.** Window memory has lower token cost and simpler implementation — for applications where older context genuinely doesn't matter (e.g., a customer support bot where each issue is resolved within a few turns), the added complexity of Hybrid provides no benefit.

**B.** Window memory actually preserves older context through compression, making it equivalent to Hybrid.

**C.** Hybrid memory requires two LLM calls per turn (one for summary, one for generation), making it twice as expensive as Window in all cases.

**D.** The claim is correct — Hybrid is always preferred over Window in production systems.

??? success "Show answer and feedback"

    **Correct answer: A**

    **A** ✅ — Memory pattern selection is a cost-quality trade-off, not a universal ranking. Window memory is simpler, cheaper, and sufficient for use cases where only recent context matters. A customer support agent resolving issues in 5–8 turns gains nothing from summarizing older turns. "Strictly worse" ignores that the best pattern depends on the deployment scenario.

    **B** ❌ — Window memory does not compress older turns — it drops them entirely. This is the key distinction from Hybrid, which preserves older context via summary.

    **C** ❌ — Hybrid does add a summarization step, but the cost comparison depends on session length. For long sessions, Hybrid's bounded summary is cheaper than Buffer's unbounded growth. The claim that it's "twice as expensive in all cases" is incorrect.

    **D** ❌ — The lesson presents four patterns as trade-offs, not a hierarchy. Each pattern has a best-fit use case.

### Question 5

The Chapter 3 lesson states that for multi-agent systems (Module 4), LangGraph manages conversation state as a typed, structured graph node. Why is this preferred over `RunnableWithMessageHistory` for multi-agent applications?

**A.** LangGraph supports longer context windows than LangChain's memory abstractions.

**B.** LangGraph state is explicit, inspectable, and testable — each agent's memory is declared as typed fields in the state schema, making it possible to log, assert on, and audit state at each step.

**C.** `RunnableWithMessageHistory` cannot store messages persistently, while LangGraph automatically persists state to a database.

**D.** LangGraph is required because `RunnableWithMessageHistory` does not support `session_id` for concurrent conversations.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ — Context window size is determined by the LLM model, not by the memory framework. Both approaches face the same context window constraints.

    **B** ✅ — LangGraph State Schema makes memory explicit: all fields are declared, state is inspectable after each node execution, and the full state at each step can be logged and reviewed. For multi-agent systems where multiple agents read and write shared state, this explicitness is essential for debugging and auditability. `RunnableWithMessageHistory` is sufficient for single-agent applications but does not provide the structured, typed state that multi-agent coordination requires.

    **C** ❌ — `RunnableWithMessageHistory` can be configured with persistent backends. The distinction is not about persistence but about explicit structure and multi-agent coordination.

    **D** ❌ — `RunnableWithMessageHistory` does support `session_id` for concurrent conversations. The preference for LangGraph in multi-agent systems is about typed state structure, not session management.

## Chapter 4 Quiz — Retrieval Optimization and Context Window Management { #chapter-4-quiz }

*Based on Reading Guide 4: Gao et al. (2023) Section 5, LCEL Documentation*

### Question 1

Gao et al. (2023) state that chunking is "the most consequential single decision in RAG pipeline design." A RAG system serving a medical reference corpus consistently produces answers that are partially correct — they address the correct topic but omit critical dosing information that appears in the same passage as the correctly retrieved content. Which chunking strategy change most directly addresses this failure mode?

A. Increase chunk_overlap from 50 to 200 characters to ensure that boundary-spanning information is always fully represented in at least one chunk.

B. Switch from fixed-size chunking to semantic chunking that splits at paragraph boundaries, so that each chunk corresponds to a coherent medical concept (e.g., an indication, a dosing section, a contraindication section) rather than an arbitrary character count.

C. Reduce chunk_size from 512 to 256 tokens so that each chunk is more atomically focused, reducing the probability that irrelevant content dilutes the relevant dosing information.

D. Increase k from 4 to 8 to retrieve more candidate chunks, increasing the probability that the dosing information is present somewhere in the retrieved set.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The symptom — correct topic retrieval but missing critical dosing information from the same passage — indicates that the chunking boundary is splitting a medically coherent unit (e.g., an indication paragraph that includes both the condition description and the dosing regime) into two chunks. The condition description is in one chunk; the dosing information is in the next. Only the condition description chunk is retrieved (because it better matches the query embedding), and the dosing information is lost. Semantic chunking, which splits at paragraph or section boundaries rather than character counts, preserves medically coherent units in single chunks — the indication and its associated dosing parameters stay together, ensuring that a relevant chunk retrieved for the condition query also contains the dosing information.

    ❌ **A is incorrect.** Increasing chunk_overlap addresses boundary-spanning information within a fixed-size split, but it does not change the fundamental problem: fixed-size splitting still breaks semantic units at arbitrary points. A 200-character overlap helps preserve context across the boundary but does not guarantee that the full dosing information — which may be 500 characters long — is captured in the same chunk as the condition description.

    ❌ **C is incorrect.** Reducing chunk_size from 512 to 256 would make the chunking problem worse, not better. Smaller chunks mean that medically coherent units (indication + dosing) are even more likely to be split across multiple chunks. The symptom indicates that the problem is fragmentation of coherent medical concepts, which smaller chunks would amplify.

    ❌ **D is incorrect.** Increasing k is a recall improvement strategy — it increases the probability that any relevant chunk is in the retrieved set. But if the dosing information is in a chunk that is not similar to the query embedding (because the chunk was split from its condition context), increasing k does not guarantee its retrieval. The root cause is chunking strategy, not retrieval depth.

### Question 2

A RAG system is built on a corpus of 5,000 corporate policy documents, many of which share standard boilerplate language (e.g., the same legal disclaimer appears in 800 documents). A practitioner configures the retriever with similarity search (k=4) and observes that all four retrieved chunks frequently contain the same legal disclaimer in response to policy-related queries. Which retrieval method change most directly addresses this failure, and what parameter controls the key trade-off?

A. Switch to metadata-filtered retrieval and filter by document category to exclude legal disclaimer documents; the key trade-off is that queries genuinely about the legal disclaimers will return no results.

B. Switch from similarity search to MMR (Maximum Marginal Relevance) retrieval; the `lambda_mult` parameter controls the balance between relevance to the query and diversity among retrieved chunks — reducing lambda_mult increases the diversity penalty, reducing redundancy in the retrieved set.

C. Increase k from 4 to 8 to retrieve more chunks, which statistically increases the probability of retrieving diverse content alongside the boilerplate; no additional parameter tuning is required.

D. Switch to re-ranking with a cross-encoder, which scores each retrieved chunk on its unique informational contribution and penalizes chunks with near-identical content to already-selected chunks.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** This is the canonical scenario for which MMR was designed: a corpus with significant redundancy (the same boilerplate in 800 documents) causes similarity search to retrieve near-identical chunks because they all have high cosine similarity to any policy query. MMR addresses this by introducing a diversity penalty: after retrieving the first chunk, subsequent retrievals are scored as a weighted combination of similarity to the query and dissimilarity to already-retrieved chunks. The `lambda_mult` parameter (λ) controls this balance: at λ=1.0, MMR degenerates to pure similarity search; at λ=0.5, equal weight is given to relevance and diversity; at λ=0.0, pure diversity maximization occurs. For a high-redundancy corpus, λ values in the 0.3–0.5 range typically produce meaningfully diverse retrievals while maintaining relevance.

    ❌ **A is incorrect.** Metadata filtering by category would require a reliable taxonomy that distinguishes boilerplate documents from substantive policy documents — a classification that may not exist in the metadata and would require manual annotation. More importantly, the boilerplate appears within substantive policy documents (not in separate documents), so filtering at the document level would not address boilerplate chunks within otherwise relevant documents.

    ❌ **C is incorrect.** Increasing k from 4 to 8 does not address redundancy — it makes it worse. With similarity search, the top 8 most similar chunks for a policy query in a boilerplate-heavy corpus will likely be 8 variations of the same boilerplate, not 4 boilerplate chunks and 4 substantive chunks. Higher k amplifies the redundancy problem.

    ❌ **D is incorrect.** Re-ranking with a cross-encoder improves the precision of retrieved chunks by rescoring them for relevance to the specific query, but standard cross-encoders do not inherently penalize near-duplicate content in the retrieved set. Cross-encoders score each chunk independently for relevance; they do not apply a diversity criterion across the set. MMR's diversity penalty (B) is the correct tool for redundancy reduction.

### Question 3

The Unit 4 optimization experiment protocol specifies that each of the four experimental runs must change only one parameter at a time while holding all others constant. A student argues that varying chunk_size and retrieval method simultaneously would produce results more quickly. What is the specific methodological flaw in the student's proposed approach?

A. Varying multiple parameters simultaneously violates LangChain's API constraints — the library requires sequential parameter updates.

B. Varying chunk_size and retrieval method simultaneously produces a confounded experiment: if the mean evaluation score changes between runs, the practitioner cannot determine whether the change was caused by the chunk_size variation, the retrieval method variation, or an interaction between them — making the result uninterpretable for production decision-making.

C. Varying multiple parameters simultaneously increases the probability of a software error in the experiment configuration, introducing noise that could make either configuration appear artificially superior.

D. The Unit 4 experiment protocol specifies exactly four runs, and varying two parameters simultaneously would complete the experiment in two runs instead of four, violating the assessment rubric's requirement for four data points.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** This is the foundational principle of controlled experimentation: in a multi-variable system, varying one parameter at a time is necessary to attribute observed changes in the output metric to a specific parameter. If chunk_size and retrieval method are varied simultaneously and the mean evaluation score improves, the practitioner faces an attribution problem: the improvement may be due to (a) the chunk_size change alone, (b) the retrieval method change alone, or (c) a specific interaction between the two changes that would not occur if either were varied alone. Without knowing the specific cause, the practitioner cannot make an informed decision about which optimization to apply in production — and may mistakenly discard a beneficial change because a confounded poor change masked its benefit, or vice versa. The module explicitly identifies this as "the correct professional practice for RAG optimization."

    ❌ **A is incorrect.** LangChain imposes no API constraints preventing simultaneous parameter changes in experiment configuration. The constraint is methodological and scientific, not technical. Any LangChain chain can be configured with any combination of parameters.

    ❌ **C is incorrect.** Software error risk is a practical concern in any experiment, but it is not the primary methodological flaw in multi-variable experimentation. Even a perfectly executed experiment that varies two parameters simultaneously produces confounded results — the flaw is analytical (attribution is impossible), not operational (error probability).

    ❌ **D is incorrect.** The number of experiment runs is not the primary concern. Even if the experiment ran only two runs (one per parameter combination), the methodological flaw would be the same: results would be uninterpretable because changes cannot be attributed to specific parameters. The requirement for four runs is a design feature that enables systematic exploration, not the reason single-variable experimentation is methodologically correct.

### Question 4

Context compression (LLMLingua) introduces an additional LLM inference call to compress each retrieved chunk before context injection. Under which deployment scenario is context compression most likely to deliver a positive ROI relative to uncompressed retrieval?

A. A RAG system with small (256-token) chunks and a low-context LLM backbone (4K context window), where each retrieved chunk contains primarily relevant content and compression would remove most of the useful information.

B. A RAG system with large (1,024-token) chunks retrieved from long-form technical documents, where a typical query requires information from only 2–3 sentences within each chunk, and the LLM backbone charges per input token or has a limited context window.

C. A RAG system using MMR retrieval, where the retrieved chunks are already maximally diverse and contain minimal redundant content, making compression redundant.

D. A RAG system serving real-time queries requiring sub-second response latency, where the additional LLM inference call for compression is justified because it reduces overall token processing time.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Context compression delivers positive ROI when two conditions are simultaneously true: (1) the retrieved chunks are large (high token cost) and (2) only a portion of each chunk is relevant to the specific query. In this scenario, a 1,024-token chunk retrieved from a technical document may contain a 3-sentence relevant passage surrounded by 900 tokens of non-query-relevant content. Without compression, all 1,024 tokens are injected into the context window. LLMLingua identifies and removes the 900 tokens of non-relevant content, injecting only the ~100-token relevant passage. The ROI is: (cost of compression LLM call) vs. (savings from injecting 100 tokens instead of 1,024 tokens at the generation stage). When the generation LLM is expensive (per-token pricing), the context window is limited, or multiple chunks are retrieved, the savings at the generation stage typically exceed the compression call cost.

    ❌ **A is incorrect.** Small 256-token chunks are already compact, and if they contain primarily relevant content, compression removes useful information rather than noise. In this scenario, compression reduces context quality without meaningfully reducing token cost — the ROI is negative.

    ❌ **C is incorrect.** MMR retrieval produces diverse chunks, but diversity does not imply query-relevance of all content within each chunk. A diverse set of 512-token chunks can still contain large proportions of query-irrelevant text within each chunk. The relationship between retrieval diversity and intra-chunk relevance is independent — MMR does not make context compression unnecessary.

    ❌ **D is incorrect.** This scenario has the trade-off backwards. Context compression introduces an additional LLM inference call, which adds latency — it does not reduce overall response time for a real-time system. The benefit of compression is token cost reduction (and potentially quality improvement from removing noise), not latency reduction. For sub-second response latency requirements, context compression is typically counterindicated.

### Question 5

A practitioner profiling a RAG system finds that the retrieved context block (k=4 chunks at chunk_size=512) accounts for 68% of total input tokens per turn. They propose reducing k from 4 to 2 to cut token cost. What quantitative check must they run before adopting this change?

A. A check that the vector store contains at least 2 chunks for every query in the evaluation set — otherwise k=2 would return empty results.

B. A comparison of the mean evaluation score at k=4 vs. k=2 on the same evaluation query set and rubric, to measure how much answer quality the roughly 50% cut in retrieved context tokens costs before deciding whether the saving is worth it.

C. A check that the embedding model produces embeddings of consistent quality for both 4-chunk and 2-chunk retrieved sets, since different retrieval depths may produce embeddings with different semantic coherence.

D. A comparison of API response latency at k=4 vs. k=2, to verify that the token reduction produces a measurable latency improvement that justifies the change.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** This is the check that matters: reducing k from 4 to 2 saves approximately 50% of the retrieved context tokens but risks degrading retrieval recall — fewer retrieved chunks means lower probability of including all relevant information in the context. The only way to know whether that risk materializes is a controlled comparison — the same design as the module's retrieval experiment: hold everything else fixed, run the same evaluation queries under k=4 and k=2, score both on the same rubric, and compare the means. If quality drops by more than the token saving can justify, a different strategy is needed, such as trimming the system prompt or compressing the retrieved context.

    ❌ **A is incorrect.** A vector store with at least 2 chunks per query is trivially satisfied by any non-empty corpus — the check does not address the relevant quality risk. The meaningful question is not whether 2 chunks can be retrieved but whether 2 chunks are sufficient to answer the evaluation queries with acceptable quality.

    ❌ **C is incorrect.** Embedding model quality does not depend on k — the embedding model produces the same embedding for a given text regardless of how many chunks are retrieved. The embedding model is upstream of the retrieval step; k is a retrieval parameter, not an embedding parameter.

    ❌ **D is incorrect.** Latency improvement from k reduction is a secondary benefit — the motivation here is token cost reduction (which reduces API expense, not necessarily latency, depending on the provider's pricing and infrastructure). More importantly, demonstrating latency improvement does not address the quality risk the change introduces. The quality check in B has to come first; latency profiling is optional.

## Chapter 5 Quiz — RAGAS Evaluation: Structured, Reproducible Diagnosis { #chapter-5-quiz }

*Based on Reading Guide 5: Es et al. (2024), Gao et al. (2023)*

### Question 1

Es et al. (2024) define the faithfulness metric as measuring whether all claims in the generated answer are supported by the retrieved context. A RAG system produces the following output for a query about a drug's approved indication:

*Retrieved context:* "Drug X is approved by the FDA for the treatment of moderate-to-severe plaque psoriasis in adults."

*Generated answer:* "Drug X is approved for the treatment of moderate-to-severe plaque psoriasis in adults and has shown promising results in clinical trials for rheumatoid arthritis."

Which statement correctly identifies the faithfulness violation and its diagnostic implication?

A. There is no faithfulness violation — the generated answer accurately describes Drug X's FDA approval, and adding information about clinical trials is an appropriate use of the model's parametric knowledge.

B. The generated answer contains a faithfulness violation: the claim "has shown promising results in clinical trials for rheumatoid arthritis" is not supported by the retrieved context and represents parametric knowledge injection — generating a claim beyond the retrieved evidence. The faithfulness score for this answer would be less than 1.0, indicating hallucination.

C. The faithfulness violation is that the generated answer omits key information from the retrieved context (the specific phrase "moderate-to-severe") — faithfulness measures completeness of retrieval, not accuracy of generation.

D. There is a faithfulness violation, but it is minor — adding clinical trial information is a beneficial enhancement that improves answer quality. The faithfulness metric should not penalize factually accurate additions from parametric memory.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Faithfulness measures whether all claims in the generated answer are entailed by the retrieved context — not whether they are factually correct from the model's parametric knowledge. The claim about rheumatoid arthritis clinical trials is not present in the retrieved context. Even if this claim happens to be factually correct based on the model's training data, it constitutes a faithfulness violation because the retrieved context does not support it. In a high-stakes domain (medical, legal, financial), faithfulness violations are dangerous regardless of the factual accuracy of the parametric claim — the system cannot attribute the claim to a verifiable source, and the claim may be outdated, jurisdiction-specific, or simply incorrect. A faithfulness score < 1.0 is the diagnostic signal that the LLM is generating beyond its retrieved evidence.

    ❌ **A is incorrect.** This option commits precisely the error that faithfulness is designed to detect: treating parametric knowledge injection as "appropriate." In a RAG system deployed for medical reference, the restriction of answers to retrieved evidence is not optional — it is the primary safety guarantee. The faithfulness metric specifically flags this behavior as a failure, regardless of the claim's accuracy.

    ❌ **C is incorrect.** Faithfulness does not measure completeness of retrieval — that is context recall's domain. Faithfulness measures whether each claim in the generated answer is supported by the retrieved context. The omission of "moderate-to-severe" from the answer would be an answer relevance or accuracy concern, not a faithfulness violation (the generated answer includes this phrase correctly).

    ❌ **D is incorrect.** The faithfulness metric does penalize factually accurate additions from parametric memory, and this design choice is intentional. In domains where the system's authority derives from its ability to ground answers in cited sources, an answer that cannot be attributed to a retrieved source is less trustworthy than one that can — even if the claim happens to be correct. Faithfulness is a grounding metric, not an accuracy metric.

### Question 2

A RAG system returns the following RAGAS evaluation scores: faithfulness = 0.91, answer relevance = 0.89, context precision = 0.38, context recall = 0.84. Which failure mode does this profile most precisely diagnose, and what is the most targeted remediation?

A. The system has a generation failure — the high context recall indicates that relevant documents are being retrieved, but the high faithfulness indicates the LLM is ignoring them; the remediation is to increase the temperature parameter to encourage the model to use the retrieved context.

B. The system has a retrieval noise problem — context recall is high (the relevant information is being retrieved) but context precision is low (many irrelevant chunks are also being retrieved, consuming context window space with noise). The remediation is to improve retrieval precision through MMR, metadata filtering, re-ranking, or smaller, more semantically focused chunks.

C. The system has a hallucination problem — the low context precision indicates that the LLM is generating claims based on retrieved noise rather than on the relevant evidence. The remediation is to reduce k to eliminate the irrelevant chunks.

D. The system has a corpus coverage problem — the high context recall (0.84) is insufficient to cover the full range of queries, and context precision (0.38) indicates that half the documents in the corpus are irrelevant. The remediation is to expand the corpus with additional source documents.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** This RAGAS profile has a specific and unambiguous diagnostic signature: high faithfulness (the LLM is using the retrieved context faithfully, not hallucinating) + high answer relevance (the generated answers address the questions) + low context precision (less than 40% of retrieved chunks are genuinely relevant) + high context recall (most relevant information is present in the retrieved set). This is the textbook retrieval noise profile: the retriever is successfully finding the relevant information (high recall) but is also retrieving a large proportion of irrelevant chunks (low precision). The irrelevant chunks consume context window tokens and potentially dilute the LLM's attention, but because faithfulness is high, the LLM is not being misled by the noise — it is generating faithful answers despite it. The targeted remediations are precision-focused: MMR (reduces redundant retrievals), metadata filtering (restricts the search space), re-ranking (rescores for precision), or smaller chunks (reduces thematic mixing within each retrieved unit).

    ❌ **A is incorrect.** High faithfulness does not indicate the LLM is "ignoring" the retrieved context — it indicates the opposite: the LLM is generating answers that are well-supported by the retrieved context. Increasing temperature would not address the context precision problem and would likely decrease faithfulness.

    ❌ **C is incorrect.** Low context precision does not directly cause hallucination — that would be indicated by low faithfulness. In this profile, faithfulness is 0.91 (high), indicating that despite the noisy retrieved context, the LLM is producing faithful answers. Reducing k reduces recall along with noise; it is a blunt instrument that may make the already-low precision problem worse by removing some of the relevant chunks along with the irrelevant ones.

    ❌ **D is incorrect.** Context recall of 0.84 does not mean "insufficient corpus coverage" — it means 84% of the ground-truth answer information is present in the retrieved context, which is a strong recall score. Context precision of 0.38 does not mean "half the documents are irrelevant" — it measures the proportion of retrieved chunks (per query) that are relevant, not the proportion of documents in the corpus. Expanding the corpus would likely worsen precision further by increasing the retrieval candidate pool without improving the retrieval algorithm.

### Question 3

Es et al. (2024) describe RAGAS as using an "LLM-as-judge" approach to automated evaluation. Which scenario most precisely identifies a condition under which the LLM-as-judge approach would systematically underdetect faithfulness violations?

A. The judge LLM is a smaller, less capable model than the generation LLM, causing it to miss faithfulness violations that require domain expertise to detect.

B. The judge LLM and the generation LLM are from the same model family and trained on the same data, so both models share the same parametric biases — if the generation LLM believes a claim is true (even if the retrieved context does not support it), the judge LLM may also consider it plausible and score it as faithful.

C. The judge LLM has a smaller context window than the generation LLM, causing it to truncate the retrieved context when evaluating faithfulness — missing violations in the truncated portion.

D. The judge LLM is evaluated at a higher temperature than the generation LLM, causing stochastic variation in faithfulness scores that reduces their reliability.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** This is the fundamental limitation of LLM-as-judge for faithfulness evaluation: the judge is asked to determine whether a claim in the generated answer is supported by the retrieved context. If the judge LLM independently "knows" (from its own parametric memory) that the claim is factually correct, it may score the claim as entailed by the context even when the context does not actually contain the supporting evidence. This is especially problematic when the judge and the generation model share a training distribution — the same biases and parametric beliefs are encoded in both. For high-stakes domains where faithfulness to retrieved evidence is a safety requirement, this shared-bias failure mode may cause the evaluation to systematically underreport violations. The practical implication: the judge model should be from a different model family or should be calibrated against human evaluation on domain-specific faithfulness test cases.

    ❌ **A is incorrect** as stated. Model capability matters, but the primary failure mode for faithfulness evaluation is not capability — it is shared-bias contamination. A smaller model may miss subtle violations, but the systematic underdetection risk identified in the RAGAS literature is specifically about the judge's own parametric knowledge interfering with its ability to evaluate context-grounding objectively.

    ❌ **C is incorrect.** Context window truncation is a practical implementation concern, not the primary methodological limitation of LLM-as-judge identified by Es et al. Modern judge models used in RAGAS evaluations typically have context windows sufficient for the retrieved context + generated answer combination. If truncation occurs, it is a configuration error, not a systematic bias.

    ❌ **D is incorrect.** Evaluation temperature is typically set to 0 (or near 0) for judge LLMs to ensure deterministic, reproducible scoring. Stochastic variation from high temperature would be a configuration error, not a systematic bias of the LLM-as-judge approach.

### Question 4

A different RAG system produces the following RAGAS scores: faithfulness = 0.58, answer relevance = 0.86, context precision = 0.87, context recall = 0.39. Which prioritized remediation plan most precisely targets the highest-severity failure mode?

A. Priority 1: Improve answer relevance by refining the system prompt to instruct the LLM to address the user's question more directly. Priority 2: Address faithfulness by switching to a smaller, less creative LLM.

B. Priority 1: Improve context recall by increasing k or expanding the corpus — the low context recall (0.39) means the relevant information for 61% of ground-truth answer components is not being retrieved, starving the LLM of the evidence it needs to generate faithful answers. Priority 2: Address faithfulness by investigating whether the generation failures are caused by the LLM filling in with parametric knowledge when relevant context is unavailable.

C. Priority 1: Improve context precision (already at 0.87 — no action needed). Priority 2: Improve faithfulness by adding a post-generation fact-checking step using a cross-encoder.

D. Priority 1: Improve context recall by reducing chunk_size from 512 to 256 — smaller chunks cover more of the corpus per retrieval operation, improving recall coverage. Priority 2: Faithfulness will improve automatically once recall improves.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** This RAGAS profile is the inverse of Question 2's profile and has its own unambiguous diagnostic signature: low context recall (0.39) + high context precision (0.87) + low faithfulness (0.58). This is a retrieval gap profile: the retriever is finding highly relevant chunks when it retrieves (high precision) but is systematically missing a large portion of the relevant corpus content (low recall, meaning 61% of ground-truth answer components are not present in the retrieved set). With only 39% of the necessary evidence in the context window, the LLM faces a choice at each turn: refuse to answer (unhelpful), generate an incomplete answer (low quality), or fill the evidence gap with parametric knowledge (faithfulness violation). The low faithfulness score (0.58) is the direct consequence of this evidence gap — not a generation failure independent of retrieval. Remediation must target recall first: increase k, expand corpus coverage, improve chunking granularity, or use query transformation to retrieve from underrepresented corpus regions.

    ❌ **A is incorrect.** Answer relevance at 0.86 is a strong score — the generated answers do address the user's questions. There is no answer relevance problem to address. Additionally, switching to a smaller LLM to address faithfulness is a blunt intervention that would likely degrade all other metrics; the correct diagnosis attributes faithfulness failures to the retrieval gap, not to generation creativity.

    ❌ **C is incorrect.** Context precision at 0.87 is healthy and requires no intervention — correctly identified. However, the proposed remediation for faithfulness (adding a post-generation fact-checking step) addresses a symptom rather than the root cause. If faithfulness is low because the LLM is filling retrieval gaps with parametric knowledge, fact-checking will flag the violations but will not reduce their frequency. Improving context recall (B) reduces the frequency of the gap-filling behavior at its source.

    ❌ **D is incorrect.** Reducing chunk_size from 512 to 256 increases the number of chunks but does not guarantee improved context recall. Recall is affected by whether the relevant information is being retrieved — which depends on the query-embedding alignment and k, not just chunk granularity. Smaller chunks may improve precision within each retrieved unit but can reduce recall if the relevant information is spread across now-smaller chunks that are less likely to be retrieved. Additionally, "faithfulness will improve automatically once recall improves" understates the remediation — while improving recall is the correct priority, faithfulness must be monitored independently after recall improvement to confirm that the generation failures were retrieval-driven.

### Question 5

Es et al. (2024) propose integrating RAGAS evaluation into a CI/CD pipeline for continuous RAG quality monitoring. A team maintains a RAG system over a corporate knowledge base that is updated weekly with new policy documents. Which trigger event most precisely justifies an unscheduled, immediate RAGAS evaluation run?

A. The LLM provider announces a new, more capable model version — because the new model's parametric knowledge distribution may interact differently with the retrieval component, producing unpredictable changes in faithfulness and answer relevance.

B. The weekly corpus update adds a large batch of documents containing significant revisions to existing policy content — because revised policy content may create conflicting information between old and new document versions in the vector store, specifically degrading context precision and potentially faithfulness if the LLM retrieves outdated chunks alongside new ones.

C. A developer changes the system prompt — because prompt changes directly affect answer relevance, and the RAGAS evaluation must be run to confirm that the new prompt does not reduce answer relevance below the established baseline.

D. User session volume increases by 30% in a week — because higher session volume increases the probability that edge-case queries are submitted, and RAGAS evaluation is needed to assess performance on the expanded query distribution.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Among all the trigger events listed, adding revised policy documents to the corpus most precisely creates a specific and predictable RAGAS failure risk that requires immediate evaluation. When new documents revise existing policy content, the vector store may contain both the old version (from a prior ingestion) and the new version of the same policy. A query about the policy may retrieve chunks from both versions simultaneously — producing low context precision (some retrieved chunks contain outdated information) and low faithfulness (if the LLM reconciles conflicting versions by generating a synthesized answer not fully supported by either). This is a corpus integrity failure with a predictable RAGAS signature that should be evaluated immediately — not deferred to the next scheduled evaluation cycle when users may already be receiving incorrect policy information.

    ❌ **A is incorrect** as the highest-priority trigger. Model version changes do create RAGAS evaluation obligations, but they represent a scheduled, planned event (the team chose to upgrade the model) rather than an emergent corpus integrity risk. Model upgrade evaluations should be conducted as part of the upgrade process, but they do not represent an unscheduled risk in the same way that corpus revision conflicts do.

    ❌ **C is incorrect.** Prompt changes are a planned configuration change that should be evaluated before deployment (part of a normal CI/CD gate), not after. The appropriate protocol is to run RAGAS evaluation as part of the prompt change deployment pipeline — if a prompt change is deployed without prior evaluation, the team has a process failure, not a trigger for an unscheduled evaluation.

    ❌ **D is incorrect.** Increased session volume does not change the RAG system's quality on existing query types — it changes the probability of encountering low-frequency edge cases. This is a valid long-term monitoring concern (the evaluation set may not cover edge cases adequately) but does not represent a specific, immediate RAGAS failure risk that justifies an unscheduled evaluation run. A volume increase in itself does not degrade the pipeline — corpus integrity failures do.

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-3.2-Addendum){target=_blank} (wiki page last changed 2026-08-12). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-3/chapter-quizzes.md){target=_blank}.</p>
