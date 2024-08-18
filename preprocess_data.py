# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 10:41:08 2024

@author: Tayyab
"""

import pandas as pd
import pickle
from data_processor import DataProcessor

# Load and process data
data_processor = DataProcessor('data/spotify_tracks.csv')
processed_data = data_processor.get_processed_data()

# Save processed data as pickle
with open('data/processed_data.pkl', 'wb') as f:
    pickle.dump(processed_data, f)

print("Data processed and saved as pickle file.")