# app.py
# Super-simple To-Do (SQLite, terminal). Learning version.
# Goal: feel CRUD in SQL. No Flask.

import sqlite3

DB = "todos.db"

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
        print("Deleted." if cur.rowcount else "Id not found.")

def main():
    setup()
    while True:
        print("\n1) List  2) Add  3) Toggle  4) Edit  5) Delete  6) Quit")
        choice = input("> ").strip()
        if choice == "1": list_items()
        elif choice == "2": add_item()
        elif choice == "3": toggle_done()
        elif choice == "4": edit_item()
        elif choice == "5": delete_item()
        elif choice == "6": break
        else: print("Choose 1–6.")

if __name__ == "__main__":
    main()
