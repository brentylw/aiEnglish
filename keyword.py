import os  
import pandas as pd  
import spacy  
import streamlit as st  
from collections import Counter  
from spacy.lang.en.stop_words import STOP_WORDS  
import numpy as np  

# Load spaCy model  
nlp = spacy.load('en_core_web_sm')  
nlp.max_length = 20000000  # Adjust max_length if necessary  

def load_corpus(uploaded_files):  
    """Load and return text from uploaded files."""  
    texts = []  
    for uploaded_file in uploaded_files:  
        if uploaded_file.type == "text/plain":  
            texts.append(uploaded_file.getvalue().decode("utf-8").lower())  
    return ' '.join(texts)  

def clean_text(text):  
    """Cleanup the text using spaCy, processing in chunks if necessary."""  
    chunk_size = 1000000  # 1 million characters  
    tokens = []  
    
    for i in range(0, len(text), chunk_size):  
        doc = nlp(text[i:i + chunk_size])  
        tokens.extend([token.text for token in doc if token.is_alpha and token.text not in STOP_WORDS])  
    
    return tokens  

def calculate_keyword_distribution(observed_text, reference_text):  
    """Calculate the frequency of keywords in observed compared to reference using LLR."""  
    observed_tokens = clean_text(observed_text)  
    reference_tokens = clean_text(reference_text)  

    # Frequency distributions  
    observed_freq = Counter(observed_tokens)  
    reference_freq = Counter(reference_tokens)  

    # Total counts  
    total_observed = sum(observed_freq.values())  
    total_reference = sum(reference_freq.values())  

    # Keyness calculation using LLR  
    keyness = {}  
    
    for word, observed_count in observed_freq.items():  
        expected_count = (observed_count / total_observed) * total_reference  
        # LLR calculation  
        if expected_count > 0:  
            llr = 2 * ((observed_count * np.log(observed_count / expected_count)) +   
                        ((total_reference - observed_count) * np.log((total_reference - observed_count) / (total_reference - expected_count))))  
            keyness[word] = llr  

    return keyness  

def get_key_keywords(keywords, threshold):  
    """Filter keywords based on the distribution threshold."""  
    return {word: value for word, value in keywords.items() if value > threshold}  

# Streamlit UI  
st.title("Keyword Analysis App")  

# Upload files  
st.subheader("Upload Observed Corpus")  
observed_files = st.file_uploader("Choose text files for observed corpus", type="txt", accept_multiple_files=True)  

st.subheader("Upload Reference Corpus")  
reference_files = st.file_uploader("Choose text files for reference corpus", type="txt", accept_multiple_files=True)  

if st.button("Analyze Keywords"):  
    if observed_files and reference_files:  
        # Load corpora  
        observed_corpus = load_corpus(observed_files)  
        reference_corpus = load_corpus(reference_files)  

        # Keyness analysis  
        keywords = calculate_keyword_distribution(observed_corpus, reference_corpus)  

        # Filter key keywords  
        threshold = st.slider("Select Threshold for Key Keywords", min_value=0.0, max_value=100.0, value=1.0, step=0.1)  
        key_keywords = get_key_keywords(keywords, threshold)  

        # Output results in a structured table format  
        key_keywords_df = pd.DataFrame(list(key_keywords.items()), columns=['Keyword', 'LLR'])  
        
        if not key_keywords_df.empty:  
            st.write("### Key Keywords Found:")  
            st.dataframe(key_keywords_df.style.highlight_max(axis=0))  # Highlight the maximum LLR value  
        else:  
            st.write("No key keywords found with the given threshold.")  
    else:  
        st.warning("Please upload both observed and reference corpora.")