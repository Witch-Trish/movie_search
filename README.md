# Movie_search User Manual

Welcome to **movie_search**, a user-friendly console-based Python application that lets you explore movies in the `sakila` MySQL database. This manual guides you through what the application does, how to use its features, and how to set it up and run it after downloading the repository from GitHub. Get ready to discover your favorite films with ease!

## Overview

movie_search is a command-line tool that connects to the `sakila` MySQL database, offering multiple ways to search for movies. Its intuitive interface features centered menus, left-aligned input prompts that keep your typing on the same line, and smart input handling that ignores extra spaces and ensures smooth operation.

### What the Application Can Do
- **Search Movies**:
  - **By Keyword**: Find movies by entering a word or phrase that matches the title or description.
  - **By Genre and Year**: Search for movies in a specific genre (e.g., Action, Drama) and release year, with a list of available genres and years provided.
  - **By Year**: Retrieve all movies released in a given year.
  - **By Year Range**: Discover movies released between two specified years.
- **View Popular Searches**: Display the top 10 most frequent search queries, including the query, search type, and number of times searched.
- **User-Friendly Features**:
  - Centered menu tables for a clean, professional display.
  - Input prompts that stay on the same line, preventing wrapping when typing or pressing the spacebar.
  - Ignores leading/trailing spaces (e.g., "   2   " is treated as "2").
  - Validates inputs to reject empty or invalid entries, with clear error messages.
- **Search Logging**: Tracks all searches in a custom MySQL database (`group_111124_fp_Kulykovska`) to power the popular searches feature.

## System Requirements
To run movie_search, ensure you have:
- **Python**: Version 3.6 or higher.
- **MySQL**: A running MySQL server with the `sakila` database installed.
- **Git**: For cloning the repository from GitHub.
- **Dependencies** (installed automatically):
  - `mysql-connector-python>=8.0.0`
  - `tabulate>=0.9.0`
  - `python-dotenv>=1.0.0`
- **Operating System**: Windows, macOS, or Linux.
- **Terminal**: A standard terminal (e.g., Command Prompt, PowerShell, macOS Terminal, or Linux Bash) is recommended.

## Setting Up and Running the Application

Follow these steps to download movie_search from GitHub and get it running on your system.

### 1. Clone the Repository
1. Open a terminal and navigate to the directory where you want to store the project.
2. Clone the repository from GitHub (replace `<repository-url>` with the actual GitHub repository URL):
   ```bash
   git clone <repository-url>
   ```
   Example:
   ```bash
   git clone https://github.com/Witch-Trish/movie_search.git
   ```
3. Navigate to the project directory:
   ```bash
   cd movie_search
   ```

### 2. Verify Directory Structure
Ensure the repository contains the following files and directories:
```
movie_search/
│
├── movie_search/
│   ├── __init__.py
│   ├── database.py
│   ├── utils.py
│   └── ui.py
│
├── main.py
├── requirements.txt
└── README.md
```
- **Note**: The `.env` file is not included in the repository for security reasons and must be created manually (see step 4).

### 3. Install Dependencies
1. Ensure Python and `pip` are installed:
   ```bash
   python --version
   pip --version
   ```
2. Install the required Python packages listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   This installs `mysql-connector-python`, `tabulate`, and `python-dotenv`.

### 4. Create the `.env` File
The application uses environment variables to store MySQL connection details.
1. In the `movie_search` directory, create a file named `.env`.
2. Add the following content, using your MySQL credentials:
   ```plaintext
   # Read-only connection
   host_read=localhost
   user_read=readonly_user
   password_read=readonly_password
   database=sakila

   # Read-write connection
   host_write=localhost
   user_write=readwrite_user
   password_write=readwrite_password
   ```
3. Save and close the file.

### 5. Run the Application
1. From the `movie_search` directory, start the application:
   ```bash
   python main.py
   ```
2. The main menu should appear, indicating the app is running successfully.

## Using movie_search

movie_search is designed for simplicity and ease of use. Below is a detailed guide on how to navigate and use each feature.

### Main Menu
Upon launching the app, you’ll see a centered main menu (example for an 80-character console width):

```
           Welcome to movie_search! Choose an option from the menu below:
           +----------+-----------------------+
           | Option   | Description           |
           +==========+=======================+
           | 1        | By keyword            |
           +----------+-----------------------+
           | 2        | By genre and year     |
           +----------+-----------------------+
           | 3        | By year               |
           +----------+-----------------------+
           | 4        | By year range         |
           +----------+-----------------------+
           | 5        | Show popular searches |
           +----------+-----------------------+
           | 6        | Exit the program      |
           +----------+-----------------------+
Select an option (1-6): 
```

- **How to Navigate**:
  - Type a number (1 to 6) and press Enter.
  - Leading or trailing spaces are ignored (e.g., "   2   " is treated as "2").
  - The input cursor stays on the same line as the prompt, and pressing the spacebar does not cause wrapping.
- **Error Handling**:
  - Invalid inputs (e.g., letters, numbers outside 1-6, or spaces only) trigger clear error messages:
    ```
    Incorrect choice. Choose a number from 1 to 6
    ```
    or
    ```
    Input cannot be empty or just spaces. Choose a number from 1 to 6
    ```

### Features and How to Use Them

#### 1. Search by Keyword
- **Purpose**: Find movies where the title or description contains a specific keyword or phrase.
- **Steps**:
  1. Select option `1` from the main menu.
  2. At the prompt `Enter keyword: `, type a word or phrase (e.g., "Adventure").
  3. Press Enter. Your input stays on the same line.
  4. If movies are found, they are displayed in a centered table with columns for ID, Title, Genre, Year, and Description.
  5. If no matches are found, you’ll see:
     ```
            Movies not found
     ```
