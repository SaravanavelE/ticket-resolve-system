import sys
import os
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_llm
from rag.utils import setup_logger

logger = setup_logger("HallucinationChecker")

def check_hallucination(answer: str, context: str) -> dict:
    """
    Verifies if the generated answer is grounded in the retrieved context.
    Returns a dict with 'score' (0.0 to 1.0) and 'explanation'.
    """
    llm = get_llm()
    
    system_prompt = """You are a strict grading assistant.
    Given a context and an answer, evaluate whether the answer is fully grounded in the context.
    If the answer hallucinates information not present in the context, penalize it.
    
    Output a JSON object with:
    - "score": A float between 0.0 (completely hallucinated/incorrect) and 1.0 (fully grounded).
    - "explanation": A short sentence explaining the score.
    
    Do NOT output any other text, only the JSON.
    """
    
    prompt_text = f"CONTEXT:\n{context}\n\nANSWER:\n{answer}"
    
    try:
        response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=prompt_text)])
        content = response.content.strip()
        
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
            
        result = json.loads(content)
        return {
            "score": float(result.get("score", 0.0)),
            "explanation": result.get("explanation", "Failed to parse explanation.")
        }
    except Exception as e:
        logger.error(f"Hallucination check failed: {e}")
        return {"score": 0.0, "explanation": f"Error during verification: {str(e)}"}
