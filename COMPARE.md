# CSV → JSON → SQL → ORM: Hands-on Comparison Guide

This guide compares four implementations of the same To-Do app. Every version has the same menu and features; only the way data is stored changes.

- **Part A: CSV vs JSON.** Start from a format you already know. The CSV and JSON apps share identical logic, so every difference you see comes from the file format alone.
- **Part B: JSON vs SQL vs SQLAlchemy ORM.** Move from files to a real database, then to a database accessed through Python objects.

## Setup

Install dependencies once, from the repository root (`JSON-to-SQL/`):

```bash
pip install -r requirements.txt
```

Each part tells you which apps to open. Run each app in its own terminal window, from inside its folder, with `python app.py`.

## Resetting the Data

Every app saves to disk, so **restarting an app does NOT clear its data**. Whenever an exercise says "reset", quit the apps (option `8`) and then, from the repository root:

- **CSV**: replace the contents of `csv_todo_starter/todos.csv` with just the header line `id,title,done`
- **JSON**: replace the contents of `json_todo_starter/todos.json` with `[]`
- **SQL**: delete `sql_todo_starter/todos.db`
- **SQLAlchemy ORM**: delete `ORM_sql_alchemy/todos.db`

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

The apps recreate empty storage on the next run. Reset before starting each part so all apps begin from the same state.

---

# Part A: CSV vs JSON

### Setup
1. Reset the data
2. Terminal 1: `cd csv_todo_starter` then `python app.py`
3. Terminal 2: `cd json_todo_starter` then `python app.py`
4. Keep a third terminal free for the Python experiments in Exercises A2 and A3

## Exercise A1: Same App, Different File

1. In **both** apps, add two items (option `2`):
   - "Buy groceries"
   - "Call doctor"
2. In both apps, toggle item `1` to done (option `3`)
3. Open `csv_todo_starter/todos.csv` and `json_todo_starter/todos.json` in VS Code and compare them:

   ```
   id,title,done
   1,Buy groceries,True
   2,Call doctor,False
   ```

   ```json
   [
     {
       "id": 1,
       "title": "Buy groceries",
       "done": true
     },
     {
       "id": 2,
       "title": "Call doctor",
       "done": false
     }
   ]
   ```

4. Compare the code: in VS Code, right-click `csv_todo_starter/app.py` → **Select for Compare**, then right-click `json_todo_starter/app.py` → **Compare with Selected**. Almost all the differences are in `load_data()` and `save_data()`.

**Learning Points:**
- CSV is a **table**: the column names appear once, in the header row, and each line is a row
- JSON is a **list of objects**: `[ ]` is a list, `{ }` is an object, and each object has `"key": value` pairs
- JSON repeats the field names on every item. The file is bigger, but each item describes itself
- `true`/`false` in JSON are real true/false values, not text

## Exercise A2: Commas in Titles

1. In both apps, add the item: "Milk, eggs"
2. Look at both files again:
   - **CSV**: `3,"Milk, eggs",False`. The title had to be wrapped in quotes, otherwise its comma would look like a new column
   - **JSON**: `"title": "Milk, eggs"`. Every string in JSON is already in quotes, so commas are never confusing
3. See what happens if you read the CSV the "simple" way. In your third terminal, `cd csv_todo_starter`, start Python with `python`, and type:

   ```python
   >>> [line.split(",") for line in open("todos.csv").read().splitlines()]
   [['id', 'title', 'done'], ['1', 'Buy groceries', 'True'], ['2', 'Call doctor', 'False'], ['3', '"Milk', ' eggs"', 'False']]
   ```

   Row 3 has split into **four** pieces instead of three.

**Learning Points:**
- Splitting CSV lines on `,` breaks as soon as the data contains a comma
- Python's `csv` module (used in the app) understands the quoting rules, which is why the app still works
- JSON's syntax has no such ambiguity: strings are always quoted

## Exercise A3: Everything in CSV Is Text

1. Still in the Python prompt inside `csv_todo_starter`, type:

   ```python
   >>> import csv
   >>> rows = list(csv.DictReader(open("todos.csv", newline="")))
   >>> rows[1]
   {'id': '2', 'title': 'Call doctor', 'done': 'False'}
   >>> bool(rows[1]["done"])
   True
   ```

   `id` is the text `'2'`, not the number `2`, and `done` is the text `'False'`. Worse, `bool('False')` is `True`, because any non-empty text counts as true.

