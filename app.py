import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 45px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #666;
    margin-bottom: 30px;
}

.feature-box {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    text-align: center;
    min-height: 130px;
}

.score-box {
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #ddd;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🤖 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume. Match your dream job. Identify your skill gaps.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# INTRODUCTION
# =========================================================

st.info(
    "Upload your resume and paste a job description to discover "
    "your matching skills, missing skills and overall job compatibility."
)


# =========================================================
# FEATURES
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-box">
        <h3>📄 Resume Analysis</h3>
        <p>Extract and analyze skills from your resume.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="feature-box">
        <h3>🎯 Job Matching</h3>
        <p>Compare your skills with job requirements.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="feature-box">
        <h3>💡 Smart Insights</h3>
        <p>Find skill gaps and improve your resume.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# =========================================================
# INPUT SECTION
# =========================================================

st.header("🔍 Analyze Your Resume")

col1, col2 = st.columns(2)


with col1:

    resume = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )


with col2:

    job_description = st.text_area(
        "💼 Paste Job Description",
        height=200,
        placeholder="Paste the job description here..."
    )


# =========================================================
# SKILL DATABASE
# =========================================================

skills = [
    "python",
    "java",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "matplotlib",
    "machine learning",
    "deep learning",
    "statistics",
    "data analysis",
    "data visualization",
    "html",
    "css",
    "javascript",
    "git",
    "github",
    "mongodb",
    "mysql"
]


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🚀 Analyze Resume",
    use_container_width=True
):

    if resume is None:

        st.warning("Please upload your resume.")

    elif not job_description.strip():

        st.warning("Please enter a job description.")

    else:

        # -------------------------------------------------
        # Extract Resume Text
        # -------------------------------------------------

        reader = PdfReader(resume)

        resume_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                resume_text += text + " "


        resume_text = resume_text.lower()

        job_text = job_description.lower()


        # -------------------------------------------------
        # Find Resume Skills
        # -------------------------------------------------

        resume_skills = []

        for skill in skills:

            if skill in resume_text:

                resume_skills.append(skill)


        # -------------------------------------------------
        # Find Required Skills
        # -------------------------------------------------

        required_skills = []

        for skill in skills:

            if skill in job_text:

                required_skills.append(skill)


        # -------------------------------------------------
        # Matching Skills
        # -------------------------------------------------

        matched_skills = []

        for skill in required_skills:

            if skill in resume_skills:

                matched_skills.append(skill)


        # -------------------------------------------------
        # Missing Skills
        # -------------------------------------------------

        missing_skills = []

        for skill in required_skills:

            if skill not in resume_skills:

                missing_skills.append(skill)


        # -------------------------------------------------
        # Match Score
        # -------------------------------------------------

        if len(required_skills) > 0:

            match_score = (
                len(matched_skills)
                / len(required_skills)
            ) * 100

        else:

            match_score = 0


        # =================================================
        # RESULTS
        # =================================================

        st.divider()

        st.header("📊 Resume Analysis Dashboard")


        # =================================================
        # KPI CARDS
        # =================================================

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "🎯 Match Score",
                f"{match_score:.1f}%"
            )


        with col2:

            st.metric(
                "🧠 Skills Found",
                len(resume_skills)
            )


        with col3:

            st.metric(
                "✅ Matched",
                len(matched_skills)
            )


        with col4:

            st.metric(
                "⚠ Missing",
                len(missing_skills)
            )


        # =================================================
        # SCORE MESSAGE
        # =================================================

        if match_score >= 80:

            st.success(
                "Excellent match! Your resume aligns strongly "
                "with this job description."
            )

        elif match_score >= 60:

            st.info(
                "Good match! A few additional skills could "
                "strengthen your profile."
            )

        else:

            st.warning(
                "Your resume has several skill gaps for this role."
            )


        # =================================================
        # CHART
        # =================================================

        if required_skills:

            st.subheader("📈 Skills Comparison")


            chart_data = []


            for skill in required_skills:

                chart_data.append({

                    "Skill": skill.title(),

                    "Matched": (
                        1 if skill in matched_skills else 0
                    )

                })


            df = pd.DataFrame(chart_data)


            fig, ax = plt.subplots(
                figsize=(10, 5)
            )


            ax.bar(
                df["Skill"],
                df["Matched"]
            )


            ax.set_title(
                "Job Requirements vs Resume Skills"
            )

            ax.set_ylabel(
                "Match Status"
            )

            ax.set_ylim(0, 1.2)


            plt.xticks(
                rotation=45,
                ha="right"
            )

            plt.tight_layout()


            st.pyplot(fig)


        # =================================================
        # TWO COLUMN ANALYSIS
        # =================================================

        st.subheader("🧩 Skill Gap Analysis")


        col1, col2 = st.columns(2)


        with col1:

            st.markdown("### ✅ Matched Skills")

            if matched_skills:

                for skill in matched_skills:

                    st.write(
                        f"✓ {skill.title()}"
                    )

            else:

                st.write(
                    "No matching skills found."
                )


        with col2:

            st.markdown("### ❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:

                    st.write(
                        f"✗ {skill.title()}"
                    )

            else:

                st.success(
                    "No major missing skills detected!"
                )


        # =================================================
        # RESUME SKILLS
        # =================================================

        st.subheader("📄 Skills Detected in Resume")


        if resume_skills:

            st.write(
                ", ".join(
                    skill.title()
                    for skill in resume_skills
                )
            )

        else:

            st.write(
                "No recognized technical skills detected."
            )


        # =================================================
        # ATS STYLE SCORE
        # =================================================

        st.subheader("📋 Resume Compatibility")


        keyword_score = min(
            100,
            len(matched_skills) * 15
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Keyword Score",
                f"{keyword_score}%"
            )


        with col2:

            st.metric(
                "Job Skill Coverage",
                f"{match_score:.1f}%"
            )


        with col3:

            st.metric(
                "Required Skills",
                len(required_skills)
            )


        # =================================================
        # RECOMMENDATIONS
        # =================================================

        st.subheader("💡 Recommendations")


        if missing_skills:

            for skill in missing_skills:

                st.write(
                    f"• Consider learning or highlighting "
                    f"**{skill.title()}** in your resume."
                )

        else:

            st.success(
                "Your resume covers all detected skills "
                "required by this job."
            )


        # =================================================
        # SUMMARY
        # =================================================

        st.divider()

        st.subheader("🔎 Analysis Summary")


        st.write(
            f"""
            Your resume contains **{len(resume_skills)}**
            recognized technical skills.

            The job description contains
            **{len(required_skills)}** recognized required skills.

            **{len(matched_skills)}** skills matched the
            job requirements.

            Your overall job compatibility score is
            **{match_score:.1f}%**.
            """
        )


        # =================================================
        # FUTURE IMPROVEMENTS
        # =================================================

        with st.expander("🚀 Future Enhancements"):

            st.write(
                """
                • Advanced NLP-based semantic matching

                • Machine learning based resume scoring

                • DOCX resume support

                • Education and experience analysis

                • ATS optimization

                • Multiple job comparison

                • Resume improvement suggestions
                """
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Resume Analyzer | Python • Streamlit • Pandas • NLP-style Skill Matching"
)