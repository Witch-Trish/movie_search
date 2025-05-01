from movie_search.database import MovieDatabase
from movie_search.utils import center_text
from tabulate import tabulate
import math

def handle_post_search():
    while True:
        print(center_text("\nFind another movie or exit the program?"))
        menu = [
            ["1", "New search"],
            ["2", "Exit"]
        ]
        print(center_text(tabulate(menu, headers=["Option", "Description"], tablefmt="grid")))
        print("Choose your option (1-2): ", end="")
        choice = input().strip()

        if not choice:
            print("Input cannot be empty or just spaces. Choose 1 or 2")
            continue

        if choice not in ["1", "2"]:
            print("Incorrect choice. Choose 1 or 2")
            continue

        if choice == "1":
            return True
        elif choice == "2":
            return False

def handle_menu_choice():
    while True:
        print(center_text("\nSelect an option:"))
        menu = [
            ["1", "Return to main menu"],
            ["2", "Exit the program"]
        ]
        print(center_text(tabulate(menu, headers=["Option", "Description"], tablefmt="grid")))
        print("Select option (1-2): ", end="")
        choice = input().strip()

        if not choice:
            print("Input cannot be empty or just spaces. Choose 1 or 2")
            continue

        if choice not in ["1", "2"]:
            print("Incorrect choice. Choose 1 or 2")
            continue

        if choice == "1":
            return True
        elif choice == "2":
            return False

