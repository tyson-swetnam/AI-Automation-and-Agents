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
time_estimate: "Part A about 2 hours, Part B about 2 hours"
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

**Time:** Part A about 2 hours, Part B about 2 hours | **Deliverable:** this notebook, run top to bottom, with your answers typed into the *Lab Notebook* cells

**Corpus:** NIST's [AI Risk Management Framework (NIST AI 100-1)](https://doi.org/10.6028/NIST.AI.100-1) and its [Generative AI Profile (NIST AI 600-1)](https://doi.org/10.6028/NIST.AI.600-1). Both are US government publications in the public domain. The Configuration step downloads them for you.

| Part | Step | What you do | Time |
|---|---|---|---|
| A | A1 | Load the PDF corpus, inspect document metadata | ~15 min |
| A | A2 | Split into chunks, embed, persist to Chroma | ~20 min |
| A | A3 | Build a retrieval QA chain, run 5 test queries | ~15 min |
| A | A4 | Add a second corpus, re-run the queries, compare | ~10 min |
| B | Runs 1–4 | Controlled experiment: change one retrieval setting at a time, score ten evaluation questions | ~75 min |
| B | Log + RAGAS | Write up the experiment, then interpret four RAGAS scores for a non-technical reader | ~30 min |

The step times are for the work itself. Allow extra for setup, reading output, and writing your answers. On the free path, allow more for Part B — its introduction explains why.

#### How to work through this notebook

Run the cells in order — each step depends on variables defined by the one before it.

Markdown cells marked *Lab Notebook — record your answer* are where you type your findings. Fill them in as you go rather than saving them for the end. Several steps ask you to read printed output and make a judgement call; those judgements are what your submission is assessed on, not the code.

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
- `CORPUS_1` / `CORPUS_2` — where the two lab PDFs are saved. The cell after the API key cell downloads them if they are not already there, so there is nothing to upload.

