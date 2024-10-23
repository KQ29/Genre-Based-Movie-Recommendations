from imdb import IMDb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize IMDb instance
ia = IMDb()

def find_movie_globally(title):
    """
    Search for the movie globally via IMDb.
    Loads full movie data to improve recommendations.
    """
    search_results = ia.search_movie(title)
    if search_results:
        # Get full details of the first movie result
        movie_full = ia.get_movie(search_results[0].movieID)
        return movie_full
    return None

def get_movie_data(movie):
    """
    Print the movie's title, genre, rating, and production company information.
    If genres, ratings, or production companies are not available, display a default message.
    """
    genres = ', '.join(movie.get('genres', ['No genres available']))
    rating = movie.get('rating', 'No rating available')

    # Extract production companies
    companies = movie.get('production companies', [])
    company_names = ', '.join([company['name'] for company in companies]) if companies else 'No production companies available'

    # Печатаем информацию о фильме с пробелами между блоками
    print(f"Title: {movie['title']}, Year: {movie.get('year', 'N/A')}")
    print(f"Genres: {genres}")
    print(f"Rating: {rating}")
    print(f"Produced by: {company_names}")
    print("-" * 40)
    print("")  # Добавляем пустую строку для пробела между фильмами

def fetch_similar_movies(movie):
    """
    Fetches similar movies from IMDb based on the selected movie.
    If similar movies are not found, checks for sequels or related parts manually.
    Includes movies with either genres or ratings if available.
    """
    try:
        recommendations = movie.get('recommendations', [])
        
        if not recommendations:
            print(f"\nSorry, no similar movies found for '{movie['title']}'.")
            print("Checking for sequels or related parts...")
            
            # Search for the same title or variations of it
            sequels = ia.search_movie(movie['title'])
            related_movies = [m for m in sequels if m.movieID != movie.movieID]

            # Filter based on movie title similarity (to catch sequels)
            related_filtered = [m for m in related_movies if movie['title'].lower() in m['title'].lower()]

            if related_filtered:
                print("Found related movies (possibly sequels or prequels):")
                return related_filtered[:5]  # Return the first 5 found sequels/prequels
            
            print("No sequels or related parts found. Searching by genre...")
            return recommend_based_on_genres(movie)
        
        # Filter movies to include those with either genres or ratings
        filtered_recommendations = [m for m in recommendations if 'genres' in m or 'rating' in m]
        return filtered_recommendations[:5] if filtered_recommendations else None
    except Exception as e:
        print(f"An error occurred while fetching similar movies: {e}")
        return []

def recommend_based_on_genres(movie):
    """
    Recommend movies based on the same genre if no similar movies are found.
    Includes movies that have genres, even if ratings are not available.
    """
    genre = movie['genres'][0]  # Используем первый жанр
    search_results = ia.search_movie(genre)
    
    # Filter movies that have valid genres (even if ratings are missing)
    filtered_results = [
        m for m in search_results if m.get('genres')
    ]
    
    # Sort by rating if available and return top 5
    top_rated_movies = sorted(filtered_results, key=lambda m: m.get('rating', 0), reverse=True)
    return top_rated_movies[:5]

def recommend_based_on_company(movie):
    """
    Recommend movies based on the same production company.
    """
    companies = movie.get('production companies', [])
    if not companies:
        return []
    
    # Search for movies produced by the same companies
    recommendations = []
    for company in companies:
        search_results = ia.search_movie(company['name'])
        filtered_results = [
            m for m in search_results if 'genres' in m and 'rating' in m
        ]
        recommendations.extend(filtered_results[:5])  # Include top 5 movies from each company
    
    return recommendations[:5]

if __name__ == "__main__":
    print("Welcome to the Global Movie Search System!\n")
    
    # Step 1: User enters movie title
    movie_choice = input("Enter the name of your favorite movie: ").strip()

    # Step 2: Search for the movie globally
    selected_movie = find_movie_globally(movie_choice)

    if selected_movie:
        # Display movie data
        print("\nMovie found!")
        get_movie_data(selected_movie)

        # Fetch and display similar movies
        recommendations = fetch_similar_movies(selected_movie)

        if recommendations:
            print(f"\nMovies similar to '{selected_movie['title']}':\n")
            for rec in recommendations[:5]:  # Display top 5 similar movies
                get_movie_data(rec)
        
        # Recommend based on the same genre if no recommendations found
        else:
            genre_based = recommend_based_on_genres(selected_movie)
            if genre_based:
                print(f"\nMovies based on the same genre as '{selected_movie['title']}':")
                for rec in genre_based:
                    get_movie_data(rec)
            else:
                print(f"Sorry, no similar movies found for '{selected_movie['title']}'.")

        # Recommend based on production companies
        company_based = recommend_based_on_company(selected_movie)
        if company_based:
            print(f"\nMovies from the same production companies as '{selected_movie['title']}':")
            for rec in company_based:
                get_movie_data(rec)
        else:
            print(f"Sorry, no movies found based on production companies of '{selected_movie['title']}'.")
    else:
        print(f"Sorry, no movie found with the title '{movie_choice}'.")