def main():
    try:
        db = MovieDatabase()
    except Exception as e:
        print(f"Database initialization error: {e}")
        return

    while True:
        print(center_text("\nWelcome to movie_search! Choose an option from the menu below:"))
        menu = [
            ["1", "By keyword"],
            ["2", "By genre and year"],
            ["3", "By year"],
            ["4", "By year range"],
            ["5", "Show popular searches"],
            ["6", "Exit the program"]
        ]
        print(center_text(tabulate(menu, headers=["Option", "Description"], tablefmt="grid")))
        print("Select an option (1-6): ", end="")
        choice = input().strip()

        if not choice:
            print("Input cannot be empty or just spaces. Choose a number from 1 to 6")
            continue

        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Incorrect choice. Choose a number from 1 to 6")
            continue

        try:
            if choice == "1":
                print("Enter keyword: ", end="")
                keyword = input().strip()
                if not keyword:
                    raise ValueError("Keyword cannot be empty or just spaces")
                results = db.search_movies("keyword", keyword)
                if results:
                    print(center_text("\nFound movies:"))
                    table = [
                        [movie['film_id'], movie['title'], movie['genre'], movie['release_year'], movie['description']]
                        for movie in results
                    ]
                    print(center_text(tabulate(table, headers=["ID", "Title", "Genre", "Year", "Description"], tablefmt="grid")))
                else:
                    print(center_text("Movies not found"))

                if not handle_post_search():
                    break
                continue

            elif choice == "2":
                # Fetch available years and genres
                years = db.get_available_years()
                if not years:
                    print("Unable to fetch available years")
                    if not handle_menu_choice():
                        break
                    continue
                min_year, max_year = min(years), max(years)
                print(center_text(f"Films are available from {min_year} to {max_year}"))

                genres = db.get_available_genres()
                if not genres:
                    print("Unable to fetch available genres")
                    if not handle_menu_choice():
                        break
                    continue

                # Split genres into two columns
                num_genres = len(genres)
                mid_point = math.ceil(num_genres / 2)  # Split into roughly equal parts
                left_column = genres[:mid_point]
                right_column = genres[mid_point:] + [None] * (mid_point - len(genres[mid_point:]))  # Pad with None if uneven
                table = [[left_column[i], right_column[i] if right_column[i] else ""] for i in range(mid_point)]
                print(center_text("\nList of genres:"))
                print(center_text(tabulate(table, tablefmt="grid", colalign=("left", "left"))))

                # Genre input with case-insensitive validation
                while True:
                    print("Enter genre: ", end="")
                    genre_input = input().strip()
                    if not genre_input:
                        print("Error: Genre cannot be empty or just spaces")
                        continue
                    # Convert input to lowercase for comparison
                    genre_lower = genre_input.lower()
                    # Find matching genre (case-insensitive)
                    matching_genre = next((g for g in genres if g.lower() == genre_lower), None)
                    if not matching_genre:
                        print(f"Error: '{genre_input}' is not among the available genres. Please choose from the list below:")
                        print(center_text("\nList of genres:"))
                        print(center_text(tabulate(table, tablefmt="grid", colalign=("left", "left"))))
                        continue
                    # Use the original genre case for the database query
                    genre = matching_genre
                    break

                # Year input with validation
                while True:
                    print("Enter year: ", end="")
                    year = input().strip()
                    if not year:
                        print("Error: Year cannot be empty or just spaces")
                        continue
                    if not year.isdigit() or int(year) not in years:
                        print(f"Error: '{year}' is not within the available year range ({min_year} to {max_year}). Please enter a valid year:")
                        print(center_text(f"Films are available from {min_year} to {max_year}"))
                        continue
                    break

                results = db.search_movies("genre", (genre, year))
                if results:
                    print(center_text("\nFound movies:"))
                    table = [
                        [movie['film_id'], movie['title'], movie['genre'], movie['release_year'], movie['description']]
                        for movie in results
                    ]
                    print(center_text(tabulate(table, headers=["ID", "Title", "Genre", "Year", "Description"], tablefmt="grid")))
                else:
                    print(center_text("Movies not found"))

                if not handle_post_search():
                    break
                continue

            elif choice == "3":
                # Fetch available years
                years = db.get_available_years()
                if not years:
                    print("Unable to fetch available years")
                    if not handle_menu_choice():
                        break
                    continue
                min_year, max_year = min(years), max(years)
                print(center_text(f"Films are available from {min_year} to {max_year}"))

                # Year input with validation
                while True:
                    print("Enter year: ", end="")
                    year = input().strip()
                    if not year:
                        print("Error: Year cannot be empty or just spaces")
                        continue
                    if not year.isdigit() or int(year) not in years:
                        print(f"Error: '{year}' is not within the available year range ({min_year} to {max_year}). Please enter a valid year:")
                        print(center_text(f"Films are available from {min_year} to {max_year}"))
                        continue
                    break

                results = db.search_movies("year", year)
                if results:
                    print(center_text("\nFound movies:"))
                    table = [
                        [movie['film_id'], movie['title'], movie['genre'], movie['release_year'], movie['description']]
                        for movie in results
                    ]
                    print(center_text(tabulate(table, headers=["ID", "Title", "Genre", "Year", "Description"], tablefmt="grid")))
                else:
                    print(center_text("Movies not found"))

                if not handle_post_search():
                    break
                continue

            elif choice == "4":
                # Fetch available years
                years = db.get_available_years()
                if not years:
                    print("Unable to fetch available years")
                    if not handle_menu_choice():
                        break
                    continue
                min_year, max_year = min(years), max(years)
                print(center_text(f"Films are available from {min_year} to {max_year}"))

                # Start year input with validation
                while True:
                    print("Enter starting year: ", end="")
                    start_year = input().strip()
                    if not start_year:
                        print("Error: Starting year cannot be empty or just spaces")
                        continue
                    if not start_year.isdigit() or int(start_year) not in years:
                        print(f"Error: '{start_year}' is not within the available year range ({min_year} to {max_year}). Please enter a valid year:")
                        print(center_text(f"Films are available from {min_year} to {max_year}"))
                        continue
                    break

                # End year input with validation
                while True:
                    print("Enter ending year: ", end="")
                    end_year = input().strip()
                    if not end_year:
                        print("Error: Ending year cannot be empty or just spaces")
                        continue
                    if not end_year.isdigit() or int(end_year) not in years:
                        print(f"Error: '{end_year}' is not within the available year range ({min_year} to {max_year}). Please enter a valid year:")
                        print(center_text(f"Films are available from {min_year} to {max_year}"))
                        continue
                    if int(end_year) < int(start_year):
                        print(f"Error: Ending year ({end_year}) cannot be earlier than starting year ({start_year}). Please enter a valid year:")
                        print(center_text(f"Films are available from {min_year} to {max_year}"))
                        continue
                    break

                results = db.search_movies("year_range", (start_year, end_year))
                if results:
                    print(center_text("\nFound movies:"))
                    table = [
                        [movie['film_id'], movie['title'], movie['genre'], movie['release_year'], movie['description']]
                        for movie in results
                    ]
                    print(center_text(tabulate(table, headers=["ID", "Title", "Genre", "Year", "Description"], tablefmt="grid")))
                else:
                    print(center_text("Movies not found"))

                if not handle_post_search():
                    break
                continue

            elif choice == "5":
                top_searches = db.get_top_searches()
                print(center_text("\nTop 10 popular searches:"))
                if top_searches:
                    table = [
                        [search['query'], search['search_type'], search['count']]
                        for search in top_searches
                    ]
                    print(center_text(tabulate(table, headers=["Query", "Search Type", "Times Searched"], tablefmt="grid")))
                else:
                    print(center_text("Search logs are empty"))

                if not handle_menu_choice():
                    break
                continue

            elif choice == "6":
                break

        except ValueError as e:
            print(f"Error: {e}")
            if not handle_menu_choice():
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            if not handle_menu_choice():
                break