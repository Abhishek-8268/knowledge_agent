import sys
from agent import run_agent, memory 

def main():
    print("==================================================")
    print("🧠 Knowledge Agent Initialized.")
    print("Type 'exit' or 'quit' to end the session.")
    print("==================================================\n")

    chat_history = []
    
    while True:
        try:
            # 1. READ
            user_question = input("\nUser > ")
            
            if user_question.strip().lower() in ['exit', 'quit']:
                print("Ending session. Goodbye!")
                break
                
            if not user_question.strip():
                continue

            # 2. EVALUATE
            print("Agent is thinking...")
            answer = run_agent(user_question, chat_history=chat_history)
            
            # Update short-term memory (keep last 5 interactions to avoid huge prompts)
            chat_history.append({"role": "user", "content": user_question})
            chat_history.append({"role": "assistant", "content": answer})
            if len(chat_history) > 10:
                chat_history = chat_history[-10:]
            
            # 3. PRINT
            print(f"\nAgent > {answer}\n")
            print("-" * 50)
            
            # 4. PERSISTENCE (Save to Memory)
            memory.save_turn(user_question, answer)

        except KeyboardInterrupt:
            # Handles if the user presses Ctrl+C
            print("\nSession interrupted. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")

if __name__ == "__main__":
    main()