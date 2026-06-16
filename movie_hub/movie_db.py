"""
Movie Rating Database
=====================
A command-line application to track movies you've watched and their ratings.
Uses Python's built-in sqlite3 library, with no external packages required.

Usage:
    python movie_db.py
"""

import sqlite3


# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

def get_connection():
    """
    Open (or create) the SQLite database file and return the connection.
    SQLite automatically creates 'movies.db' if it doesn't exist yet.
    """
    conn = sqlite3.connect("movies.db")

    # Row factory lets us access columns by name (e.g. row["title"])
    # instead of only by index (row[0]).
    conn.row_factory = sqlite3.Row
    return conn


def create_table(conn):
    """
    Create the 'movies' table if it hasn't been created yet.
    'IF NOT EXISTS' makes this safe to call every time the program starts.
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            title  TEXT    NOT NULL,
            rating REAL    NOT NULL
        )
    """)
    conn.commit()


# ---------------------------------------------------------------------------
# CRUD operations
# ---------------------------------------------------------------------------

def add_movie(conn):
    """
    Prompt the user for a title and rating, then INSERT a new row.

    Parameterized query: the '?' placeholders are filled in by sqlite3
    using the values tuple.  This prevents SQL injection and handles
    special characters like apostrophes automatically (e.g. "Schindler's List").
    """
    title = input("  Movie title: ").strip()
    if not title:
        print("  [!] Title cannot be empty.")
        return

    while True:
        try:
            rating = float(input("  Rating (1-10): "))
            if 1 <= rating <= 10:
                break
            print("  [!] Please enter a number between 1 and 10.")
        except ValueError:
            print("  [!] Invalid input — please enter a number.")

    # The tuple (title, rating) maps 1-to-1 to the two '?' placeholders.
    conn.execute("INSERT INTO movies (title, rating) VALUES (?, ?)", (title, rating))
    conn.commit()
    print(f'  ✓ "{title}" added with a rating of {rating}.')


def view_movies(conn):
    """
    SELECT all rows and display them in a tidy table.
    """
    rows = conn.execute("SELECT id, title, rating FROM movies ORDER BY id").fetchall()

    if not rows:
        print("  No movies in the database yet.")
        return

    print(f"\n  {'ID':<5} {'Title':<40} {'Rating':>6}")
    print("  " + "-" * 55)
    for row in rows:
        print(f"  {row['id']:<5} {row['title']:<40} {row['rating']:>6.1f}")


def update_rating(conn):
    """
    Ask for a movie ID and a new rating, then UPDATE that specific row.
    Using '?' placeholders protects against injection even for numeric values.
    """
    try:
        movie_id = int(input("  Enter the ID of the movie to update: "))
    except ValueError:
        print("  [!] ID must be a whole number.")
        return

    # Verify the movie exists before asking for a new rating.
    row = conn.execute("SELECT title FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if not row:
        print(f"  [!] No movie found with ID {movie_id}.")
        return

    while True:
        try:
            new_rating = float(input(f'  New rating for "{row["title"]}" (1-10): '))
            if 1 <= new_rating <= 10:
                break
            print("  [!] Please enter a number between 1 and 10.")
        except ValueError:
            print("  [!] Invalid input — please enter a number.")

    conn.execute(
        "UPDATE movies SET rating = ? WHERE id = ?",
        (new_rating, movie_id)          # values tuple mirrors the two '?' above
    )
    conn.commit()
    print(f'  ✓ Rating updated to {new_rating}.')


def delete_movie(conn):
    """
    Ask for a movie ID and DELETE that row from the table.
    """
    try:
        movie_id = int(input("  Enter the ID of the movie to delete: "))
    except ValueError:
        print("  [!] ID must be a whole number.")
        return

    row = conn.execute("SELECT title FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if not row:
        print(f"  [!] No movie found with ID {movie_id}.")
        return

    confirm = input(f'  Delete "{row["title"]}"? (y/n): ').strip().lower()
    if confirm != "y":
        print("  Cancelled.")
        return

    conn.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    conn.commit()
    print(f'  ✓ "{row["title"]}" deleted.')


def view_statistics(conn):
    """
    Display overall stats using SQL aggregate functions in a single query.

    COUNT(title)  — counts every row where 'title' is not NULL.
                    Using the column name (not '*') is a deliberate signal
                    that we only want non-NULL values counted.

    AVG(rating)   — computes the arithmetic mean of the 'rating' column.
                    SQLite returns NULL (Python None) when the table is empty,
                    so we use 'or 0' below to fall back to 0 safely.

    Both aggregates run in one round-trip to the database, which is more
    efficient than two separate queries.
    """
    row = conn.execute("SELECT COUNT(title) AS total, AVG(rating) AS average FROM movies").fetchone()

    total   = row["total"]          # always an integer (0 when empty)
    average = row["average"] or 0   # None → 0 when the table is empty

    print(f"\n  Movies watched : {total}")
    print(f"  Average rating : {average:.2f} / 10.00")


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

MENU = """
╔══════════════════════════════════╗
║      Movie Rating Database       ║
╠══════════════════════════════════╣
║  1. Add a movie                  ║
║  2. View all movies              ║
║  3. Update a rating              ║
║  4. Delete a movie               ║
║  5. View statistics              ║
║  6. Exit                         ║
╚══════════════════════════════════╝"""


def main():
    conn = get_connection()
    create_table(conn)

    while True:
        print(MENU)
        choice = input("  Choose an option (1-6): ").strip()

        print()  # blank line for readability

        if choice == "1":
            add_movie(conn)
        elif choice == "2":
            view_movies(conn)
        elif choice == "3":
            update_rating(conn)
        elif choice == "4":
            delete_movie(conn)
        elif choice == "5":
            view_statistics(conn)
        elif choice == "6":
            conn.close()
            print("  Goodbye! Database connection closed.")
            break
        else:
            print("  [!] Invalid choice — please enter a number from 1 to 6.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()