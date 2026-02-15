## LinkedIn Post Generator (FastAPI + LLM)



An AI-powered web application that generates structured, professional LinkedIn posts from user input.



This project collects structured details such as role, achievement, learnings, and resources, then uses a Large Language Model (Groq Llama-3.1) to automatically produce a clean, human-like LinkedIn post.



---



## Why I Built This



Many students and developers struggle to write professional LinkedIn posts even after completing good projects.

They either:



* don’t know how to structure it

* sound robotic

* or write overly long posts



This tool solves that problem by converting structured inputs into a properly formatted LinkedIn-ready post.



---



## Features



* Structured form-based input

* AI-generated LinkedIn post

* Human-style writing (not marketing tone)

* Image attachment preview

* Copy-to-clipboard (LinkedIn safe formatting)

* URL auto-detection (clickable links)

* Hashtag and mention formatting

* Field validation (prevents low-quality inputs)



---



## Tech Stack



**Backend**



* FastAPI

* Python

* Groq LLM API (Llama-3.1-8B)



**Frontend**



* HTML

* CSS

* JavaScript (Vanilla)



---



## Project Structure



```

linkedin-post-generator/

│

├── main.py

├── requirements.txt

├── .env (not uploaded)

│

├── templates/

│   └── index.html

│

└── static/

&nbsp;   └── style.css

```



---



## Installation \& Run (Local)



### 1. Clone Repository



```

git clone https://github.com/Madhu2312/linkedin-post-generator.git

cd linkedin-post-generator

```



### 2. Create Virtual Environment



```

python -m venv venv

venv\\Scripts\\activate

```



### 3. Install Dependencies



```

pip install -r requirements.txt

```



### 4. Add API Key



Create a `.env` file and add:



```

GROQ\_API\_KEY=your\_api\_key\_here

```



### 5. Run Server



```

uvicorn main:app --reload

```



Open browser:



```

http://127.0.0.1:8000

```



---



## What I Learned



* Prompt engineering for LLMs

* FastAPI request handling

* Form processing

* API integration

* Frontend-backend communication

* Input validation and UX design



---



## Future Improvements



* Direct LinkedIn posting via OAuth

* Post templates (Job update / Internship / Achievement)

* Tone selector (formal / casual / storytelling)

* Post analytics scoring



---



