# Resume-JD-Compatibility-Checker
A Streamlit app that evaluates how well a candidate’s resume matches job requirements using AI models such as Google Gemini (default) or other providers (e.g., OpenAI GPT).
<img width="830" height="738" alt="image" src="https://github.com/user-attachments/assets/1385ea46-2365-4d4b-81f7-f1d0e6b8f6f7" />

This tool helps recruiters and job seekers quickly check compatibility scores between a resume (PDF) and job description requirements.

🚀 Features

Upload your resume (PDF)

Add multiple job requirements one by one

Delete or edit requirements easily

Click a button to check compatibility

Works with different AI providers (Gemini, OpenAI, etc.) → just update your API key

AI evaluates:

If the resume meets each requirement (Yes/No)

Provides a short explanation

Assigns a compatibility score (0–100%)

Clean, interactive Streamlit UI

<img width="838" height="787" alt="image" src="https://github.com/user-attachments/assets/b249e4a4-8319-4c5e-9206-790972f3235a" />

🛠️ Tech Stack

Python

Streamlit – for web interface

PyPDF2 – to extract text from resumes (PDFs)

Google Generative AI (gemini-1.5-flash) (default) – for semantic matching

python-dotenv – for API key management

(Optional) OpenAI GPT – can be swapped in by changing API configuration
