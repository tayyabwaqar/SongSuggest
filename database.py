# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 11:18:51 2024

@author: Tayyab
"""

import sqlite3
import pandas as pd

def create_database(csv_file, db_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_file)
    
    # Write the dataframe to a SQLite table
    df.to_sql('songs', conn, if_exists='replace', index=False)
    
    # Create an index on the track_name and artist_name columns for faster searching
    conn.execute('CREATE INDEX idx_track_artist ON songs(track_name, artist_name)')
    
    conn.close()
    
    print(f"Database created successfully with {len(df)} rows.")
    print(f"Columns in the database: {', '.join(df.columns)}")

def search_songs(db_file, query, limit=10):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Use LIKE for case-insensitive prefix matching
    cursor.execute("""
    SELECT track_name, artist_name FROM songs 
    WHERE track_name LIKE ? || '%' OR artist_name LIKE ? || '%'
    LIMIT ?
    """, (query, query, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return [f"{track} by {artist}" for track, artist in results]

def get_song_details(db_file, track_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM songs WHERE track_name = ?", (track_name,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, result))
    return None

def get_stats(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    stats = {}
    cursor.execute("SELECT COUNT(*) FROM songs")
    stats['total_songs'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT artist_name) FROM songs")
    stats['unique_artists'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(popularity) FROM songs")
    stats['avg_popularity'] = round(cursor.fetchone()[0], 2)
    
    cursor.execute("SELECT genre, COUNT(*) as count FROM songs GROUP BY genre ORDER BY count DESC LIMIT 1")
    result = cursor.fetchone()
    stats['most_common_genre'] = result[0] if result else "N/A"
    
    cursor.execute("SELECT MIN(year), MAX(year) FROM songs")
    min_year, max_year = cursor.fetchone()
    stats['year_range'] = f"{min_year} - {max_year}" if min_year and max_year else "N/A"
    
    conn.close()
    return stats

def get_genre_distribution(db_file):
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query("SELECT genre, COUNT(*) as count FROM songs GROUP BY genre ORDER BY count DESC LIMIT 10", conn)
    conn.close()
    return df