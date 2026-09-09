---
title: 'Module 3: Additional Suggested Resources'
description: Supplementary notes for Module 3 explaining parametric vs. non-parametric agent memory, the six-stage RAG pipeline with its design decisions and consequences, the RAGAS faithfulness metric, and text-splitting strategies.
type: Resource List
tags:
- module-3
- student-facing
- resources
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
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-3:-Additional-Suggested-Resources
  title: 'AI Automation and Agents v2 wiki: Module-3:-Additional-Suggested-Resources'
  author: Carlos Lizárraga-Celaya
  last_modified: '2026-06-25T13:40:03-07:00'
authorship:
  created: '2026-05-10'
  updated: '2026-05-10'
  contributors:
  - C. Lizárraga
wiki_page: Module-3:-Additional-Suggested-Resources
---
# Module 3: Additional Suggested Resources

## Primary Classes of Memory

**Parametric memory** refers to the static knowledge encoded directly into an LLM's neural network weights during its initial training phase. 

**Non-parametric memory** is information that the agent dynamically retrieves from external sources—like databases, APIs, or documents—at the exact time of a user's request, often using Retrieval-Augmented Generation (RAG) pipelines. 

Non-parametric memory is essential because an LLM's parametric memory is frozen after training and only contains public data. To act on private, domain-specific, or real-time information, an agent must be able to retrieve and read external data directly within its context window. This allows the agent to provide accurate, up-to-date answers without requiring constant, expensive model retraining.

## RAG Pipeline

The RAG pipeline operates through six interconnected stages:

*   **Document Ingestion:** Raw documents are loaded into the pipeline to serve as the external knowledge base. 
*   **Text Splitting:** Text is divided using strategies like fixed-size, recursive, semantic, or sentence-window chunking. *Decision:* Setting the optimal chunk size and overlap. *Consequence:* Determines how efficiently the LLM's context window is used; poor chunking can break apart related concepts or waste token budgets.
*   **Embedding Generation:** Text chunks are converted into mathematical vectors using pre-trained models like OpenAI Ada-002 or sentence-transformers. *Decision:* Selecting the embedding model. *Consequence:* Dictates the semantic accuracy of how information is mapped and compared.
*   **Vector Store Indexing:** The generated embeddings are ingested into a vector database, such as FAISS, Chroma, or Pinecone. *Decision:* Database selection. *Consequence:* Impacts retrieval latency, scalability, and integration capabilities.
*   **Similarity Retrieval:** The system retrieves the most relevant document chunks using similarity searches, Maximum Marginal Relevance (MMR), or metadata filtering and re-ranking. *Decision:* Choosing the search and filtering methodology. *Consequence:* Directly dictates context precision and recall; failures at this stage lead to context irrelevance or complete retrieval failure.
*   **Augmented Generation:** The retrieved context is combined with the user's prompt to generate the final response. *Decision:* Dynamic prompt construction and applying context compression. *Consequence:* Ultimately determines the answer's faithfulness and relevance, directly impacting whether the model hallucinates.

**RAGAS**

The RAGAS framework evaluates "faithfulness" to measure whether the model's generated answer is entirely grounded in the retrieved context documents. This metric specifically helps identify hallucinations by ensuring the AI hasn't invented information that wasn't provided by the retrieval pipeline.

**Choosing different text splitting strategies**

You choose a text splitting strategy based on your data's structure and how you need to manage the LLM's finite context window. 

*   **Fixed-size or recursive chunking:** Good general-purpose methods to strictly manage your token budget, though they run the risk of breaking apart related concepts.
*   **Sentence-window chunking:** Best when you want to pinpoint a specific sentence for an answer but need to feed the LLM the surrounding text so it understands the broader context.
*   **Semantic chunking:** Ideal for complex documents because it analyzes the meaning of the text to keep closely related ideas together.

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-3:-Additional-Suggested-Resources){target=_blank} (wiki page last changed 2026-06-25). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-3/resources.md){target=_blank}.</p>
