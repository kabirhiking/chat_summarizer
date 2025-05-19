import os
import re
from collections import defaultdict, Counter
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk


 # This script processes chat logs, counts messages, and extracts keywords using TF-IDF or simple frequency analysis.
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

def parse_chat_log(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    messages = defaultdict(list)

    for line in lines:
        line = line.strip()
        if line.startswith("User:"):
            messages['user'].append(line.replace("User:", "").strip())
        elif line.startswith("AI:"):
            messages['ai'].append(line.replace("AI:", "").strip())

    return messages

def count_messages(messages):
    return {
        "total": len(messages['user']) + len(messages['ai']),
        "user": len(messages['user']),
        "ai": len(messages['ai']),
    }
    

# Function to extract keywords using simple frequency analysis
def get_most_common_keywords(messages, top_n=5):
    all_text = " ".join(messages['user'] + messages['ai']).lower()
    words = re.findall(r'\b\w+\b', all_text)
    filtered_words = [word for word in words if word not in STOPWORDS]
    counter = Counter(filtered_words)
    return [word for word, _ in counter.most_common(top_n)]

def get_tfidf_keywords(messages, top_n=5):
    all_texts = messages['user'] + messages['ai']
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    scores = tfidf_matrix.sum(axis=0).A1
    feature_names = vectorizer.get_feature_names_out()
    scored_words = list(zip(feature_names, scores))
    top_keywords = sorted(scored_words, key=lambda x: x[1], reverse=True)[:top_n]
    return [word for word, _ in top_keywords]

def summarize_chat(messages, use_tfidf=False):
    stats = count_messages(messages)
    keywords = get_tfidf_keywords(messages) if use_tfidf else get_most_common_keywords(messages)

    summary = f"""Summary:
- The conversation had {stats['total']} exchanges.
- User sent {stats['user']} messages, AI sent {stats['ai']} messages.
- Most common keywords: {', '.join(keywords)}.
"""
    return summary

def process_folder(folder_path, use_tfidf=False):
    summaries = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            path = os.path.join(folder_path, file_name)
            messages = parse_chat_log(path)
            summary = summarize_chat(messages, use_tfidf=use_tfidf)
            summaries.append((file_name, summary))
    return summaries
