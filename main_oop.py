# Import required libraries
import nltk
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from collections import Counter


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
