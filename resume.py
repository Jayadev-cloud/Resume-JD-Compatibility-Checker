import streamlit as st
import PyPDF2
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Extract text from PDF
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# UI setup
st.set_page_config(page_title="Resume-JD Compatibility Checker", layout="centered")
st.title("📄 Resume-JD Compatibility Checker")
st.markdown("Upload your **PDF Resume** and enter job requirements to check compatibility.")

# Resume upload
uploaded_file = st.file_uploader("📎 Upload your Resume (PDF only)", type=["pdf"])

# Job requirements input section
st.subheader("📝 Job Requirements")

if 'requirements' not in st.session_state:
    st.session_state.requirements = []
    st.session_state.req_number = 1  # Start with Requirement 1

current_req_number = st.session_state.req_number
new_req = st.text_input(f"Enter Requirement #{current_req_number}")

col1, col2 = st.columns([3, 2])

with col1:
    if st.button("➕ Add Requirement"):
        if new_req.strip():
            st.session_state.requirements.append(new_req.strip())
            st.session_state.req_number += 1
            st.success(f"Requirement #{current_req_number} added!")
            st.rerun()
        else:
            st.warning("Please enter a valid job requirement.")

if st.session_state.requirements:
    st.markdown("#### Current Requirements:")
    for i, req in enumerate(st.session_state.requirements):
        col_req, col_del = st.columns([8, 1])
        with col_req:
            st.markdown(f"- {req}")
        with col_del:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.requirements.pop(i)
                if st.session_state.req_number > len(st.session_state.requirements):
                    st.session_state.req_number = len(st.session_state.requirements) + 1
                st.rerun()

st.markdown("<br><br>", unsafe_allow_html=True)

col4, col5 = st.columns([2, 1])
with col5:
    done_button = st.button(" 🔍 Compatibility Check", key="done_button")

if done_button:
    if not uploaded_file:
        st.error("❌ Please upload a resume file.")
    elif not st.session_state.requirements:
        st.error("❌ Please enter at least one job requirement.")
    else:
        resume_text = extract_text(uploaded_file)

        st.subheader("🤖 Gemini Matching Results")

        results = []
        with st.spinner("Fetching results from Gemini..."):
            model = genai.GenerativeModel("gemini-1.5-flash")

            for req in st.session_state.requirements:
                prompt = (
                    f"Check if the following resume meets the requirement.\n"
                    f"Requirement: {req}\n\n"
                    f"Resume:\n{resume_text}\n\n"
                    f"Answer with Yes or No and explain briefly.\n"
                    f"Also provide a Compatibility Score (0 to 100%)."
                )
                try:
                    response = model.generate_content(prompt)
                    answer = response.text
                    results.append((req, answer))
                except Exception as e:
                    st.error(f"⚠️ Gemini Error: {e}")
                    results.append((req, "Error occurred"))

        # Display results
        for req, answer in results:
            score = ""
            if "Compatibility Score" in answer:
                try:
                    score = answer.split("Compatibility Score")[-1].strip().split()[0]
                except:
                    score = "N/A"

                st.markdown(f"""
                    <div style='width: 100%; display: flex; justify-content: space-between; align-items: center;'>
                        <span>📌 {req}</span>
                        <span><strong>Compatibility Score: {score}</strong></span>
                    </div>
                """, unsafe_allow_html=True)

                explanation = answer.replace(f"Compatibility Score: {score}", "").strip()
                with st.expander("Explanation"):
                    st.markdown(f"**Explanation:** {explanation}")
