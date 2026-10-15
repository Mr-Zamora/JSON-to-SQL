# Programming for the Web: Data Before Flask

Before we delve into web frameworks like Flask, it's crucial to understand the foundational concepts of data management, specifically CRUD, and the different tools you can use for data storage, like JSON and SQL.

NotebookLM: https://notebooklm.google.com/notebook/1514357e-9cf4-41c8-9853-1a7c21b3abf8

**Unit path**

1. The Importance of Learning CRUD
2. Get the Code
3. Lesson 1: JSON To-Do Program
4. Lesson 2: SQL To-Do Program
5. Lesson 3: Hands-on Comparison (CSV → JSON → SQL)
6. The Difference Between Using JSON and SQL
7. Lesson 4: ORM (SQLAlchemy)
8. Lesson 5: Relationships: Users, Categories, Joins and GROUP BY
9. How Do You Know We're Ready to Move to Flask?

> **Exam scope.** HSC questions use the SQL syntax in the course specifications: `SELECT`, `FROM`, `WHERE` with `AND`, `OR` and `NOT`, `ORDER BY` with `ASC` or `DESC`, `GROUP BY`, the aggregate functions `COUNT`, `SUM`, `AVG`, `MAX` and `MIN`, `AS` for column display names, and joins written as a comma-separated `FROM` list with the join condition in `WHERE`. Items marked **Extension** in this unit, such as `LEFT JOIN`, `HAVING`, `LIKE`, and writing `INSERT`, `UPDATE` or `DELETE` statements, go beyond that syntax. They are still worth learning because you will use them in Flask.

---

## 1. The Importance of Learning CRUD

CRUD is an acronym that stands for **Create, Read, Update, and Delete**. The NotebookLM sources emphasise that learning CRUD is fundamental because it is the pattern used by almost every application to handle data. Whether you are using social media or a banking app, these four operations are at the core of how you interact with information.

Here's why it's so important to learn this concept first:

- **It's a Universal Pattern:** CRUD provides the basic "heartbeat" for nearly all data-driven applications. Mastering this pattern means you understand the essential cycle of data handling that you will use in almost every future project.
- **Moves from Theory to Practice:** By building a simple application that uses CRUD, you move beyond just memorising definitions and get to "feel CRUD in a real program". This hands-on experience is essential for building any application.
- **Builds Foundational Confidence:** The sources outline a teaching strategy focused on building a simple command-line tool specifically to isolate and teach CRUD without the extra complexity of web frameworks. This ensures you grasp the core data handling cycle before adding more layers.

To make it more relatable, think of a school locker:

| CRUD | Locker |
|---|---|
| **Create** | Putting a new book in |
| **Read** | Checking what books are there |
| **Update** | Changing a label on a folder or book |
| **Delete** | Taking a book out |

---

## 2. Get the Code

Clone my repo: https://github.com/Mr-Zamora/JSON-to-SQL

```bash
git clone https://github.com/Mr-Zamora/JSON-to-SQL.git
cd JSON-to-SQL
pip install -r requirements.txt
```

The repo contains the same To-Do app written four ways:

| Folder | Stores data in | Used in |
|---|---|---|
| `csv_todo_starter/` | `todos.csv` | Lesson 3 (warm-up) |
| `json_todo_starter/` | `todos.json` | Lesson 1 |
| `sql_todo_starter/` | `todos.db` (SQLite) | Lesson 2 |
| `ORM_sql_alchemy/` | `todos.db` (SQLite via SQLAlchemy) | Lesson 4 |

Run any version from inside its folder:

```bash
cd json_todo_starter
python app.py
```

Every version shows the same menu:

```
1) List  2) Add  3) Toggle  4) Edit  5) Delete  6) Search  7) Bulk Add  8) Quit
```

> **Data is saved to disk.** Restarting an app does not clear it. The README and COMPARE.md explain how to reset each app's data.

---

## 3. Lesson 1: JSON To-Do Program

Folder: `json_todo_starter/app.py`

Run it. You will see the menu. Choose numbers to use each feature. Start by adding two items.

### Read and write explained

Open `app.py` on the left of your screen and `todos.json` on the right.

This function **loads** data from the file:

```python
def load_data():
    if not os.path.exists(PATH):
        return []
    with open(PATH, "r", encoding="utf-8") as f:
        return json.load(f)  # Read JSON text and turn it into Python data
```

This function **saves** data to the file:

```python
def save_data(todos):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)  # Turn Python data into JSON text and write it
```

**So basically...** `json.load` reads the text and makes Python objects. `json.dump` takes Python objects and writes text to the file. That is all JSON is doing here.

**Think of it this way...** `todos.json` is your notebook. `load_data` opens it to read. `save_data` writes a new page.

### CRUD in action

Add, List, Toggle, Edit and Delete items, and watch `todos.json` change after each one.

- **Create:** Add a new item with a unique `id`.
- **Read:** List all items. Do not guess. Read them from the file.
- **Update:** Change the title or toggle done.
- **Delete:** Remove by `id` and then save.

### How the `id` is chosen

`id` is a unique number. It helps us find the exact record to update or delete. This app picks the **first unused number**, so IDs freed by a delete are reused:

```python
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
```

Example: with IDs `1, 2, 4`, the next item gets `3`. With IDs `1, 2, 3`, it gets `4`.

Keep this in mind. In Lesson 3 you will see that SQL deliberately **never** reuses an ID, and why that matters.

### Common mistakes and fixes

**Watch out for...**

- **Empty titles.** Fix by checking `if not title: print("Please enter something.")`
- **Forgetting to save.** After any change, call `save_data(todos)`.
- **Wrong `id`.** If the program says "Id not found", list items first, then try again.

**Tip:** these problems show up in almost every app. The fix is the same: validate input, use clear messages, and always save after changes.

### Why JSON first, SQL later

