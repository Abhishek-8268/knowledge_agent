import json
from groq import Groq
from web_tools import web_search, read_url
from sql_tool import query_database
from memory import MemoryManager

# Initialize our core services
client = Groq()
memory = MemoryManager()

# 1. Define the tools so the LLM knows what they do and how to use them
agent_tools = [
    {
        "type": "function",
        "function": {
            "name": "query_database",
            "description": "Translates a natural language question into SQL, executes it against the local e-commerce database, and returns the results. Use this for questions about customers, products, or orders.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The natural language question to translate to SQL."}
                },
                "required": ["question"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Searches the internet for current events, news, or external information not found in the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_url",
            "description": "Extracts the readable text content from a specific web page URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The exact URL to read."}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_memory",
            "description": "Searches past conversation history. Use this if the user refers to something discussed earlier.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The topic to search for in memory."}
                },
                "required": ["query"]
            }
        }
    }
]

def execute_tool(tool_call) -> str:
    """Executes the correct Python function based on the LLM's decision."""
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    
    print(f"\n[Agent Thinking] * Calling Tool: {name} with arguments: {args}")
    
    try:
        if name == "query_database":
            return query_database(args["question"])
        elif name == "web_search":
            return web_search(args["query"])
        elif name == "read_url":
            return read_url(args["url"])
        elif name == "retrieve_memory":
            return memory.retrieve_context(args["query"])
        else:
            return f"Error: Unknown tool {name}"
    except Exception as e:
        return f"Tool execution failed: {str(e)}"

def run_agent(user_question: str, chat_history: list = None, max_steps: int = 5) -> str:
    """The core agentic loop."""
    
    if chat_history is None:
        chat_history = []
        
    # Automatically retrieve context on new questions
    past_context = memory.retrieve_context(user_question)
    
    messages = [
        {
            "role": "system", 
            "content": f"""You are a helpful e-commerce data assistant. You have access to tools (SQL database, Web Search, Memory).
            
            Relevant Past Conversation Context:
            {past_context}
            
            CRITICAL RULES:
            1. Conversational Memory: Always pay attention to the chat history and the Relevant Past Conversation Context provided above. If the user introduces themselves, makes small talk, or asks a casual question, respond naturally and politely WITHOUT using tools.
            2. No Tangents: When using the `query_database` tool, strictly target exactly what the user is asking. Do NOT invent broad, unrelated queries.
            3. Context Awareness: If the user asks a short follow-up (e.g., "what is its price?"), use the chat history to identify the specific item.
            4. Final Answer: Once you have the data, or if no tools are needed, output a clear, human-readable answer and stop.
            5. Sources: If you used `web_search` or `read_url`, you MUST append a 'Sources:' list (Title + URL) at the end of your final answer."""
        }
    ]
    
    # Append short-term chat history
    messages.extend(chat_history)
    
    messages.append({
        "role": "user",
        "content": user_question
    })
    
    for step in range(max_steps):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                tools=agent_tools,
                tool_choice="auto",
                temperature=0.2 # Gives the model just enough creativity to formulate a natural response
            )
        except Exception as e:
            # Our trusty guardrail from earlier
            print(f"\n[Agent Stumbled] Groq API parsing error encountered. Forcing retry...")
            messages.append({
                "role": "user", 
                "content": "Your previous tool call failed due to a formatting error. Please try calling the tool again, ensuring strict JSON compliance."
            })
            continue
            
        response_message = response.choices[0].message
        
        # THE EXIT CONDITION: If the LLM didn't call any tools, it has the final answer!
        if not response_message.tool_calls:
            return response_message.content
            
        # If it did call tools, append its request to history
        messages.append(response_message)
        
        # Execute the tools
        for tool_call in response_message.tool_calls:
            tool_result = execute_tool(tool_call)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": str(tool_result)
            })
            
    return "Agent reached maximum steps without finding a final answer."
if __name__ == "__main__":
    # Test 1: Should trigger the SQL Tool
    print("--- Test 1 ---")
    print(run_agent("How many orders are in the database?"))
    
    # Test 2: Should trigger the Web Search Tool
    print("\n--- Test 2 ---")
    print(run_agent("What are the latest changes to GSTR-3B filing rules?"))