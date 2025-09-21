# app.py
# Super-simple To-Do (JSON, terminal). Learning version.
# Goal: feel CRUD (Create/Read/Update/Delete). No security, no Flask.

import json, os

PATH = "todos.json"

def load_data():
    if not os.path.exists(PATH):
        return []
    with open(PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(todos):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)

def next_id(todos):
    return 1 if not todos else max(item["id"] for item in todos) + 1

def add_item(todos):
    title = input("New to-do title: ").strip()
    if not title:
        print("Please enter something.")
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
    else:
        print("Id not found.")

def main():
    todos = load_data()
    while True:
        print("\n1) List  2) Add  3) Toggle  4) Edit  5) Delete  6) Quit")
        choice = input("> ").strip()
        if choice == "1": list_items(todos)
        elif choice == "2": add_item(todos)
        elif choice == "3": toggle_done(todos)
        elif choice == "4": edit_item(todos)
        elif choice == "5": delete_item(todos)
        elif choice == "6": break
        else: print("Choose 1–6.")

if __name__ == "__main__":
    main()
