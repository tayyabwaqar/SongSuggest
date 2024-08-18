# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 09:28:11 2024

@author: Tayyab
"""

import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)
        self.process_data()
        
    def process_data(self):
        # Select relevant features
        features = ['artist_name', 'track_name', 'popularity', 'year', 'genre', 
                    'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
                    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
        self.data = self.data[features]
        
        # Rename columns for consistency
        self.data = self.data.rename(columns={'artist_name': 'artist', 'track_name': 'song'})
        
        # Fill NaN values
        self.data['genre'] = self.data['genre'].fillna('Unknown')
        self.data['year'] = self.data['year'].fillna(self.data['year'].median())
        self.data['popularity'] = self.data['popularity'].fillna(self.data['popularity'].median())
        
        # Fill NaN values in numeric columns with their median
        numeric_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
                            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
        self.data[numeric_features] = self.data[numeric_features].fillna(self.data[numeric_features].median())
        
        # Combine relevant features into a single string for recommendation
        self.data['features'] = self.data[numeric_features].astype(str).agg(' '.join, axis=1)
        self.data['features'] += ' ' + self.data['artist'].fillna('') + ' ' + self.data['genre'].fillna('') + ' ' + self.data['year'].astype(str)
        
        # Ensure all values in 'features' are strings
        self.data['features'] = self.data['features'].fillna('').astype(str)
        
    def get_processed_data(self):
        return self.data
    
    @staticmethod
    def get_dataset_stats(data):
        return {
            'total_songs': len(data),
            'unique_artists': data['artist'].nunique(),
            'avg_popularity': round(data['popularity'].mean(), 2),
            'most_common_genre': data['genre'].mode().iloc[0],
            'year_range': f"{data['year'].min():.0f} - {data['year'].max():.0f}"
        }