2. Type `exit()`, then `cd ../json_todo_starter`, start `python` again, and type:

   ```python
   >>> import json
   >>> items = json.load(open("todos.json"))
   >>> items[1]
   {'id': 2, 'title': 'Call doctor', 'done': False}
   >>> type(items[1]["done"])
   <class 'bool'>
   ```

   JSON gives back a real number and a real `False`.

3. Open `csv_todo_starter/app.py` and find `load_data()`. Notice the lines that convert each value: `int(row["id"])` and `row["done"] == "True"`.

4. **Try it:** change `row["done"] == "True"` to `bool(row["done"])`, save, restart the CSV app and list the items. Every item now shows as done (✓). Change it back afterwards.

**Learning Points:**
- CSV has no types: every value is text, and the program must convert it correctly
- Getting the conversion wrong produces bugs that don't crash, so they're easy to miss
- JSON keeps text, numbers, `true`/`false` and `null` as different types

## Exercise A4: Opening the File in Excel (Windows, if Excel is installed)

1. Open `csv_todo_starter/todos.csv` in Excel and leave it open
2. In the CSV app, add a new item
3. The app crashes with `PermissionError`: Excel has locked the file, so Python can't write to it, and the item you just added is lost
4. Close Excel, restart the CSV app and add the item again; it works now

**Learning Points:**
- A file is hard to share: only one program can safely write to it at a time
- Being able to open the data in Excel is convenient, but it can block or even change the data (Excel may reformat values when saving)
- Databases (Part B) are designed so many users and programs can safely read and write the same data at once

## Part A Summary

| | CSV | JSON |
|---|---|---|
| Shape | Table: rows and columns | List of objects (can also nest lists inside objects) |
| Types | Everything is text; you convert it yourself | Text, numbers, `true`/`false`, `null` |
| Field names | Once, in the header | On every item |
| Commas and quotes in data | Quoting rules (use the `csv` module) | Strings always quoted |
| Common use | Spreadsheets, data export | Web APIs, JavaScript, config files |

**What CSV and JSON share** (and what Part B fixes):
- The whole file is loaded into memory and rewritten on every change
- Rules like "no duplicate titles" must be written by hand in Python
- No protection if the program crashes while writing the file
- Only one program can safely write at a time

JSON is the format web browsers and web APIs use to send data, which is why it matters in web programming. But it is still just a file. Part B shows what a database adds.

---

# Part B: JSON vs SQL vs SQLAlchemy ORM

### Setup
1. Reset the data
2. Terminal 1: `cd json_todo_starter` then `python app.py`
3. Terminal 2: `cd sql_todo_starter` then `python app.py`
4. Terminal 3: `cd ORM_sql_alchemy` then `python app.py`

## Exercise 1: Basic CRUD Operations

### Create
1. **JSON** (Terminal 1): Select option `2` to add an item
   - Enter title: "Complete homework"
2. **SQL** (Terminal 2): Select option `2` to add an item
   - Enter the same title: "Complete homework"
3. **SQLAlchemy ORM** (Terminal 3): Select option `2` to add an item
   - Enter the same title: "Complete homework"

### Read
1. **JSON**: Select option `1` to list all items
2. **SQL**: Select option `1` to list all items
3. **SQLAlchemy ORM**: Select option `1` to list all items

### Update
1. **JSON**: Select option `4` to edit an item
   - Enter ID: `1`
   - New title: "Complete math homework"
2. **SQL**: Select option `4` to edit an item
   - Enter ID: `1`
   - New title: "Complete math homework"
3. **SQLAlchemy ORM**: Select option `4` to edit an item
   - Enter ID: `1`
   - New title: "Complete math homework"

### Toggle Status
1. **JSON**: Select option `3` to toggle completion status
   - Enter ID: `1`
2. **SQL**: Select option `3` to toggle completion status
   - Enter ID: `1`
3. **SQLAlchemy ORM**: Select option `3` to toggle completion status
   - Enter ID: `1`

