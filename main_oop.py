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


# Example usage
if __name__ == "__main__":
    summarizer = JobDescriptionSummarizer()

    job_description = """
    We are looking for a Python Developer to join our team. The ideal candidate should have experience with Python, Django, and Flask.
    Responsibilities include developing and maintaining web applications, writing clean and scalable code, and collaborating with cross-functional teams.
    The candidate should have a strong understanding of software development principles and be able to work in an agile environment.
    Experience with REST APIs, databases, and version control systems like Git is a plus.
    """

    result = summarizer.summarize_job_description(job_description)
    print("Keywords:", result["keywords"])
    print("Summary:", result["summary"])

    job_description2 = """
    UniHub UniHub Dashboard James Notifications0 Spencer Academies Trust Nottingham, East Midlands, United Kingdom 1 job Teaching Intern United Kingdom £425 per week for full attendance & participation Full-time, Temporary Teaching Internship Programme takes place in Spencer Academies Trust schools across Nottinghamshire and Derbyshire. You will gain an insight into the life of a teacher and participate in training sessions. Applications close on 9 Feb 2025 Job details Teaching Internship Programme takes place in Spencer Academies Trust schools across Nottinghamshire and Derbyshire. You will gain an insight into the life of a teacher and participate in training sessions. Subjects: Maths Physics Chemistry Computing MFL. On the programme you will gain in-school experience, learn about the life of a teacher, support pupils in the classroom, shadow experienced teachers, discover the routes into teaching and participate in teaching. Eligibility You must be an undergraduate or master’s student, studying in a UK university, who is considering a career in teaching. The programme lasts for 3 weeks, 9th to 27th June 2025. You'll receive personalised post-programme support to assist you with getting into a career in teaching. More info Job types Graduate job Internship Expected commencement 9th June 2024 Posted 7 Nov 2024 Applications close on 9 Feb 2025 More jobs Independent Advisory Group – Volunteer – Derbyshire Derbyshire Constabulary Derbyshire, England, United Kingdom Youth Work Volunteer Safe and Sound Group First Floor East Mill, Darley Abbey Mills, Darley Abbey., Derby, Derbyshire, England, DE22 1DZ, United Kingdom Awareness Volunteer Safe and Sound Group First Floor East Mill, Darley Abbey Mills, Darley Abbey, Derby, Derbyshire, England, DE22 1DZ, United Kingdom
    """

    result2 = summarizer.summarize_job_description(job_description2)
    print("Keywords:", result2["keywords"])
    print("Summary:", result2["summary"])