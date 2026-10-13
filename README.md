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

- Python 3.7 or higher
- SQLAlchemy 1.4+ (listed in `requirements.txt`)
- Built-in `json` and `sqlite3` modules (included with Python)

### Running the Applications

1. Clone this repository:
   ```bash
   git clone https://github.com/Mr-Zamora/JSON-to-SQL.git
   cd JSON-to-SQL
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the JSON implementation:
   ```bash
   cd json_todo_starter
   python app.py
   ```

4. Run the SQL implementation:
   ```bash
   cd sql_todo_starter
   python app.py
   ```

5. Run the SQLAlchemy implementation:
   ```bash
   cd ORM_sql_alchemy
   python app.py
   ```

### Resetting the Data

All three apps save to disk, so **restarting an app does not clear its data**. To start fresh, quit the apps and from the repository root:

```bash
# macOS / Linux / Git Bash
echo [] > json_todo_starter/todos.json
rm -f sql_todo_starter/todos.db ORM_sql_alchemy/todos.db
```

```powershell
# Windows PowerShell
Set-Content json_todo_starter/todos.json "[]"
Remove-Item sql_todo_starter/todos.db, ORM_sql_alchemy/todos.db -ErrorAction SilentlyContinue
```

> **Upgrading from an earlier version?** Delete any existing `ORM_sql_alchemy/todos.db`. Databases created before the `sqlite_autoincrement` fix were built without `AUTOINCREMENT` and will still reuse IDs.

## 🔍 Repository Structure

```
JSON-to-SQL/
├── COMPARE.md            # Detailed comparison guide with exercises
├── README.md             # This file
├── requirements.txt      # Python dependencies (SQLAlchemy)
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
- **SQLAlchemy**: Relies on the database AUTOINCREMENT behavior (on SQLite this requires `__table_args__ = {"sqlite_autoincrement": True}`; `autoincrement=True` on the column alone does not emit the keyword)

### 3. Data Integrity
- **JSON**: Manual implementation of constraints and validation, which is easy to miss (the JSON bulk insert skips the duplicate check)
- **SQL**: Built-in constraints (UNIQUE, NOT NULL, etc.)
- **SQLAlchemy**: Surfaces database constraint violations as Python exceptions

### 4. Performance
- **JSON**: Degrades as dataset grows, loads everything into memory
- **SQL**: More consistent performance, only loads what's needed
- **SQLAlchemy**: Thin abstraction over SQL; slower than raw SQL but scales evenly

Differences only show at scale. Sample bulk insert timings (fresh data each run):

| Items | JSON | SQL | SQLAlchemy |
|---|---|---|---|
| 500 | 0.014 s | 0.008 s | 0.030 s |
| 5,000 | 2.04 s | 0.023 s | 0.24 s |
| 10,000 | 9.18 s | 0.040 s | 0.46 s |

The JSON slowdown is O(n²): `next_id()` rebuilds the full set of IDs for every new item.

### 5. Transactions
- **JSON**: No built-in transaction support; a crash while the file is being written can leave it truncated and lose all data
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

Follow these exercises to gain practical insights into when to use each approach. Reset the data (see above) before Exercise 1 and wherever the guide says so, so all three apps start from the same state.

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
    __table_args__ = {"sqlite_autoincrement": True}  # emit AUTOINCREMENT so IDs are never reused
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
