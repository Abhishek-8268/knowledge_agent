# Design Decisions & Tradeoffs

## LLM-Driven Tool Use vs. Hard-Coded Pipeline

**Tradeoffs:**
Allowing the LLM to dynamically choose tools (an Agentic Loop) provides immense flexibility. The agent can handle unpredictable, multi-step queries (e.g., searching the web *then* querying the database) without needing pre-programmed `if/else` logic for every possible scenario. 

However, the tradeoff is reliability and latency. LLMs can occasionally hallucinate tool arguments or get stuck in repetitive loops. Furthermore, each decision requires a network call to the LLM API, making the overall response time slower compared to a hard-coded, deterministic pipeline.

## Failure Modes & Mitigations

**1. Bad/Malicious SQL Generation:**
* **Risk:** The LLM might hallucinate columns that don't exist or generate destructive commands (e.g., `DROP TABLE`, `DELETE FROM`).
* **Mitigation:** I implemented a strict Python-level regex guardrail in `tools/sql_tool.py`. Before any SQL reaches the database, the code verifies that the query starts with `SELECT` and explicitly rejects any DDL/DML keywords (like `UPDATE`, `INSERT`, `DROP`).

**2. API Parsing and Formatting Errors:**
* **Risk:** The model might format its internal tool-call JSON incorrectly, causing the Groq API parser to fail and crash the local script.
* **Mitigation:** I implemented a `try-except` block around the LLM API call in the main agent loop. If a `400 BadRequestError` (parsing failure) occurs, the agent catches the error, prevents the crash, and sends a system message forcing the LLM to retry its generation with strict formatting.

## Handling Large Context Windows

If the context (past memory + tool results + database schema) gets too large, it will exceed the model's maximum token limit.

* **Context Length Mitigation:** The `read_url` tool explicitly truncates extracted web page text to a maximum of 2,000 characters to prevent a single long article from overflowing the context window. Additionally, I implemented a "rolling window" approach in `main.py` that only keeps the last 5 conversation turns in the active short-term prompt memory to prevent the LLM context from blowing up over a long session.