import os
import time
from sqlalchemy import Column, Integer, String, create_engine, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "todos.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)
Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    done = Column(Integer, nullable=False, default=0)


def setup():
    Base.metadata.create_all(engine)


def add_item():
    title = input("New to-do title: ").strip()
    if not title:
        print("Please enter something.")
        return
    session = SessionLocal()
    try:
        session.add(Todo(title=title, done=0))
        session.commit()
        print("Added.")
    except IntegrityError:
        session.rollback()
        print("That title already exists (UNIQUE rule via SQLAlchemy).")
    finally:
        session.close()


def list_items():
    session = SessionLocal()
    try:
        rows = (
            session.query(Todo)
            .order_by(Todo.done, Todo.id)
            .all()
        )
        if not rows:
            print("No to-dos yet.")
            return
        for todo in rows:
            mark = "✓" if todo.done else " "
            print(f"{todo.id}. [{mark}] {todo.title}")
    finally:
        session.close()


def toggle_done():
    try:
        i = int(input("Id to toggle done: "))
    except ValueError:
        print("Enter a number.")
        return
    session = SessionLocal()
    try:
        todo = session.query(Todo).filter(Todo.id == i).one_or_none()
        if not todo:
            print("Id not found.")
            return
        todo.done = 0 if todo.done else 1
        session.commit()
        print("Toggled.")
    finally:
        session.close()


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
    session = SessionLocal()
    try:
        todo = session.query(Todo).filter(Todo.id == i).one_or_none()
        if not todo:
            print("Id not found.")
            return
        todo.title = new_title
        session.commit()
        print("Updated.")
    except IntegrityError:
        session.rollback()
        print("That title already exists (UNIQUE rule via SQLAlchemy).")
    finally:
        session.close()


def delete_item():
    try:
        i = int(input("Id to delete: "))
    except ValueError:
        print("Enter a number.")
        return
    session = SessionLocal()
    try:
        todo = session.query(Todo).filter(Todo.id == i).one_or_none()
        if not todo:
            print("Id not found.")
            return
        session.delete(todo)
        session.commit()
        print("Deleted.")
        print("Note: With SQLAlchemy, AUTOINCREMENT still prevents ID reuse.")
    finally:
        session.close()


def search_items():
    keyword = input("Search keyword: ").strip()
    if not keyword:
        print("Please enter a search term.")
        return
    print("\nSQLAlchemy Search Results:")
    print("Note: SQLAlchemy translates high-level queries into efficient SQL.")
    start_time = time.time()
    session = SessionLocal()
    try:
        keyword_lower = keyword.lower()
        rows = (
            session.query(Todo)
            .filter(func.lower(Todo.title).contains(keyword_lower))
            .order_by(Todo.id)
            .all()
        )
    finally:
        session.close()
    search_time = time.time() - start_time
    if not rows:
        print(f"No matches found for '{keyword}'")
    else:
        for todo in rows:
            mark = "✓" if todo.done else " "
            print(f"{todo.id}. [{mark}] {todo.title}")
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
    print(f"\nAdding {count} items with SQLAlchemy session management...")
    print("Note: SQLAlchemy batches changes and commits efficiently.")
    start_time = time.time()
    session = SessionLocal()
    try:
        for i in range(1, count + 1):
            title = f"Bulk item #{i}"
            session.add(Todo(title=title, done=0))
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Error: {e}")
        return
    finally:
        session.close()
    total_time = time.time() - start_time
    print(f"Added {count} items in {total_time:.3f} seconds")
    print(f"Average time per item: {(total_time/count):.6f} seconds")


def main():
    print(f"Using database via SQLAlchemy: {DB_PATH}")
    setup()
    while True:
        print("\n1) List  2) Add  3) Toggle  4) Edit  5) Delete  6) Search  7) Bulk Add  8) Quit")
        choice = input("> ").strip()
        if choice == "1":
            list_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            toggle_done()
        elif choice == "4":
            edit_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            search_items()
        elif choice == "7":
            bulk_insert()
        elif choice == "8":
            break
        else:
            print("Choose 1–8.")


if __name__ == "__main__":
    main()
