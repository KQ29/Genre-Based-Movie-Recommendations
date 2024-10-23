import os

def main_menu():
    print("Welcome to the Movie Recommendation System!")
    print()
    print("1. Search movies by entering its name (Global Search)")
    print()
    print("2. Get movie recommendations based on genre")
    print()

    choice = input("Please enter your choice (1 or 2): ")

    if choice == '1':
        print()
        # Run global movie search script
        os.system('python global_movie_search.py')
    elif choice == '2':
        print()
        # Run genre-based recommendation system
        os.system('python Movie-Recommendation-AI.py')
    else:
        print()
        print("Invalid choice. Please enter 1 or 2.")
        print()

if __name__ == "__main__":
    main_menu()
1