# Overview

As a software engineer and data analyst, I am continuously working to deepen my understanding of backend database integration and data engineering principles. I wrote this software to get hands-on experience building a lightweight, functional application that bridges Python logic with raw SQL execution, specifically focusing on data persistence, parameterized queries, and programmatic CRUD operations.

This software is a command-line Movie Rating Database application. It integrates directly with a local SQLite relational database to store and manage movie records. Users interact with a text-based terminal menu to add new movies with a rating from 1 to 10, view a formatted list of all tracked movies, update existing ratings, or delete records entirely. The program also features an automated statistics calculator that queries the database to display the total number of films watched and the user's overall average rating.

[Software Demo Video](https://youtu.be/4KLt2ZM34fE)

# Relational Database

This project utilizes **SQLite**, a C-language library that implements a small, fast, self-contained, high-reliability SQL database engine. 

The database contains a single table named `movies` with the following structure:
* **`id`**: INTEGER (Primary Key, Autoincrement) - Acts as the unique identifier for each movie record.
* **`title`**: TEXT (Not Null) - Stores the name of the movie.
* **`rating`**: REAL (Not Null) - Stores the numerical rating assigned to the movie (from 1 to 10).

# Development Environment

**Tools Used:**
* Visual Studio Code (IDE)
* Command Line / Terminal
* DB Browser for SQLite (Optional, for manual database inspection)

**Programming Language & Libraries:**
* **Python 3**: The core programming language used for the application logic and user interface.
* **`sqlite3`**: Python's built-in library used to establish the database connection, execute SQL commands, and fetch query results.

# Useful Websites

- [Python Official Documentation: sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [SQLite Official Documentation](https://www.sqlite.org/docs.html)
- [W3Schools SQL Tutorial](https://www.w3schools.com/sql/)

# Future Work

- Implement a second `genres` table and perform a `JOIN` to categorize the movies.
- Add an export feature to allow the user to save their database records to a `.csv` file.
- Enhance the input validation to prevent users from accidentally adding duplicate movie titles to the database.