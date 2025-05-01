from .database import MovieDatabase
from .utils import center_text
from tabulate import tabulate

def handle_post_search():
    while True:
        print(center_text("\nFind another movie or exit the program?"))
        menu = [
            ["1", "New search"],
            ["2", "Exit"]
        ]
        print(center_text(tabulate(menu, headers=["Option", "Description"], tablefmt="grid")))
        choice = input(center_text("Choose your option (1-2): ").strip())

        if choice == "1":
            return True
        elif choice == "2":
            return False
        else:
            print(center_text("Incorrect choice. Choose 1 or 2"))

def handle_menu_choice():
    while True:
        print(center_text("\nSelect an option:"))
        menu = [
            ["1", "Return to main menu"],
            ["2", "Exit the program"]
        ]
        print(center_text(tabulate(menu, headers=["Option", "Description"], tablefmt="grid")))
        choice = input(center_text("Select option (1-2): ").strip())

        if choice == "1":
            return True
        elif choice == "2":
            return False
        else:
            print(center_text("Incorrect choice. Choose 1 or 2"))

def main():
    try:
        db = MovieDatabase()
    except Exception as e:
        print(center_text(f"Database initialization error: {e}"))
        return

    while True:
        print(center_text("\nWelcome to the Movie Search Engine! Choose an option from the menu below:"))
        menu = [
            ["1", "By keyword"],
            ["2", "By genre and year"],
            ["3", "By year"],
            ["4", "By year range"],
            ["5", "Show popular searches"],
            ["6", "Exit the program"]
        ]
        print(center_text(tabulate(menu, headers=["Option", "Description"], tablefmt="grid")))
        choice = input(center_text("Select an option (1-6): ").strip())

        try:
            if choice == "1":
                keyword = input(center_text("Enter keyword: ").strip())
                if not keyword:
                    raise ValueError("Keyword cannot be empty")
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
                # Fetch available years
                years = db.get_available_years()
                if years:
                    print(center_text(f"Films are available from {min(years)} to {max(years)}"))
                else:
                    print(center_text("Unable to fetch available years"))

                # Fetch and display available genres
                genres = db.get_available_genres()
                if genres:
                    print(center_text("\nAvailable genres:"))
                    table = [[genre] for genre in genres]
                    print(center_text(tabulate(table, headers=["Genre"], tablefmt="grid")))
                else:
                    print(center_text("Unable to fetch available genres"))

                genre = input(center_text("Enter genre: ").strip())
                if not genre:
                    raise ValueError("Genre cannot be empty")
                year = input(center_text("Enter year: ").strip())
                if not year:
                    raise ValueError("Year cannot be empty")
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
                year = input(center_text("Enter year: ").strip())
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
                start_year = input(center_text("Enter starting year: ").strip())
                end_year = input(center_text("Enter ending year: ").strip())
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

            else:
                print(center_text("Incorrect choice. Choose a number from 1 to 6"))
                continue

        except ValueError as e:
            print(center_text(f"Error: {e}"))
            if not handle_menu_choice():
                break
        except Exception as e:
            print(center_text(f"An error occurred: {e}"))
            if not handle_menu_choice():
                break