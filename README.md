# JSON vs SQL: Hands-on Comparison

This repository provides a practical comparison between JSON file-based storage, raw SQL database storage, and SQLAlchemy ORM abstractions through three implementations of the same To-Do list application. It serves as an educational resource to understand the fundamental differences, advantages, and trade-offs between these common data storage approaches.

## 📋 Project Overview

The repository contains three parallel implementations of a simple To-Do list application:

1. **JSON Implementation**: Uses a JSON file for data storage
2. **SQL Implementation**: Uses SQLite database for data storage
3. **SQLAlchemy Implementation**: Uses SQLite through SQLAlchemy ORM for data access

All implementations provide identical functionality but differ in their underlying data access and storage mechanisms, allowing for direct comparison of performance, data integrity, and implementation complexity.

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- SQLAlchemy 1.4+ (install with `pip install sqlalchemy`)
- Built-in `json` and `sqlite3` modules (included with Python)

### Running the Applications

1. Clone this repository:
   ```bash
   git clone https://github.com/Mr-Zamora/JSON-to-SQL.git
   cd JSON-to-SQL
   ```

2. Run the JSON implementation:
   ```bash
   cd json_todo_starter
   python app.py
   ```

3. Run the SQL implementation:
   ```bash
   cd sql_todo_starter
   python app.py
   ```

4. Run the SQLAlchemy implementation:
   ```bash
   cd ORM_sql_alchemy
   python app.py
   ```

## 🔍 Repository Structure

```
JSON-to-SQL/
├── COMPARE.md            # Detailed comparison guide with exercises
├── README.md             # This file
├── json_todo_starter/    # JSON implementation
│   ├── app.py           # Main application code
│   └── todos.json       # JSON data storage file
├── sql_todo_starter/     # SQL implementation
│   └── app.py           # Main application code (creates todos.db)
└── ORM_sql_alchemy/      # SQLAlchemy ORM implementation
    └── app.py           # Main application code (creates todos.db)
```

## 💡 Features

All implementations include:

- **Create**: Add new to-do items
- **Read**: List all to-do items
- **Update**: Edit existing to-do items
- **Delete**: Remove to-do items
- **Toggle**: Mark items as done/undone
- **Search**: Find items by keyword
- **Bulk Insert**: Add multiple items at once (for performance testing)

## 📊 Key Differences

### 1. Data Storage
- **JSON**: Stores all data in a single file as a JSON array
- **SQL**: Uses a SQLite database with a proper schema
- **SQLAlchemy**: Uses the same SQLite database through ORM models

### 2. ID Management
- **JSON**: Reuses IDs to maintain a compact sequence
- **SQL**: Never reuses IDs once assigned (AUTOINCREMENT)
- **SQLAlchemy**: Relies on the database AUTOINCREMENT behavior

### 3. Data Integrity
- **JSON**: Manual implementation of constraints and validation
- **SQL**: Built-in constraints (UNIQUE, NOT NULL, etc.)
- **SQLAlchemy**: Surfaces database constraint violations as Python exceptions

### 4. Performance
- **JSON**: Degrades as dataset grows, loads everything into memory
- **SQL**: More consistent performance, only loads what's needed
- **SQLAlchemy**: Thin abstraction over SQL with similar performance characteristics

### 5. Transactions
- **JSON**: No built-in transaction support
- **SQL**: ACID transactions ensure data integrity
- **SQLAlchemy**: Manages transactions via sessions and commits

### 6. Search Efficiency
- **JSON**: Linear search through all items
- **SQL**: Optimized search algorithms, can use indexes
- **SQLAlchemy**: Compiles high-level queries into efficient SQL statements

### 7. Scalability
- **JSON**: Good for small datasets, simple applications
- **SQL**: Better for larger datasets, complex applications
- **SQLAlchemy**: Supports scalable patterns such as relationships and eager/lazy loading

## 📝 Hands-on Exercises

The repository includes a comprehensive guide (`COMPARE.md`) with step-by-step exercises to explore and understand the differences across all three implementations. The exercises cover:

1. Basic CRUD Operations
2. ID Management
3. Uniqueness Constraints
4. Search Performance
5. Bulk Insert Performance
6. Data Integrity
7. Listing Large Datasets

Follow these exercises to gain practical insights into when to use each approach.

## 🧪 Implementation Details

### JSON Implementation

```python
# Key aspects of the JSON implementation
def load_data():
    if not os.path.exists(PATH):
        return []
    with open(PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(todos):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)
```

### SQL Implementation

```python
# Key aspects of the SQL implementation
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
```

### SQLAlchemy Implementation

```python
# Key aspects of the SQLAlchemy implementation
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    done = Column(Integer, nullable=False, default=0)
```

## 🎓 Educational Value

This repository is designed for:

- Students learning about data storage options
- Developers deciding between file-based and database storage
- Instructors teaching database concepts
- Anyone interested in understanding the practical differences between JSON, SQL, and ORM approaches

## 📚 Further Learning

After exploring this repository, consider:

1. Adding indexes to the SQL implementation to further improve search performance
2. Implementing pagination for listing large datasets
3. Adding more complex data relationships that would benefit from a relational database
4. Exploring NoSQL databases as another alternative

## 📄 License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

## 👤 Author

Created by [Mr-Zamora](https://github.com/Mr-Zamora)
