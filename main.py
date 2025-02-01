import os
import uvicorn
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key not found. Check your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Define FastAPI app
app = FastAPI()

# Define request model
class TranslationRequest(BaseModel):
    source_code: str
    source_lang: str
    target_lang: str

@app.post("/translate")
async def translate_code(request: TranslationRequest):
    prompt = f"Convert the following {request.source_lang} code to {request.target_lang}:\n\n```{request.source_lang}\n{request.source_code}\n```"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an AI code translator."},
                      {"role": "user", "content": prompt}],
            temperature=0.2
        )

        translated_code = response.choices[0].message.content if response.choices else "Translation failed"
        return {"translated_code": translated_code}

    except Exception as e:
        return {"error": str(e)}        

# Retrieve Render-assigned PORT and run Uvicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)

