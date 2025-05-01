import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

class MovieDatabase:
    def __init__(self):
        # Credentials for read-only connection
        self.read_host = os.getenv("host_read")
        self.read_user = os.getenv("user_read")
        self.read_password = os.getenv("password_read")
        self.movie_db = os.getenv("database")  # Should be 'sakila'

        # Credentials for read-write connection
        self.rw_host = os.getenv("host_write")
        self.rw_user = os.getenv("user_write")
        self.rw_password = os.getenv("password_write")
        self.log_db = "group_111124_fp_Kulykovska"  # Database for logs

        # Validate environment variables
        if not all([self.read_host, self.read_user, self.read_password, self.movie_db,
                    self.rw_host, self.rw_user, self.rw_password]):
            raise ValueError("Missing environment variables. Check host_read, user_read, password_read, database, host_write, user_write, password_write in .env")

        self.setup_log_database()

    def get_read_connection(self):
        try:
            if not self.movie_db:
                raise ValueError("Database name not specified in .env (key 'database')")
            config = {
                "host": self.read_host,
                "user": self.read_user,
                "password": self.read_password,
                "database": self.movie_db,
                "charset": "utf8mb4"
            }
            conn = mysql.connector.connect(**config)
            conn.autocommit = True
            cursor = conn.cursor()  # Avoid dictionary=True to ensure compatibility
            cursor.execute("SET SESSION TRANSACTION READ ONLY")
            return conn
        except Error as e:
            from .utils import center_text
            print(center_text(f"Error connecting to read-only database {self.movie_db}: {e}"))
            return None
        except ValueError as e:
            from .utils import center_text
            print(center_text(f"Configuration error: {e}"))
            return None

    def get_rw_connection(self, database=None):
        try:
            config = {
                "host": self.rw_host,
                "user": self.rw_user,
                "password": self.rw_password,
                "charset": "utf8mb4"
            }
            if database:
                config["database"] = database
            conn = mysql.connector.connect(**config)
            return conn
        except Error as e:
            from .utils import center_text
            print(center_text(f"Error connecting to read-write database: {e}"))
            return None

    def setup_log_database(self):
        try:
            conn = self.get_rw_connection()
            if not conn:
                raise ValueError("Failed to establish read-write connection for log database setup")
            cursor = conn.cursor()

            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.log_db}")
            cursor.execute(f"USE {self.log_db}")

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    query VARCHAR(255) NOT NULL,
                    search_type VARCHAR(50) NOT NULL,
                    count INT DEFAULT 1,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE INDEX idx_query_type (query, search_type)
                )
            ''')

            conn.commit()
            cursor.close()
            conn.close()

        except Error as e:
            from .utils import center_text
            print(center_text(f"Error configuring log database: {e}"))
        except ValueError as e:
            from .utils import center_text
            print(center_text(f"Error: {e}"))

    def get_available_years(self):
        """Fetch distinct release years from the film table."""
        conn = self.get_read_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT release_year FROM film
                ORDER BY release_year
            ''')
            years = [row[0] for row in cursor.fetchall()]
            return years
        except Error as e:
            from .utils import center_text
            print(center_text(f"Error fetching available years: {e}"))
            return None
        finally:
            cursor.close()
            conn.close()

    def get_available_genres(self):
        """Fetch distinct genres from the database."""
        conn = self.get_read_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT t3.name 
                FROM film AS t1
                LEFT JOIN film_category AS t2 ON t1.film_id = t2.film_id
                LEFT JOIN category AS t3 ON t2.category_id = t3.category_id
                WHERE t3.name IS NOT NULL
                ORDER BY t3.name
            ''')
            genres = [row[0] for row in cursor.fetchall()]
            return genres
        except Error as e:
            from .utils import center_text
            print(center_text(f"Error fetching available genres: {e}"))
            return []
        finally:
            cursor.close()
            conn.close()

    def log_search(self, query, search_type):
        conn = self.get_rw_connection(self.log_db)
        if not conn:
            return
        try:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, count FROM search_logs 
                WHERE query = %s AND search_type = %s
            ''', (query, search_type))
            result = cursor.fetchone()

            if result:
                cursor.execute('''
                    UPDATE search_logs 
                    SET count = count + 1, timestamp = CURRENT_TIMESTAMP
                    WHERE id = %s
                ''', (result[0],))  # Use tuple index since result is a tuple
            else:
                cursor.execute('''
                    INSERT INTO search_logs (query, search_type, count) 
                    VALUES (%s, %s, 1)
                ''', (query, search_type))

            conn.commit()
        except Error as e:
            from .utils import center_text
            print(center_text(f"Error writing log: {e}"))
        finally:
            cursor.close()
            conn.close()

    def get_top_searches(self, limit=10):
        conn = self.get_rw_connection(self.log_db)
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT query, search_type, count
                FROM search_logs
                ORDER BY count DESC, timestamp DESC
                LIMIT %s
            ''', (limit,))
            results = [
                {"query": row[0], "search_type": row[1], "count": row[2]}
                for row in cursor.fetchall()
            ]
            return results
        except Error as e:
            from .utils import center_text
            print(center_text(f"Error retrieving popular searches: {e}"))
            return []
        finally:
            cursor.close()
            conn.close()

    def search_movies(self, search_type, value):
        conn = self.get_read_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()

            if search_type == "keyword":
                cursor.execute('''
                    SELECT t1.film_id, t1.title, t3.name AS genre, t1.release_year, t1.description
                    FROM film AS t1
                    LEFT JOIN film_category AS t2 ON t1.film_id = t2.film_id
                    LEFT JOIN category AS t3 ON t2.category_id = t3.category_id
                    WHERE t1.title LIKE %s OR t1.description LIKE %s
                ''', (f'%{value}%', f'%{value}%'))

            elif search_type == "genre":
                genre, year = value  # Expect value to be a tuple (genre, year)
                if not year.isdigit():
                    raise ValueError("Invalid input, year must be a number")
                cursor.execute('''
                    SELECT t1.film_id, t1.title, t3.name AS genre, t1.release_year, t1.description
                    FROM film AS t1
                    LEFT JOIN film_category AS t2 ON t1.film_id = t2.film_id
                    LEFT JOIN category AS t3 ON t2.category_id = t3.category_id
                    WHERE t3.name = %s AND t1.release_year = %s
                ''', (genre, int(year)))

            elif search_type == "year":
                if not value.isdigit():
                    raise ValueError("Invalid input, year must be a number")
                cursor.execute('''
                    SELECT t1.film_id, t1.title, t3.name AS genre, t1.release_year, t1.description
                    FROM film AS t1
                    LEFT JOIN film_category AS t2 ON t1.film_id = t2.film_id
                    LEFT JOIN category AS t3 ON t2.category_id = t3.category_id
                    WHERE t1.release_year = %s
                ''', (int(value),))

            elif search_type == "year_range":
                start_year, end_year = value
                if not (start_year.isdigit() and end_year.isdigit()):
                    raise ValueError("Invalid input, years must be numbers")
                cursor.execute('''
                    SELECT t1.film_id, t1.title, t3.name AS genre, t1.release_year, t1.description
                    FROM film AS t1
                    LEFT JOIN film_category AS t2 ON t1.film_id = t2.film_id
                    LEFT JOIN category AS t3 ON t2.category_id = t3.category_id
                    WHERE t1.release_year BETWEEN %s AND %s
                ''', (int(start_year), int(end_year)))

            # Convert tuples to dictionaries
            results = [
                {
                    "film_id": row[0],
                    "title": row[1],
                    "genre": row[2],
                    "release_year": row[3],
                    "description": row[4]
                }
                for row in cursor.fetchall()
            ]
            self.log_search(str(value), search_type)
            return results

        except Error as e:
            from .utils import center_text
            print(center_text(f"Database error: {e}"))
            return []
        except ValueError as e:
            from .utils import center_text
            print(center_text(f"Input error: {e}"))
            return []
        finally:
            cursor.close()
            conn.close()