### Delete
1. **JSON**: Select option `5` to delete an item
   - Enter ID: `1`
2. **SQL**: Select option `5` to delete an item
   - Enter ID: `1`
3. **SQLAlchemy ORM**: Select option `5` to delete an item
   - Enter ID: `1`

**Learning Points:**
- Basic operations work similarly across all three implementations
- Notice differences in feedback messages between manual SQL and ORM
- SQLAlchemy demonstrates how ORMs provide the same constraints with higher-level syntax

## Exercise 2: ID Management

1. Add three items to all three applications:
   - "Buy groceries"
   - "Call doctor"
   - "Pay bills"

2. List items (option `1`) and compare the IDs. Exercise 1 already used and deleted ID 1:
   - **JSON**: IDs 1, 2, 3 (ID 1 was free again, so it is reused)
   - **SQL**: IDs 2, 3, 4 (ID 1 is never handed out again)
   - **SQLAlchemy ORM**: IDs 2, 3, 4 (same as SQL)

3. Delete the middle item, "Call doctor", in each application. Its ID differs per app:
   - **JSON**: Select option `5`, enter ID `2`
   - **SQL**: Select option `5`, enter ID `3`
   - **SQLAlchemy ORM**: Select option `5`, enter ID `3`

4. Add a new item to each:
   - "New task"

   - **JSON**: Should reuse ID 2 (the first available ID)
   - **SQL**: Should use ID 5 (never reuses IDs)
   - **SQLAlchemy ORM**: Should use ID 5 (the ORM still relies on AUTOINCREMENT)

**Learning Points:**
- JSON implementation reuses IDs to keep a compact sequence
- SQL with AUTOINCREMENT never reuses IDs once assigned
- SQLAlchemy ORM still depends on the database's AUTOINCREMENT behavior. On SQLite this must be requested explicitly with `__table_args__ = {"sqlite_autoincrement": True}`; `autoincrement=True` on the column alone does not emit the `AUTOINCREMENT` keyword
- Database-backed approaches are better for data integrity and referential integrity

## Exercise 3: Uniqueness Constraints

1. Try adding an item with the same title in all applications:
   - **JSON**: Add "Buy groceries" (already exists)
   - **SQL**: Add "Buy groceries" (already exists)
   - **SQLAlchemy ORM**: Add "Buy groceries" (already exists)

2. Observe the different behaviors:
   - **JSON**: Custom code checks for duplicates
   - **SQL**: Built-in UNIQUE constraint prevents duplicates

**Learning Points:**
- SQL has built-in data integrity constraints
- SQLAlchemy exposes those constraints through exceptions (e.g., `IntegrityError`)
- In JSON, we must implement constraints manually, and remember to do it everywhere. Look at `bulk_insert()` in the JSON app: it does not check for duplicates. Running bulk add twice in JSON creates duplicate titles, while SQL and SQLAlchemy refuse
- Database constraints are more reliable and consistent

## Exercise 4: Search Performance

1. Add more items to all applications using bulk insert:
   - Select option `7` in each terminal
   - Enter `50` as the number of items to add

2. Search for a term in all applications:
   - Select option `6` in each terminal
   - Enter search term: "item"

3. Compare the search results and execution times:
   - **JSON**: Must loop through all items in memory
   - **SQL**: Uses database engine's optimized search
   - **SQLAlchemy ORM**: Translates `contains()` into efficient SQL LIKE queries

**Learning Points:**
- For small datasets, performance difference may be minimal
- As data grows, SQL's optimized search becomes more efficient
- SQL can use indexes for extremely fast searches (not implemented in this demo)

## Exercise 5: Bulk Insert Performance

1. Reset all applications (see "Resetting the Data" above). Otherwise the bulk titles from Exercise 4 already exist and SQL/SQLAlchemy will reject the batch with a UNIQUE constraint error

2. Use bulk insert to add a small number of items:
   - Select option `7` in each terminal
   - Enter `500` as the number of items to add
   - At this size JSON may actually be the fastest! Small datasets hide the differences

3. Reset again, then bulk insert a larger number:
   - Select option `7` in each terminal
   - Enter `5000` as the number of items

