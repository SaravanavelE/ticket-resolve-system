import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.retriever import TicketRAG
from rag.hallucination_checker import check_hallucination

def run_tests():
    print("Initializing TicketRAG...")
    rag = TicketRAG()
    
    query = "User cannot map printer on the 3rd floor"
    print(f"\n--- Testing Retrieval for query: '{query}' ---")
    results = rag.retrieve_for_ticket(query)
    
    if not results:
        print("No results found! Have you ingested documents?")
        return
        
    context = "\n".join([r['content'] for r in results])
    print(f"Top Result Metadata: {results[0]['metadata']}")
    print(f"Top Result Snippet: {results[0]['content'][:100]}...")
    
    print("\n--- Testing Hallucination Checker ---")
    
    good_answer = "You need to restart the Print Spooler service and then remap using \\\\printserver01\\MKT-3FL-PTR."
    print(f"Testing Good Answer: '{good_answer}'")
    # Will fail if GROQ_API_KEY is dummy
    try:
        result1 = check_hallucination(good_answer, context)
        print(f"Result: {result1}")
    except Exception as e:
        print(f"LLM Error (missing key?): {e}")
    
    bad_answer = "You need to format the laptop and install a new printer driver from HP.com."
    print(f"\nTesting Bad Answer: '{bad_answer}'")
    try:
        result2 = check_hallucination(bad_answer, context)
        print(f"Result: {result2}")
    except Exception as e:
        print(f"LLM Error: {e}")

if __name__ == "__main__":
    run_tests()
