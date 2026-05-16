from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# 1. Initialize FastAPI app
app = FastAPI(title="AI Sentiment API")

# 2. ALLOW CORS (Crucial: This lets ANY website call your API securely)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any website domain to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load the AI Model (Using our cached downloaded model)
analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Define what the incoming website data should look like
class ReviewInput(BaseModel):
    review: str

# 4. Create the API Endpoint
@app.post("/predict")
def predict_sentiment(data: ReviewInput):
    if not data.review.strip():
        return {"error": "Review text cannot be empty"}
    
    # Run AI inference
    result = analyzer(data.review)
    
    # Return structured JSON back to the website
    return {
        "text": data.review,
        "sentiment": result["label"],
        "confidence": round(result["score"] * 100, 2)
    }