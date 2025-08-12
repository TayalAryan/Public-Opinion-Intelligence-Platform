# twitter_client.py
import streamlit as st
import tweepy
import pandas as pd

# Securely get the bearer token from the secrets.toml file
bearer_token = st.secrets["twitter"]["bearer_token"]

client = tweepy.Client(bearer_token)

def search_tweets(query, max_results=10):
    try:
        response = client.search_recent_tweets(f"{query} -is:retweet", max_results=max_results)
        tweets = response.data
        if not tweets:
            return pd.DataFrame()
        tweet_data = [{'id': tweet.id, 'text': tweet.text, 'created_at': tweet.created_at} for tweet in tweets]
        return pd.DataFrame(tweet_data)
    except Exception as e:
        print(f"Error searching tweets: {e}")
        return pd.DataFrame()