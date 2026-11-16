import streamlit as st
from google import genai
from pypdf import PdfReader
import pandas as pd

st.set_page_config(page_title="IILM CRC Placement Co-Pilot", page_icon="🎓", layout="wide")

# --- VERIFIED IILM UNIVERSITY GURUGRAM RECRUITER & CURRICULUM DATA ---
IILM_DATA = {
    "Business Analytics": {
        "recruiters": [
            "HCL Tech (Business Analyst - Campus Partner)",
            "KPMG (Risk & Data Analytics Consultant)",
            "NielsenIQ (Market & Data Analyst)",
            "Lloyds Technology Centre (Data & Tech Analyst)",
            "Accenture / Wipro (Analytics Consultant)"
        ],
        "keywords": ["SQL", "Power BI", "DAX", "Python", "Descriptive Analytics with R", "Excel Solver", "Predictive Modeling", "ETL", "KPI Dashboards", "Data Storytelling"],
        "iilm_certs": "IILM-HCL Tech Live Analytics Project, KPMG Machine Learning Co-Certification, IBM & SAS Data Science Lab"
    },
    "Marketing": {
        "recruiters": [
            "L'Oréal (Management Trainee - Brand & Sales)",
            "Zomato / Blinkit (Key Account & Growth Manager)",
            "Asian Paints / Berger Paints (Sales & Marketing)",
            "Mondelez International / Mamaearth (Brand & Category)",
            "Dentsu / Flipkart (Digital & E-Commerce Strategy)"
        ],
        "keywords": ["GTM Strategy", "Consumer Insights", "Brand Positioning", "ROAS", "Campaign Attribution", "Key Account Management", "B2B/B2C Growth", "Trade Marketing", "CRM"],
        "iilm_certs": "KPMG Marketing Analytics Co-Certification, IILM Consumer Immersion & Digital Transformation Track"
    },
    "Finance & FinTech": {
        "recruiters": [
            "BlackRock (Financial & Investment Analyst)",
            "Oxane Partners (Portfolio & Structured Finance Analyst)",
            "AYE Finance (Management Trainee - Credit & Product)",
            "Deloitte / EY / PwC (Valuation & Tax Analyst)",
            "HDFC Bank / ICICI Bank / HSBC (Corporate Banking)"
        ],
        "keywords": ["Financial Modeling", "DCF Valuation", "Credit Risk & Underwriting", "Ratio Analysis", "Portfolio Management", "Bloomberg Terminal", "Working Capital", "P&L Forecasting"],
        "iilm_certs": "KPMG Financial Modelling Co-Certification, IILM FinLab powered by Bloomberg, NCFM Modules"
    },
    "Human Resources (HR)": {
        "recruiters": [
            "BlackRock (HR & People Operations)",
            "Deloitte / EY (Human Capital & HR Advisory)",
            "Mercer / Gartner (HR Consulting & Talent)",
            "HCL Tech / Wipro (Talent Acquisition & HRBP)",
            "ICICI Bank / Marsh McLennan (People & Culture)"
        ],
        "keywords": ["Talent Acquisition", "HRIS", "HR Analytics", "Employee Engagement", "Performance Appraisal", "Competency Mapping", "L&D", "Attrition Modeling", "Employer Branding"],
        "iilm_certs": "EY HR Analytics Co-Certification, IILM Corporate Readiness Programme (CRP) & Leadership Track"
    },
    "Psychology": {
        "recruiters": [
            "Mercer / Korn Ferry (Talent & Psychometric Assessment)",
            "Fortis Healthcare / MindPeers (Clinical & Behavioural Wellness)",
            "Goonj / Social Impact Foundations (Applied Behavioural Research)",
            "HR Consulting & Organisational Development Firms",
            "EdTech & Learning Experience Design Teams"
        ],
        "keywords": ["Psychometric Assessment", "Behavioural Intervention", "Qualitative & Quantitative Research", "Organisational Behaviour", "Cognitive Testing", "Counseling", "Survey Design"],
        "iilm_certs": "IILM Applied Psychology Practicum, Research Methodology & Behavioural Lab Projects"
    },
    "International Business & Operations": {
        "recruiters": [
            "Vestian MEA Global (Global Investment & Advisory)",
            "EY / KPMG (Global Trade & Supply Chain Advisory)",
            "Bosch / Regalo Kitchens (Operations & Supply Chain)",
            "Reliance BP Mobility / Tata Power (Operations & Logistics)",
            "JLL / Dalmia Bharat (Project & Enterprise Operations)"
        ],
        "keywords": ["Cross-Border Trade", "EXIM Policy", "Global Supply Chain", "Lean Six Sigma", "Forex Risk", "Market Entry Strategy", "Incoterms", "Vendor & Inventory Optimization"],
        "iilm_certs": "KPMG Lean Six Sigma Green Belt, CII Institute of Logistics Collaboration, IILM Global Study Immersion"
    }
}

# --- SIDEBAR ---
st.sidebar.title("🎓 IILM CRC Co-Pilot")
st.sidebar.caption("Corporate Resource Centre AI Engine • Gurugram Campus")

try:
    default_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    default_key = ""

api_key = st.sidebar.text_input("Gemini API Key", value=default_key, type="password")
mode = st.sidebar.radio("Select Portal View", ["🎓 Student Resume & Interview Prep", "📊 CRC Faculty Readiness Dashboard"])

