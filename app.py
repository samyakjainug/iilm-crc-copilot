import streamlit as st
from google import genai
from pypdf import PdfReader
import pandas as pd

st.set_page_config(page_title="IILM CRC Placement Co-Pilot", page_icon="🎓", layout="wide")

# --- PROGRAM -> SPECIALIZATION -> IILM RECRUITER & KEYWORD MAPPING ---
PROGRAM_DATA = {
    "BBA (Hons.) 2024–2028": {
        "Business Analytics": {
            "recruiters": ["HCL Tech (Business Analyst)", "NielsenIQ (Market & Data Analyst)", "KPMG (Risk & Data Analyst)", "Wipro (Analytics Associate)"],
            "keywords": ["SQL", "Power BI", "DAX", "Excel Solver", "Descriptive Analytics", "KPI Dashboards", "Data Storytelling", "Python"],
            "iilm_certs": "IILM-HCL Tech Live Analytics Project, IBM & SAS Business Analytics Lab"
        },
        "Marketing & Innovation": {
            "recruiters": ["L'Oréal (Management Trainee)", "Zomato / Blinkit (Key Account Executive)", "Asian Paints (Sales & Marketing)", "Mamaearth (Brand Associate)"],
            "keywords": ["GTM Strategy", "Consumer Insights", "Brand Positioning", "ROAS", "Campaign Attribution", "B2B/B2C Sales", "Market Research", "CRM"],
            "iilm_certs": "KPMG Marketing Analytics Co-Certification, IILM Consumer Immersion Project"
        },
        "Finance & FinTech": {
            "recruiters": ["BlackRock (Financial Operations Analyst)", "Oxane Partners (Portfolio Analyst)", "AYE Finance (Credit Management Trainee)", "HDFC Bank / ICICI Bank"],
            "keywords": ["Financial Modeling", "Ratio Analysis", "Credit Underwriting", "Working Capital", "Bloomberg Terminal", "Excel Valuation", "P&L Analysis"],
            "iilm_certs": "IILM FinLab powered by Bloomberg, NCFM Financial Markets Modules"
        },
        "Human Resources (HR) & OB": {
            "recruiters": ["Deloitte (Human Capital Analyst)", "Mercer (HR Consulting Associate)", "HCL Tech (Talent Acquisition)", "ICICI Bank (HRBP Trainee)"],
            "keywords": ["Talent Acquisition", "HRIS", "Employee Engagement", "Performance Appraisal", "Competency Mapping", "L&D", "Employer Branding"],
            "iilm_certs": "EY HR Analytics Co-Certification, IILM Corporate Readiness Programme (CRP)"
        },
        "International Business": {
            "recruiters": ["Vestian MEA Global (Global Advisory)", "EY (Global Trade Analyst)", "DHL / Maersk (Supply Chain Associate)", "Export Houses NCR"],
            "keywords": ["Cross-Border Trade", "EXIM Policy", "Global Supply Chain", "Forex Risk", "Market Entry Strategy", "Incoterms", "Trade Compliance"],
            "iilm_certs": "IILM Global Study Immersion (Germany/France/Singapore), CII Logistics Workshop"
        },
        "Entrepreneurship": {
            "recruiters": ["IILM Innovation Foundation (Venture Incubation)", "Early-Stage VC & Startup Founder's Office", "Zomato / Blinkit (Growth & Ops)"],
            "keywords": ["Business Model Canvas", "Lean Startup", "MVP Validation", "Unit Economics", "Pitch Deck", "Go-To-Market", "Customer Discovery"],
            "iilm_certs": "IILM-IF On-Campus Incubator & Seed Funding Track, Design Thinking Immersion"
        }
    },
    "MBA (2026–2028)": {
        "Data Science & Strategy (with HCL Tech)": {
            "recruiters": ["HCL Tech (Strategy & Data Consultant)", "KPMG (Management & Data Consulting)", "Lloyds Technology Centre (BI Lead)", "Accenture Strategy"],
            "keywords": ["Predictive Modeling", "SQL", "Power BI", "Business Strategy", "ETL Pipelines", "A/B Testing", "Executive Dashboards", "Python"],
            "iilm_certs": "HCL Tech Co-Branded Data Science Track, KPMG Machine Learning Certification"
        },
        "AI & Innovation Management (with HCL Tech)": {
            "recruiters": ["HCL Tech (AI Product Manager)", "Deloitte Digital (Tech Transformation)", "Gartner (Tech Advisory)", "Microsoft Partner Ecosystem"],
            "keywords": ["AI Product Strategy", "GenAI Workflows", "Digital Transformation", "Agile Product Management", "Prompt Engineering", "Tech ROI"],
            "iilm_certs": "HCL Tech AI & Innovation Track, CESIM Business Simulations"
        },
        "Marketing Management": {
            "recruiters": ["L'Oréal (Area Sales / Brand Manager)", "Mondelez International (Sales & Category)", "Flipkart / Zomato (Category Manager)", "Dentsu (Brand Strategy)"],
            "keywords": ["Product & Brand Management", "Sales & Distribution", "GTM Strategy", "ROAS", "Trade Marketing", "Key Account Management", "Consumer Behaviour"],
            "iilm_certs": "KPMG Marketing Analytics Co-Certification, IIM Sambalpur / Kashipur Immersion"
        },
        "Financial Modelling & Valuation": {
            "recruiters": ["BlackRock (Investment Analyst)", "Oxane Partners (Structured Finance)", "EY / PwC (Valuations & Deals)", "HSBC / ICICI Corporate Banking"],
            "keywords": ["DCF Valuation", "LBO & M&A Modeling", "Financial Statement Analysis", "Credit Risk", "Portfolio Optimization", "Bloomberg Terminal"],
            "iilm_certs": "KPMG Financial Modelling & Valuation Certification, Bloomberg FinLab"
        },
        "HRM & Behavioural Science": {
            "recruiters": ["BlackRock (People Operations)", "Deloitte / EY (People Advisory Services)", "Mercer / Marsh McLennan (Total Rewards)", "Nestlé (HRBP)"],
            "keywords": ["HR Analytics", "Organisational Development", "Talent Strategy", "Change Management", "Attrition Modeling", "HRIS", "Leadership Development"],
            "iilm_certs": "EY HR Analytics Co-Certification, IILM Deep Purpose Leadership Retreat"
        },
        "Operations & Supply Chain": {
            "recruiters": ["Bosch (Supply Chain Planner)", "Tata Power / Reliance BP Mobility (Operations)", "JLL (Project Operations)", "Dalmia Bharat"],
            "keywords": ["Lean Six Sigma", "Supply Chain Optimization", "ERP / SAP", "Inventory Management", "Logistics Planning", "Procurement", "S&OP"],
            "iilm_certs": "KPMG Lean Six Sigma Green Belt Certification, CII Logistics Collaboration"
        }
    },
    "B.Sc. / B.A. (Hons.) Psychology": {
        "Clinical Psychology": {
            "recruiters": ["Fortis Healthcare (Clinical Psychology Intern/Assistant)", "Max Healthcare / VIMHANS (Mental Health Support)", "MindPeers (Clinical Wellness)"],
            "keywords": ["Psychodiagnostics", "CBT & REBT", "Case History Taking", "Mental Status Examination (MSE)", "DSM-5 / ICD-11", "Clinical Assessment"],
            "iilm_certs": "IILM Institute of Clinical Psychology (IICM) Practicum & Hospital Fieldwork"
        },
        "Counselling Psychology": {
            "recruiters": ["MindPeers / YourDOST (Mental Health Counsellor)", "K-12 International Schools (School Counsellor)", "Goonj / Social Wellness NGOs"],
            "keywords": ["Active Listening", "Therapeutic Alliance", "Crisis Intervention", "Group Counselling", "Emotional Intelligence", "Wellbeing Workshops"],
            "iilm_certs": "IILM Counselling Simulation Lab & Community Mental Health Immersion"
        },
        "Forensic Psychology": {
            "recruiters": ["Forensic & Legal Consultancy Cells", "Correctional & Juvenile Rehabilitation Centres", "Criminal Justice Policy Think Tanks"],
            "keywords": ["Criminal Profiling", "Forensic Assessment", "Victimology", "Legal & Ethical Psychology", "Investigative Interviewing", "Behavioural Risk"],
            "iilm_certs": "IILM Forensic Psychology Specialization & Legal-Psych Case Studies"
        },
        "Behaviour and Data": {
            "recruiters": ["NielsenIQ (Consumer Behaviour Researcher)", "UX Research Teams (Flipkart / Zomato)", "Behavioural Economics & Policy Labs"],
            "keywords": ["Quantitative Research", "SPSS / R Statistical Analysis", "Behavioural Economics", "UX User Research", "Survey Design", "Experimental Psychology"],
            "iilm_certs": "IILM Psychology Lab & Quantitative Behavioural Data Practicum"
        },
        "AI and Psychology": {
            "recruiters": ["EdTech & Conversational AI Design Teams", "Human-Computer Interaction (HCI) Research Labs", "Digital Mental Health Startups"],
            "keywords": ["Human-AI Interaction", "Cognitive Modeling", "Ethical AI", "User Empathy Mapping", "Conversational UX", "Behavioural Nudges"],
            "iilm_certs": "IILM Interdisciplinary AI & Psychology Track"
        },
        "Organisational Behaviour & Applied Psychology": {
            "recruiters": ["Mercer / Korn Ferry (Psychometric & Talent Assessment)", "Deloitte Human Capital (Change & Culture)", "HR Consulting Firms"],
            "keywords": ["Psychometric Testing", "Organisational Culture", "Workplace Wellbeing", "Employee Motivation", "360-Degree Feedback", "Group Dynamics"],
            "iilm_certs": "IILM Applied Psychology & Corporate OD Assessment Lab"
        }
    },
    "B.Tech": {
        "CSE – Artificial Intelligence & Machine Learning": {
            "recruiters": ["HCL Tech (AI/ML Engineer)", "Lloyds Technology Centre (ML Developer)", "Accenture (AI Analyst)", "IBM / Wipro"],
            "keywords": ["Python", "PyTorch / TensorFlow", "Scikit-Learn", "Deep Learning", "NLP", "Computer Vision", "Model Deployment", "SQL"],
            "iilm_certs": "Microsoft Azure AI Co-Certification, IILM NVIDIA AI & Robotics Lab"
        },
        "CSE – Generative AI": {
            "recruiters": ["AI Product Startups (GenAI Engineer)", "HCL Tech (LLM Solutions Developer)", "KPMG (GenAI Consulting)"],
            "keywords": ["LLMs", "RAG (Retrieval-Augmented Generation)", "LangChain", "Prompt Engineering", "Vector Databases", "Transformers", "Python", "APIs"],
            "iilm_certs": "IILM Generative AI Research Track & Applied LLM Capstone"
        },
        "CSE – Data Science & Data Engineering": {
            "recruiters": ["NielsenIQ (Data Engineer)", "KPMG (Data & Analytics)", "HCL Tech (Big Data Developer)", "Oxane Partners (Data Tech)"],
            "keywords": ["Python", "SQL", "Apache Spark", "ETL Pipelines", "Power BI", "Cloud Data Warehousing", "Statistical Modeling", "Pandas"],
            "iilm_certs": "IBM & SAS Data Science Co-Certification, IILM Big Data Lab"
        },
        "CSE – Cloud Computing & Cyber Security": {
            "recruiters": ["KPMG / EY (Cyber Risk & Cloud Security)", "HCL Tech (Cloud & DevOps Engineer)", "Palo Alto / Security Operations Centres"],
            "keywords": ["AWS / Microsoft Azure", "Docker & Kubernetes", "Network Security", "Ethical Hacking", "VAPT", "SIEM", "CI/CD Pipelines", "Linux"],
            "iilm_certs": "Microsoft Cloud & Cyber Security Track, IILM Cyber Forensics Lab"
        },
        "Robotics & Artificial Intelligence": {
            "recruiters": ["Bosch (Robotics & Automation Engineer)", "Industrial Automation & Drone Tech Firms", "R&D Mechatronics Labs"],
            "keywords": ["ROS (Robot Operating System)", "Embedded C++ / Python", "Computer Vision", "Sensors & Actuators", "Edge AI", "IoT", "Mechatronics"],
            "iilm_certs": "IILM Robotics, Sensors & Industry 4.0 Hardware Lab"
        },
        "Biotechnology & Bioinformatics": {
            "recruiters": ["Biocon / Panacea Biotec (R&D Associate)", "Clinical Research Organizations (CROs)", "Computational Biology & Genomics Labs"],
            "keywords": ["Genomics & Proteomics", "Molecular Docking", "PCR / ELISA", "Bioinformatics Databases", "Bioprocess Engineering", "Python / R for Bio"],
            "iilm_certs": "IILM Department of Biotechnology Wet-Lab & Computational Biology Practicum"
        }
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
st.sidebar.caption("Grounded in IILM University Gurugram Programmes & 500+ Recruiting Partners")

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join([page.extract_text() or "" for page in reader.pages])

# --- VIEW 1: STUDENT PORTAL ---
if mode == "🎓 Student Resume & Interview Prep":
    st.title("🎓 IILM Placement & Resume Readiness Co-Pilot")
    st.caption("Program-Specific Recruiter Matching, Keyword Optimization & Mock Interviews for IILM Gurugram")

    col1, col2 = st.columns([1, 1])
    with col1:
        program = st.selectbox("Select Your Program", list(PROGRAM_DATA.keys()))
        available_specs = list(PROGRAM_DATA[program].keys())
        spec = st.selectbox(f"Select {program} Specialization", available_specs)
        spec_info = PROGRAM_DATA[program][spec]
        target_company = st.selectbox("Target IILM Campus Recruiter", spec_info["recruiters"])
    with col2:
        uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
        custom_jd = st.text_area("Optional: Paste Specific CRC Notice / Job Description", height=100, placeholder="Leave blank to benchmark against IILM's verified recruiter profile...")

    st.info(
        f"**Target ATS Keywords for {spec}:** {', '.join(spec_info['keywords'])}\n\n"
        f"**Recommended IILM Campus Credentials to Highlight:** {spec_info['iilm_certs']}"
    )

    if st.button("🚀 Analyze Resume & Generate IILM Prep Kit", type="primary"):
        if not api_key:
            st.error("Please enter your Gemini API Key in the left sidebar.")
        elif not uploaded_resume:
            st.warning("Please upload your resume PDF first.")
        else:
            with st.spinner(f"Benchmarking {program} ({spec}) resume against {target_company}..."):
                try:
                    resume_text = extract_pdf_text(uploaded_resume)
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    You are the official Corporate Resource Centre (CRC) AI Placement Co-Pilot at IILM University, Gurugram.
                    Analyze this student's resume for the program '{program}' and specialization '{spec}' targeting '{target_company}'.
                    
                    Target Keywords for {spec}: {spec_info['keywords']}
                    Relevant IILM Campus Certifications & Labs: {spec_info['iilm_certs']}
                    Optional Specific JD: {custom_jd}
                    Student Resume Text: {resume_text}
                    
                    Provide a sharp, actionable response with:
                    1. **ATS & IILM Recruiter Fit Score (out of 100)** with a 2-line justification referencing their projects/experience.
                    2. **Missing High-Impact Keywords & IILM Credentials** specifically valued by {target_company} (suggest relevant IILM labs/certifications like {spec_info['iilm_certs']} if missing).
                    3. **3 Rewritten Resume Bullet Points** (take weak lines from their resume and upgrade them with strong action verbs and quantified impact).
                    4. **5 Tailored Mock Interview Questions** that {target_company} asks IILM {program} ({spec}) candidates during campus drives, with brief hints on how to answer.
                    """
                    response = client.models.generate_content(model="gemini-4-hydrogen", contents=prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- VIEW 2: CRC FACULTY ANALYTICS DASHBOARD ---
else:
    st.title("📊 CRC Batch Readiness Analytics (Management View)")
    st.caption("School-Wise Skill Gap Intelligence across BBA, MBA, Psychology & B.Tech (Highest: ₹26 LPA | Avg: ₹8.6 LPA | Top 10%: ₹13.64 LPA)")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Recruiters", "500+", "Consulting, BFSI, Tech, Healthcare")
    m2.metric("Batch Avg. ATS Score", "75%", "+12% post-CRP")
    m3.metric("Top Hiring Schools", "Management & CSE", "81% Avg Readiness")
    m4.metric("Top 10% Avg CTC", "₹13.64 LPA", "Highest: ₹26 LPA")

    df = pd.DataFrame({
        "IILM School / Programme": [
            "School of Management (BBA & MBA)",
            "School of Computer Science (B.Tech CSE/AI)",
            "Department of Psychology (BA/BSc Hons)",
            "Engineering & Bio (Robotics & Biotech)"
        ],
        "Active Specializations Covered": [
            "Analytics, Marketing, Finance, HR, IB, Entrepreneurship",
            "AI/ML, Generative AI, Data Science, Cloud & Cyber Security",
            "Clinical, Counselling, Forensic, Behaviour & Data, AI & Psych",
            "Robotics & AI, Biotechnology & Bioinformatics"
        ],
        "Avg Recruiter Match (%)": [79, 82, 71, 74],
        "Primary Skill Gap Identified": [
            "DCF Valuation & Power BI DAX Dashboards",
            "End-to-End RAG / Cloud Deployment Projects",
            "SPSS/R Quantitative Research & Psychometric Tools",
            "ROS Simulation & Computational Genomics Pipelines"
        ]
    })
    st.subheader("School-Wise Readiness & CRP Workshop Recommendations")
    st.dataframe(df, use_container_width=True)

    st.success("💡 **AI Recommendation for IILM CRC:** Run targeted Corporate Readiness Programme (CRP) bootcamps on *DCF Financial Modeling (KPMG module)* for Management, *GenAI & RAG Deployment* for B.Tech, and *SPSS/R Behavioural Data Analysis* for Psychology ahead of upcoming drives.")
