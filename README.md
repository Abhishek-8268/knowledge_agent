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
