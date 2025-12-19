 🚀 Resume Shortlister Pro  
### Advanced Resume & Job Description Matching System

Resume Shortlister Pro is a Machine Learning–based web application that automatically analyzes and matches **candidate resumes** with **job descriptions** to assist HR teams in fast and unbiased shortlisting.

---

## 📌 Features

- 📄 Upload Resume (PDF)
- 📋 Upload Job Description (PDF)
- 🧠 NLP-based text processing
- 📊 Resume–JD Match Percentage
- ✅ Automatic Shortlist / ❌ Reject decision
- 📈 Skill Match Analysis
- 🌐 User-friendly web interface using Streamlit

---

## 🧠 How It Works

1. User uploads a **Resume (PDF)**
2. User uploads a **Job Description (PDF)**
3. Text is extracted using PDF parsing
4. Natural Language Processing (NLP) techniques are applied
5. Resume and JD are converted into numerical vectors using **TF-IDF**
6. **Cosine Similarity** is used to calculate match score
7. System displays:
   - Overall Match Percentage
   - Skill Match
   - Shortlisting Decision

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Machine Learning:** Scikit-learn  
- **NLP:** TF-IDF Vectorizer  
- **Similarity Measure:** Cosine Similarity  
- **Web Framework:** Streamlit  
- **PDF Handling:** PyPDF2  

---

## 📂 Project Structure

resume-shortlister/
│
├── app.py # Streamlit web app
├── model.py # ML & similarity logic
├── utils.py # PDF text extraction
├── requirements.txt # Project dependencies
└── README.md # Project documentation

yaml
Copy code

---

## ▶️ How to Run the Project

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
2️⃣ Run the Application
bash
Copy code
streamlit run app.py
3️⃣ Open in Browser
The app will open automatically in your default browser.

📊 Output Example
Overall Match: 78%

Skill Match: 100%

Decision: ✅ SHORTLISTED

🎯 Use Cases
HR Resume Screening

Internship & Job Shortlisting

Applicant Tracking System (ATS) simulation

Academic Mini / Major Projects

🚀 Future Enhancements
Ranking multiple resumes

Skill gap analysis

Experience-based weighting

AI-based resume feedback

Support for DOCX files.






