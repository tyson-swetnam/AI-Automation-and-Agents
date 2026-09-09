---
title: "Module 3 Lab: Building a RAG Pipeline with LangChain + Chroma"
description: "Read-only rendering of the Module 3 lab notebook, Building a RAG Pipeline with LangChain + Chroma, with links to open it in Google Colab or download the .ipynb file."
type: Lab
tags:
  - module-3
  - student-facing
  - lab
  - colab
  - langchain
  - ollama
  - chroma
module: 3
time_estimate: "~60 minutes"
status: stable
stale_after: "2027-09-08T00:00:00Z"
generated:
  by: "process:nbconvert"
  at: "2026-09-08T00:00:00Z"
sources:
  - id: notebook
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module3/Module-3-Lab.ipynb"
    title: "Module-3-Lab.ipynb"
    author: "team:ua-ai2s"
    last_modified: "2026-09-02T10:27:43-07:00"
---

# Module 3 Lab: Building a RAG Pipeline with LangChain + Chroma

[![Open in Colab](../../assets/colab-badge.svg)](https://colab.research.google.com/github/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module3/Module-3-Lab.ipynb){ target=_blank }

[:material-download: Download the notebook (.ipynb)](../../materials/module3/Module-3-Lab.ipynb){ .md-button }
[:fontawesome-brands-github: View on GitHub](https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module3/Module-3-Lab.ipynb){ .md-button target=_blank }

!!! warning "API keys"

    Keep API keys out of the notebook. In Colab store them as **Secrets** (the key
    icon in the left sidebar) or enter them through the `getpass` prompt the setup
    cell provides; never paste a key into a code cell, and clear outputs before you
    submit. See [Labs, Colab, and API keys](../../start-here/labs-and-notebooks.md) for the full checklist.

!!! note "Read-only rendering"

    This page is a static rendering of the notebook with all outputs cleared. To
    run the cells, open it in Google Colab with the badge above or download the
    `.ipynb` and run it in Jupyter.

**Time:** ~60 minutes | **Deliverable:** this notebook (run top to bottom) + your completed Lab Notebook answers

| Step | What you build | Time |
|---|---|---|
| A1 | Load the PDF corpus, inspect document metadata | ~15 min |
| A2 | Split into chunks, embed, persist to Chroma | ~20 min |
| A3 | Build a retrieval QA chain, run 5 test queries | ~15 min |
| A4 | Add a second corpus, re-run the queries, compare | ~10 min |

#### How to work through this notebook

Run the cells in order — each step depends on variables defined by the one before it.

Markdown cells marked *Lab Notebook — record your answer* are where you type your findings. Fill them in as you go rather than saving them for the end. Several steps ask you to read printed output and make a judgement call; those judgements are the graded part of this lab, not the code.

This notebook runs on **LangChain 1.4.0**. The install cell pins that version and the check cell that follows confirms it before you go any further.

### Setup

Run the next cell once. It pins `langchain==1.4.0` and installs the integration packages this lab needs. On Colab this takes 2–4 minutes.

Pick your path before running:

- **Paid path** — OpenAI embeddings + OpenAI chat model. Fastest, needs an API key.
- **Free path** — local `sentence-transformers/all-MiniLM-L6-v2` embeddings. No key, no cost, first run downloads ~90 MB.

The install cell covers both; you choose which one is active in the Configuration cell below.

```python
# Installs the pinned LangChain stack. Safe to re-run.
%pip install -q \
    "langchain==1.4.0" \
    "langchain-community" \
    "langchain-text-splitters" \
    "langchain-chroma" \
    "chromadb" \
    "pypdf"

# Paid path (OpenAI embeddings + chat model)
%pip install -q "langchain-openai"

# Free path (local sentence-transformers embeddings)
%pip install -q "langchain-huggingface" "sentence-transformers" "accelerate"

print("Install step finished.")
```

```python
# Verify the installed versions before going further.
# If langchain is not 1.4.0, stop and fix it here before running anything else.
from importlib.metadata import version, PackageNotFoundError

for pkg in [
    "langchain", "langchain-core", "langchain-community", "langchain-text-splitters",
    "langchain-chroma", "chromadb", "pypdf",
    "langchain-openai", "langchain-huggingface", "sentence-transformers",
]:
    try:
        print(f"{pkg:<28} {version(pkg)}")
    except PackageNotFoundError:
        print(f"{pkg:<28} (not installed)")

assert version("langchain").startswith("1."), "This lab requires LangChain 1.4.0. Re-run the install cell."
```

**Troubleshooting.** If an import below fails with a version or dependency conflict, uncomment and run the cell that follows, then restart the runtime (`Runtime > Restart session` in Colab) and re-run from the top. Do not skip the restart — Python keeps the already-imported module in memory.

```python
# TROUBLESHOOTING ONLY - uncomment and run if you hit a package conflict, then restart the runtime.
# %pip install -q --force-reinstall "langchain==1.4.0" "langchain-core" "langchain-community" "langchain-chroma"
```

### Configuration

Set your options here. Everything downstream reads these variables, so this is the only cell you need to edit for path/model choices.

- `EMBEDDING_PATH` — `"openai"` or `"local"`
- `LLM_PROVIDER` — `"openai"`, `"local"`, `"ollama"`, or `"none"`. `"local"` downloads a small model that runs on the Colab CPU, so the free path can still generate answers. Use `"none"` only if you have no model access at all: retrieval still runs and Steps A1–A2 and A4's retrieval comparison still work, but the generated answers in A3 are stubs and you will not be able to observe the faithfulness behavior the lab asks about.
- `CORPUS_1` / `CORPUS_2` — paths to the lab PDFs. On Colab, upload them to `/content/` first (file browser in the left sidebar, or the upload cell below).

```python
import os

EMBEDDING_PATH = "openai"        # "openai" | "local"
LLM_PROVIDER   = "openai"        # "openai" | "local" | "ollama" | "none"

OPENAI_EMBED_MODEL = "text-embedding-3-small"
OPENAI_CHAT_MODEL  = "gpt-4o-mini"
LOCAL_EMBED_MODEL  = "sentence-transformers/all-MiniLM-L6-v2"
LOCAL_CHAT_MODEL   = "Qwen/Qwen2.5-0.5B-Instruct"   # free-path generator
OLLAMA_CHAT_MODEL  = "llama3.1"

CORPUS_1 = "/content/Module3_Lab_Corpus.pdf"
CORPUS_2 = "/content/Module3_Lab_Corpus_2.pdf"   # used in Step A4

CHROMA_DIR        = "./chroma_db"
COLLECTION_NAME   = "module3_lab"
RESET_VECTORSTORE = True         # True wipes CHROMA_DIR before building - see the note in Step A2

CHUNK_SIZE    = 512
CHUNK_OVERLAP = 50
TOP_K         = 4

# Quiet down two noisy libraries so the lab output stays readable.
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

print(f"Embeddings: {EMBEDDING_PATH} | LLM: {LLM_PROVIDER} | chunk_size={CHUNK_SIZE} overlap={CHUNK_OVERLAP} k={TOP_K}")
```

```python
# API key. Only needed if EMBEDDING_PATH or LLM_PROVIDER is "openai".
# On Colab, prefer the key manager (key icon in the left sidebar, name the secret OPENAI_API_KEY).
import os
from getpass import getpass

if "openai" in (EMBEDDING_PATH, LLM_PROVIDER) and not os.environ.get("OPENAI_API_KEY"):
    try:
        from google.colab import userdata
        os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
        print("Key loaded from Colab secrets.")
    except Exception:
        os.environ["OPENAI_API_KEY"] = getpass("OPENAI_API_KEY: ")
        print("Key set for this session.")
else:
    print("No key needed, or key already set.")
```

```python
# Confirm the corpus files are where the config says they are.
# On Colab, uncomment the upload block if you have not uploaded them yet.
import os

# from google.colab import files
# files.upload()   # select Module3_Lab_Corpus.pdf (and _2 later); uploads land in /content/

for label, path in [("CORPUS_1", CORPUS_1), ("CORPUS_2", CORPUS_2)]:
    status = "found" if os.path.exists(path) else "MISSING"
    print(f"{label:<9} {status:<8} {path}")

assert os.path.exists(CORPUS_1), f"Upload the first corpus to {CORPUS_1} before continuing."
```

---
### Step A1 — Environment setup and document loading  *(~15 min)*

`PyPDFLoader` returns one `Document` per page. Each `Document` has two attributes: `page_content` (the extracted text) and `metadata` (a dict). The metadata dict is what you will filter on in the A4 extension, so look at it now rather than when you need it.

The import below may print a `DeprecationWarning`. This is the documented import path for `PyPDFLoader` and it works as expected — ignore the warning.

```python
# Load the first corpus. One Document per PDF page.
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(CORPUS_1)
documents = loader.load()

print(f"Loaded {len(documents)} pages from {CORPUS_1}")
```

```python
# Inspect the raw Document objects: full repr of the first one, then the metadata schema.
print("=== FULL FIRST DOCUMENT OBJECT ===")
print(documents[0])

print("\n=== METADATA FIELDS PRESENT ON DOCUMENT 0 ===")
for key, value in documents[0].metadata.items():
    print(f"  {key:<20} {type(value).__name__:<8} {value!r}")

print("\n=== FIELDS PRESENT ON EVERY DOCUMENT (safe to filter on) ===")
common = set(documents[0].metadata)
for d in documents:
    common &= set(d.metadata)
print(" ", sorted(common))

print(f"\n=== PAGE COUNT: {len(documents)} ===")
print(f"First 300 characters of page 0:\n{documents[0].page_content[:300]}")
```

#### Lab Notebook — record your answer (A1)

1. **Total pages loaded:** 

2. **Metadata fields available on each Document object:** 

3. **One field usable for retrieval filtering in the A4 extension, and why filtering on it improves precision for domain-specific queries:** 

---
### Step A2 — Text splitting and embedding generation  *(~20 min)*

`RecursiveCharacterTextSplitter` tries a list of separators in order (`\n\n`, then `\n`, then `" "`, then character-level) and takes the first one that keeps chunks under `chunk_size`. It measures size in **characters**, not tokens. `chunk_overlap` repeats the tail of one chunk at the head of the next so a sentence split across the boundary is still retrievable from at least one chunk.

The splitter copies each source page's metadata onto every chunk it produces. The cell below also tags each chunk with `corpus`, which is what makes the Step A4 comparison readable.

```python
# Split the corpus into chunks with the baseline parameters.
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)
chunks = splitter.split_documents(documents)

# Tag provenance so Step A4 can tell the two corpora apart in retrieval results.
for c in chunks:
    c.metadata["corpus"] = "corpus_1"

lengths = [len(c.page_content) for c in chunks]
print(f"Total chunks: {len(chunks)}")
print(f"Chunk length - min {min(lengths)}, median {sorted(lengths)[len(lengths)//2]}, max {max(lengths)}")
```

```python
# Three representative chunks: beginning, middle, end.
# The boundary check is a heuristic - confirm it by eye, do not just copy the label.
import re

SENTENCE_END = re.compile(r"[.!?][\"')\]]?$")

def boundary_label(text):
    return "ends at sentence boundary" if SENTENCE_END.search(text.strip()) else "ends MID-SENTENCE"

positions = {"BEGINNING": 0, "MIDDLE": len(chunks) // 2, "END": len(chunks) - 1}

for label, i in positions.items():
    c = chunks[i]
    print(f"\n{'=' * 70}\n{label} - chunk index {i} (page {c.metadata.get('page')}) - {len(c.page_content)} chars")
    print(f"VERDICT: {boundary_label(c.page_content)}")
    print("-" * 70)
    print(c.page_content)
```

```python
# Overlap check: how much text does chunk i actually share with chunk i+1?
# Measure it rather than assume it - the configured value is a ceiling, not a guarantee.
def shared_overlap(a, b, max_len=200):
    # Longest suffix of a that is also a prefix of b.
    for n in range(min(len(a), len(b), max_len), 0, -1):
        if a[-n:] == b[:n]:
            return n
    return 0

i = len(chunks) // 2
tail = chunks[i].page_content[-CHUNK_OVERLAP:]
head = chunks[i + 1].page_content[:CHUNK_OVERLAP]

print(f"Chunk {i} - last {CHUNK_OVERLAP} chars:\n  {tail!r}")
print(f"\nChunk {i + 1} - first {CHUNK_OVERLAP} chars:\n  {head!r}")

print(f"\nActual shared characters: {shared_overlap(chunks[i].page_content, chunks[i + 1].page_content)} (configured: {CHUNK_OVERLAP})")
print(f"Same source page: {chunks[i].metadata.get('page') == chunks[i + 1].metadata.get('page')}")

print("\n=== OVERLAP ACROSS EVERY ADJACENT PAIR ===")
same_page, cross_page = [], []
for j in range(len(chunks) - 1):
    n = shared_overlap(chunks[j].page_content, chunks[j + 1].page_content)
    (same_page if chunks[j].metadata.get("page") == chunks[j + 1].metadata.get("page") else cross_page).append(n)

if same_page:
    print(f"Within a page ({len(same_page):>3} pairs): min {min(same_page)}, max {max(same_page)} chars")
if cross_page:
    print(f"Across a page ({len(cross_page):>3} pairs): min {min(cross_page)}, max {max(cross_page)} chars")
print("\nOverlap is applied when a single page is split, so it does not carry across a page boundary.")
print("Actual overlap also runs a little under the configured value because separators are consumed.")
```

> ### Common mistake — read before submitting
>
> The most common Step A2 error is skipping chunk inspection and going straight to embedding. `chunk_size=512` with the default separator list can split in the middle of a table row or a bulleted list, producing chunks with fragmented meaning. That damage is invisible until the Step A3 evaluation queries return odd results. Inspecting three chunks is the diagnostic step that catches silent pipeline failures — not optional scaffolding.

#### Lab Notebook — record your answer (A2)

1. **Total chunks produced:** 

2. **Three representative chunks** (beginning / middle / end) — paste each, and note for each whether it ends at a coherent sentence boundary or mid-sentence:
   - Beginning: 
   - Middle: 
   - End: 

3. **Is `chunk_overlap=50` sufficient?** Paste the last 50 characters of one chunk and the first 50 of the next, then answer:
   - Tail: 
   - Head: 
   - Verdict and reasoning: 

#### Embedding and persistence

An embedding model maps each chunk to a fixed-length vector; Chroma stores those vectors and returns nearest neighbors at query time. The same model must be used for indexing and querying, which is why `embedding_model` is passed once here and reused everywhere.

`Chroma` comes from the `langchain-chroma` package and writes to disk automatically once you pass `persist_directory`, so there is no separate save step to call.

```python
# Build the embedding model for whichever path you selected in Configuration.
if EMBEDDING_PATH == "openai":
    from langchain_openai import OpenAIEmbeddings
    embedding_model = OpenAIEmbeddings(model=OPENAI_EMBED_MODEL)
    print(f"Using OpenAI embeddings: {OPENAI_EMBED_MODEL}")
elif EMBEDDING_PATH == "local":
    from langchain_huggingface import HuggingFaceEmbeddings
    embedding_model = HuggingFaceEmbeddings(model_name=LOCAL_EMBED_MODEL)
    print(f"Using local embeddings: {LOCAL_EMBED_MODEL}")
else:
    raise ValueError('EMBEDDING_PATH must be "openai" or "local"')

# Smoke test: confirm the model returns a vector before you spend time embedding the whole corpus.
probe = embedding_model.embed_query("test query")
print(f"Embedding dimension: {len(probe)}")
```

```python
# Embed the chunks and persist to Chroma.
# RESET_VECTORSTORE=True deletes the existing store first. Leave it True while iterating:
# re-running from_documents against a live directory appends a second copy of every chunk,
# which quietly corrupts your retrieval results and your Step A4 comparison.
import shutil, os
from langchain_chroma import Chroma

if RESET_VECTORSTORE and os.path.isdir(CHROMA_DIR):
    shutil.rmtree(CHROMA_DIR)
    print(f"Cleared {CHROMA_DIR}")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=CHROMA_DIR,
    collection_name=COLLECTION_NAME,
)

def collection_size():
    # How many vectors are in the store right now. Used again in Step A4.
    try:
        return vectorstore._collection.count()
    except Exception:
        return len(vectorstore.get(include=[])["ids"])

print(f"Indexed {collection_size()} chunks into '{COLLECTION_NAME}'")
```

```python
# Verify the store answers a similarity search and returns a Document object.
hit = vectorstore.similarity_search("test query", k=1)
print(f"Returned {len(hit)} result(s), type: {type(hit[0]).__name__}")
print(f"Metadata: {hit[0].metadata}")
print(f"Preview: {hit[0].page_content[:200]}...")
```

---
### Step A3 — Retrieval QA chain configuration and testing  *(~15 min)*

A retrieval QA chain is four steps wired together:

1. **retrieve** — the retriever pulls the top `k` chunks for the question
2. **format** — those chunks are stitched into a single context string
3. **prompt** — context and question are placed into a prompt template
4. **generate** — the model answers from that prompt

You build it explicitly below instead of calling one prebuilt helper. That costs about six extra lines and buys you an inspectable value at every stage, which is precisely what this step's diagnostic work needs. The chain returns two keys: `result` (the generated answer) and `source_documents` (the chunks the retriever actually supplied). Record both — a good answer built on bad retrieval is still a pipeline failure, and you can only see that by reading the sources.

> **Free path note.** With `LLM_PROVIDER = "local"` the generator is a small model and will give short or hedged answers. Do not read a thin answer as a retrieval failure. Judge the retrieval on the source chunks, and judge the answer against what those chunks actually contain.

```python
# Chat model. init_chat_model is the unified entry point - "provider:model" or model_provider=.
from langchain_core.output_parsers import StrOutputParser

llm = None
if LLM_PROVIDER == "openai":
    from langchain.chat_models import init_chat_model
    llm = init_chat_model(f"openai:{OPENAI_CHAT_MODEL}", temperature=0)
    print(f"Chat model: openai:{OPENAI_CHAT_MODEL}")
elif LLM_PROVIDER == "local":
    # Free path: a small instruction-tuned model pulled from Hugging Face. No account or
    # token needed - this model is public. Uses the GPU if the runtime has one, else CPU.
    # First run downloads ~1 GB. It is deliberately small, so expect short, plain answers.
    from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

    pipe = HuggingFacePipeline.from_model_id(
        model_id=LOCAL_CHAT_MODEL,
        task="text-generation",
        device_map="auto",
        pipeline_kwargs={
            "max_new_tokens": 192,
            "do_sample": False,          # deterministic, so your five queries are reproducible
            "return_full_text": False,   # return only the answer, not the prompt echoed back
        },
    )
    llm = ChatHuggingFace(llm=pipe)      # applies the model's own chat template
    print(f"Local model: {LOCAL_CHAT_MODEL}")
elif LLM_PROVIDER == "ollama":
    # Requires: %pip install -q langchain-ollama, and a running local Ollama server.
    from langchain.chat_models import init_chat_model
    llm = init_chat_model(OLLAMA_CHAT_MODEL, model_provider="ollama", temperature=0)
    print(f"Chat model: ollama:{OLLAMA_CHAT_MODEL}")
else:
    print("LLM_PROVIDER='none' - retrieval will run, but answers will be stubs.")
```

```python
# Retriever (k=4) + prompt + chain.
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Answer the question using only the context below. "
     "If the context does not contain the answer, say that you do not know. "
     "Keep the answer to three sentences or fewer.\n\nContext:\n{context}"),
    ("human", "{question}"),
])

def format_docs(docs):
    # One labeled block per retrieved chunk, so provenance survives into the prompt.
    return "\n\n".join(
        f"[{d.metadata.get('corpus', '?')} | page {d.metadata.get('page', '?')}]\n{d.page_content}"
        for d in docs
    )

def build_prompt_inputs(x):
    return {"context": format_docs(x["source_documents"]), "question": x["question"]}

if llm is not None:
    answer_step = RAG_PROMPT | llm | StrOutputParser()
else:
    answer_step = RunnableLambda(
        lambda d: "[NO LLM CONFIGURED] Top retrieved context:\n" + d["context"][:600]
    )

# Step 1 fans out: the raw question passes through, the retriever fetches chunks.
# Step 2 adds 'result' by formatting those chunks, prompting, and generating.
rag_chain = RunnableParallel(
    question=RunnablePassthrough(),
    source_documents=retriever,
) | RunnablePassthrough.assign(
    result=RunnableLambda(build_prompt_inputs) | answer_step
)

def ask(question):
    return rag_chain.invoke(question)   # -> {"question", "source_documents", "result"}

demo = ask("What is this document about?")
print(demo["result"])
print(f"\nRetrieved {len(demo['source_documents'])} source chunks.")
```

#### Run the five test queries

Replace the placeholders below with the five queries from your Lab Notebook template in the LMS. Keep them in a list — Step A4 re-runs this exact list, and the comparison only means anything if the queries are identical.

```python
# REPLACE these with the five provided test queries from your Lab Notebook template.
TEST_QUERIES = [
    "QUERY 1 - replace with the provided query",
    "QUERY 2 - replace with the provided query",
    "QUERY 3 - replace with the provided query",
    "QUERY 4 - replace with the provided query",
    "QUERY 5 - replace with the provided query",
]

assert len(TEST_QUERIES) == 5, "The lab expects exactly five test queries."
for i, q in enumerate(TEST_QUERIES, 1):
    print(f"{i}. {q}")
```

```python
# Run all five. For each, read the answer AND the retrieved chunks - you are grading the
# retrieval, not just the answer. Ask yourself: could this answer have come from this context?
A3_RESULTS = {}

for i, query in enumerate(TEST_QUERIES, 1):
    out = ask(query)
    A3_RESULTS[query] = out

    print("=" * 78)
    print(f"QUERY {i}: {query}")
    print("-" * 78)
    print(f"ANSWER:\n{out['result']}\n")
    print(f"SOURCE DOCUMENTS ({len(out['source_documents'])}):")
    for j, d in enumerate(out["source_documents"], 1):
        print(f"  [{j}] {d.metadata.get('corpus')} | page {d.metadata.get('page')}")
        print(f"      {d.page_content[:220].strip()}...")
    print()
```

#### Lab Notebook — record your answer (A3)

| # | Query | Answer produced | Are the retrieved sources visibly relevant? |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

**Highly relevant context** — the query whose sources contain the exact information needed:

**Marginal context** — the query whose sources are related but not directly answer-relevant, where the model appears to fill the gap from parametric knowledge:

> Annotate that second query **`potential faithfulness issue`**. It is the most analytically important observation in Step A3 and a direct demonstration of why RAGAS's faithfulness metric exists — you will reuse it in the Unit 5 RAGAS analysis.

**How I could tell the model went beyond the context** (specific claim in the answer with no support in the retrieved chunks):

---
### Step A4 — Multi-document extension  *(~10 min)*

Add a second corpus to the same collection, using the same splitter configuration, then re-run the identical five queries. Expanding a corpus increases recall and costs precision: there are now more plausible-looking neighbors competing for the same four slots, so some queries will surface a chunk that is topically close but useless. Finding that case is the point of the step.

```python
# Load, split, tag, and add the second corpus to the existing vector store.
import os
assert os.path.exists(CORPUS_2), f"Upload the second corpus to {CORPUS_2} first."

before = collection_size()

loader2 = PyPDFLoader(CORPUS_2)
docs2 = loader2.load()
chunks2 = splitter.split_documents(docs2)      # same splitter, same parameters
for c in chunks2:
    c.metadata["corpus"] = "corpus_2"

vectorstore.add_documents(chunks2)

after = collection_size()
print(f"Corpus 2: {len(docs2)} pages -> {len(chunks2)} chunks")
print(f"Collection size: {before} -> {after}")
```

```python
# Re-run the same five queries against the expanded store.
A4_RESULTS = {}

for i, query in enumerate(TEST_QUERIES, 1):
    out = ask(query)
    A4_RESULTS[query] = out

    mix = [d.metadata.get("corpus") for d in out["source_documents"]]
    print("=" * 78)
    print(f"QUERY {i}: {query}")
    print(f"SOURCE MIX: {mix.count('corpus_1')} from corpus_1, {mix.count('corpus_2')} from corpus_2")
    print("-" * 78)
    print(f"ANSWER:\n{out['result']}\n")
    for j, d in enumerate(out["source_documents"], 1):
        print(f"  [{j}] {d.metadata.get('corpus')} | page {d.metadata.get('page')}")
        print(f"      {d.page_content[:220].strip()}...")
    print()
```

```python
# Side-by-side summary: how many slots corpus_2 took, and whether the answer text changed at all.
print(f"{'#':<3} {'c2 chunks':<10} {'answer changed':<15} query")
print("-" * 78)

for i, query in enumerate(TEST_QUERIES, 1):
    a3, a4 = A3_RESULTS[query], A4_RESULTS[query]
    c2 = sum(1 for d in a4["source_documents"] if d.metadata.get("corpus") == "corpus_2")
    changed = "yes" if a3["result"].strip() != a4["result"].strip() else "no"
    print(f"{i:<3} {f'{c2}/{TOP_K}':<10} {changed:<15} {query[:45]}")

print("\nA changed answer is not automatically a better answer. Read both before you judge.")
```

#### Lab Notebook — record your answer (A4)

| # | Retrieved chunks now include corpus 2? | Answer quality: improved / degraded / stable | Why |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

**Irrelevant chunk introduced by the second corpus** — name the query, quote the chunk, and explain why it scored well despite being unhelpful:

**The precision tradeoff in one sentence:**

#### Optional extension — metadata filtering

This is where your A1 metadata answer pays off. A filter is applied *before* the similarity search, so the `k` slots are spent only on candidates that already satisfy the constraint. Chroma takes a `where`-style dict: `{"corpus": "corpus_2"}` for equality, `{"page": {"$lt": 5}}` for a range.

```python
# Same query, three retrieval configurations. Compare which chunks each one surfaces.
probe_query = TEST_QUERIES[0]

configs = {
    "unfiltered":       {"k": TOP_K},
    "corpus_2 only":    {"k": TOP_K, "filter": {"corpus": "corpus_2"}},
    "pages 0-4 only":   {"k": TOP_K, "filter": {"page": {"$lt": 5}}},
}

for label, kwargs in configs.items():
    docs = vectorstore.as_retriever(search_kwargs=kwargs).invoke(probe_query)
    print(f"\n{label} -> {len(docs)} chunks")
    for d in docs:
        print(f"   {d.metadata.get('corpus')} | page {d.metadata.get('page')} | {d.page_content[:90].strip()}...")
```

---
### Before you submit

- [ ] Every cell ran top to bottom without errors, and the outputs are saved in the file
- [ ] `TEST_QUERIES` holds the five provided queries, not the placeholders
- [ ] A1: page count, metadata fields, and your filtering-field justification
- [ ] A2: chunk count, three inspected chunks with boundary verdicts, overlap analysis
- [ ] A3: all five answers assessed, plus the highly-relevant and marginal cases identified
- [ ] The marginal case is annotated `potential faithfulness issue` — carry it into Unit 5
- [ ] A4: per-query comparison, plus one documented irrelevant chunk from corpus 2

```python
# Optional: dump the numbers you need for the write-up in one place.
print(f"Corpus 1 pages:       {len(documents)}")
print(f"Corpus 1 chunks:      {len(chunks)}")
print(f"Corpus 2 chunks:      {len(chunks2) if 'chunks2' in globals() else 'not loaded'}")
print(f"Collection size:      {collection_size()}")
print(f"chunk_size / overlap: {CHUNK_SIZE} / {CHUNK_OVERLAP}")
print(f"k:                    {TOP_K}")
print(f"Embeddings:           {EMBEDDING_PATH} | LLM: {LLM_PROVIDER}")
```

<p class="course-provenance" markdown>Rendered by nbconvert from the notebook [Module-3-Lab.ipynb](../../materials/module3/Module-3-Lab.ipynb) (`docs/materials/module3/Module-3-Lab.ipynb` in the [course repository](https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module3/Module-3-Lab.ipynb){target=_blank}); outputs cleared. Spotted a problem? Fix the notebook, not this page.</p>
