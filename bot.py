import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict

class CDPChatbot:
    def __init__(self):
        self.cdp_docs = {
            "Segment": "https://segment.com/docs/",
            "mParticle": "https://docs.mparticle.com/",
            "Lytics": "https://docs.lytics.com/",
            "Zeotap": "https://docs.zeotap.com/home/en-us/",
        }
        self.doc_index = defaultdict(lambda: defaultdict(list))
        self.load_documentation()

    def load_documentation(self):
        """Loads and indexes the documentation for each CDP."""
        for cdp, url in self.cdp_docs.items():
            try:
                self.index_documentation(cdp, url)
            except Exception as e:
                print(f"Error loading documentation for {cdp}: {e}")

    def index_documentation(self, cdp, url):
        """Indexes the documentation for a specific CDP."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            text_parts = [p.get_text(separator=" ", strip=True) for p in soup.find_all("p")]
            text_parts.extend([h.get_text(separator=" ", strip=True) for h in soup.find_all(re.compile("^h[1-6]$"))])

            full_text = " ".join(text_parts)
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', full_text)

            for sentence in sentences:
                words = re.findall(r'\w+', sentence.lower())
                for word in words:
                    self.doc_index[cdp][word].append(sentence)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
        except Exception as e:
            print(f"Error indexing URL {url}: {e}")

    def find_relevant_cdp(self, question):
        """Identifies the CDP mentioned in the question."""
        question_lower = question.lower()
        for cdp in self.cdp_docs:
            if cdp.lower() in question_lower:
                return cdp
        return None

    def answer_question(self, question):
        """Answers a user's question based on the indexed documentation."""
        cdp = self.find_relevant_cdp(question)
        if not cdp:
            return "Sorry, I couldn't identify which CDP you're asking about. Please specify Segment, mParticle, Lytics, or Zeotap."

        question_words = re.findall(r'\w+', question.lower())
        relevant_sentences = set()

        for word in question_words:
            relevant_sentences.update(self.doc_index[cdp].get(word, []))

        if relevant_sentences:
            return f"Here's what I found in the {cdp} documentation:\n\n" + "\n".join(relevant_sentences)
        else:
            return f"Sorry, I couldn't find specific instructions for that in the {cdp} documentation. Please try rephrasing your question."

# Example usage:
chatbot = CDPChatbot()

questions = [
    "How do I set up a new source in Segment?",
    "How can I create a user profile in mParticle?",
    "How do I build an audience segment in Lytics?",
    "How can I integrate my data with Zeotap?",
    "Which Movie",
    "How do I create a very long and detailed query regarding user attributes and data ingestion within the Lytics platform, considering various integration methods and potential data transformations?",
]

for question in questions:
    print(f"\nQuestion: {question}")
    answer = chatbot.answer_question(question)
    print(f"Answer: {answer}")