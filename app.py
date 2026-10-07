import json
import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader

# Page configuration
st.set_page_config(
    page_title="AI Resume ATS Score & Optimizer",
    page_icon="📄",
    layout="wide",
)

st.title("📄 AI Resume ATS Analyzer & Optimizer")
st.markdown(
    "Upload your resume (PDF) and paste the Job Description to get an instant **ATS Score**, "
    "matching analysis, and detailed improvement recommendations powered by **Gemini Flash**."
)

# Sidebar: API Key input with session storage option
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "Enter Gemini API Key:",
        type="password",
        help="Get your key from Google AI Studio (https://aistudio.google.com/)",
    )
    st.info("💡 Your key is processed securely in runtime and never stored.")


def extract_text_from_pdf(uploaded_file) -> str:
    """Extracts raw text content from an uploaded PDF file."""
    try:
        reader = PdfReader(uploaded_file)
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        return extracted_text.strip()
    except Exception as e:
        st.error(f"Error reading PDF file: {str(e)}")
        return ""


def analyze_resume_with_gemini(
    resume_text: str, job_description: str, key: str
) -> dict:
    """Queries Gemini Flash model to evaluate ATS score and provide actionable feedback."""
    client = genai.Client(api_key=key)

    prompt = f"""
    You are an expert HR Specialist and Applicant Tracking System (ATS) auditor.
    Analyze the following Candidate Resume against the provided Job Description.

    JOB DESCRIPTION:
    {job_description}

    CANDIDATE RESUME:
    {resume_text}

    Instructions:
    Provide a thorough evaluation formatted as a JSON object matching this exact schema:
    {{
        "ats_score": integer (0 to 100 representing overall ATS match percentage),
        "match_summary": "A concise paragraph summarizing the candidate's fit.",
        "key_matching_skills": ["skill 1", "skill 2", ...],
        "missing_keywords": ["keyword 1", "keyword 2", ...],
        "structural_and_formatting_issues": ["issue 1", "issue 2", ...],
        "actionable_improvements": [
            "Specific improvement point 1",
            "Specific improvement point 2",
            ...
        ]
    }}
    Return ONLY valid JSON. Do not include markdown code block syntax or extra text outside JSON.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
        ),
    )

    return json.loads(response.text)


# Main Interface layout
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("1. Upload Resume")
    uploaded_pdf = st.file_uploader(
        "Upload Resume (PDF format)", type=["pdf"], help="Select a PDF resume file"
    )

    st.subheader("2. Target Job Description")
    job_desc = st.text_area(
        "Paste Job Description here:",
        height=220,
        placeholder="Paste requirements, responsibilities, and qualifications...",
    )

    analyze_btn = st.button("🚀 Analyze Resume", type="primary", use_container_width=True)

with col2:
    st.subheader("3. ATS Evaluation & Analysis")

    if analyze_btn:
        if not api_key:
            st.error("⚠️ Please enter your Gemini API Key in the sidebar.")
        elif not uploaded_pdf:
            st.warning("⚠️ Please upload a PDF resume.")
        elif not job_desc.strip():
            st.warning("⚠️ Please enter the Job Description.")
        else:
            with st.spinner("Analyzing resume content against job requirements..."):
                resume_text = extract_text_from_pdf(uploaded_pdf)

                if not resume_text:
                    st.error("Could not extract text from the uploaded PDF. Ensure it is not password-protected or image-only.")
                else:
                    try:
                        results = analyze_resume_with_gemini(
                            resume_text, job_desc, api_key
                        )

                        # Display Score Gauge / Metric
                        score = results.get("ats_score", 0)
                        if score >= 75:
                            st.success(f"### ATS Match Score: {score}/100 🎯 (Strong Match)")
                        elif score >= 50:
                            st.warning(f"### ATS Match Score: {score}/100 ⚠️ (Moderate Match)")
                        else:
                            st.error(f"### ATS Match Score: {score}/100 ❌ (Needs Improvement)")

                        st.progress(score / 100)

                        # Match Summary
                        st.markdown("#### 📝 Fit Summary")
                        st.write(results.get("match_summary", ""))

                        # Skills & Keywords
                        sk_col1, sk_col2 = st.columns(2)
                        with sk_col1:
                            st.markdown("#### ✅ Matching Keywords Found")
                            for skill in results.get("key_matching_skills", []):
                                st.markdown(f"- `{skill}`")

                        with sk_col2:
                            st.markdown("#### 🔍 Critical Missing Keywords")
                            for keyword in results.get("missing_keywords", []):
                                st.markdown(f"- `{keyword}`")

                        st.divider()

                        # Actionable Improvements
                        st.markdown("#### 💡 Actionable Improvement Steps")
                        for imp in results.get("actionable_improvements", []):
                            st.markdown(f"- {imp}")

                        # Structural / Formatting Check
                        formatting = results.get("structural_and_formatting_issues", [])
                        if formatting:
                            st.markdown("#### 🛠️ Formatting / Readability Notes")
                            for item in formatting:
                                st.markdown(f"- {item}")

                    except Exception as e:
                        st.error(f"Failed to analyze resume: {str(e)}")
