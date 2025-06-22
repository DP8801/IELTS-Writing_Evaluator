import os
import requests
import uvicorn
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from enum import Enum
from typing import List, Dict, Optional
import json
import re
import logging
# import ollama

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ollama API URL
OLLAMA_API_URL = "http://localhost:11434/api/"

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define the task types
class TaskType(str, Enum):
    TASK1 = "task1"  # Letter writing
    TASK2 = "task2"  # Essay writing

# Input models
class WritingSubmission(BaseModel):
    task_type: TaskType
    question: str
    response: str
    model: str  # New field for selecting model ("chatGPT" or "llama3.2")

# Rating criteria models
class Criterion(BaseModel):
    score: float
    feedback: str

class DetailedRating(BaseModel):
    task_achievement: Criterion
    coherence_cohesion: Criterion
    lexical_resource: Criterion
    grammatical_range: Criterion
    overall_score: float
    overall_feedback: str

# Response model
class RatingResponse(BaseModel):
    rating: DetailedRating
    debug_info: Optional[Dict] = None  # For debugging purposes

# Create FastAPI app
app = FastAPI(
    title="IELTS Writing Rating API",
    description="API for rating IELTS General Training writing tasks using OpenAI or Ollama",
    version="1.1.0"
)

def count_words(text: str) -> int:
    """Count the number of words in a text."""
    return len(text.split())

def evaluate_with_llm(submission: WritingSubmission) -> tuple[Optional[DetailedRating], Dict]:
    """Use OpenAI or Ollama (Llama3.2) to evaluate the writing submission."""
    model_name = submission.model.lower()  # Ensure lowercase handling
    debug_info = {}
    word_count = count_words(submission.response)
    
    prompt = f"""
    You are a certified IELTS examiner, assessing the following {submission.task_type} response according to official IELTS scoring criteria.

    ### **IELTS Assessment Criteria:**
    - **Task Achievement** (For Task 1) / **Task Response** (For Task 2): Relevance, clarity, and completeness of the answer.
    - **Coherence & Cohesion**: Logical organization, paragraphing, and use of linking words.
    - **Lexical Resource**: Range, accuracy, and appropriateness of vocabulary.
    - **Grammatical Range & Accuracy**: Variety and correctness of sentence structures.
    - **Overall Band Score**: The final IELTS writing band score (0-9, increments of 0.5).

    ---
    ### **Task Question:**
    {submission.question}

    ### **Student Response ({word_count} words):**
    {submission.response}

    ---
    ### **Instructions:**
    - **Rate the response fairly** based on **IELTS standards**, avoiding extreme scores unless justified.
    - Provide a **detailed but concise** explanation for each category.
    - Ensure **balanced feedback** with both strengths and weaknesses.
    - Assign **scores in 0.5 increments** to match IELTS standards.

    ---
    ### **Return JSON Format** (Use realistic scores and feedback):
    {{
    "task_achievement": {{ 
        "score": [realistic_score], 
        "feedback": "[Explain how well the response answers the question. Mention strengths and areas for improvement.]" 
    }},
    "coherence_cohesion": {{ 
        "score": [realistic_score], 
        "feedback": "[Assess logical flow, paragraphing, and use of linking words. Highlight improvements.]" 
    }},
    "lexical_resource": {{ 
        "score": [realistic_score], 
        "feedback": "[Evaluate vocabulary range and accuracy. Mention strong word choices and any misused words.]" 
    }},
    "grammatical_range": {{ 
        "score": [realistic_score], 
        "feedback": "[Review sentence structures, grammatical errors, and complexity. Suggest improvements.]" 
    }},
    "overall_score": [realistic_overall_score],
    "overall_feedback": "[Summarize the response quality, key strengths, and areas for improvement.]"
    }}
    """


    try:
        if model_name == "chatgpt":
            import openai
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY environment variable is not set.")
            
            client = openai.OpenAI(api_key=OPENAI_API_KEY)

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are an IELTS examiner."},
                          {"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=500
            )
            response_content = response.choices[0].message.content

        elif model_name == "llama3.2":
            # ✅ Use Ollama's Python SDK instead of HTTP requests
            response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
            response_content = response['message']['content']  # Extract text response

        else:
            raise ValueError("Invalid model selection. Choose 'chatGPT' or 'llama3.2'.")

        debug_info["response_preview"] = response_content[:200] + "..." if len(response_content) > 200 else response_content
        
        # Extract JSON response
        json_match = re.search(r'({[\s\S]*})', response_content)
        if json_match:
            json_str = json_match.group(1)
        else:
            raise ValueError("Could not extract JSON from model response")
        
        rating_data = json.loads(json_str)
        
        return DetailedRating(
            task_achievement=Criterion(score=float(rating_data["task_achievement"]["score"]), feedback=rating_data["task_achievement"]["feedback"]),
            coherence_cohesion=Criterion(score=float(rating_data["coherence_cohesion"]["score"]), feedback=rating_data["coherence_cohesion"]["feedback"]),
            lexical_resource=Criterion(score=float(rating_data["lexical_resource"]["score"]), feedback=rating_data["lexical_resource"]["feedback"]),
            grammatical_range=Criterion(score=float(rating_data["grammatical_range"]["score"]), feedback=rating_data["grammatical_range"]["feedback"]),
            overall_score=float(rating_data["overall_score"]),
            overall_feedback=rating_data["overall_feedback"]
        ), debug_info

    except Exception as e:
        logger.error(f"Error using LLM ({model_name}): {type(e).__name__}: {str(e)}")
        debug_info["error_message"] = str(e)
        return None, debug_info

@app.post("/rate", response_model=RatingResponse)
async def rate_writing(submission: WritingSubmission = Body(...), debug_mode: bool = False):
    """Rate an IELTS writing task submission using OpenAI or Ollama."""
    try:
        rating, debug_info = evaluate_with_llm(submission)
        if rating is None:
            raise HTTPException(status_code=500, detail="LLM evaluation failed.")
        response = {"rating": rating}
        if debug_mode:
            response["debug_info"] = debug_info
        return response
    except Exception as e:
        logger.error(f"Error in rate_writing endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
