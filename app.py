# app.py
import streamlit as st
import pandas as pd

# Import all our custom modules
from summarizer import generate_summary
from ner_extractor import extract_entities
from key_theme_extractor import extract_key_themes
from sentiment_analyzer import analyze_sentiment
from twitter_client import search_tweets
from db_manager import get_or_create_topic, save_tweets_to_db, load_tweets_by_topic, load_all_topics

# --- Page Configuration ---
st.set_page_config(page_title="Topic-Based AI Analyzer", layout="wide")
st.title("Topic-Based AI Analyzer 🎯")

# --- Sidebar ---
st.sidebar.header("Select or Search Topic")

# Load all existing topics for the dropdown menu
topics_df = load_all_topics()
topic_options = {row['query_text']: row['topic_id'] for index, row in topics_df.iterrows()}

# Dropdown for existing topics
selected_topic_query = st.sidebar.selectbox("Choose a previous topic:", options=topic_options.keys())

# Text input for a new topic
new_topic_query = st.sidebar.text_input("Or, enter a new topic to analyze:")

if st.sidebar.button("Analyze Topic"):
    # Determine which query to use (from dropdown or new input)
    query_to_process = new_topic_query if new_topic_query else selected_topic_query

    if query_to_process:
        # Get or create the topic ID in the database
        topic_id = get_or_create_topic(query_to_process)

        # Fetch new tweets from Twitter API
        with st.spinner(f"Fetching latest tweets for '{query_to_process}'..."):
            tweets_df = search_tweets(query_to_process, max_results=10)
            if not tweets_df.empty:
                # Process and save new tweets
                sentiments = tweets_df['text'].apply(analyze_sentiment)
                sentiment_df = pd.json_normalize(sentiments)
                results_df = pd.concat([tweets_df.reset_index(drop=True), sentiment_df], axis=1)
                results_df.rename(columns={'label': 'sentiment_label', 'score': 'sentiment_score'}, inplace=True)
                save_tweets_to_db(results_df, topic_id)
                st.sidebar.success(f"{len(results_df)} new tweets saved.")
            else:
                st.sidebar.info("No new tweets found.")

        # Store the selected topic ID in the session state for display
        st.session_state['current_topic_id'] = topic_id
        st.session_state['current_topic_query'] = query_to_process
    else:
        st.sidebar.error("Please select or enter a topic.")

# --- Main Dashboard Display ---
if 'current_topic_id' in st.session_state:
    topic_id = st.session_state['current_topic_id']
    query = st.session_state['current_topic_query']

    # Load all tweets for the currently selected topic
    topic_data = load_tweets_by_topic(topic_id)

    st.header(f"Analysis for: '{query}'")

    if topic_data.empty:
        st.warning("No tweets have been collected for this topic yet. Fetch new tweets from the sidebar.")
    else:
        # --- AI Summary Section ---
        st.subheader("AI-Generated Summary")
        summary_text = generate_summary(topic_data['text'].tolist())
        st.markdown(summary_text)

        st.divider()

        # --- Metrics & Analysis Section ---
        st.subheader("Topic Analytics")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Tweets Collected", len(topic_data))
            positive_count = topic_data[topic_data['sentiment_label'] == 'POSITIVE'].shape[0]
            negative_count = topic_data[topic_data['sentiment_label'] == 'NEGATIVE'].shape[0]
            st.metric("Positive Tweets", positive_count)
            st.metric("Negative Tweets", negative_count)

        with col2:
            st.subheader("Key Positive Themes")
            positive_themes = extract_key_themes(topic_data[topic_data['sentiment_label'] == 'POSITIVE']['text'].tolist())
            for theme in positive_themes:
                st.markdown(f"- **{theme}**")

            st.subheader("Key Negative Themes")
            negative_themes = extract_key_themes(topic_data[topic_data['sentiment_label'] == 'NEGATIVE']['text'].tolist())
            for theme in negative_themes:
                st.markdown(f"- **{theme}**")

        st.divider()

        st.subheader("Mentioned Entities & Raw Data")
        col1, col2 = st.columns([1, 2]) # Make the data table wider

        with col1:
             mentioned_entities = extract_entities(topic_data['text'].tolist())
             df_entities = pd.DataFrame(mentioned_entities, columns=['Entity', 'Count'])
             st.dataframe(df_entities)

        with col2:
            with st.expander("View All Tweets for this Topic"):
                st.dataframe(topic_data)
else:
    st.info("Select a topic from the sidebar to begin analysis.")