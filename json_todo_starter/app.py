# app.py
# Super-simple To-Do (JSON, terminal). Learning version.
# Goal: feel CRUD (Create/Read/Update/Delete). No security, no Flask.

import json
import os.path
import os

# Use absolute path to ensure we're always writing to the correct file
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todos.json")

def load_data():
    if not os.path.exists(PATH):
        return []
    with open(PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(todos):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)

def next_id(todos):
    """Find the first available ID, reusing any gaps in the sequence."""
    if not todos:
        return 1
        
    # Get all existing IDs
    existing_ids = set(item["id"] for item in todos)
    
    # Find the first gap in the sequence
    for i in range(1, max(existing_ids) + 2):
        if i not in existing_ids:
            return i

def add_item(todos):
    title = input("New to-do title: ").strip()
    if not title:
        print("Please enter something.")
        return
        
    # Check for duplicate titles (SQL does this automatically with UNIQUE constraint)
    for todo in todos:
        if todo["title"] == title:
            print("Note: In JSON, we have to manually check for duplicates.")
            print("That title already exists.")
            return
            
    todos.append({"id": next_id(todos), "title": title, "done": False})
    save_data(todos)
    print("Added.")

def list_items(todos):
    if not todos:
        print("No to-dos yet.")
        return
    for item in todos:
        mark = "✓" if item["done"] else " "
        print(f'{item["id"]}. [{mark}] {item["title"]}')

def toggle_done(todos):
    try:
        i = int(input("Id to toggle done: "))
    except ValueError:
        print("Enter a number.")
        return
    for item in todos:
        if item["id"] == i:
            item["done"] = not item["done"]
            save_data(todos)
            print("Toggled.")
            return
    print("Id not found.")

def edit_item(todos):
    try:
        i = int(input("Id to edit: "))
    except ValueError:
        print("Enter a number.")
        return
    for item in todos:
        if item["id"] == i:
            new_title = input("New title: ").strip()
            if new_title:
                item["title"] = new_title
                save_data(todos)
                print("Updated.")
            else:
                print("Title unchanged.")
            return
    print("Id not found.")

def delete_item(todos):
    try:
        i = int(input("Id to delete: "))
    except ValueError:
        print("Enter a number.")
        return
    before = len(todos)
    todos[:] = [t for t in todos if t["id"] != i]
    if len(todos) < before:
        save_data(todos)
        print("Deleted.")
        print("Note: In JSON implementation, the next new item will reuse this ID if it's the lowest available.")
    else:
        print("Id not found.")

def search_items(todos):
    keyword = input("Search keyword: ").strip().lower()
    if not keyword:
        print("Please enter a search term.")
        return
        
    print("\nJSON Search Results:")
    print("Note: In JSON, we have to loop through all items in memory to search")
    
    # Start timing
    import time
    start_time = time.time()
    
    # Search through all todos in memory
    results = []
    for item in todos:
        if keyword in item["title"].lower():
            results.append(item)
    
    # Calculate search time
    search_time = time.time() - start_time
    
    # Display results
    if not results:
        print(f"No matches found for '{keyword}'")
    else:
        for item in results:
            mark = "✓" if item["done"] else " "
            print(f'{item["id"]}. [{mark}] {item["title"]}')
    
    print(f"Search completed in {search_time:.6f} seconds")

def bulk_insert(todos):
    try:
        count = int(input("How many items to add? "))
    except ValueError:
        print("Please enter a number.")
        return
        
    if count <= 0:
        print("Please enter a positive number.")
        return
        
    print(f"\nAdding {count} items to JSON storage...")
    print("Note: In JSON, we need to load the entire file, modify it, and save it back")
    
    # Start timing
    import time
    start_time = time.time()
    
    # Add items
    for i in range(1, count + 1):
        title = f"Bulk item #{i}"
        todos.append({"id": next_id(todos), "title": title, "done": False})
    
    # Save all at once
    save_data(todos)
    
    # Calculate time
    total_time = time.time() - start_time
    
    print(f"Added {count} items in {total_time:.3f} seconds")
    print(f"Average time per item: {(total_time/count):.6f} seconds")

def main():
    print(f"Using todo file: {PATH}")
    todos = load_data()
    while True:
        print("\n1) List  2) Add  3) Toggle  4) Edit  5) Delete  6) Search  7) Bulk Add  8) Quit")
        choice = input("> ").strip()
        if choice == "1": list_items(todos)
        elif choice == "2": add_item(todos)
        elif choice == "3": toggle_done(todos)
        elif choice == "4": edit_item(todos)
        elif choice == "5": delete_item(todos)
        elif choice == "6": search_items(todos)
        elif choice == "7": bulk_insert(todos)
        elif choice == "8": break
        else: print("Choose 1–8.")

if __name__ == "__main__":
    main()
