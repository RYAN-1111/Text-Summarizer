# summarizer.py

from transformers import pipeline
import nltk

# Download punkt tokenizer for sentence splitting
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Load the summarization pipeline with Pegasus model
summarizer = pipeline("summarization", model="google/pegasus-xsum",framework="pt")  # Use device=0 for GPU, or -1 for CPU

def chunk_text(text, max_tokens=800):
    """
    Splits text into smaller chunks for summarization.
    Pegasus works best under 1024 tokens.
    """
    sentences = sent_tokenize(text)
    chunks = []
    chunk = ""

    for sentence in sentences:
        if len(chunk.split()) + len(sentence.split()) <= max_tokens:
            chunk += " " + sentence
        else:
            chunks.append(chunk.strip())
            chunk = sentence
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def summarize_text(text):
    """
    Summarizes long input text using Pegasus model.
    Automatically chunks and recombines summaries.
    """
    chunks = chunk_text(text)
    print(f"[INFO] Splitting input into {len(chunks)} chunk(s)...")
    
    summaries = summarizer(
        chunks,
        max_length=200,   # Pegasus prefers shorter summaries
        min_length=50,
        do_sample=False
    )

    full_summary = " ".join([s['summary_text'] for s in summaries])
    return full_summary


