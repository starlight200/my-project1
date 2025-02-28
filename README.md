# my-project1
Overview:
This project is a chatbot designed to answer "how-to" questions related to four Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap. It extracts relevant information from official documentation and provides users with accurate responses.

Features:
  Automated Documentation Scraping: Retrieves data from official CDP documentation.
  NLP-Powered Query Processing: Uses SentenceTransformer to understand user queries.
  Fast Search with FAISS: Implements FAISS indexing for efficient information retrieval.
  REST API with FastAPI: Provides a simple endpoint for users to ask questions.
 
Technologies Used:
  Python (FastAPI, Requests, BeautifulSoup)
  NLP Model (SentenceTransformer: all-MiniLM-L6-v2)
  Vector Search (FAISS)
  Web Scraping (BeautifulSoup)
