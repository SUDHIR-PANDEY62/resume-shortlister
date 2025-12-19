from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from collections import Counter
from difflib import SequenceMatcher

def calculate_match(resume_text, jd_text):
    """
    Calculate overall match percentage between resume and job description
    using multiple algorithms for accuracy
    """
    # Method 1: TF-IDF Cosine Similarity (weighted)
    documents = [resume_text, jd_text]
    vectorizer = TfidfVectorizer(stop_words='english', max_features=500, ngram_range=(1, 2))
    vectors = vectorizer.fit_transform(documents)
    tfidf_score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    
    # Method 2: Sequence Matching (checks actual text similarity)
    sequence_score = SequenceMatcher(None, resume_text.lower(), jd_text.lower()).ratio()
    
    # Method 3: Common words matching
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())
    
    common_words = resume_words.intersection(jd_words)
    all_words = resume_words.union(jd_words)
    
    if len(all_words) > 0:
        word_match_score = len(common_words) / len(all_words)
    else:
        word_match_score = 0
    
    # Combine all methods (weighted average)
    # 40% TF-IDF, 35% Sequence Match, 25% Word Overlap
    combined_score = (tfidf_score * 0.40) + (sequence_score * 0.35) + (word_match_score * 0.25)
    
    final_score = round(combined_score * 100, 2)
    
    # Ensure score doesn't go below 0 or above 100
    return max(0, min(100, final_score))


def get_skill_match(resume_text, jd_text):
    """
    Calculate skill match percentage by analyzing technical keywords
    """
    # Common technical skills and keywords
    tech_keywords = {
        'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'golang', 'rust', 'php', 'ruby', 'swift'],
        'web': ['html', 'css', 'react', 'angular', 'vue', 'node', 'django', 'flask', 'fastapi', 'express'],
        'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'cassandra', 'elasticsearch'],
        'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github'],
        'data': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'sklearn', 'spark'],
    }
    
    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()
    
    matched_skills = 0
    total_jd_keywords = 0
    
    for category, keywords in tech_keywords.items():
        for keyword in keywords:
            if keyword in jd_lower:
                total_jd_keywords += 1
                if keyword in resume_lower:
                    matched_skills += 1
    
    if total_jd_keywords == 0:
        return 50.0
    
    skill_match_score = (matched_skills / total_jd_keywords) * 100
    return round(min(skill_match_score, 100), 2)


def get_keyword_analysis(resume_text, jd_text):
    """
    Analyze and extract key matching keywords between resume and JD
    """
    # Extract words
    def extract_keywords(text):
        # Convert to lowercase and remove special characters
        text = text.lower()
        # Extract words
        words = re.findall(r'\b[a-z]{3,}\b', text)
        return set(words)
    
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)
    
    # Find matching keywords
    common_keywords = resume_keywords.intersection(jd_keywords)
    
    return {
        'matching': sorted(list(common_keywords)),
        'from_jd_only': sorted(list(jd_keywords - resume_keywords))[:10],
        'match_count': len(common_keywords)
    }
