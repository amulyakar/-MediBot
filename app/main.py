
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.schemas import QuestionRequest, AnswerResponse
from app.agents.medical_team import medical_team


# ==========================================
# 1. CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="MediBot - Medical Information Assistant",
    description="An educational multi-agent medical information assistant",
    version="1.0.0"
)


# ==========================================
# 2. CONNECT FRONTEND STATIC FILES
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# ==========================================
# 3. MEDICAL DISCLAIMER
# ==========================================

DISCLAIMER = (
    "MediBot provides educational information only and is not "
    "a substitute for professional medical advice, diagnosis, or treatment."
)


# ==========================================
# 4. HOMEPAGE
# ==========================================

@app.get("/", response_class=HTMLResponse)
def home():

    html_file = BASE_DIR / "static" / "index.html"

    return html_file.read_text(encoding="utf-8")


# ==========================================
# 5. HEALTH CHECK API
# ==========================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "app_name": "MediBot",
        "message": "Medical Assistant Backend is running"
    }


# ==========================================
# 6. ASK MEDIBOT API
# ==========================================

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):

    try:

        # Send the user's question to the three-agent team
        response = medical_team.run(request.question)

        # Extract the final AI-generated answer
        answer = response.content

        # Check whether an answer was generated
        if not answer:

            raise HTTPException(
                status_code=503,
                detail="MediBot could not generate an answer."
            )

        # Return the answer in structured JSON format
        return AnswerResponse(
            question=request.question,
            answer=str(answer),
            disclaimer=DISCLAIMER
        )

    except HTTPException:
        raise

    except Exception:

        # Handle unexpected errors without exposing API details
        raise HTTPException(
            status_code=503,
            detail=(
                "MediBot is temporarily unable to answer. "
                "Please try again later."
            )
        )
