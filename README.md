# SongSuggest

SongSuggest is a music recommendation application built with Streamlit that helps users discover new songs based on their preferences. The app utilizes a recommender system to provide personalized song suggestions, making it easy for users to explore new music.

## Live Demo

You can try the live demo of the application at the following link:
[Live Demo - SongSuggest](https://songsuggest.streamlit.app/)

## Usage
- **Enter a song you like in the input box.**
- **Select from the suggested songs.**
- **Explore the recommended songs based on your selection.**
- **Enjoy music trivia and visualizations!**

## Features

- **Song Recommendations**: Enter a song you like, and receive personalized recommendations based on your input.
- **User-Friendly Interface**: Intuitive design for easy navigation and interaction.
- **Data Visualization**: Insights into song statistics and genre distributions.
- **Music Trivia**: Fun facts about random songs to enhance user engagement.

## Machine Learning

The SongSuggest application employs several machine-learning techniques to deliver accurate and personalized music recommendations:

- **Collaborative Filtering**: This method analyzes user behavior and preferences to recommend songs that similar users have enjoyed. It helps in identifying patterns in user interactions with songs, enhancing the personalization of recommendations.

- **Content-Based Filtering**: The app utilizes features from the Spotify dataset, such as acoustics, danceability, energy, instrumentalness, loudness, speechiness, tempo, and valence. By analyzing these audio features, the model can recommend songs that are sonically similar to those the user has liked in the past.

- **Hybrid Recommendation System**: By combining collaborative filtering and content-based filtering, the application provides a more robust recommendation system that addresses the shortcomings of each method when used independently. This approach enhances user engagement by offering diverse song suggestions.

- **Machine Learning Models**: The recommendation engine employs algorithms such as k-Nearest Neighbors (k-NN) and various clustering methods to group similar songs and predict user preferences based on historical data.

## Database

The application uses SQLite as its database management system, providing a lightweight and efficient way to store and retrieve song data:

- **SQLite Integration**: The app utilizes the `pysqlite3-binary` package to manage the SQLite database, ensuring compatibility and ease of use in the deployment environment. This allows for fast querying of song data and user preferences.

- **Data Storage**: The song dataset includes metadata and audio features, which are essential for the recommendation algorithms. The database schema is designed to efficiently store and retrieve information, enabling quick access to song attributes during the recommendation process.

- **Continuous Learning**: The system is designed to learn from user interactions over time, improving its recommendations as it gains more data on user preferences. This feature ensures that the app remains relevant and engaging for users.

## Installation

To run this application locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/tayyabwaqar/SongSuggest.git
   cd SongSuggest

2. **Create a Virtual Environment (optional but recommended)**:
   ```bash
   python -m venv venv

3. **Activate the Virtual Environment**:
   - **On Windows**:
     ```bash
     venv\Scripts\activate

   - **On macOS/Linux**:
     ```bash
     source venv/bin/activate

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

5. **Run the Application**:
   ```bash
   streamlit run app.py


## Contribution
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Streamlit for the fantastic framework.
Pandas and NumPy for data manipulation.
Scikit-learn for the machine learning algorithms used in the recommender system.
SQLite for lightweight database management.
