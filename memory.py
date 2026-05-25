import chromadb

class MemoryManager:
    def __init__(self, persist_directory: str = "./memory_db"):
        # Initialize a local Chroma vector store
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="conversation_history")
        # Keep a basic counter for generating unique document IDs
        self.interaction_count = self.collection.count()

    def save_turn(self, question: str, answer: str):
        """Saves a question-answer pair to the vector database."""
        document = f"User asked: {question}\nAgent answered: {answer}"
        self.interaction_count += 1
        doc_id = f"turn_{self.interaction_count}"
        
        self.collection.add(
            documents=[document],
            metadatas=[{"question": question}],
            ids=[doc_id]
        )

    def retrieve_context(self, current_question: str, n_results: int = 2) -> str:
        """Retrieves relevant past conversations based on the new question."""
        if self.collection.count() == 0:
            return "No prior memory available."
            
        # Perform a semantic similarity search
        results = self.collection.query(
            query_texts=[current_question],
            n_results=min(n_results, self.collection.count())
        )
        
        retrieved_docs = results['documents'][0]
        if not retrieved_docs:
            return "No relevant past memory found."
            
        return "\n\n---\n\n".join(retrieved_docs)

if __name__ == "__main__":
    mem = MemoryManager()
    print("Testing Memory Save...")
    mem.save_turn("What is my top customer?", "Your top customer is Abhishek in New Delhi.")
    
    print("\nTesting Memory Retrieval...")
    # Notice we ask a different phrasing, but the vector DB understands the semantic meaning
    print(mem.retrieve_context("Who did we say was the best customer?"))