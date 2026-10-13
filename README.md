# JSON to SQL: Hands-on Comparison (CSV → JSON → SQL → ORM)

This repository provides a practical comparison between CSV and JSON file-based storage, raw SQL database storage, and SQLAlchemy ORM abstractions through four implementations of the same To-Do list application. It starts from CSV, a format most students already know, and builds up step by step to databases and ORMs.

## 📋 Project Overview

The repository contains four parallel implementations of a simple To-Do list application:

1. **CSV Implementation**: Uses a CSV file for data storage (the familiar starting point)
2. **JSON Implementation**: Uses a JSON file for data storage
3. **SQL Implementation**: Uses SQLite database for data storage
4. **SQLAlchemy Implementation**: Uses SQLite through SQLAlchemy ORM for data access

All implementations provide identical functionality but differ in their underlying data access and storage mechanisms, allowing for direct comparison of performance, data integrity, and implementation complexity. The CSV and JSON versions share identical logic, so comparing them isolates the effect of the file format alone.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- SQLAlchemy 1.4+ (listed in `requirements.txt`)
- Built-in `csv`, `json` and `sqlite3` modules (included with Python)

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

3. Run the CSV implementation:
   ```bash
   cd csv_todo_starter
   python app.py
   ```

4. Run the JSON implementation:
   ```bash
   cd json_todo_starter
   python app.py
   ```

5. Run the SQL implementation:
   ```bash
   cd sql_todo_starter
   python app.py
   ```

6. Run the SQLAlchemy implementation:
   ```bash
   cd ORM_sql_alchemy
   python app.py
   ```

### Resetting the Data

All apps save to disk, so **restarting an app does not clear its data**. To start fresh, quit the apps and from the repository root:

```bash
# macOS / Linux / Git Bash
echo id,title,done > csv_todo_starter/todos.csv
echo [] > json_todo_starter/todos.json
rm -f sql_todo_starter/todos.db ORM_sql_alchemy/todos.db
```

```powershell
# Windows PowerShell
Set-Content csv_todo_starter/todos.csv "id,title,done"
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
├── csv_todo_starter/     # CSV implementation
│   ├── app.py           # Main application code
│   └── todos.csv        # CSV data storage file
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
- **CSV**: Stores all data in a single file as a table (header row plus one line per item)
- **JSON**: Stores all data in a single file as a JSON array
- **SQL**: Uses a SQLite database with a proper schema
- **SQLAlchemy**: Uses the same SQLite database through ORM models

### 2. Data Types
- **CSV**: Everything is text; the program converts types itself (and `bool("False")` is `True`)
- **JSON**: Keeps strings, numbers, `true`/`false` and `null` as distinct types
- **SQL**: Column types declared in the schema
- **SQLAlchemy**: Column types declared on the Python model

### 3. ID Management
- **CSV / JSON**: Reuse IDs to maintain a compact sequence
- **SQL**: Never reuses IDs once assigned (AUTOINCREMENT)
- **SQLAlchemy**: Relies on the database AUTOINCREMENT behavior (on SQLite this requires `__table_args__ = {"sqlite_autoincrement": True}`; `autoincrement=True` on the column alone does not emit the keyword)

### 4. Data Integrity
- **CSV / JSON**: Manual implementation of constraints and validation, which is easy to miss (the bulk insert skips the duplicate check)
- **SQL**: Built-in constraints (UNIQUE, NOT NULL, etc.)
- **SQLAlchemy**: Surfaces database constraint violations as Python exceptions

### 5. Performance
- **CSV / JSON**: Degrade as dataset grows, load everything into memory
- **SQL**: More consistent performance, only loads what's needed
- **SQLAlchemy**: Thin abstraction over SQL; slower than raw SQL but scales evenly

Differences only show at scale. Sample bulk insert timings (fresh data each run):

| Items | CSV | JSON | SQL | SQLAlchemy |
|---|---|---|---|---|
| 500 | 0.013 s | 0.014 s | 0.008 s | 0.030 s |
| 5,000 | 1.57 s | 2.04 s | 0.023 s | 0.24 s |
| 10,000 | 8.41 s | 9.18 s | 0.040 s | 0.46 s |

The CSV/JSON slowdown is O(n²): `next_id()` rebuilds the full set of IDs for every new item.

### 6. Transactions
- **CSV / JSON**: No built-in transaction support; a crash while the file is being written can leave it truncated and lose all data
- **SQL**: ACID transactions ensure data integrity
- **SQLAlchemy**: Manages transactions via sessions and commits

### 7. Search Efficiency
- **CSV / JSON**: Linear search through all items
- **SQL**: Optimized search algorithms, can use indexes
- **SQLAlchemy**: Compiles high-level queries into efficient SQL statements

### 8. Scalability
- **CSV / JSON**: Good for small datasets, simple applications
- **SQL**: Better for larger datasets, complex applications
- **SQLAlchemy**: Supports scalable patterns such as relationships and eager/lazy loading

## 📝 Hands-on Exercises

The repository includes a comprehensive guide (`COMPARE.md`) with step-by-step exercises in two parts.

**Part A: CSV vs JSON** (start here if you have only used CSV)

- A1. Same App, Different File
- A2. Commas in Titles
- A3. Everything in CSV Is Text
- A4. Opening the File in Excel

**Part B: JSON vs SQL vs SQLAlchemy ORM**

1. Basic CRUD Operations
2. ID Management
3. Uniqueness Constraints
4. Search Performance
5. Bulk Insert Performance
6. Data Integrity
7. Listing Large Datasets

Follow these exercises to gain practical insights into when to use each approach. Reset the data (see above) before each part and wherever the guide says so, so all apps start from the same state.

## 🧪 Implementation Details

### CSV Implementation

```python
# Key aspects of the CSV implementation
def load_data():
    if not os.path.exists(PATH):
        return []
    with open(PATH, "r", encoding="utf-8", newline="") as f:
        todos = []
        for row in csv.DictReader(f):
            # CSV stores everything as text, so we must convert types ourselves.
            todos.append({
                "id": int(row["id"]),
                "title": row["title"],
                "done": row["done"] == "True",
            })
        return todos

def save_data(todos):
    with open(PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(todos)
```

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
- Anyone interested in understanding the practical differences between CSV, JSON, SQL, and ORM approaches

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
