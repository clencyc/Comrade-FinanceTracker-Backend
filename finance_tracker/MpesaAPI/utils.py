import requests
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans


def get_access_token():
    consumer_key = "iSrGmRANhliLTHf3T2dfpQ8V0Lh5afWAPAaSgcvcKXohV5qM"
    consumer_secret = "DQLtzDydwKCbVkv8S0opePWl2He9oIMZnsWMTANpUDDomYo2iDDLdOt9DCbUYHKP"
    auth_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception("Failed to get access token")


def categorize_transaction(description):
    if description is None:
        return "Unknown"
    
    new_description = vectorizer.transform([description])
    # Sample data for training
    data = {
        'description': ['KFC meal', 'Uber ride', 'Textbook purchase', 'Airtime top-up'],
        'category': ['Food', 'Transport', 'Education', 'Airtime']
    }
    df = pd.DataFrame(data)

    # Train a simple text classification model
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['description'])
    kmeans = KMeans(n_clusters=4, random_state=42)
    kmeans.fit(X)

    # Predict category for the new transaction
    new_description = vectorizer.transform([description])
    category_id = kmeans.predict(new_description)[0]
    return df['category'].unique()[category_id]