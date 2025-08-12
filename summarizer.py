# summarizer.py
import streamlit as st
import google.generativeai as genai
import pandas as pd

def generate_summary(tweet_texts):
    """
    Generates a summary of a topic based on a list of tweets using the Gemini API.

    Args:
        tweet_texts (list of str): A list containing the text of tweets.

    Returns:
        str: A summary of the topic, or an error message.
    """
    if not tweet_texts or len(tweet_texts) < 3:
        return "Not enough new tweets to generate a meaningful summary."

    try:
        # Configure the API key from secrets
        api_key = st.secrets["google_ai"]["api_key"]
        genai.configure(api_key=api_key)

        # Create the generative model
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Combine all tweets into a single block of text for the prompt
        all_tweets_text = "\n".join(f"- {text}" for text in tweet_texts)

        # Create the prompt for the model
        prompt = f"""
        Based on the following recent tweets, please provide a concise, neutral summary of the current conversation and key points regarding the topic.

        Tweets:
        {all_tweets_text}

        Summary:
        """

        # Generate the content
        response = model.generate_content(prompt)

        # Clean up the response text
        summary_text = response.text.strip().replace('•', '*')

        return summary_text

    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return "Could not generate summary due to an error."