# JSON vs SQL: Hands-on Comparison Guide

This guide provides step-by-step instructions for comparing JSON, raw SQL, and SQLAlchemy ORM implementations of a simple CRUD application. By following these exercises, you'll gain practical understanding of the key differences between file-based storage, direct database access, and using an ORM layer.

## Setup

1. Install dependencies from the repository root: `pip install -r requirements.txt`
2. Open three terminal windows side by side, each in the repository root (`JSON-to-SQL/`)
3. In Terminal 1: `cd json_todo_starter`
4. In Terminal 2: `cd sql_todo_starter`
5. In Terminal 3: `cd ORM_sql_alchemy`
6. Run all applications:
   - Terminal 1: `python app.py`
   - Terminal 2: `python app.py`
   - Terminal 3: `python app.py`

## Resetting the Data

All three apps save to disk, so **restarting an app does NOT clear its data**. Whenever an exercise says "reset", quit all three apps (option `8`) and then, from the repository root:

- **JSON**: replace the contents of `json_todo_starter/todos.json` with `[]`
- **SQL**: delete `sql_todo_starter/todos.db`
- **SQLAlchemy ORM**: delete `ORM_sql_alchemy/todos.db`

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

The apps recreate empty storage on the next run. Reset before Exercise 1 so all three start from the same state.

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
