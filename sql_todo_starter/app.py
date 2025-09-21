# app.py
# Super-simple To-Do (SQLite, terminal). Learning version.
# Goal: feel CRUD in SQL. No Flask.

import sqlite3
import os.path

# Use absolute path to ensure we're always using the correct database file
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todos.db")

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def setup():
    with connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS todos(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL UNIQUE,
              done INTEGER NOT NULL DEFAULT 0
            )
        """)

def add_item():
    title = input("New to-do title: ").strip()
    if not title:
        print("Please enter something.")
        return
    try:
        with connect() as con:
            con.execute("INSERT INTO todos(title) VALUES (?)", (title,))
        print("Added.")
    except sqlite3.IntegrityError:
        print("That title already exists (UNIQUE rule).")

def list_items():
    with connect() as con:
        rows = con.execute("SELECT id, title, done FROM todos ORDER BY done, id").fetchall()
        if not rows:
            print("No to-dos yet.")
            return
        for r in rows:
            mark = "✓" if r["done"] else " "
            print(f'{r["id"]}. [{mark}] {r["title"]}')

def toggle_done():
    try:
        i = int(input("Id to toggle done: "))
    except ValueError:
        print("Enter a number.")
        return
    with connect() as con:
        con.execute("UPDATE todos SET done = CASE done WHEN 0 THEN 1 ELSE 0 END WHERE id = ?", (i,))
        if con.total_changes:
            print("Toggled.")
        else:
            print("Id not found.")

def edit_item():
    try:
        i = int(input("Id to edit: "))
    except ValueError:
        print("Enter a number.")
        return
    new_title = input("New title: ").strip()
    if not new_title:
        print("Title unchanged.")
        return
    try:
        with connect() as con:
            con.execute("UPDATE todos SET title = ? WHERE id = ?", (new_title, i))
        print("Updated.")
    except sqlite3.IntegrityError:
        print("That title already exists (UNIQUE rule).")

def delete_item():
    try:
        i = int(input("Id to delete: "))
    except ValueError:
        print("Enter a number.")
        return
    with connect() as con:
        cur = con.execute("DELETE FROM todos WHERE id = ?", (i,))
        if cur.rowcount:
            print("Deleted.")
            print("Note: In SQL implementation, this ID will never be reused due to AUTOINCREMENT.")
        else:
            print("Id not found.")

def search_items():
    keyword = input("Search keyword: ").strip()
    if not keyword:
        print("Please enter a search term.")
        return
        
    print("\nSQL Search Results:")
    print("Note: In SQL, the database engine handles the search efficiently")
    
    # Start timing
    import time
    start_time = time.time()
    
    # Use SQL's LIKE operator to search
    with connect() as con:
        rows = con.execute(
            "SELECT id, title, done FROM todos WHERE title LIKE ? ORDER BY id", 
            (f"%{keyword}%",)
        ).fetchall()
    
    # Calculate search time
    search_time = time.time() - start_time
    
    # Display results
    if not rows:
        print(f"No matches found for '{keyword}'")
    else:
        for r in rows:
            mark = "✓" if r["done"] else " "
            print(f'{r["id"]}. [{mark}] {r["title"]}')
    
    print(f"Search completed in {search_time:.6f} seconds")

def bulk_insert():
    try:
        count = int(input("How many items to add? "))
    except ValueError:
        print("Please enter a number.")
        return
        
    if count <= 0:
        print("Please enter a positive number.")
        return
        
    print(f"\nAdding {count} items to SQL database...")
    print("Note: In SQL, we can use transactions for efficient bulk operations")
    
    # Start timing
    import time
    start_time = time.time()
    
    # Use a transaction for better performance
    with connect() as con:
        # Begin transaction
        con.execute("BEGIN TRANSACTION")
        try:
            for i in range(1, count + 1):
                title = f"Bulk item #{i}"
                con.execute("INSERT INTO todos(title) VALUES (?)", (title,))
            # Commit all changes at once
            con.execute("COMMIT")
        except Exception as e:
            # Roll back on error
            con.execute("ROLLBACK")
            print(f"Error: {e}")
            return
    
    # Calculate time
    total_time = time.time() - start_time
    
    print(f"Added {count} items in {total_time:.3f} seconds")
    print(f"Average time per item: {(total_time/count):.6f} seconds")

def main():
    print(f"Using database: {DB}")
    setup()
    while True:
        print("\n1) List  2) Add  3) Toggle  4) Edit  5) Delete  6) Search  7) Bulk Add  8) Quit")
        choice = input("> ").strip()
        if choice == "1": list_items()
        elif choice == "2": add_item()
        elif choice == "3": toggle_done()
        elif choice == "4": edit_item()
        elif choice == "5": delete_item()
        elif choice == "6": search_items()
        elif choice == "7": bulk_insert()
        elif choice == "8": break
        else: print("Choose 1–8.")

if __name__ == "__main__":
    main()
