import streamlit as st
import google.generativeai as genai

# --------------------------
# 🔑 Hardcode your API key here
# --------------------------
API_KEY = "AIzaSyDnNDR_Y6JPrDD3cjahXb4mN3PmUTULlX8"

# --------------------------
# 🎨 Streamlit App Layout
# --------------------------
st.set_page_config(page_title="AI Mail Generator", page_icon="📧", layout="wide")

st.title("📧 AI Mail Generator with Gemini")
st.write("Generate professional job application emails using Gemini by providing a job description and company details.")

# --------------------------
# Sidebar Controls
# --------------------------
with st.sidebar:
    st.subheader("🔐 API & Model")
    st.info("Using API Key set inside the code")

    model_name = st.selectbox("Model", ["gemini-1.5-flash", "gemini-1.5-pro"], index=0)
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.4, 0.05)

    st.markdown("---")
    st.subheader("✍️ Style Controls")
    tone = st.selectbox("Tone", ["warm & professional", "concise & direct", "enthusiastic trainee", "formal"], index=0)
    length_pref = st.selectbox("Length", ["short (8–10 lines)", "medium (12–16 lines)", "long (up to ~250 words)"], index=1)
    extras = st.text_area("Extra instructions (optional)", placeholder="e.g., emphasize immediate joining, mention relocation to Kochi, etc.")

# --------------------------
# User Inputs
# --------------------------
st.subheader("📄 Job Description")
job_desc = st.text_area("Paste the Job Description", height=180, placeholder="Enter job description here...")

st.subheader("🏢 About the Company")
company_desc = st.text_area("Paste About the Company", height=120, placeholder="Enter company details here...")

# --------------------------
# Generate Email Button
# --------------------------
if st.button("🚀 Generate Email"):
    if not job_desc or not company_desc:
        st.error("⚠️ Please provide both Job Description and Company details.")
    elif not API_KEY:
        st.error("⚠️ API Key not set. Please update API_KEY variable in the code.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(model_name)

            prompt = f"""
            Write a professional email applying for the role described below.
            - Job Description: {job_desc}
            - About the Company: {company_desc}

            The email should:
            - Be addressed properly
            - Have a subject line
            - Highlight relevant skills (machine learning, AI, Python, etc.)
            - End politely with interest in further discussion
            - Tone: {tone}
            - Length: {length_pref}
            - Extra instructions: {extras}

            Format output as:

            Subject: ...
            
            Dear [Hiring Team/Manager],

            [Email body]

            Best regards,
            Anandha Krishnan S
            """

            with st.spinner("✍️ Generating email..."):
                response = model.generate_content(prompt, generation_config={"temperature": temperature})
                mail_text = response.text

            st.success("✅ Email Generated!")
            st.markdown("### 📧 Generated Email")
            st.write(mail_text)

            st.download_button("⬇️ Download Email", mail_text, file_name="job_application_email.txt")

        except Exception as e:
            st.error(f"❌ Error: {e}")