JSON is perfect for learning because you can see the data in a file. Later we will use SQL when we need rules like unique values, fast search, and many users at once. Today is about the shape of CRUD. Next lesson we compare this with SQL.

Further reading: https://olibr.com/blog/json-vs-sql-whats-the-difference/

### Quick challenge

Try this yourself:

1. Add three items
2. Toggle one done
3. Edit a title
4. Delete by `id`
5. Open `todos.json` and point to `id`, `title`, `done`

If all five work, you have learned CRUD (with JSON).

---

## 4. Lesson 2: SQL To-Do Program

Folder: `sql_todo_starter/app.py`

Last lesson you saved To-Dos in a JSON file. It worked. Today you'll see why apps switch to SQL as they grow, and you'll run simple SQL commands that do the same Create, Read, Update, and Delete.

### Lesson goals

- Spot JSON pain points
- Know what a database table is
- Map CRUD to four SQL commands

### JSON pain points

- JSON is great for tiny, single-user tasks. You can open the file and read it like a notebook. It starts to hurt when you need **rules**. Example: "No duplicate titles". You had to write code to check that.
- It starts to hurt when more than one program writes to the file. Two saves at the same time can lose data.
- Searching and sorting get messy as the file grows, and every change rewrites the whole file.
- Validation is all on you. The file will accept anything unless you check every rule in Python.

Databases fix these problems with built-in rules, safe writes, and queries.

### What is a database table

- A **database** is software that stores data safely and lets you ask questions about it.
- A **table** is like a spreadsheet. It has columns such as `id`, `title`, and `done`, and rows for each task.
- A **schema** is the set of rules for a table. Example: `title` cannot be empty. `title` must be unique. `id` counts up by itself.

**Think of...** JSON as a single notebook. A database as a library system that tracks every book with clear rules.

### CRUD in SQL

| CRUD | SQL command |
|---|---|
| Create | `INSERT` |
| Read | `SELECT` |
| Update | `UPDATE` |
| Delete | `DELETE` |

You already know the actions. SQL gives each action a clear word. Insert, Select, Update, Delete. You will run one of each in a moment.

### Minimal demo replacing the JSON To-Do

This is the table the SQL app creates when it starts (see `setup()` in `app.py`):

```sql
CREATE TABLE IF NOT EXISTS todos(
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL UNIQUE,
  done  INTEGER NOT NULL DEFAULT 0
);
```

- `PRIMARY KEY AUTOINCREMENT`: the database makes the id, and never reuses one.
- `NOT NULL`: cannot be empty.
- `UNIQUE`: no duplicates for `title`.
- `DEFAULT 0`: start as not done. (SQLite has no true/false type, so `0` = not done, `1` = done.)

Now map each JSON feature to one SQL line.

```sql
-- Create (Add)
INSERT INTO todos(title) VALUES ('Buy milk');

-- Read (List)
SELECT id, title, done FROM todos ORDER BY done, id;

-- Update (Toggle)
UPDATE todos SET done = CASE done WHEN 0 THEN 1 ELSE 0 END WHERE id = 1;

-- Update (Edit title)
UPDATE todos SET title = 'Buy oat milk' WHERE id = 1;

-- Delete
DELETE FROM todos WHERE id = 1;
```

These five lines replace the core JSON work you did last lesson.

> **Extension for the exam.** HSC questions ask you to read and write `SELECT` queries. Writing `INSERT`, `UPDATE` and `DELETE` statements goes beyond exam syntax, but every Flask app needs them, so learn them here.

The big win is the rule inside the table. If you try the same title twice, the database blocks it.

### Run it in Python

This is `add_item()` from `sql_todo_starter/app.py`:

```python
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
```

Three things to notice:

1. **The SQL is a string that Python sends to the database.** The database runs it and does the safe write.
2. **The `?` is a placeholder.** The title is passed separately as `(title,)`. Never build SQL by joining strings, e.g. `"... VALUES ('" + title + "')"`, because a user could type SQL into the title and run it. This attack is called **SQL injection**. Placeholders prevent it.
3. **No duplicate check in Python.** Compare this with the JSON `add_item()`, which loops through every todo looking for the same title. Here the database's `UNIQUE` rule raises `sqlite3.IntegrityError`, and we just report it.

This is the same CRUD you used with JSON. Now the database enforces rules for you.

### How to view an SQLite database file

SQLite database files (like your `todos.db`) aren't plain text files like JSON, so you can't just open them in a text editor. Here are some beginner-friendly ways to view your SQLite database:

**Option 1: VS Code extension (no separate install)**

1. In VS Code, open Extensions and install **SQLite Viewer**
2. Click `sql_todo_starter/todos.db` in the Explorer to see the table

**Option 2: DB Browser for SQLite (most features)**

