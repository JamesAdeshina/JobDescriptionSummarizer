# Import required libraries
import ssl
import streamlit as st
import nltk
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from collections import Counter

# Additional libraries for file processing
import PyPDF2
import docx2txt

# ------------------ SSL Context for NLTK Downloads ------------------
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')


class JobDescriptionSummarizer:
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")

    def preprocess_text(self, text):
        # Tokenize and remove stopwords
        doc = self.nlp(text)
        tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
        return tokens

    def extract_keywords(self, tokens, top_n=10):
        # Count word frequencies
        word_freq = Counter(tokens)
        # Get the most common words
        keywords = word_freq.most_common(top_n)
        return keywords

    def summarize_text(self, text, sentences_count=3):
        # Create a parser and tokenizer
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        # Use LSA Summarizer
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences_count)
        return ' '.join([str(sentence) for sentence in summary])

    def summarize_job_description(self, jd_text):
        # Preprocess the text
        tokens = self.preprocess_text(jd_text)
        # Extract keywords
        keywords = self.extract_keywords(tokens)
        # Summarize the text
        summary = self.summarize_text(jd_text)
        return {
            "keywords": keywords,
            "summary": summary
        }


def read_uploaded_file(uploaded_file):
    """
    Process the uploaded file based on its type.
    Supports PDF, DOCX, and TXT files.
    """
    file_type = uploaded_file.name.split('.')[-1].lower()
    if file_type == 'pdf':
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    elif file_type == 'docx':
        text = docx2txt.process(uploaded_file)
        return text
    elif file_type == 'txt':
        return uploaded_file.read().decode("utf-8")
    elif file_type == 'doc':
        st.error("DOC format is not supported. Please convert the file to DOCX.")
        return None
    else:
        st.error("Unsupported file type")
        return None



def main():
    st.title("Job Description Summarizer")

    # Allow user to choose input method: direct text or file upload
    input_method = st.selectbox("Choose input method", ["Text Input", "File Upload"])

    if input_method == "Text Input":
        jd_text = st.text_area("Enter Job Description", height=300)
    else:
        uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt", "docx", "doc"])
        jd_text = ""
        if uploaded_file is not None:
            jd_text = read_uploaded_file(uploaded_file)

    if st.button("Summarize"):
        if jd_text:
            summarizer = JobDescriptionSummarizer()
            result = summarizer.summarize_job_description(jd_text)
            st.subheader("Keywords")
            st.write(result["keywords"])
            st.subheader("Summary")
            st.write(result["summary"])
        else:
            st.error("Please provide a valid job description either via text input or file upload.")

# streamlit run "/Users/apple2015/Documents/MSc/SchoolStuff/NLP/Personal/Job Description (JD) Summarizer/main_oop_ui.py"


if __name__ == "__main__":
    main()