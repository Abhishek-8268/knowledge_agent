# Knowledge Agent

A terminal-based research assistant powered by LLM tool-calling. It combines conversational memory, a local SQLite database (E-commerce domain), and web search to answer user queries.

## Setup Instructions

**1. Prerequisites:** Python 3.11+ is required.

**2. Virtual Environment:**
Create and activate a virtual environment to isolate dependencies.
`python -m venv venv`

On Windows:
`.\venv\Scripts\activate`

On Mac/Linux:
`source venv/bin/activate`

**3. Install Dependencies:**
Install the required packages using the requirements file.
`pip install -r requirements.txt`

**4. Environment Variables:**
Create a `.env` file in the root directory (you can rename `.env.example` if you created one) and add your Groq API key:
`GROQ_API_KEY=your_actual_api_key_here`

## Database Seeding

To initialize the E-commerce database with ~150 rows of sample data (Customers, Products, and Orders), run the seed script:
`python database.py`

## Running the Agent

Once the database is seeded and your environment is active, start the interactive REPL:
`python main.py`

# System Architecture

## Control Flow
1. **User Input:** The user submits a natural language question via the terminal REPL in `main.py`.
2. **Agent Loop (`agent.py`):** The LLM (`llama-3.3-70b-versatile` via Groq) evaluates the prompt and the system instructions.
3. **Decision Engine:** The LLM independently decides whether to answer directly or call a tool (`query_database`, `web_search`, `read_url`, `retrieve_memory`).
4. **Tool Execution:** The requested tool runs locally in Python. The resulting data (SQL rows, web text, or past memory) is parsed into a string and appended back to the LLM's message history as a "tool" role message.
5. **Synthesis:** The LLM receives the external data, synthesizes it, and outputs the final natural language answer to the user.
6. **Persistence:** Upon a successful loop completion, `main.py` saves the Question and Answer pair to the ChromaDB vector database.

## Tool Components
* **Memory (`memory.py`):** Utilizes a local ChromaDB instance to perform vector-based semantic searches of past interactions, allowing the agent to answer follow-up questions effectively.
* **Database (`sql_tool.py`):** Translates natural language to SQL using the LLM. It validates the generated SQL against a strict, read-only Python guardrail before executing it against the `sqlite3` database.
* **Web (`web_tools.py`):** Uses the `duckduckgo-search` library for keyless, free internet searching and `BeautifulSoup4` for HTML stripping and readable content extraction.