- **Example**:
  ```
  Select an option (1-6): 1
  Enter keyword: Adventure
            Found movies:
            +------+-------------+---------+--------+-----------------------------------------+
            | ID   | Title       | Genre   | Year   | Description                             |
            +======+=============+=========+========+=========================================+
            | 123  | Some Movie  | Action  | 2006   | An action-packed adventure...           |
            +------+-------------+---------+--------+-----------------------------------------+
  ```

#### 2. Search by Genre and Year
- **Purpose**: Locate movies that match a specific genre and release year, with guidance on available options.
- **Steps**:
  1. Select option `2`.
  2. The app displays the range of available years (e.g., 2003 to 2006) and a centered table of genres (e.g., Action, Comedy).
  3. At `Enter genre: `, type a genre exactly as shown in the list (e.g., "Action"). Case matters.
  4. At `Enter year: `, type a year (e.g., "2006").
  5. Results are shown in a centered table, or you’ll see "Movies not found" if none match.
  6. Invalid inputs (e.g., empty or spaces) trigger errors like:
     ```
     Error: Genre cannot be empty or just spaces
     ```
- **Example**:
  ```
  Select an option (1-6): 2
            Films are available from 2003 to 2006
            Available genres:
            +------------+
            | Genre      |
            +============+
            | Action     |
            +------------+
            | Comedy     |
            +------------+
  Enter genre: Action
  Enter year: 2006
            Found movies:
            +------+-------------+---------+--------+-----------------------------------------+
            | ID   | Title       | Genre   | Year   | Description                             |
            +======+=============+=========+========+=========================================+
            | 123  | Some Movie  | Action  | 2006   | An action-packed adventure...           |
            +------+-------------+---------+--------+-----------------------------------------+
  ```

#### 3. Search by Year
- **Purpose**: List all movies released in a specific year.
- **Steps**:
  1. Select option `3`.
  2. At `Enter year: `, type a year (e.g., "2006").
  3. Results are displayed in a centered table, or "Movies not found" if none match.
- **Example**:
  ```
  Select an option (1-6): 3
  Enter year: 2006
            Found movies:
            +------+-------------+---------+--------+-----------------------------------------+
            | ID   | Title       | Genre   | Year   | Description                             |
            +======+=============+=========+========+=========================================+
            | 123  | Some Movie  | Action  | 2006   | An action-packed adventure...           |
            +------+-------------+---------+--------+-----------------------------------------+
  ```

#### 4. Search by Year Range
- **Purpose**: Find movies released between two years.
- **Steps**:
  1. Select option `4`.
  2. At `Enter starting year: `, type the start year (e.g., "2005").
  3. At `Enter ending year: `, type the end year (e.g., "2006").
  4. Results are shown in a centered table.
- **Example**:
  ```
  Select an option (1-6): 4
  Enter starting year: 2005
  Enter ending year: 2006
            Found movies:
            +------+-------------+---------+--------+-----------------------------------------+
            | ID   | Title       | Genre   | Year   | Description                             |
            +======+=============+=========+========+=========================================+
            | 123  | Some Movie  | Action  | 2006   | An action-packed adventure...           |
            +------+-------------+---------+--------+-----------------------------------------+
  ```

#### 5. View Popular Searches
- **Purpose**: Display the top 10 most frequent search queries, including the query, search type, and count.
- **Steps**:
  1. Select option `5`.
  2. A centered table shows the top searches. If no searches have been logged, you’ll see:
     ```
            Search logs are empty
     ```
- **Example**:
  ```
  Select an option (1-6): 5
            Top 10 popular searches:
            +-----------------+--------------+-----------------+
            | Query           | Search Type  | Times Searched  |
            +=================+==============+=================+
            | Adventure       | keyword      | 5               |
            +-----------------+--------------+-----------------+
            | ('Action', '2006') | genre     | 3               |
            +-----------------+--------------+-----------------+
  ```

#### 6. Exit the Program
- **Purpose**: Close the application.
- **Steps**:
  1. Select option `6` to exit.

### Post-Search Options
After completing a search (options 1-4), you’ll see a follow-up menu:
```
           Find another movie or exit the program?
           +----------+---------------+
           | Option   | Description   |
           +==========+===============+
           | 1        | New search    |
           +----------+---------------+
           | 2        | Exit          |
           +==========+===============+
Choose your option (1-2): 
```
- Enter `1` to return to the main menu.
- Enter `2` to exit.

If an error occurs (e.g., invalid input), a similar menu appears:
```
           Select an option:
           +----------+-------------------+
           | Option   | Description       |
           +==========+===================+
           | 1        | Return to main menu |
           +----------+-------------------+
           | 2        | Exit the program  |
           +==========+===================+
Select option (1-2): 
```

## Tips for Effective Use
- **Use a Standard Terminal**: Run the app in a standard terminal (e.g., Command Prompt, PowerShell, macOS Terminal) for the best experience.
- **Match Genre Spelling**: When searching by genre, use the exact spelling and case from the displayed list (e.g., "Action", not "action").
- **Spaces Are Ignored**: Extra spaces before or after inputs are automatically removed (e.g., "   Action   " becomes "Action").
- **Handle Errors**: If you see an error, read the message and try again. The app provides clear guidance, such as:
  ```
  Incorrect choice. Choose a number from 1 to 6
  ```

## License
This project is for educational purposes and uses the `sakila` database, which is provided by MySQL under its own license. Ensure compliance with the `sakila` database license when using this application.

## Start Exploring Movies!
With movie_search, finding movies is simple and fun. Follow this manual to set up and dive into searching, and enjoy discovering films that match your interests!