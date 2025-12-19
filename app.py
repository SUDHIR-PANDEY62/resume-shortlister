import streamlit as st
from utils import extract_text_from_pdf
from model import calculate_match, get_skill_match, get_keyword_analysis
import os
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Resume Shortlister Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: rgba(0,0,0,0.65);
        color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .success-box {
        background-color: #2f855a; /* dark green */
        color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 6px solid #2f855a;
    }
    .danger-box {
        background-color: #9b2c2c; /* dark red */
        color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 6px solid #9b2c2c;
    }
    .warning-box {
        background-color: #b45309; /* dark amber */
        color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 6px solid #b45309;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🚀 Resume Shortlister Pro")
st.markdown("### Advanced Resume & Job Description Matching System")
st.divider()

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    threshold = st.slider(
        "Match Score Threshold (%)",
        min_value=30,
        max_value=100,
        value=50,
        step=5,
        help="Minimum score required for shortlisting. Default: 50%"
    )
    
    show_analysis = st.checkbox("Show Detailed Analysis", value=True)
    st.markdown("---")
    st.info("💡 **Pro Tip**: Upload clear PDFs for better text extraction and more accurate matching")

# Main content area
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📄 Resume")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume")
    if resume_file:
        st.success(f"✅ Loaded: {resume_file.name}")

with col2:
    st.subheader("📋 Job Description")
    jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"], key="jd")
    if jd_file:
        st.success(f"✅ Loaded: {jd_file.name}")

st.divider()

# Analysis button
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn1:
    analyze_btn = st.button("🔍 Analyze Match", use_container_width=True, type="primary")

with col_btn2:
    clear_btn = st.button("🗑️ Clear All", use_container_width=True)

# Clear functionality
if clear_btn:
    st.rerun()

# Main analysis
if analyze_btn:
    if resume_file and jd_file:
        try:
            with st.spinner("Analyzing files..."):
                # Extract text
                resume_text = extract_text_from_pdf(resume_file)
                jd_text = extract_text_from_pdf(jd_file)
                
                if not resume_text or not jd_text:
                    st.error("❌ Could not extract text from PDFs. Please try with different files.")
                else:
                    # Calculate scores
                    overall_score = calculate_match(resume_text, jd_text)
                    skill_match = get_skill_match(resume_text, jd_text)
                    
                    # Display results
                    st.divider()
                    st.subheader("📊 Analysis Results")
                    
                    # Score display
                    col_score1, col_score2, col_score3 = st.columns(3)
                    
                    with col_score1:
                        st.metric(
                            label="Overall Match",
                            value=f"{overall_score:.1f}%",
                            delta=f"Target: {threshold}%"
                        )
                    
                    with col_score2:
                        st.metric(
                            label="Skill Match",
                            value=f"{skill_match:.1f}%"
                        )
                    
                    with col_score3:
                        status = "✅ SHORTLISTED" if overall_score >= threshold else "❌ NOT SHORTLISTED"
                        st.metric(
                            label="Decision",
                            value=status
                        )
                    
                    # Decision box with color coding
                    st.divider()
                    if overall_score >= threshold:
                        st.markdown(
                            f"<div class='success-box'><h3>✅ Candidate SHORTLISTED</h3><p>Match Score: <strong>{overall_score:.1f}%</strong> (Threshold: {threshold}%)</p></div>",
                            unsafe_allow_html=True
                        )
                    else:
                        gap = threshold - overall_score
                        st.markdown(
                            f"<div class='danger-box'><h3>❌ Candidate NOT SHORTLISTED</h3><p>Match Score: <strong>{overall_score:.1f}%</strong> (Threshold: {threshold}%)<br>Gap: <strong>{gap:.1f}%</strong></p></div>",
                            unsafe_allow_html=True
                        )
                    
                    # Detailed analysis
                    if show_analysis:
                        st.divider()
                        st.subheader("📈 Detailed Analysis")
                        
                        analysis_tab1, analysis_tab2 = st.tabs(["📊 Score Breakdown", "📝 Content Summary"])
                        
                        with analysis_tab1:
                            col_a1, col_a2 = st.columns(2)
                            with col_a1:
                                st.write("**Resume Length:**")
                                st.info(f"{len(resume_text)} characters")
                            with col_a2:
                                st.write("**Job Description Length:**")
                                st.info(f"{len(jd_text)} characters")
                        
                        with analysis_tab2:
                            col_t1, col_t2 = st.columns(2)
                            with col_t1:
                                st.write("**Resume Preview:**")
                                st.text_area(
                                    "Resume Text",
                                    value=resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
                                    height=200,
                                    disabled=True,
                                    label_visibility="collapsed"
                                )
                            with col_t2:
                                st.write("**Job Description Preview:**")
                                st.text_area(
                                    "JD Text",
                                    value=jd_text[:500] + "..." if len(jd_text) > 500 else jd_text,
                                    height=200,
                                    disabled=True,
                                    label_visibility="collapsed"
                                )
                    
                    # Footer with timestamp
                    st.divider()
                    col_f1, col_f2 = st.columns([3, 1])
                    with col_f1:
                        st.caption(f"Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    with col_f2:
                        if st.button("📥 Export Results"):
                            st.success("Export feature coming soon!")
        
        except Exception as e:
            st.error(f"❌ Error processing files: {str(e)}")
    
    else:
        st.markdown(
            "<div class='warning-box'><h3>⚠️ Missing Files</h3><p>Please upload both Resume and Job Description files to proceed.</p></div>",
            unsafe_allow_html=True
        )
