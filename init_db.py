# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 11:20:24 2024

@author: Tayyab
"""

from database import create_database
import os

if __name__ == "__main__":
    csv_file = 'data/spotify_tracks.csv'
    db_file = 'data/songs.db'
    
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
    else:
        print(f"CSV file found: {csv_file}")
        print(f"Creating database at: {db_file}")
        create_database(csv_file, db_file)
        print("Database creation process completed.")