1. Download and install [DB Browser for SQLite](https://sqlitebrowser.org/dl/). It's free and easy to use
2. Open the program after installation
3. Click "Open Database" and navigate to `sql_todo_starter\todos.db`
4. Browse data. You'll see tabs for:
   - "Database Structure" (shows your tables)
   - "Browse Data" (view the actual data in tables)
   - "Execute SQL" (run your own queries)

**Option 3: SQLite command line (learning experience)**

1. Check if SQLite is installed by opening a terminal and typing `sqlite3 --version`
2. If not installed, download the [SQLite command-line tools](https://www.sqlite.org/download.html)
3. Open your database:

   ```
   cd sql_todo_starter
   sqlite3 todos.db
   ```

4. Explore:

   ```
   .tables              -- list tables
   .schema todos        -- show the table's rules
   SELECT * FROM todos; -- show all rows
   .exit                -- quit
   ```

### Transfer the idea to other apps

Once you can Create, Read, Update, and Delete with SQL, you can manage anything. Tasks, contacts, products, bookings. The four actions stay the same. Only the columns change.

So for a user manager app... `username` becomes a `UNIQUE` field. The same idea stops duplicates. Later we add password hashing for real security.

---

## 5. Lesson 3: Hands-on Comparison (CSV → JSON → SQL)

Now that you have used both apps, compare them side by side. The exercises live in the repo so they always match the code:

**[COMPARE.md: Hands-on Comparison Guide](https://github.com/Mr-Zamora/JSON-to-SQL/blob/main/COMPARE.md)**

- **Part A: CSV vs JSON.** Start from the format you already know. Same app, same logic, only the file format changes. (Exercises A1–A4)
- **Part B: JSON vs SQL vs SQLAlchemy ORM.** ID management, uniqueness rules, search, bulk insert performance, data integrity and large datasets. (Exercises 1–7) Do Exercises 1–7 with the JSON and SQL apps now. You will run the ORM app in Lesson 4.

Follow the reset instructions in COMPARE.md before each part, and record your timings: they become evidence in the readiness questions.

---

## 6. The Difference Between Using JSON and SQL

JSON and SQL are two different tools for data persistence, each with its own strengths and ideal use cases. The suggested learning path is to start with JSON to understand the shape of CRUD, and then move to SQL for greater power and complexity.

NotebookLM: https://notebooklm.google.com/notebook/1940c10c-e4a9-4e92-a88b-21b7f5445295

| Feature | JSON (JavaScript Object Notation) | SQL (Structured Query Language) |
|---|---|---|
| **Primary purpose in this context** | Perfect for learning and small-scale data. It is chosen specifically because it is simple and transparent. | For more robust and complex applications that have advanced needs. |
| **Data format and visibility** | A simple, human-readable text format that looks like Python lists and dictionaries. You can open the `.json` file and directly see how your data is stored, which makes the connection between code and storage very clear for a beginner. | Data is stored in **tables** (rows and columns) with a schema of rules, inside a database file (`todos.db`) that is not plain text. You view and change it through SQL or a database tool, not a text editor. |
| **Key strengths** | Simplicity and immediate visual feedback. Great for getting started without the overhead of setting up a database. | Enforcing data integrity rules (like ensuring values are unique), safe all-or-nothing writes (transactions), querying and combining data, and supporting many users safely. |
| **When to use it** | When you are learning the fundamentals of CRUD and data persistence, or for small, single-user data such as settings. | When your application grows and needs strict rules, better performance at scale, and the ability to handle multiple users at once. |
| **Learning trajectory** | The first foundational step in understanding data persistence: the "shape of CRUD". | The next logical step after mastering CRUD with JSON: rebuild the same app in SQL to see how a database can enforce rules. |

In summary, you start with JSON to clearly see and understand the four CRUD operations in a simple, tangible way. Once you have mastered that pattern, you can then apply it to a more powerful tool like SQL when your application's needs become more demanding.

### Adding a search feature

Both apps have option `6) Search`. Compare how each one finds matching items.

**JSON:** Python loops through every item in memory and checks each title:

```python
results = []
for item in todos:
    if keyword in item["title"].lower():
        results.append(item)
```

**SQL:** one query asks the database for matching rows. `%` means "any characters", so `%milk%` matches any title containing "milk":

```sql
SELECT id, title, done FROM todos WHERE title LIKE ? ORDER BY id
```

```python
rows = con.execute(
    "SELECT id, title, done FROM todos WHERE title LIKE ? ORDER BY id",
    (f"%{keyword}%",)
).fetchall()
```

> **Extension: `LIKE` and `CONTAINS`.** The course specifications describe text matching with the word `CONTAINS`, for example `WHERE title CONTAINS 'milk'`. SQLite has no `CONTAINS` operator, so working code uses `WHERE title LIKE '%milk%'`. Learn to recognise both: an exam may use `CONTAINS`, and your code will use `LIKE`.

**What the timings show:** in this app both searches are very fast, and JSON can even be slightly faster, because its data is already in memory. A search for `%word%` makes the database check every row too. The SQL advantage is that you **describe** what you want and the database works out how to find it. With an **index** on a column, exact searches like `WHERE title = 'Buy milk'` can find a row without checking every row, even in millions of rows.

### Multiple users

**JSON:**
- Only one user can safely make changes at a time
- Example: if two students load the file, both add a todo and both save, the second save overwrites the first, and one todo is lost

**SQL:**
- The database manages multiple users making changes, so no update is lost
- Example: two students add todos at the same time. SQLite queues the writes one after the other (it locks the file for each write), and both todos are saved. Larger databases such as PostgreSQL and MySQL can process many writes at once

### Organisation and relationships

**JSON:**
- Hard to connect related data
- Example: to add categories to todos, you would copy the category name into every todo, or build complex nested structures

**SQL:**
- Easy to connect related information
- Example: link todos to categories, users or priorities with a **foreign key**, then combine them with a **JOIN**. You will do exactly this in Lesson 5

### Real-world comparison

Think of it like this:

- **JSON** is like a notebook: simple, portable, but gets unwieldy with lots of pages
- **SQL** is like a library with a catalogue system: more complex to set up, but much better for organising large amounts of information

For a classroom project with a few todos, both work fine. For a real application with thousands of items, multiple users, or complex data relationships, SQL is much better suited.

---

## 7. Lesson 4: ORM (SQLAlchemy)

Folder: `ORM_sql_alchemy/app.py`

### What is an ORM?

An **Object-Relational Mapping (ORM)** is a **layer of abstraction** between your program and the database. It lets programmers use their own programming language (here, Python) to access the database, instead of writing SQL strings. You work with database rows as Python **objects** and describe a table as a Python **class**. The ORM writes the SQL for you and sends it to the database.

The ORM is a translator between your **objects** (Python) and your **relational** database (tables).

Run the ORM app. It behaves exactly like the SQL app, and it even uses the same kind of `todos.db` file. Only the code is different.

### The table as a class

**SQL** (`sql_todo_starter`):

```sql
CREATE TABLE todos(
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL UNIQUE,
  done  INTEGER NOT NULL DEFAULT 0
);
```

**ORM** (`ORM_sql_alchemy`):

```python
class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    done = Column(Integer, nullable=False, default=0)
```

Same rules, Python syntax. `Base.metadata.create_all(engine)` turns the class into the `CREATE TABLE` statement.

### CRUD: SQL vs ORM

Taken from the two `app.py` files:

| CRUD | SQL (`sqlite3`) | ORM (SQLAlchemy) |
|---|---|---|
| Create | `con.execute("INSERT INTO todos(title) VALUES (?)", (title,))` | `session.add(Todo(title=title, done=0))` |
| Read | `con.execute("SELECT id, title, done FROM todos ORDER BY done, id")` | `session.query(Todo).order_by(Todo.done, Todo.id).all()` |
| Update | `con.execute("UPDATE todos SET title = ? WHERE id = ?", (new_title, i))` | `todo.title = new_title` |
| Delete | `con.execute("DELETE FROM todos WHERE id = ?", (i,))` | `session.delete(todo)` |
| Save | automatic at the end of `with connect() as con:` | `session.commit()` |
| Rule broken | `except sqlite3.IntegrityError:` | `except IntegrityError:` (from `sqlalchemy.exc`) |

With the ORM, updating a row is just changing an attribute (`todo.title = new_title`). The ORM notices the change and writes the `UPDATE` when you call `session.commit()`.

### Compare ORM to SQL

| | Raw SQL | ORM |
|---|---|---|
| **You write** | SQL strings inside Python | Python classes and method calls |
| **Learning curve** | Must learn SQL | Must learn the ORM library (and still benefit from knowing SQL) |
| **Control** | Full control over every query | The ORM writes the queries; complex queries can be harder to express |
| **Safety** | Safe only if you always use `?` placeholders | Parameters handled automatically, which protects against SQL injection |
| **Changing databases** | SQL may need rewriting (SQLite → PostgreSQL) | Usually just change the connection URL |
| **Performance** | Fastest; nothing in between | Small overhead (COMPARE.md Exercise 5 measures it) |
| **Joining tables** | Write the join in the query (`FROM todos, categories WHERE ...` or `JOIN ... ON`) | Call `.join()` in a query, or follow attributes like `todo.category.name` (Lesson 5) |

**Both approaches can join tables.** The difference is how you write the code, not what it can do. With raw SQL you write the query yourself. With an ORM you use your own programming language to access the database, and the ORM writes the SQL.

**An ORM hides SQL, and sometimes hides important details.** Without the line `__table_args__ = {"sqlite_autoincrement": True}`, SQLAlchemy does not add `AUTOINCREMENT` on SQLite. SQLite then gives each new row the current highest ID plus one, so the ID of the most recently added row can be reused if that row is deleted. Gaps in the middle are never refilled. A developer who only knew the ORM would never spot that. This is why we learn SQL before an ORM.

> **Libraries.** `sqlite3` is part of Python's standard library. SQLAlchemy is a third-party package that you install with `pip`, which is why it is listed in `requirements.txt`.

**Why it matters for Flask:** Flask apps commonly use **Flask-SQLAlchemy**, which is this same ORM. The class you just read is very close to what you will write in a Flask app.

---

## 8. Lesson 5: Relationships: Users, Categories, Joins and GROUP BY

So far there has been one table. Real apps connect tables: todos belong to users and categories, orders belong to customers, posts belong to users. Here we add a `users` table and a `categories` table, and link each todo to them.

Exam questions show tables like this: as **data grids** of sample rows, not as `CREATE TABLE` statements. Practise reading them.

**users**

| id | username |
|---|---|
| 1 | alex |
| 2 | sam |

**categories**

| id | name |
|---|---|
| 1 | School |
| 2 | Home |
| 3 | Health |

**todos**

| id | title | done | minutes | category_id | user_id |
|---|---|---|---|---|---|
| 1 | Complete maths homework | 1 | 45 | 1 | 1 |
| 2 | Study for SE exam | 0 | 90 | 1 | 2 |
| 3 | Finish English essay | 0 | 60 | 1 | 1 |
| 4 | Buy groceries | 0 | 30 | 2 | 2 |
| 5 | Pay bills | 1 | 10 | 2 | 1 |
| 6 | Call doctor | 0 | 5 | 3 | 2 |
| 7 | Go for a run | 1 | 30 | 3 | 1 |
| 8 | Learn guitar | 0 | 20 | NULL | 2 |

- `users.id` and `categories.id` are **primary keys**: each uniquely identifies a row
- `todos.category_id` and `todos.user_id` are **foreign keys**: each stores the `id` of a row in another table
- `NULL` means "no category". Every todo must have a user, so `user_id` is never `NULL`
- `minutes` is the estimated time each todo takes

The `user_id` link prepares you for login in Flask. A web app uses it to show each user only their own todos.

### Part 1: In SQL

Create a new file `categories_demo.py` (anywhere). It uses an in-memory database, so every run starts fresh and your `todos.db` is untouched.

```python
# categories_demo.py
# Three related tables: every todo belongs to a user and can belong to a category.
import sqlite3

con = sqlite3.connect(":memory:")  # in-memory database: fresh every run, nothing to reset
con.execute("PRAGMA foreign_keys = ON")  # SQLite only enforces foreign keys when asked

con.executescript("""
CREATE TABLE users(
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE
);

CREATE TABLE categories(
  id   INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE todos(
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  title       TEXT NOT NULL UNIQUE,
  done        INTEGER NOT NULL DEFAULT 0,
  minutes     INTEGER NOT NULL,
  category_id INTEGER REFERENCES categories(id),
  user_id     INTEGER NOT NULL REFERENCES users(id)
);

INSERT INTO users(username) VALUES ('alex'), ('sam');

INSERT INTO categories(name) VALUES ('School'), ('Home'), ('Health');

INSERT INTO todos(title, done, minutes, category_id, user_id) VALUES
  ('Complete maths homework', 1, 45, 1,    1),
  ('Study for SE exam',       0, 90, 1,    2),
  ('Finish English essay',    0, 60, 1,    1),
  ('Buy groceries',           0, 30, 2,    2),
  ('Pay bills',               1, 10, 2,    1),
  ('Call doctor',             0,  5, 3,    2),
  ('Go for a run',            1, 30, 3,    1),
  ('Learn guitar',            0, 20, NULL, 2);
""")

def show(sql):
    print("\n" + sql.strip())
    for row in con.execute(sql):
        print("  ", row)

# 1. WHERE: filter rows
show("SELECT title FROM todos WHERE done = 0")

# 2. NOT and ORDER BY ... ASC
show("""
SELECT title, minutes
FROM todos
WHERE NOT minutes > 30
ORDER BY minutes ASC, title ASC
""")

# 3a. Join two tables: exam style (comma-separated FROM, join condition in WHERE)
show("""
SELECT todos.title, categories.name
FROM todos, categories
WHERE todos.category_id = categories.id
ORDER BY todos.id
""")

# 3b. The same join written with JOIN ... ON
show("""
SELECT todos.title, categories.name
FROM todos
JOIN categories ON todos.category_id = categories.id
ORDER BY todos.id
""")

# 4. Join three tables
show("""
SELECT users.username, todos.title, categories.name
FROM users, todos, categories
WHERE todos.user_id = users.id
  AND todos.category_id = categories.id
ORDER BY users.username, todos.id
""")

# 5. GROUP BY with aggregate functions and AS
show("""
SELECT categories.name AS Category, COUNT(todos.id) AS Total,
       SUM(todos.done) AS Completed, AVG(todos.minutes) AS AvgMinutes,
       MIN(todos.minutes) AS Shortest, MAX(todos.minutes) AS Longest
FROM todos, categories
WHERE todos.category_id = categories.id
GROUP BY categories.name
ORDER BY Total DESC, Category ASC
""")

# 6. GROUP BY two fields, ORDER BY an alias
show("""
SELECT categories.name, todos.done, COUNT(todos.id) AS Total
FROM todos, categories
WHERE todos.category_id = categories.id
GROUP BY categories.name, todos.done
ORDER BY Total DESC, categories.name ASC, todos.done ASC
""")

# 7. Extension: LEFT JOIN keeps todos that have no category
show("""
SELECT todos.title, categories.name
FROM todos
LEFT JOIN categories ON todos.category_id = categories.id
ORDER BY todos.id
""")

# 8. Foreign key rule: category 99 does not exist
try:
    con.execute("INSERT INTO todos(title, minutes, category_id, user_id) VALUES ('Mystery task', 5, 99, 1)")
except sqlite3.IntegrityError as e:
    print("\nBlocked:", e)
```

**Predict before you run.** Use the data grids above to write down the rows you expect from each query, in order. Exams ask you to do exactly this. Then run `python categories_demo.py` and open the expected output below to check your predictions.

<details>
<summary>Expected output</summary>

```
SELECT title FROM todos WHERE done = 0
   ('Study for SE exam',)
   ('Finish English essay',)
   ('Buy groceries',)
   ('Call doctor',)
   ('Learn guitar',)

SELECT title, minutes
FROM todos
WHERE NOT minutes > 30
ORDER BY minutes ASC, title ASC
   ('Call doctor', 5)
   ('Pay bills', 10)
   ('Learn guitar', 20)
   ('Buy groceries', 30)
   ('Go for a run', 30)

SELECT todos.title, categories.name
FROM todos, categories
WHERE todos.category_id = categories.id
ORDER BY todos.id
   ('Complete maths homework', 'School')
   ('Study for SE exam', 'School')
   ('Finish English essay', 'School')
   ('Buy groceries', 'Home')
   ('Pay bills', 'Home')
   ('Call doctor', 'Health')
   ('Go for a run', 'Health')

SELECT todos.title, categories.name
FROM todos
JOIN categories ON todos.category_id = categories.id
ORDER BY todos.id
   ('Complete maths homework', 'School')
   ('Study for SE exam', 'School')
   ('Finish English essay', 'School')
   ('Buy groceries', 'Home')
   ('Pay bills', 'Home')
   ('Call doctor', 'Health')
   ('Go for a run', 'Health')

SELECT users.username, todos.title, categories.name
FROM users, todos, categories
WHERE todos.user_id = users.id
  AND todos.category_id = categories.id
ORDER BY users.username, todos.id
   ('alex', 'Complete maths homework', 'School')
   ('alex', 'Finish English essay', 'School')
   ('alex', 'Pay bills', 'Home')
   ('alex', 'Go for a run', 'Health')
   ('sam', 'Study for SE exam', 'School')
   ('sam', 'Buy groceries', 'Home')
   ('sam', 'Call doctor', 'Health')

SELECT categories.name AS Category, COUNT(todos.id) AS Total,
       SUM(todos.done) AS Completed, AVG(todos.minutes) AS AvgMinutes,
       MIN(todos.minutes) AS Shortest, MAX(todos.minutes) AS Longest
FROM todos, categories
WHERE todos.category_id = categories.id
GROUP BY categories.name
ORDER BY Total DESC, Category ASC
   ('School', 3, 1, 65.0, 45, 90)
   ('Health', 2, 1, 17.5, 5, 30)
   ('Home', 2, 1, 20.0, 10, 30)

SELECT categories.name, todos.done, COUNT(todos.id) AS Total
FROM todos, categories
WHERE todos.category_id = categories.id
GROUP BY categories.name, todos.done
ORDER BY Total DESC, categories.name ASC, todos.done ASC
   ('School', 0, 2)
   ('Health', 0, 1)
   ('Health', 1, 1)
   ('Home', 0, 1)
   ('Home', 1, 1)
   ('School', 1, 1)

SELECT todos.title, categories.name
FROM todos
LEFT JOIN categories ON todos.category_id = categories.id
ORDER BY todos.id
   ('Complete maths homework', 'School')
   ('Study for SE exam', 'School')
   ('Finish English essay', 'School')
   ('Buy groceries', 'Home')
   ('Pay bills', 'Home')
   ('Call doctor', 'Health')
   ('Go for a run', 'Health')
   ('Learn guitar', None)

Blocked: FOREIGN KEY constraint failed
```

</details>

**What each query teaches:**

1. **`WHERE`** filters rows: only todos that are not done.
2. **`NOT`** reverses a condition: `NOT minutes > 30` keeps todos of 30 minutes or less. **`ASC`** sorts smallest first. It is the default, but exam answers often write it. The second sort key, `title ASC`, decides the order of the two 30-minute todos.
3. **Joining two tables.** Both versions match each todo's `category_id` with a category's `id`, so we can show the category **name**. They return the same rows. "Learn guitar" is missing from both because it has no category to match.
   - **3a is the style used in exam questions, marking guidelines and the course specifications.** List the tables in `FROM`, separated by commas, and put the join condition in `WHERE`. Without that condition you get every todo paired with every category: 8 × 3 = 24 rows.
   - **3b uses `JOIN ... ON`**, which you will also see in real code and in the SQL an ORM writes. Either style should earn marks, but you must be able to read the comma style.
4. **Three tables** need two join conditions, combined with `AND`. In general, joining *n* tables needs *n* − 1 join conditions.
5. **`GROUP BY`** collapses rows into one row per category. `COUNT`, `SUM`, `AVG`, `MIN` and `MAX` are **aggregate functions**: they combine the rows in each group. Because `done` is `0` or `1`, `SUM(todos.done)` counts the completed todos. **`AS`** gives a column a display name, and `ORDER BY` can use that name (`Total`, `Category`).
6. **`GROUP BY` on two fields** makes one row for each combination of category and `done` value. This is the shape of 2025 HSC Question 21. The HSC answer sorted by `Total DESC` only. Here several rows tie on `Total`, and SQL does not guarantee the order of tied rows, so extra sort keys make the output predictable.
7. **Extension: `LEFT JOIN`** keeps every row from the left table (`todos`) even when there is no match; the missing name becomes `None` (`NULL`).
8. The **foreign key** blocks a todo pointing to a category that doesn't exist. This is called **referential integrity**.

**Try it:**

- Write a query listing only the titles in the "Home" category. (Hint: add `AND categories.name = 'Home'` to the `WHERE` of query 3a.)
- Write a query listing sam's todos that are not done, with their category names. (Hint: start from query 4.)
- Rename "Home" to "Household" with one `UPDATE` on `categories`, then rerun query 3a. Every Home todo shows the new name, but nothing in `todos` changed. With JSON, you would have to edit the name in every todo.
- **Extension:** change query 5 to show only categories with more than two todos by adding `HAVING COUNT(todos.id) > 2` after the `GROUP BY` line. (`WHERE` filters rows before grouping; `HAVING` filters groups after.)

### Part 2: The same thing with the ORM

Create `categories_orm.py` and run it.

```python
# categories_orm.py
# The same three tables, written as Python classes with SQLAlchemy.
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("sqlite:///:memory:", echo=False)  # change to echo=True to see the SQL
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    todos = relationship("Todo", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    todos = relationship("Todo", back_populates="category")

class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    done = Column(Integer, nullable=False, default=0)
    minutes = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = relationship("Category", back_populates="todos")
    user = relationship("User", back_populates="todos")

Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

alex, sam = User(username="alex"), User(username="sam")
school, home, health = Category(name="School"), Category(name="Home"), Category(name="Health")
session.add_all([alex, sam, school, home, health])
session.commit()  # save users and categories first so the todos get IDs 1-8 in list order

session.add_all([
    Todo(title="Complete maths homework", done=1, minutes=45, category=school, user=alex),
    Todo(title="Study for SE exam", minutes=90, category=school, user=sam),
    Todo(title="Finish English essay", minutes=60, category=school, user=alex),
    Todo(title="Buy groceries", minutes=30, category=home, user=sam),
    Todo(title="Pay bills", done=1, minutes=10, category=home, user=alex),
    Todo(title="Call doctor", minutes=5, category=health, user=sam),
    Todo(title="Go for a run", done=1, minutes=30, category=health, user=alex),
    Todo(title="Learn guitar", minutes=20, user=sam),
])
session.commit()

print("JOIN (follow the relationships):")
for todo in session.query(Todo).join(Todo.category).order_by(Todo.id):
    print("  ", todo.user.username, "|", todo.title, "->", todo.category.name)

print("\nThe other direction: alex.todos")
for todo in alex.todos:
    print("  ", todo.title)

print("\nGROUP BY:")
rows = (
    session.query(Category.name, func.count(Todo.id), func.sum(Todo.done))
    .join(Category.todos)
    .group_by(Category.name)
    .order_by(func.count(Todo.id).desc(), Category.name)
)
for name, total, completed in rows:
    print("  ", name, total, completed)
```

Predict the output first, then check:

<details>
<summary>Expected output</summary>

```
JOIN (follow the relationships):
   alex | Complete maths homework -> School
   sam | Study for SE exam -> School
   alex | Finish English essay -> School
   sam | Buy groceries -> Home
   alex | Pay bills -> Home
   sam | Call doctor -> Health
   alex | Go for a run -> Health

The other direction: alex.todos
   Complete maths homework
   Finish English essay
   Pay bills
   Go for a run

GROUP BY:
   School 3 1
   Health 2 1
   Home 2 1
```

</details>

**What to notice:**

- `ForeignKey("categories.id")` is the same foreign key as `REFERENCES categories(id)`.
- `relationship()` is the ORM's big extra. You never write join conditions to get a name: `todo.category.name` goes from todo to category, `todo.user.username` goes from todo to user, and `alex.todos` goes from a user to their todos.
- When creating todos we wrote `category=school` and `user=alex`, which are Python objects, not `category_id=1` and `user_id=1`. The ORM filled in the IDs for us.
- **See the SQL:** change `echo=False` to `echo=True` and run again. Among the output you will find the SQL the ORM wrote for the GROUP BY query:

  ```sql
  SELECT categories.name AS categories_name, count(todos.id) AS count_1, sum(todos.done) AS sum_1
  FROM categories JOIN todos ON categories.id = todos.category_id
  GROUP BY categories.name ORDER BY count(todos.id) DESC, categories.name
  ```

  Compare it with query 5 in Part 1. It is the same grouping written in `JOIN ... ON` style, with fewer columns. The ORM doesn't replace SQL; it writes it for you.

---

## 9. How Do You Know We're Ready to Move to Flask?

Confidently answer these questions (without AI). If you can't, then we have another 1-2 more lessons to go.

**Self-check: can you...**

- [ ] Name the four CRUD operations and the SQL command for each?
- [ ] Explain what `json.load` and `json.dump` do?
- [ ] Explain why records are found by `id` rather than by title?
- [ ] Explain what `PRIMARY KEY`, `NOT NULL`, `UNIQUE` and `AUTOINCREMENT` do?
- [ ] Explain why SQL uses `?` placeholders instead of joining strings?
- [ ] Write a `SELECT` with `WHERE`, `NOT` and `ORDER BY ... ASC/DESC` from memory?
- [ ] Join two or three tables in the comma style, and read the same join written with `JOIN ... ON`?
- [ ] Write a `GROUP BY` query using `COUNT`, `SUM`, `AVG`, `MAX` or `MIN`, with `AS` display names?
- [ ] Predict the output of a query from tables shown as data grids?
- [ ] Explain what an ORM is and give one advantage and one disadvantage compared with SQL?

### Practice Question 1 (6 marks)

A student's To-Do app stores data in `todos.json`:

```json
[
  {"id": 1, "title": "Buy groceries", "done": false},
  {"id": 2, "title": "Call doctor", "done": true},
  {"id": 4, "title": "Pay bills", "done": false}
]
```

The app uses this function to choose the `id` for each new item:

```python
def next_id(todos):
    if not todos:
        return 1
    existing_ids = set(item["id"] for item in todos)
    for i in range(1, max(existing_ids) + 2):
        if i not in existing_ids:
            return i
```

(a) Identify which CRUD operation is performed by each of the following actions in the app: listing all items; toggling an item to done; removing an item by its `id`. **(2 marks)**

(b) The user adds "Walk dog" and then "Feed cat". State the `id` each new item receives, and explain your answer with reference to the code. **(2 marks)**

(c) An SQLite version of the app uses `id INTEGER PRIMARY KEY AUTOINCREMENT`. Explain one problem that could occur if IDs are reused, as they are in the JSON version. **(2 marks)**

<details>
<summary>Marking guidelines</summary>

**(a)**

| Criteria | Marks |
|---|---|
| Correctly identifies all three operations | 2 |
| Correctly identifies two operations | 1 |

Answer: listing all items is **Read**; toggling an item to done is **Update**; removing an item is **Delete**.

**(b)**

| Criteria | Marks |
|---|---|
| States both IDs correctly and explains them with reference to the code | 2 |
| States both IDs without a valid explanation, OR states one ID correctly with an explanation | 1 |

Sample answer: "Walk dog" gets **3** and "Feed cat" gets **5**. The loop checks each number from 1 upwards and returns the first one that is not in `existing_ids`. IDs 1 and 2 are taken, so the gap at 3 is filled. After that, 1 to 4 are all taken. The range now runs to `max(existing_ids) + 2`, which is 6, so the loop reaches 5 and returns it.

**(c)**

| Criteria | Marks |
|---|---|
| Explains a problem caused by ID reuse, including its consequence | 2 |
| Identifies a problem caused by ID reuse | 1 |

Sample answer: another table, a saved link or a log may still refer to a deleted todo by its old ID. If that ID is given to a new todo, the old reference now points to the wrong record, so the app could display, update or delete the wrong todo. `AUTOINCREMENT` prevents this by never handing out an ID again.

</details>

### Practice Question 2 (10 marks)

A To-Do database contains these tables. Sample rows are shown.

**users**

| id | username |
|---|---|
| 1 | alex |
| 2 | sam |

**categories**

| id | name |
|---|---|
| 1 | School |
| 2 | Home |
| 3 | Health |

**todos**

| id | title | done | minutes | category_id | user_id |
|---|---|---|---|---|---|
| 1 | Complete maths homework | 1 | 45 | 1 | 1 |
| 2 | Study for SE exam | 0 | 90 | 1 | 2 |
| 3 | Finish English essay | 0 | 60 | 1 | 1 |
| 4 | Buy groceries | 0 | 30 | 2 | 2 |
| 5 | Pay bills | 1 | 10 | 2 | 1 |
| 6 | Call doctor | 0 | 5 | 3 | 2 |
| 7 | Go for a run | 1 | 30 | 3 | 1 |
| 8 | Learn guitar | 0 | 20 | NULL | 2 |

(a) **Extension (not HSC style):** Write an SQL statement to add a todo titled "Revise SQL", taking 40 minutes, for alex, in the category with `id` 1. **(1 mark)**

(b) Write an SQL query that lists the titles of all todos that are not done, in alphabetical order. **(1 mark)**

(c) Write an SQL query that lists the title of each todo that has a category, together with the name of its category. **(2 marks)**

(d) Write an SQL query that shows each category's name and the number of todos in that category, with the count displayed as `Total`, from most todos to fewest. **(2 marks)**

(e) Write an SQL query that lists the username, title and category name of every todo that is not done and has a category. **(2 marks)**

(f) Predict the output of this query. Show your answer as a table with column headings. **(2 marks)**

```sql
SELECT users.username, COUNT(todos.id) AS Total, SUM(todos.minutes) AS Minutes
FROM users, todos
WHERE todos.user_id = users.id AND todos.done = 0
GROUP BY users.username
ORDER BY Minutes DESC
```

<details>
<summary>Marking guidelines</summary>

Sample answers use the comma join style found in exam marking guidelines. Equivalent answers using `JOIN ... ON` are also acceptable.

**(a)**

| Criteria | Marks |
|---|---|
| Provides a correct `INSERT` statement | 1 |

```sql
INSERT INTO todos(title, minutes, category_id, user_id) VALUES ('Revise SQL', 40, 1, 1)
```

`done` can be left out because it defaults to 0.

**(b)**

| Criteria | Marks |
|---|---|
| Provides a correct query, including both the filter and the sort | 1 |

```sql
SELECT title
FROM todos
WHERE done = 0
ORDER BY title ASC
```

**(c)**

| Criteria | Marks |
|---|---|
| Provides a correct query that joins both tables with the correct join condition | 2 |
| Provides a query with the correct tables and columns but a missing or incorrect join condition | 1 |

```sql
SELECT todos.title, categories.name
FROM todos, categories
WHERE todos.category_id = categories.id
```

"Learn guitar" is correctly left out because it has no category.

**(d)**

| Criteria | Marks |
|---|---|
| Provides a correct query with the join, `GROUP BY`, `AS Total` and descending order | 2 |
| Provides a query that counts todos per category with one error or omission | 1 |

```sql
SELECT categories.name, COUNT(todos.id) AS Total
FROM todos, categories
WHERE todos.category_id = categories.id
GROUP BY categories.name
ORDER BY Total DESC
```

**(e)**

| Criteria | Marks |
|---|---|
| Provides a correct query that joins all three tables and filters to todos that are not done | 2 |
| Provides a query that joins the tables with one error, for example a missing join condition or filter | 1 |

```sql
SELECT users.username, todos.title, categories.name
FROM users, todos, categories
WHERE todos.user_id = users.id
  AND todos.category_id = categories.id
  AND todos.done = 0
```

**(f)**

| Criteria | Marks |
|---|---|
| Provides the correct rows, values, order and column headings | 2 |
| Provides correct values with an error in order or headings | 1 |

| username | Total | Minutes |
|---|---|---|
| sam | 4 | 145 |
| alex | 1 | 60 |

</details>

### Practice Question 3 (9 marks)

A school is building a web application where students record and share study tasks. Many students will use the application at the same time, and each task belongs to a subject.

(a) Justify why a relational database is more suitable than a JSON file for storing the tasks. In your answer, refer to **at least two** of: data integrity, multiple users, relationships between data. **(4 marks)**

(b) The development team is deciding whether to access the database with raw SQL or with an ORM such as SQLAlchemy. Compare the two approaches, using code examples to support your answer. **(5 marks)**

<details>
<summary>Marking guidelines</summary>

**(a)**

| Criteria | Marks |
|---|---|
| Justifies the choice with reference to at least two of the listed aspects, linked to the scenario | 4 |
| Explains why a relational database is more suitable with reference to two aspects, with limited link to the scenario | 3 |
| Describes features of a relational database or limitations of a JSON file | 2 |
| Provides some relevant information | 1 |

Answers could include:

- **Data integrity:** the schema enforces rules such as `NOT NULL`, `UNIQUE` and foreign keys, so invalid tasks are rejected by the database. A JSON file accepts anything unless every rule is checked in code.
- **Multiple users:** the database handles many students writing at once by locking and using transactions, so no update is lost. With a JSON file, two students saving at the same time can overwrite each other's changes.
- **Relationships:** each task stores a `subject_id` foreign key and is joined to a `subjects` table, so a subject name is stored once. Renaming a subject changes one row. In JSON the subject name would be copied into every task.

**(b)**

| Criteria | Marks |
|---|---|
| Provides a detailed comparison of raw SQL and an ORM, covering similarities and differences, supported by relevant code examples | 5 |
| Provides a sound comparison supported by a code example | 4 |
| Describes features of both approaches, with some reference to code | 3 |
| Describes a feature of one or both approaches | 2 |
| Provides some relevant information | 1 |

Answers could include:

- An ORM is a layer of abstraction that lets programmers use their own programming language to access the database. Tables become classes and rows become objects, for example `session.query(Task).filter_by(subject_id=3).all()`.
- Raw SQL is written as strings sent to the database, for example `con.execute("SELECT * FROM tasks WHERE subject_id = ?", (3,))`. It gives full control over each query and avoids the ORM's small performance overhead.
- Similarities: both can join tables, both enforce the same database rules, and an ORM still produces SQL behind the scenes.
- An ORM parameterises values automatically, which protects against SQL injection. Raw SQL is only safe if the programmer always uses placeholders.
- An ORM usually needs only a connection URL change to move to another database such as PostgreSQL, while raw SQL may need rewriting.
- An ORM can hide important details. For example, SQLAlchemy only adds `AUTOINCREMENT` on SQLite when asked.
- `sqlite3` is part of Python's standard library. SQLAlchemy is a third-party package installed with `pip`.

</details>
