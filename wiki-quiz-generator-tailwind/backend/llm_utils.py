import os, json
PROMPT_PATH = os.path.join(os.path.dirname(__file__), '..', 'langchain_prompts', 'quiz_prompt.txt')
try:
    PROMPT_TEMPLATE = open(PROMPT_PATH).read()
except:
    PROMPT_TEMPLATE = "Generate quiz"

def call_llm(prompt: str):
    provider = os.getenv('LLM_PROVIDER', '').lower()
    if provider:
        raise NotImplementedError("Configure LLM provider integration.")
    return fallback_generate(prompt)

def fallback_generate(article_text: str):
    qs = []
    for i in range(5):
        qs.append({
            "question": f"Sample question {i+1}",
            "options": ["A","B","C","D"],
            "answer": "A",
            "difficulty": "easy" if i<2 else "medium",
            "explanation": "Fallback explanation."
        })
    return qs, ["Related A","Related B"]
