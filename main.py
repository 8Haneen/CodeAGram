from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if API key is available
if not OPENAI_API_KEY:
    raise ValueError("API key not found. Check your .env file.")

# Initialize FastAPI app
app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model
class TranslateRequest(BaseModel):
    code: str
    source_language: str
    target_language: str

# Define the translation endpoint
@app.post("/translate")
async def translate_code(request: TranslateRequest):
    """
    Translates code from one language to another using OpenAI's GPT model.
    """

    prompt = f"Convert this {request.source_language} code to {request.target_language}:\n{request.code}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        translated_code = response['choices'][0]['message']['content'].strip()

        return {"translated_code": translated_code}

    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")

