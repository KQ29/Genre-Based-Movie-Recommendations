import random
from imdb import IMDb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize IMDb instance
ia = IMDb()

def fetch_movies_by_genre(genre, num_movies=50):
    """
    Fetches a larger number of movies from IMDb based on the user's input genre.
    Randomly selects 10 from the larger set to introduce variety.
    Only returns movies that actually belong to the specified genre.
    """
    movies = ia.search_movie(genre)
    if len(movies) > num_movies:
        movies = random.sample(movies, num_movies)  # Берем случайные num_movies фильмов
    
    # Создаем список фильмов, которые действительно принадлежат указанному жанру
    genre_filtered_movies = []
    for movie in movies:
        try:
            movie_full = ia.get_movie(movie.movieID)
            movie_genres = movie_full.get('genres', [])
            # Проверяем, относится ли фильм к нужному жанру
            if genre.capitalize() in movie_genres:
                movie['genres'] = movie_genres
                movie['rating'] = movie_full.get('rating', 'No rating available')
                movie['production companies'] = movie_full.get('production companies', [])
                genre_filtered_movies.append(movie)
        except Exception:
            continue  # Пропускаем фильмы с ошибками загрузки данных
    
    # Возвращаем случайные 10 фильмов только из фильмов нужного жанра
    return random.sample(genre_filtered_movies, min(10, len(genre_filtered_movies)))

def get_movie_data(movie):
    """
    Print the movie's title, genre, rating, and production company information.
    """
    genres = ', '.join(movie.get('genres', ['No genres available']))
    rating = movie.get('rating', 'No rating available')
    
    # Получаем список компаний, производивших фильм
    companies = movie.get('production companies', [])
    company_names = ', '.join([company['name'] for company in companies]) if companies else 'No production companies available'

    # Печатаем информацию о фильме с пробелами между блоками
    print(f"Title: {movie['title']}, Year: {movie.get('year', 'N/A')}")
    print(f"Genres: {genres}")
    print(f"Rating: {rating}")
    print(f"Produced by: {company_names}")
    print("-" * 40)
    print("")  # Добавляем пустую строку для пробела между фильмами

def recommend_content_based(movies, target_movie_title):
    """
    Recommends movies based on genre similarity (content-based).
    """
    movie_titles = [movie['title'] for movie in movies]
    movie_genres = [' '.join(movie['genres']) if 'genres' in movie else 'Unknown' for movie in movies]

    movie_genres = [genres for genres in movie_genres if genres.strip() != '']

    if not movie_genres:
        raise ValueError("No genres available for processing.")

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movie_genres)

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    indices = {movie_titles[i]: i for i in range(len(movie_titles))}
    idx = indices.get(target_movie_title)

    if idx is None:
        return []

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    movie_indices = [i[0] for i in sim_scores[1:6]]
    recommended_movies = [movies[i] for i in movie_indices]
    
    return recommended_movies

def fetch_similar_movies(movie):
    """
    Fetches similar movies from IMDb based on the selected movie.
    """
    try:
        movie_full = ia.get_movie(movie.movieID)
        recommendations = movie_full.get('recommendations', [])
        return recommendations
    except Exception:
        return []

def find_movie_by_title(title, movies):
    """
    Searches for the movie by title in the provided movie list.
    If not found, attempts to search it globally via IMDb.
    """
    for movie in movies:
        if movie['title'].lower() == title.lower():
            return movie
    return None

def find_movie_globally(title):
    """
    Search for the movie globally via IMDb if it doesn't exist in the current list.
    Loads full movie data to improve recommendations.
    """
    search_results = ia.search_movie(title)
    if search_results:
        # Get full details of the first movie result
        movie_full = ia.get_movie(search_results[0].movieID)
        return movie_full
    return None

def filter_duplicates(recommendations):
    """
    Removes duplicate movie recommendations based on title.
    """
    seen_titles = set()
    unique_recommendations = []
    for movie in recommendations:
        if movie['title'] not in seen_titles:
            unique_recommendations.append(movie)
            seen_titles.add(movie['title'])
    return unique_recommendations

# Main function to interact with the user
if __name__ == "__main__":
    print("Welcome to the Genre-based Movie Recommendation System!\n")
    
    # Step 1: User enters genre
    genre = input("Please enter a genre (e.g., Action, Drama, Comedy, Horror, Romance, Sci-Fi, Thriller, Fantasy, Documentary, Animation, Crime, Musical, Western): ").strip()

    # Fetch and display top 10 random movies from the selected genre
    movies = fetch_movies_by_genre(genre)
    print(f"\nTop 10 random movies in genre '{genre}':")
    for i, movie in enumerate(movies, 1):
        get_movie_data(movie)

    # Step 2: User selects a movie from the list or globally
    movie_choice = input("\nEnter the movie title you want recommendations based on: ").strip()

    # Step 3: Search for the movie globally if not found in the top 10
    selected_movie = find_movie_by_title(movie_choice, movies)

    if not selected_movie:
        print(f"'{movie_choice}' not found in the current genre. Searching globally...")
        selected_movie = find_movie_globally(movie_choice)

    if selected_movie:
        # Generate content-based recommendations
        recommendations = recommend_content_based(movies, selected_movie['title'])

        # Filter out duplicate movie recommendations
        unique_recommendations = filter_duplicates(recommendations)

        if unique_recommendations:
            print(f"\n\nBecause you liked '{selected_movie['title']}', you might also like:\n")
            for rec in unique_recommendations:
                get_movie_data(rec)

        # Fetch similar movies from IMDb directly
        similar_movies = fetch_similar_movies(selected_movie)

        if similar_movies:
            print(f"\nOther movies similar to '{selected_movie['title']}':\n")
            for rec in similar_movies[:5]:  # Display top 5 similar movies
                get_movie_data(rec)
        else:
            print(f"Sorry, no similar movies found for '{selected_movie['title']}'.")
    else:
        print(f"Sorry, no movie found with the title '{movie_choice}'.")
