# setup_database.py
import toml
from sqlalchemy import create_engine, text

print("Attempting to create database tables...")
try:
    secrets = toml.load(".streamlit/secrets.toml")
    DB_URL = secrets["database"]["db_url"]
    engine = create_engine(DB_URL)

    create_tables_script = """
    -- Table to store each unique search query
    CREATE TABLE IF NOT EXISTS search_topics (
        topic_id SERIAL PRIMARY KEY,
        query_text VARCHAR(255) UNIQUE NOT NULL,
        first_searched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Table to store tweets, now with a link to a search topic
    CREATE TABLE IF NOT EXISTS tweets (
        id BIGINT PRIMARY KEY,
        topic_id INTEGER NOT NULL REFERENCES search_topics(topic_id),
        text TEXT,
        created_at TIMESTAMP WITH TIME ZONE,
        sentiment_label VARCHAR(10),
        sentiment_score FLOAT
    );
    """

    with engine.connect() as conn:
        conn.execute(text(create_tables_script))
        conn.commit()

    print("Tables 'search_topics' and 'tweets' created successfully.")

except Exception as e:
    print(f"An error occurred: {e}")