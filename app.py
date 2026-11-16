import streamlit as st
from google import genai
from pypdf import PdfReader
import pandas as pd

st.set_page_config(page_title="IILM CRC Placement Co-Pilot", page_icon="🎓", layout="wide")

# --- IILM SPECIALIZATION & RECRUITER KNOWLEDGE BASE ---
IILM_DATA = {
    "Business Analytics": {
        "recruiters": ["HCL Tech (Business Analyst)", "NielsenIQ (Data Analyst)", "KPMG (Risk & Data)", "Wipro (Analytics Consultant)"],
        "keywords": ["SQL", "Power BI", "DAX", "Python", "Excel Solver", "Predictive Modeling", "ETL", "KPI Dashboards", "A/B Testing", "Data Storytelling"]
    },
    "Marketing": {
        "recruiters": ["L'Oréal (Management Trainee)", "Zomato (Key Account Manager)", "Dentsu (Brand Strategy)", "Asian Paints (Sales & Marketing)"],
        "keywords": ["GTM Strategy", "Consumer Insights", "Brand Positioning", "ROAS", "Campaign Attribution", "Market Research", "B2B/B2C Growth", "CRM", "SEO/SEM"]
    },
    "Finance": {
        "recruiters": ["BlackRock (Financial Analyst)", "Oxane Partners (Portfolio Analyst)", "EY (Assurance & Valuation)", "HDFC Bank (Corporate Banking)"],
        "keywords": ["Financial Modeling", "DCF Valuation", "Credit Risk", "Ratio Analysis", "Portfolio Management", "Working Capital", "Bloomberg", "Forecasting", "P&L Analysis"]
    },
    "Human Resources (HR)": {
        "recruiters": ["Nestlé (HR Trainee)", "Deloitte (Human Capital)", "Wipro (Talent Acquisition)", "ICICI Bank (HRBP)"],
        "keywords": ["Talent Acquisition", "HRIS", "Employee Engagement", "Performance Appraisal", "Competency Mapping", "L&D", "Attrition Analysis", "Employer Branding"]
    },
    "Psychology": {
        "recruiters": ["Korn Ferry (Talent & Assessment)", "MindPeers (Behavioural Specialist)", "HR Consulting Firms", "EdTech Learning Design"],
        "keywords": ["Psychometric Assessment", "Behavioural Intervention", "Qualitative Research", "Organisational Behaviour", "Cognitive Testing", "Counseling", "Survey Design"]
    },
    "International Business": {
        "recruiters": ["EY (Global Trade Advisory)", "DHL / Maersk (Supply Chain)", "Export Houses NCR", "Global Consulting"],
        "keywords": ["Cross-Border Trade", "EXIM Policy", "Global Supply Chain", "Forex Risk", "Market Entry Strategy", "Incoterms", "International Logistics", "Trade Compliance"]
    }
}

# --- SIDEBAR ---
st.sidebar.title("🎓 IILM CRC Co-Pilot")
st.sidebar.caption("Corporate Resource Centre AI Engine")

try:
    default_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    default_key = ""

api_key = st.sidebar.text_input("Gemini API Key", value=default_key, type="password")
mode = st.sidebar.radio("Select Portal View", ["🎓 Student Resume & Interview Prep", "📊 CRC Faculty Readiness Dashboard"])

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join([page.extract_text() or "" for page in reader.pages])

# --- VIEW 1: STUDENT PORTAL ---
if mode == "🎓 Student Resume & Interview Prep":
    st.title("🎓 IILM Placement & Resume Readiness Co-Pilot")
    st.caption("Tailored for IILM University Specializations & Campus Recruiters")

    col1, col2 = st.columns([1, 1])
    with col1:
        program = st.selectbox("Program", ["BBA (2024–2028)", "MBA", "BA (Hons) Psychology", "B.Tech"])
        spec = st.selectbox("Select Your Specialization", list(IILM_DATA.keys()))
        target_company = st.selectbox("Target IILM Campus Recruiter", IILM_DATA[spec]["recruiters"])
    with col2:
        uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
        custom_jd = st.text_area("Optional: Paste Specific Job Description (JD)", height=100, placeholder="Leave blank to use IILM's standard recruiter profile...")

    st.info(f"**Top IILM Recruiter Keywords for {spec}:** " + ", ".join(IILM_DATA[spec]["keywords"]))

    if st.button("🚀 Analyze Resume & Generate Prep Kit", type="primary"):
        if not api_key:
            st.error("Please enter your Gemini API Key in the left sidebar.")
        elif not uploaded_resume:
            st.warning("Please upload your resume PDF first.")
        else:
            with st.spinner("Analyzing against IILM recruiter benchmarks..."):
                try:
                    resume_text = extract_pdf_text(uploaded_resume)
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    You are the Corporate Resource Centre (CRC) AI Placement Co-Pilot at IILM University, Gurugram.
                    Analyze this student's resume for the specialization '{spec}' ({program}) targeting '{target_company}'.
                    
                    IILM Target Keywords for {spec}: {IILM_DATA[spec]['keywords']}
                    Optional JD: {custom_jd}
                    Student Resume Text: {resume_text}
                    
                    Provide a structured response with:
                    1. **ATS & IILM Recruiter Fit Score (out of 100)** with a 2-line justification.
                    2. **Missing High-Impact Keywords** specifically needed for {target_company}.
                    3. **3 Rewritten Resume Bullet Points** (take weak lines from their resume and upgrade them with strong action verbs and quantified impact).
                    4. **5 Tailored Mock Interview Questions** that {target_company} typically asks IILM {spec} candidates, along with brief hints on how to answer.
                    """
                    response = client.models.generate_content(model="gemini-4-hydrogen", contents=prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- VIEW 2: CRC FACULTY ANALYTICS DASHBOARD ---
else:
    st.title("📊 CRC Batch Readiness Analytics (Management View)")
    st.caption("Live skill-gap intelligence across IILM specializations before placement drives")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Resumes Analyzed", "412", "+38 this week")
    m2.metric("Avg. ATS Readiness", "74%", "+11% post-AI")
    m3.metric("Top Performing Track", "Business Analytics", "81% Avg Score")
    m4.metric("Upcoming Drives", "14 Companies", "Next 30 Days")

    df = pd.DataFrame({
        "Specialization": list(IILM_DATA.keys()),
        "Students Screened": [95, 110, 82, 55, 35, 35],
        "Avg Recruiter Match (%)": [81, 76, 74, 71, 68, 72],
        "Top Missing Skill Gap": [
            "SQL & Power BI DAX",
            "Quantified Campaign ROAS",
            "Financial Modeling & DCF",
            "HRIS & Attrition Metrics",
            "Psychometric Tool Exposure",
            "EXIM & Trade Compliance"
        ]
    })
    st.subheader("Specialization-Wise Readiness & Workshop Recommendations")
    st.dataframe(df, use_container_width=True)

    st.success("💡 **AI Recommendation for CRC:** Schedule a 2-hour hands-on *Financial Modeling* workshop for Finance and *Campaign Attribution* bootcamp for Marketing ahead of next week's drives.")
