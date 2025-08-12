# db_manager.py
import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

DB_URL = st.secrets["database"]["db_url"]
engine = create_engine(DB_URL)

def get_or_create_topic(query_text):
    """
    Finds the ID of an existing topic or creates a new one and returns the ID.
    """
    with engine.connect() as conn:
        # Check if topic exists
        result = conn.execute(text("SELECT topic_id FROM search_topics WHERE query_text = :query"), {"query": query_text}).scalar_one_or_none()

        if result:
            # Topic exists, return its ID
            return result
        else:
            # Topic doesn't exist, insert it and return the new ID
            insert_result = conn.execute(
                text("INSERT INTO search_topics (query_text) VALUES (:query) RETURNING topic_id"),
                {"query": query_text}
            )
            conn.commit()
            return insert_result.scalar_one()

def save_tweets_to_db(df, topic_id):
    """
    Saves a DataFrame of tweets to the database, including the topic_id.
    """
    df['topic_id'] = topic_id  # Add the topic_id column to the DataFrame

    # Reorder columns to match the table structure
    df = df[['id', 'topic_id', 'text', 'created_at', 'sentiment_label', 'sentiment_score']]

    try:
        existing_ids = pd.read_sql("SELECT id FROM tweets", engine)['id'].tolist()
        df_to_save = df[~df['id'].isin(existing_ids)]
        if not df_to_save.empty:
            df_to_save.to_sql('tweets', engine, if_exists='append', index=False)
    except Exception as e:
        print(f"Error saving tweets: {e}")

def load_tweets_by_topic(topic_id):
    """
    Loads all tweets for a specific topic ID from the database.
    """
    # This new version uses a '?' placeholder and passes parameters
    # in a way that the database driver understands.
    sql_query = "SELECT * FROM tweets WHERE topic_id = %(topic_id)s ORDER BY created_at DESC"

    return pd.read_sql(
        sql_query,
        engine,
        params={"topic_id": topic_id}
    )

def load_all_topics():
    """
    Loads all previously searched topics from the database.
    """
    return pd.read_sql("SELECT topic_id, query_text FROM search_topics ORDER BY first_searched_at DESC", engine)