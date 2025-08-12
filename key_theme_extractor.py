# key_theme_extractor.py
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def extract_key_themes(tweet_texts, top_n=5):
    """
    Extracts key themes from a list of tweet texts using TF-IDF.

    Args:
        tweet_texts (list of str): A list containing the text of tweets.
        top_n (int): The number of top themes to return.

    Returns:
        list of str: A list of the top N key themes.
    """
    # Return an empty list if the input is not valid
    if not tweet_texts or len(tweet_texts) < 2:
        return []

    try:
        # We look for single words and two-word phrases (bigrams)
        # min_df=2 means a term must appear in at least 2 tweets to be considered
        vectorizer = TfidfVectorizer(
            stop_words='english', 
            ngram_range=(1, 2), 
            max_df=0.9,
            min_df=2     
        )

        tfidf_matrix = vectorizer.fit_transform(tweet_texts)

        # Get feature names (the words and phrases)
        feature_names = vectorizer.get_feature_names_out()

        # Create a DataFrame of terms and their TF-IDF scores
        df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

        # Get the mean tf-idf score for each term and sort to find the most important ones
        top_terms = df_tfidf.mean().sort_values(ascending=False).head(top_n)

        return top_terms.index.tolist()

    except ValueError:
        # This can happen if all words are stop words or too infrequent
        return []