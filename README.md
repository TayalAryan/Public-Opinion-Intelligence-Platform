# Public Opinion Intelligence Platform

This is a full-stack data science application built with Python and Streamlit that analyzes real-time data from the Twitter/X API for any given topic. It provides an AI-generated summary, sentiment analysis, key theme extraction, and named entity recognition.

## Key Features

* **AI-Powered Summaries:** Uses the Google Gemini API to generate dynamic summaries of the conversation.
* **Topic-Based Analysis:** Employs a relational PostgreSQL database to store and analyze tweets on a per-topic basis, ensuring data integrity.
* **Detailed NLP Insights:** Performs sentiment analysis, key theme extraction (TF-IDF), and Named Entity Recognition (spaCy).
* **Interactive Dashboard:** Built with Streamlit for a user-friendly experience.

## How to Run This Project

1.  Clone the repository: `git clone <repository-url>`
2.  Navigate into the project directory: `cd <repository-name>`
3.  Create a virtual environment: `python -m venv venv`
4.  Activate it: `venv\Scripts\activate.bat`
5.  Install required packages: `pip install -r requirements.txt`
6.  Set up your API keys and database URL in `.streamlit/secrets.toml`.
7.  Run the database setup script: `python setup_database.py`
8.  Run the Streamlit app: `streamlit run app.py`