# Genre-Based Movie Recommendations
 
# Movie Recommendation System

This project is a **movie recommendation system** that allows users to search for movies by genre or title using the IMDb API. It recommends movies based on genre similarity, production companies, and related sequels or prequels. The system also filters out duplicates and provides top recommendations based on content-based filtering.

## Features

- **Search by Genre**: Users can search for movies by genre, and the system will display a list of the top 10 random movies that belong to the specified genre.
- **Global Movie Search**: Users can search for any movie by title, and the system will fetch detailed information, including genres, production companies, and ratings.
- **Content-Based Recommendations**: The system recommends similar movies based on the selected movie's genre or production companies.
- **Filter Duplicates**: Ensures that duplicate recommendations are removed for a cleaner user experience.
- **Sequels and Related Parts**: The system attempts to find sequels or related parts if no direct recommendations are found.

## How It Works

1. **Genre-Based Search**: The user can search for movies by specifying a genre (e.g., Action, Drama, Comedy). The system will fetch movies that belong to that genre, ensuring that only relevant results are displayed.
2. **Global Movie Search**: Users can search for a movie by entering its title. If the movie is found, the system provides detailed information and related recommendations based on genres and production companies.
3. **Recommendations**: Once a movie is selected, the system uses content-based filtering (TF-IDF and cosine similarity) to recommend movies with similar genres or from the same production companies.
4. **Sequels and Prequels**: If no direct recommendations are available, the system checks for sequels or prequels to provide related movie suggestions.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/KQ29/movie-recommendation-system.git
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the project:

    ```bash
    python main.py
    ```

## Usage

1. **Search by Genre**:
    - Enter a genre when prompted, and the system will provide a list of 10 random movies from that genre.
    - Example genres: "Action", "Drama", "Sci-Fi", "Comedy".

2. **Search by Movie Title**:
    - Enter a movie title to get detailed information about that movie, including genres, production companies, and ratings.

3. **Get Recommendations**:
    - After selecting a movie, the system will provide recommendations based on genre similarity, production companies, or related sequels.

        Example interaction:
        Please enter a genre (e.g., Action, Drama, Comedy): Action Top 10 random movies in genre 'Action': Title: Inception, Year: 2010 Genres: Action, Adventure, Sci-Fi Rating: 8.8 Produced by: Warner Bros.

        Enter the movie title you want recommendations based on: Inception

        Because you liked 'Inception', you might also like: Title: The Matrix, Year: 1999 Genres: Action, Sci-Fi Rating: 8.7 Produced by: Warner Bros.

## Requirements

- **Python 3.x**
- **IMDbPY**: For accessing movie data via the IMDb API.
- **scikit-learn**: For handling content similarity with TF-IDF and cosine similarity.

### Python Libraries

- `IMDbPY`: Used to fetch movie data from IMDb.
- `scikit-learn`: To calculate content similarity and make content-based recommendations.

## Roadmap

- [ ] Add user feedback to adjust recommendations based on ratings.
- [ ] Support collaborative filtering for better personalization.
- [ ] Integrate user authentication and profile management for persistent preferences.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any inquiries or assistance, please contact me at [kamronbekibra2005@gmail.com].
