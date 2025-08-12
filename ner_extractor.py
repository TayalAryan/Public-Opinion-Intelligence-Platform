# ner_extractor.py
import spacy
from collections import Counter
import pandas as pd

# Load the spaCy model. This can take a moment on first run.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Spacy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm'")
    nlp = None

def extract_entities(tweet_texts, entity_types=['PERSON', 'ORG'], top_n=5):
    """
    Extracts named entities (like people or organizations) from a list of tweets.

    Args:
        tweet_texts (list of str): A list of tweet texts.
        entity_types (list of str): The types of entities to look for (e.g., 'PERSON', 'ORG').
        top_n (int): The number of top entities to return.

    Returns:
        list of tuples: A list of (entity, count) tuples.
    """
    if not nlp or not tweet_texts or not isinstance(tweet_texts, list):
        return []

    all_entities = []
    # Process tweets in batches for efficiency
    for doc in nlp.pipe(tweet_texts):
        for ent in doc.ents:
            # Check if the entity type is one we're interested in
            if ent.label_ in entity_types:
                # Add the text of the entity, stripped of leading/trailing whitespace
                all_entities.append(ent.text.strip())

    # Count the occurrences of each entity and get the most common ones
    if not all_entities:
        return []

    entity_counts = Counter(all_entities)
    return entity_counts.most_common(top_n)