4. Reset again, then try `10000` items and compare execution times:
   - **JSON**: Gets dramatically slower (roughly 4x the time for 2x the items)
   - **SQL**: Stays fast with a single transaction
   - **SQLAlchemy ORM**: Uses one transaction via session commit; a little slower than raw SQL but scales evenly

**Learning Points:**
- JSON performance degrades as the dataset grows. Here this is made worse by `next_id()`, which rebuilds the set of all IDs for every new item (an O(n²) algorithm)
- SQL with transactions maintains more consistent performance
- JSON loads the entire dataset into memory
- SQL only loads what's needed for each operation

## Exercise 6: Data Integrity

1. Reset all applications, then add a couple of normal items to each (e.g. "Buy groceries")

2. Start a bulk insert with a large number:
   - Select option `7` in each terminal
   - Enter `10000` as the number of items (JSON takes several seconds, giving you time to interrupt it; SQL may finish before you can react)

3. While items are being added, interrupt the application:
   - Press Ctrl+C to terminate the process

4. Restart the applications and list the data (option `1`):
   - **JSON**: None of the bulk items were saved, and your earlier items are still there. This app builds the list in memory and writes the file once at the end, so an interruption *before* the write loses the whole batch
   - **SQL**: Transaction ensures either all items are added or none
   - **SQLAlchemy ORM**: Session commit wraps operations in a transaction for all-or-nothing behavior

5. Discuss: what if the program crashed *while* `json.dump()` was writing the file?
   - Opening the file with `"w"` empties it immediately, so a crash mid-write leaves a truncated, invalid JSON file, which means **all** data is lost, not just the new batch
   - SQLite uses a journal file, so a crash during a write rolls back to the last committed state; the database is never left half-written

**Learning Points:**
- SQL transactions provide atomicity (all-or-nothing operations)
- JSON "all-or-nothing" here is accidental (one write at the end); the file itself has no protection against corruption
- Database transactions are crucial for data integrity

## Exercise 7: Listing Large Datasets

1. Make sure all applications have a large number of items (500+)

2. Use the list function in all applications:
   - Select option `1` in each terminal

3. Observe the behavior:
   - **JSON**: Must load all items into memory before displaying
   - **SQL**: Can retrieve items in batches (though not implemented in this demo)
   - **SQLAlchemy ORM**: Can leverage lazy loading and query limits (not implemented in this demo)

**Learning Points:**
- JSON requires loading the entire dataset into memory
- SQL can use pagination and limits to handle large datasets efficiently

## Conclusion

After completing these exercises, you should have a practical understanding of the key differences between JSON, SQL, and SQLAlchemy approaches:

1. **ID Management**:
   - JSON: Reuses IDs to maintain a compact sequence
   - SQL: Never reuses IDs once assigned (AUTOINCREMENT)

2. **Data Integrity**:
   - JSON: Manual implementation of constraints and validation
   - SQL: Built-in constraints (UNIQUE, NOT NULL, etc.)
   - SQLAlchemy: Surfaces database constraints through Python exceptions

3. **Performance**:
   - JSON: Degrades as dataset grows, loads everything into memory
   - SQL: More consistent performance, only loads what's needed
   - SQLAlchemy: Adds a thin abstraction with negligible overhead while still benefiting from SQL performance

4. **Transactions**:
   - JSON: No built-in transaction support
   - SQL: ACID transactions ensure data integrity
   - SQLAlchemy: Session management simplifies transaction handling

5. **Search Efficiency**:
   - JSON: Linear search through all items
   - SQL: Optimized search algorithms, can use indexes
   - SQLAlchemy: High-level query helpers compile down to efficient SQL

6. **Scalability**:
   - JSON: Good for small datasets, simple applications
   - SQL: Better for larger datasets, complex applications
   - SQLAlchemy: Enables scalable patterns (relationships, eager/lazy loading) as apps grow

7. **Implementation Complexity**:
   - JSON: Simpler to implement for basic needs
   - SQL: More complex but provides more features and safeguards
   - SQLAlchemy: Adds an abstraction layer that increases setup slightly but improves developer ergonomics and maintainability

These differences illustrate why most production applications use databases rather than file-based storage for data that requires CRUD operations, especially as the application grows in complexity and scale.