```python
import os

EMBEDDING_PATH = "openai"        # "openai" | "local"
LLM_PROVIDER   = "openai"        # "openai" | "local" | "ollama" | "none"

OPENAI_EMBED_MODEL = "text-embedding-3-small"
OPENAI_CHAT_MODEL  = "gpt-4o-mini"
LOCAL_EMBED_MODEL  = "sentence-transformers/all-MiniLM-L6-v2"
LOCAL_CHAT_MODEL   = "Qwen/Qwen2.5-0.5B-Instruct"   # free-path generator
OLLAMA_CHAT_MODEL  = "llama3.1"

CORPUS_1 = "NIST.AI.100-1.pdf"   # AI RMF 1.0 - Steps A1-A3 and Part B
CORPUS_2 = "NIST.AI.600-1.pdf"   # Generative AI Profile - Step A4 and Run 4

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
# Download the two corpus PDFs if they are not here yet, and confirm they are the exact files
# this lab was written against. Part B's evaluation questions cite specific pages, so a different
# edition of either document would shift those page numbers.
import hashlib, os, urllib.request

COURSE_MATERIALS = "https://tyson-swetnam.github.io/AI-Automation-and-Agents/materials/module3"
CORPUS_FILES = {
    CORPUS_1: ("https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
               "7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1"),
    CORPUS_2: ("https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf",
               "6e73620ab6b64e90ef2c04bf0e0d6246185a2f4b1b13cab0df494496cff89b6a"),
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

for path, (nist_url, expected) in CORPUS_FILES.items():
    if not os.path.exists(path):
        # The course copy first: it is the exact file the page references were checked against.
        for url in (f"{COURSE_MATERIALS}/{os.path.basename(path)}", nist_url):
            try:
                urllib.request.urlretrieve(url, path)
                print(f"Downloaded {path} from {url}")
                break
            except Exception as err:
                print(f"Could not download from {url}: {err}")
    assert os.path.exists(path), f"{path} is missing. Download it from {nist_url} and put it next to this notebook."
    same = sha256(path) == expected
    print(f"{path}: {os.path.getsize(path):,} bytes - " +
          ("matches the lab's reference copy" if same else
           "DIFFERS from the lab's reference copy, so Part B's page numbers may not line up"))
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

The five queries below are about the AI RMF. Keep them in this list and in this order: Step A4 re-runs the same list against the expanded store, and Run 4 of the project reuses it. Not all of them are easy for the pipeline — read every answer against its sources.

```python
# The five test queries for Steps A3 and A4.
TEST_QUERIES = [
    "What are the three major categories of AI bias that NIST identifies?",
    "Which specific fairness metric does the AI RMF recommend for measuring bias?",
    "What are the four functions of the AI RMF Core?",
    "How do AI risks differ from traditional software risks?",
    "What does the AI RMF say about human oversight and human-AI interaction?",
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

**Marginal context** — the query whose sources are related but not directly answer-relevant:

**What the model did with that gap** — did it fill it from parametric knowledge, or say that the context does not answer the question? Quote the part of the answer that shows which:

> Annotate that query **`potential faithfulness issue`** either way. If the model filled the gap, you have watched a faithfulness failure happen — the reason RAGAS's faithfulness metric exists. If it declined, the system prompt's "say that you do not know" instruction did its job, and you have seen the defence that failure calls for. You come back to this case in the RAGAS interpretation at the end of Part B.

**If the model went beyond the context:** the specific claim in its answer that the retrieved chunks do not support. If it declined instead, write "declined" and quote the sentence it used:

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

```python
# Optional: the Part A numbers for your write-up, in one place.
print(f"Corpus 1 pages:       {len(documents)}")
print(f"Corpus 1 chunks:      {len(chunks)}")
print(f"Corpus 2 chunks:      {len(chunks2) if 'chunks2' in globals() else 'not loaded'}")
print(f"Collection size:      {collection_size()}")
print(f"chunk_size / overlap: {CHUNK_SIZE} / {CHUNK_OVERLAP}")
print(f"k:                    {TOP_K}")
print(f"Embeddings:           {EMBEDDING_PATH} | LLM: {LLM_PROVIDER}")
```

---
### Part B — Hands-On Project: a controlled retrieval experiment  *(~2 hours)*

Part A built one pipeline with one configuration. Part B asks which configuration works better for this corpus, and makes you answer with evidence. You run the same ten evaluation questions through three configurations, changing **one setting at a time**, and score every answer on the same rubric. A fourth, optional run tests metadata filtering on the two-corpus store from Step A4.

| Run | chunk_size / overlap | Retriever | Changed from the run before |
|---|---|---|---|
| 1 | 256 / 25 | similarity, k=4 | baseline |
| 2 | 512 / 50 | similarity, k=4 | chunk size only |
| 3 | 512 / 50 | MMR, `lambda_mult=0.5`, k=4 | retriever only |
| 4 (optional) | 512 / 50 | similarity, k=4, two corpora, with and without a corpus filter | metadata filter only |

Run 2 changes chunk size and holds the retriever fixed; Run 3 changes the retriever and holds chunk size fixed. That is the whole design: if two settings change between runs, you cannot say which one caused the difference.

**Scoring rubric.** Score each answer from 1 to 4 against the reference answer and the retrieved sources:

| Score | Meaning |
|---|---|
| 4 | Complete and grounded in the retrieved context |
| 3 | Correct but incomplete |
| 2 | Partially correct |
| 1 | Incorrect or hallucinated |

Only an answer the retrieved chunks support can earn a 4. An answer that is accurate but unsupported by its chunks is the faithfulness failure you flagged in Step A3, so score it as hallucinated. With `LLM_PROVIDER = "none"` there are no answers to score: score whether the retrieved chunks contain the reference answer instead, on the same scale, and say so in your log.

**Time on the free path.** The two-hour budget assumes the paid path. With `LLM_PROVIDER = "local"`, Part B generates about 40 answers on a small CPU model — ten questions in each of Runs 1–3, and five twice in Run 4 — and that waiting is the slowest part of the lab. Do Runs 1–3 first, and Run 4 only if you have time.

```python
# The evaluation set: ten questions about the AI RMF, each with a reference answer taken from the
# document and the page(s) that hold it. Pages are the loader's 0-based page index - the number the
# retrieval printouts show - not the page number printed in the PDF.
EVAL_SET = [
    {
        "question": "What are the characteristics of trustworthy AI systems according to the AI RMF?",
        "reference": "Valid and reliable; safe; secure and resilient; accountable and transparent; explainable and interpretable; privacy-enhanced; and fair with harmful bias managed. Valid and reliable is the base for the others, and accountable and transparent relates to all of them.",
        "pages": [7, 16],
    },
    {
        "question": "Why is GOVERN described as a cross-cutting function?",
        "reference": "It applies to all stages of an organization's AI risk management and is infused throughout the other three functions: aspects of GOVERN, especially those related to compliance or evaluation, should be integrated into MAP, MEASURE and MANAGE, which are applied in specific contexts and at specific stages of the AI lifecycle.",
        "pages": [7, 24, 26],
    },
    {
        "question": "What does risk tolerance mean in the AI RMF, and does the framework prescribe it?",
        "reference": "Risk tolerance is the organization's or AI actor's readiness to bear risk in order to achieve its objectives. The AI RMF can be used to prioritize risk but does not prescribe risk tolerance; where no established guidelines exist, organizations should define a reasonable risk tolerance themselves.",
        "pages": [11],
    },
    {
        "question": "What is an AI RMF profile, and what types of profiles does the framework describe?",
        "reference": "A profile implements the AI RMF functions, categories and subcategories for a specific setting or application. The framework describes use-case profiles (for example a hiring or fair housing profile), temporal profiles (a Current Profile and a Target Profile, whose comparison reveals gaps), and cross-sectoral profiles for risks common across sectors, such as the use of large language models. It does not prescribe profile templates.",
        "pages": [37, 38],
    },
    {
        "question": "Is use of the AI RMF mandatory for organizations?",
        "reference": "No. The Framework is intended to be voluntary, rights-preserving, non-sector-specific and use-case agnostic.",
        "pages": [6],
    },
    {
        "question": "How should organizations prioritize AI risks?",
        "reference": "By assessed risk level and potential impact. The highest risks in a context of use call for the most urgent prioritization and the most thorough risk management, and where risks are unacceptable, development and deployment should cease safely until they can be managed. Systems that interact with humans, are trained on sensitive data, or whose outputs affect people may call for higher initial priority than systems that interact only with other computational systems.",
        "pages": [11, 12],
    },
    {
        "question": "What makes measuring AI risk difficult?",
        "reference": "The AI RMF lists several challenges: risks from third-party software, hardware and data; tracking emergent risks; the lack of reliable, agreed metrics; risk that differs across stages of the AI lifecycle; risk in real-world settings differing from risk measured in the lab; inscrutable systems; and the difficulty of establishing a human baseline for comparison.",
        "pages": [9, 10],
    },
    {
        "question": "What tradeoffs between trustworthiness characteristics does the AI RMF give as examples?",
        "reference": "Interpretability versus privacy; predictive accuracy versus interpretability; and privacy-enhancing techniques that can cost accuracy under conditions such as data sparsity. It adds that highly secure but unfair, accurate but opaque, and inaccurate but secure and transparent systems are all undesirable.",
        "pages": [16, 17],
    },
    {
        "question": "Why does the AI RMF say that trying to eliminate negative risk entirely can be counterproductive?",
        "reference": "Because not all incidents and failures can be eliminated, and unrealistic expectations about risk can lead organizations to allocate resources in ways that make risk triage inefficient or impractical, or that waste scarce resources.",
        "pages": [11],
    },
    {
        "question": "Why can AI systems need more frequent maintenance than traditional software?",
        "reference": "Data, model, or concept drift can trigger corrective maintenance, and the datasets used to train AI systems can become detached from their original context or stale relative to the deployment context.",
        "pages": [42],
    },
]

print(f"{len(EVAL_SET)} evaluation questions")
```

```python
# Helpers shared by every run. Each run gets its own store built from corpus 1 alone, so runs differ
# in exactly the setting the table says they do. The chain is the Step A3 chain, pointed at a new retriever.
RUNS = {}      # run label -> {"config": ..., "results": [...]}
SCORES = {}    # run label -> your 1-4 scores, recorded after each run

def build_run_store(chunk_size, chunk_overlap, name):
    run_chunks = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap).split_documents(documents)
    for c in run_chunks:
        c.metadata["corpus"] = "corpus_1"
    # In-memory collection. Delete any earlier copy first: re-running the cell would otherwise
    # add every chunk a second time, the same trap RESET_VECTORSTORE guards against in Step A2.
    Chroma(collection_name=name, embedding_function=embedding_model).delete_collection()
    store = Chroma.from_documents(documents=run_chunks, embedding=embedding_model, collection_name=name)
    print(f"{name}: {len(run_chunks)} chunks (chunk_size={chunk_size}, overlap={chunk_overlap})")
    return store

def run_eval(label, retriever, questions, config):
    chain = RunnableParallel(question=RunnablePassthrough(), source_documents=retriever) | \
        RunnablePassthrough.assign(result=RunnableLambda(build_prompt_inputs) | answer_step)
    results = []
    for i, item in enumerate(questions, 1):
        out = chain.invoke(item["question"])
        results.append(out)
        print("=" * 78)
        print(f"{label}   Q{i}: {item['question']}")
        print("-" * 78)
        print(f"ANSWER:\n{out['result']}\n")
        if "reference" in item:
            print(f"REFERENCE (page {', '.join(map(str, item['pages']))}):\n{item['reference']}\n")
        for j, d in enumerate(out["source_documents"], 1):
            print(f"  [{j}] {d.metadata.get('corpus')} | page {d.metadata.get('page')} | "
                  f"{d.page_content[:160].strip()}...")
        print()
    RUNS[label] = {"config": config, "results": results}
```

### Run 1 — Small fixed-size chunks (baseline)

`chunk_size=256`, `chunk_overlap=25`, similarity search, `k=4`. Read every answer against its reference and its sources, then record your ten scores in the cell after the output.

```python
run1_store = build_run_store(256, 25, "run1_256")
run_eval("Run 1", run1_store.as_retriever(search_kwargs={"k": 4}), EVAL_SET,
         {"chunk_size": 256, "retriever": "similarity"})
```

```python
# Your 1-4 score for each question, in order. Replace every None before you move on.
SCORES['Run 1'] = [None, None, None, None, None, None, None, None, None, None]
```

### Run 2 — Larger fixed-size chunks

`chunk_size=512`, `chunk_overlap=50`, similarity search, `k=4`. Only the chunk size changes from Run 1.

```python
run2_store = build_run_store(512, 50, "run2_512")
run_eval("Run 2", run2_store.as_retriever(search_kwargs={"k": 4}), EVAL_SET,
         {"chunk_size": 512, "retriever": "similarity"})
```

```python
# Your 1-4 score for each question, in order. Replace every None before you move on.
SCORES['Run 2'] = [None, None, None, None, None, None, None, None, None, None]
```

#### Lab Notebook — Run 2 observation

For at least two questions, compare the chunks Run 2 retrieved with the chunks Run 1 retrieved. Did the larger chunks give more complete context, or pull more irrelevant text into it?

- Question __:
- Question __:

### Run 3 — MMR retrieval

Same store as Run 2 (`chunk_size=512`, `chunk_overlap=50`, `k=4`); only the retriever changes. Maximal Marginal Relevance balances similarity to the question against diversity among the chunks it returns. At `lambda_mult=0.5` the two get equal weight: `1` is pure similarity search, `0` is pure diversity.

```python
run3_retriever = run2_store.as_retriever(search_type="mmr", search_kwargs={"k": 4, "lambda_mult": 0.5})
run_eval("Run 3", run3_retriever, EVAL_SET, {"chunk_size": 512, "retriever": "MMR (lambda_mult=0.5)"})
```

```python
# Your 1-4 score for each question, in order. Replace every None before you move on.
SCORES['Run 3'] = [None, None, None, None, None, None, None, None, None, None]
```

#### Lab Notebook — Run 3 observation

One question where MMR returned a meaningfully different set of sources than Run 2, and whether that improved or degraded the answer:

### Run 4 (optional) — Metadata-filtered retrieval

Step A4 showed corpus 2 taking retrieval slots away from corpus 1. Run 4 tests whether a source filter wins them back. It uses the two-corpus store from Step A4 and the five Part A test queries, all of which are about the AI RMF. Each query runs twice — unfiltered, then filtered to `corpus_1` — so the filter is the only thing that changes. Score both sets.

```python
RUN4_QUESTIONS = [{"question": q} for q in TEST_QUERIES]
run_eval("Run 4 unfiltered", vectorstore.as_retriever(search_kwargs={"k": 4}), RUN4_QUESTIONS,
         {"chunk_size": CHUNK_SIZE, "retriever": "similarity, both corpora"})
run_eval("Run 4 filtered",
         vectorstore.as_retriever(search_kwargs={"k": 4, "filter": {"corpus": "corpus_1"}}),
         RUN4_QUESTIONS, {"chunk_size": CHUNK_SIZE, "retriever": "similarity, corpus_1 only"})
```

```python
# Your 1-4 scores for the five queries, unfiltered and then filtered.
SCORES["Run 4 unfiltered"] = [None, None, None, None, None]
SCORES["Run 4 filtered"]   = [None, None, None, None, None]
```

#### Lab Notebook — Run 4 observation (optional)

For which queries did the filter change the sources, and did the answers get better?

```python
# The Optimization Experiment Log, with means computed from the scores you recorded.
print(f"{'Run':<18} {'chunk_size':<11} {'retriever':<28} {'scored':<8} mean (1-4)")
print("-" * 78)
for label, run in RUNS.items():
    s = [x for x in SCORES.get(label, []) if x is not None]
    mean = f"{sum(s) / len(s):.2f}" if s else "not scored"
    print(f"{label:<18} {run['config']['chunk_size']:<11} {run['config']['retriever']:<28} "
          f"{len(s)}/{len(run['results']):<6} {mean}")
```

#### Lab Notebook — Optimization Experiment Log

| Run | chunk_size | Retriever | Mean score (1–4) | Key observation |
|---|---|---|---|---|
| Run 1 — small chunks |  |  |  |  |
| Run 2 — larger chunks |  |  |  |  |
| Run 3 — MMR |  |  |  |  |
| Run 4 — metadata filter (optional) |  |  |  |  |

**Conclusion — two paragraphs, required.**

*Paragraph 1:* the single configuration change that produced the largest quality difference between any two runs, and the mechanism — why that change affects retrieval quality the way your data shows.

*Paragraph 2:* one change that did not improve quality, and why the mechanism you expected did not produce the result.

> **What a mechanistic explanation looks like.** Not "MMR was better", but the causal path: which questions changed, what the retriever returned before and after, and why that difference reached the answer. For example: *MMR helped on questions that need evidence from several sections, because similarity search returned near-duplicate chunks from one passage while MMR's diversity term pulled chunks from different sections.* Your data may show the opposite. Explain what it does show.

#### Check your conclusion against the retrieval evidence

Write your conclusion **before** running the next cell. The cell measures something your scores cannot: for each run, how many of the four retrieved chunks came from a page that holds the reference answer, summed over the ten questions. It checks retrieval only — a run can find the right pages and still produce a poor answer, and it cannot see an answer the model made up. How far the runs separate depends on the embedding model: with OpenAI embeddings the three totals can come out close or equal. That is a result, not a mistake — say what it means for your conclusion.

```python
# Retrieval check: for each run, how many retrieved chunks came from a page holding the reference answer.
for label in ("Run 1", "Run 2", "Run 3"):
    if label not in RUNS:
        continue
    per_q = [sum(d.metadata.get("page") in item["pages"] for d in out["source_documents"])
             for item, out in zip(EVAL_SET, RUNS[label]["results"])]
    print(f"{label}: {sum(per_q):>2}/{4 * len(per_q)} chunks on a reference page   per question: {per_q}")
```

#### Lab Notebook — does the retrieval check agree with your conclusion?

If it disagrees, say which you trust and why, in one or two sentences:

---
### RAGAS metric interpretation  *(~10 min)*

RAGAS scores a RAG system automatically on four metrics. Suppose a RAGAS evaluation of a production version of this assistant returned the scores below. These are provided values for you to interpret, not output from your runs.

For each metric, write **one sentence** saying what this particular score means for the people who use the system. Write for a non-technical stakeholder who has never read the RAGAS paper: interpret the score, do not restate the definition.

| RAGAS metric | Score | What it measures | Your plain-language interpretation |
|---|---|---|---|
| Faithfulness | 0.62 | The degree to which the generated answer is grounded in the retrieved context (not in parametric knowledge). Low score = hallucination. |  |
| Answer Relevance | 0.91 | The degree to which the generated answer addresses the user's actual question. Low score = off-topic or tangential responses. |  |
| Context Precision | 0.48 | The proportion of retrieved context chunks that are actually relevant to the question. Low score = noisy retrieval. |  |
| Context Recall | 0.85 | The proportion of relevant information in the corpus that was successfully included in the retrieved context. Low score = retrieval misses. |  |

**Which pipeline stage would you fix first, and which of your runs is the evidence for that choice?**

**What did the query you flagged `potential faithfulness issue` in Step A3 show about grounding — did the model fill the gap or decline — and how does that relate to a faithfulness score of 0.62?**

---
### Before you submit

**Part A**

- [ ] Every cell ran top to bottom without errors, and the outputs are saved in the file
- [ ] A1: page count, metadata fields, and your filtering-field justification
- [ ] A2: chunk count, three inspected chunks with boundary verdicts, overlap analysis
- [ ] A3: all five answers assessed, plus the highly-relevant and marginal cases identified
- [ ] The marginal case is annotated `potential faithfulness issue`, with what the model did — filled the gap from memory, or declined — and you use it again in the RAGAS interpretation
- [ ] A4: per-query comparison, plus one documented irrelevant chunk from corpus 2

**Part B**

- [ ] Runs 1–3 used the parameters in the Part B table: Run 1 `chunk_size=256, chunk_overlap=25`; Runs 2 and 3 `chunk_size=512, chunk_overlap=50`; Run 3 `search_type="mmr", lambda_mult=0.5`; every run `k=4`
- [ ] Ten scores recorded for each of Runs 1–3, with no `None` left (Run 4 is optional)
- [ ] Run 2 and Run 3 observations written
- [ ] Experiment log table filled in, and the two-paragraph conclusion written **before** you ran the retrieval check
- [ ] Retrieval check run, and whether it agrees with your conclusion noted
- [ ] RAGAS table: four plain-language sentences, plus both questions under it answered

Save the notebook as `Module3_Lab_[YourName].ipynb` and add it to your GitHub portfolio.

<p class="course-provenance" markdown>Rendered by nbconvert from the notebook [Module-3-Lab.ipynb](../../materials/module3/Module-3-Lab.ipynb) (`docs/materials/module3/Module-3-Lab.ipynb` in the [course repository](https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module3/Module-3-Lab.ipynb){target=_blank}); outputs cleared. Spotted a problem? Fix the notebook, not this page.</p>