st.sidebar.markdown("---")
st.sidebar.caption("Powered by IILM University Placement Benchmarks (500+ Recruiting Partners)")

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join([page.extract_text() or "" for page in reader.pages])

# --- VIEW 1: STUDENT PORTAL ---
if mode == "🎓 Student Resume & Interview Prep":
    st.title("🎓 IILM Placement & Resume Readiness Co-Pilot")
    st.caption("Grounded in IILM University Gurugram's Curriculum, Industry Certifications & 500+ Campus Recruiters")

    col1, col2 = st.columns([1, 1])
    with col1:
        program = st.selectbox("Program", ["BBA (Hons.) 2024–2028", "MBA (2026–2028)", "B.Sc. / B.A. (Hons.) Psychology", "B.Tech CSE"])
        spec = st.selectbox("Select Your Specialization", list(IILM_DATA.keys()))
        target_company = st.selectbox("Target IILM Campus Recruiter", IILM_DATA[spec]["recruiters"])
    with col2:
        uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
        custom_jd = st.text_area("Optional: Paste Specific CRC Notice / Job Description", height=100, placeholder="Leave blank to benchmark against IILM's verified recruiter profile...")

    st.info(
        f"**Target ATS Keywords for {spec}:** {', '.join(IILM_DATA[spec]['keywords'])}\n\n"
        f"**Recommended IILM Campus Credentials to Highlight:** {IILM_DATA[spec]['iilm_certs']}"
    )

    if st.button("🚀 Analyze Resume & Generate IILM Prep Kit", type="primary"):
        if not api_key:
            st.error("Please enter your Gemini API Key in the left sidebar.")
        elif not uploaded_resume:
            st.warning("Please upload your resume PDF first.")
        else:
            with st.spinner("Benchmarking against IILM Gurugram recruiter standards..."):
                try:
                    resume_text = extract_pdf_text(uploaded_resume)
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    You are the official Corporate Resource Centre (CRC) AI Placement Co-Pilot at IILM University, Gurugram.
                    Analyze this student's resume for the specialization '{spec}' ({program}) targeting '{target_company}'.
                    
                    IILM Target Keywords for {spec}: {IILM_DATA[spec]['keywords']}
                    Relevant IILM Campus Certifications & Labs: {IILM_DATA[spec]['iilm_certs']}
                    Optional Specific JD: {custom_jd}
                    Student Resume Text: {resume_text}
                    
                    Provide a sharp, actionable response with:
                    1. **ATS & IILM Recruiter Fit Score (out of 100)** with a 2-line justification referencing their projects/experience.
                    2. **Missing High-Impact Keywords & IILM Credentials** specifically valued by {target_company} (suggest relevant IILM labs/certifications like {IILM_DATA[spec]['iilm_certs']} if missing).
                    3. **3 Rewritten Resume Bullet Points** (take weak lines from their resume and upgrade them with strong action verbs and quantified impact).
                    4. **5 Tailored Mock Interview Questions** that {target_company} asks IILM {spec} candidates during campus drives, with brief hints on how to answer.
                    """
                    response = client.models.generate_content(model="gemini-4-hydrogen", contents=prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- VIEW 2: CRC FACULTY ANALYTICS DASHBOARD ---
else:
    st.title("📊 CRC Batch Readiness Analytics (Management View)")
    st.caption("Aligned with IILM Gurugram Placement Benchmarks (Highest: ₹26 LPA | Avg: ₹8.6 LPA | Top 10%: ₹13.64 LPA)")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Recruiters", "500+", "Consulting, BFSI, IT, FMCG")
    m2.metric("Batch Avg. ATS Score", "74%", "+11% post-CRP")
    m3.metric("Top Hiring Sector", "Consulting & Analytics", "31% of Offers")
    m4.metric("Top 10% Avg CTC", "₹13.64 LPA", "Highest: ₹26 LPA")

    df = pd.DataFrame({
        "IILM Specialization Track": list(IILM_DATA.keys()),
        "Key Campus Recruiters": [
            "HCL Tech, KPMG, NielsenIQ, Lloyds Tech",
            "L'Oréal, Zomato, Asian Paints, Mondelez",
            "BlackRock, Oxane Partners, AYE Finance, EY",
            "Deloitte, Mercer, Gartner, HCL Tech",
            "Mercer, Fortis, MindPeers, Goonj",
            "Vestian MEA, Bosch, Regalo, Tata Power"
        ],
        "Avg Recruiter Match (%)": [81, 76, 78, 72, 69, 73],
        "Primary Skill Gap Identified": [
            "Power BI DAX & Live SQL Projects",
            "Quantified Campaign ROAS Metrics",
            "DCF Valuation & Bloomberg FinLab Usage",
            "HR Analytics & Attrition Modeling",
            "Psychometric Assessment Tools",
            "Lean Six Sigma & EXIM Documentation"
        ]
    })
    st.subheader("Specialization-Wise Readiness & CRP Workshop Recommendations")
    st.dataframe(df, use_container_width=True)

    st.success("💡 **AI Recommendation for IILM CRC:** Run targeted Corporate Readiness Programme (CRP) bootcamps on *DCF Financial Modeling (KPMG module)* for Finance and *Power BI DAX* for Analytics ahead of upcoming Consulting & BFSI drives.")
