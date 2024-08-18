# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 09:27:33 2024

@author: Tayyab
"""

import sqlite3
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

class Recommender:
    def __init__(self, db_file):
        self.db_file = db_file
        self.feature_columns = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
                                'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'popularity']
    
    def get_song_features(self, track_name):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM songs WHERE track_name = ?", (track_name,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, result))
        return None
    
    def get_recommendations(self, track_name, n=5, prioritize_popular=True):
        song_features = self.get_song_features(track_name)
        if not song_features:
            return None
        
        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query("SELECT * FROM songs", conn)
        conn.close()
        
        # Prepare feature matrix
        X = df[self.feature_columns].values
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Get the features of the input song
        input_features = np.array([song_features[col] for col in self.feature_columns]).reshape(1, -1)
        input_features_scaled = scaler.transform(input_features)
        
        # Calculate similarities
        similarities = cosine_similarity(input_features_scaled, X_scaled).flatten()
        
        # Combine similarity with popularity if prioritizing popular songs
        if prioritize_popular:
            popularity_weight = 0.3
            combined_scores = (1 - popularity_weight) * similarities + popularity_weight * df['popularity'].values / 100
        else:
            combined_scores = similarities
        
        # Get top N recommendations
        top_indices = combined_scores.argsort()[-n-1:-1][::-1]
        recommendations = []
        for idx in top_indices:
            if df.iloc[idx]['track_name'] != track_name:
                rec = df.iloc[idx].to_dict()
                rec['similarity'] = similarities[idx]
                recommendations.append(rec)
        
        return recommendations
    
    def get_random_song(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM songs ORDER BY RANDOM() LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, result))
        return None