# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 09:26:17 2024

@author: Tayyab
"""

import streamlit as st
import pandas as pd
from database import search_songs, get_song_details, get_stats, get_genre_distribution
from recommender import Recommender

# Set page config first
st.set_page_config(page_title="SoundSuggest", page_icon="🎵", layout="wide")

DB_FILE = 'data/songs.db'

@st.cache_resource
def load_recommender():
    return Recommender(DB_FILE)

recommender = load_recommender()

st.title("SoundSuggest: Your Personal Music Recommender")

if 'playlist' not in st.session_state:
    st.session_state.playlist = []

# User input with autocomplete
user_input = st.text_input("Enter a song you like:", key="song_input")

# Perform search as user types
if user_input:
    suggestions = search_songs(DB_FILE, user_input)
    if suggestions:
        selected_song = st.selectbox("Did you mean:", suggestions)
    else:
        st.warning("No matching songs found. Please try a different search.")
        selected_song = None
else:
    selected_song = None

# Sidebar content
st.sidebar.title("Customize Your Experience")

# Mode selection
mode = st.sidebar.selectbox(
    "Choose your recommendation mode:",
    ("Popular songs", "Discover hidden gems")
)
prioritize_popular = mode == "Popular songs"

# Number of recommendations
recommendations_count = st.sidebar.slider('Number of recommendations', min_value=1, max_value=10, value=5)

if selected_song:
    # Extract song name from the selected option
    track_name = selected_song.split(" by ")[0]
    
    with st.spinner("Generating recommendations..."):
        recommendations = recommender.get_recommendations(track_name, n=recommendations_count, prioritize_popular=prioritize_popular)
    
    if recommendations:
        st.subheader("Recommended Songs:")
        for i, rec in enumerate(recommendations, 1):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"{i}. {rec['track_name']} by {rec['artist_name']}")
                st.write(f"   Genre: {rec['genre']}, Year: {rec['year']}, Similarity: {rec['similarity']:.2f}")
                
                # Simulated music player
                st.button(f"▶️ Play", key=f"play_{i}")
            
            with col2:
                rating = st.radio(f"Rate song {i}", options=["👍", "👎"], key=f"rating_{i}")
                if rating:
                    st.success("Thanks for your feedback!")
            
            with col3:
                if st.button(f"Add to Playlist", key=f"add_to_playlist_{i}"):
                    st.session_state.playlist.append((rec['track_name'], rec['artist_name']))
                    st.success("Added to playlist!")
    else:
        st.warning("Sorry, we couldn't find recommendations for that song. Please try another one.")

# Display playlist
if st.session_state.playlist:
    st.subheader("Your Playlist")
    for track, artist in st.session_state.playlist:
        st.write(f"{track} by {artist}")

# Display some statistics about the dataset
st.sidebar.title("Dataset Statistics")
stats = get_stats(DB_FILE)
st.sidebar.write(f"Total Songs: {stats['total_songs']}")
st.sidebar.write(f"Unique Artists: {stats['unique_artists']}")
st.sidebar.write(f"Average Popularity: {stats['avg_popularity']}")
st.sidebar.write(f"Most Common Genre: {stats['most_common_genre']}")
st.sidebar.write(f"Year Range: {stats['year_range']}")

# Visualization
st.sidebar.subheader("Genre Distribution")
genre_dist = get_genre_distribution(DB_FILE)
st.sidebar.bar_chart(genre_dist.set_index('genre')['count'])

# Music Trivia
st.sidebar.subheader("Music Trivia")
random_song = recommender.get_random_song()
if random_song:
    st.sidebar.write(f"Did you know? The song '{random_song['track_name']}' by {random_song['artist_name']} was released in {int(random_song['year'])} and has a popularity score of {random_song['popularity']:.0f}!")
else:
    st.sidebar.write("No trivia available at the moment.")