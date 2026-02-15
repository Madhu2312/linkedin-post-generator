from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile, File
from groq import Groq
import os
import shutil

from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
templates = Jinja2Templates(directory="templates")

app = FastAPI()

# ---------- NEW: create upload folder ----------
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
# ----------------------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ----------- CHANGED: added image parameter -----------
@app.post("/generate")
async def generate_post(request: Request, image: UploadFile = File(None)):
# -----------------------------------------------------

    form = await request.form()

    # ----------- NEW: save uploaded image -----------
    image_path = None
    if image and image.filename:
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # browser accessible path
        image_path = "/" + file_location.replace("\\", "/")
    # ------------------------------------------------

    role = form.get("role", "")
    role_other = form.get("role_other", "")
    tone = form.get("tone", "")
    purpose = form.get("purpose", "")
    highlight = form.get("highlight", "")
    insights = form.get("insights", "")
    gratitude = form.get("gratitude", "")
    tags = form.get("tags", "")
    resources = form.get("resources", "")
    date = form.get("date", "")
    reflection = form.get("reflection", "")
    cta = form.get("cta", "")
    hashtags = form.get("hashtags", "")
    extras = form.get("extras", "")

    print("Form data received:", form)
    final_role = role_other if role == "Other" and role_other else role

    # Build prompt
    prompt = f"""
    You are a professional LinkedIn content writer. Your task is to write an authentic, engaging, and well-structured LinkedIn post using the details below.

    Start with a compelling **hook** — one sentence that grabs attention. It should be emotional, surprising, or thought-provoking (but not clickbait).

    Main Post Inputs:
    - Role: {final_role}
    - Purpose: {purpose}
    - Highlight or Announcement: {highlight}
    - Tone: {tone}

    Additional Context (include if relevant):
    """

    optional_fields = {
        "Key challenges or insights": insights,
        "People or groups to thank": gratitude,
        "Tagged individuals or companies": tags,
        "Relevant resources or links": resources,
        "Timeline or key dates": date,
        "Personal reflection or story": reflection,
        "Clear call-to-action": cta,
        "Relevant hashtags": hashtags,
        "Any additional notes": extras,
    }

    for label, value in optional_fields.items():
        if value:
            prompt += f"- {label}: {value}\n"

    prompt += f"""
    Guidelines:
    - Write in short, skimmable paragraphs.
    - Use a {tone.lower()} tone — professional, but human and conversational.
    - Do **not** use emojis.
    - Avoid overused phrases like "excited to announce" or "game-changer."
    - Start with a strong hook line and end with a natural close or soft CTA (if applicable).
    - If the information provided is incomplete or vague:
    → Do NOT add fake details or assumptions.
    → Instead, either:
        a) Generate a short post using only the available details, OR
        b) Clearly respond that more context is needed to create a meaningful LinkedIn post.
    """

    print("Generated prompt:", prompt)

    # Call Groq API
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.8,
    )

    print("API response received:", response)

    linkedin_post = response.choices[0].message.content.strip()

    # ----------- CHANGED: return image url also -----------
    return {"linkedin_post": linkedin_post, "image_url": image_path}
