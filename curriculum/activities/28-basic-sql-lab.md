# 28. Basic SQL lab (offline, 30 minutes)

Status: practice lab for the CyberSci "basic SQL" skill (`SHOW`, `DESCRIBE`, `SELECT`, wildcards). It runs on your own machine with Python's built-in SQLite, no server needed. MySQL equivalents are listed because the competition may use MySQL.

## 1. What SQL is (layman)

A database is a set of spreadsheets (tables). SQL is how you ask questions: "show me the sheets", "show me the columns", "show me rows where the name starts with A". Web apps send SQL to a database on your behalf. SQL injection is when *your input becomes part of their question*.

## 2. Set up a practice database

Save this as `practice.py` and run `python practice.py` once:

```python
import sqlite3
db = sqlite3.connect("practice.db")
db.executescript("""
DROP TABLE IF EXISTS users; DROP TABLE IF EXISTS notes;
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, role TEXT, pw TEXT);
CREATE TABLE notes (id INTEGER PRIMARY KEY, owner INTEGER, body TEXT);
INSERT INTO users VALUES (1,'admin','admin','x1'),(2,'alice','user','x2'),(3,'adam','user','x3'),(4,'bob','user','x4');
INSERT INTO notes VALUES (1,1,'server key is hidden'),(2,2,'meeting at 3'),(3,3,'buy milk'),(4,4,'flag{practice}');
""")
db.commit()
```
Then open a prompt: `python -m sqlite3 practice.db` (or `sqlite3 practice.db` if installed).

## 3. The commands and what they map to

| Task | SQLite | MySQL |
|---|---|---|
| list databases | (one file per database) | `SHOW DATABASES;` |
| choose database | `.open practice.db` | `USE name;` |
| list tables | `.tables` | `SHOW TABLES;` |
| show columns | `.schema users` or `PRAGMA table_info(users);` | `DESCRIBE users;` |
| all rows | `SELECT * FROM users;` | same |
| some columns | `SELECT name, role FROM users;` | same |
| filter | `SELECT * FROM users WHERE role='user';` | same |
| wildcard | `WHERE name LIKE 'a%'` | same (`%` many chars, `_` one char) |
| sort/limit | `ORDER BY name DESC LIMIT 2` | same |
| count/group | `SELECT role, COUNT(*) FROM users GROUP BY role;` | same |
| join | `SELECT users.name, notes.body FROM users JOIN notes ON notes.owner=users.id;` | same |
| stack results | `SELECT name FROM users UNION SELECT body FROM notes;` | same |
| table list from metadata | `SELECT name FROM sqlite_master WHERE type='table';` | `SELECT table_name FROM information_schema.tables;` |

## 4. Exercises (try first, then check the answers below)

1. Show all tables and the columns of `users`.
2. List every user whose name starts with `ad`.
3. List the names of users who are not `admin`, sorted Z to A.
4. How many users have each role?
5. Show each user's name next to their note.
6. Use `UNION` to produce one column that lists every user name and then every note body.
7. Find the note containing the word `flag`.
8. Count the notes owned by `alice`.

<details>
<summary>Answers</summary>

1. `.tables` and `PRAGMA table_info(users);`
2. `SELECT * FROM users WHERE name LIKE 'ad%';` (returns admin and adam)
3. `SELECT name FROM users WHERE role!='admin' ORDER BY name DESC;`
4. `SELECT role, COUNT(*) FROM users GROUP BY role;`
5. `SELECT users.name, notes.body FROM users JOIN notes ON notes.owner = users.id;`
6. `SELECT name FROM users UNION SELECT body FROM notes;`
7. `SELECT * FROM notes WHERE body LIKE '%flag%';`
8. `SELECT COUNT(*) FROM notes WHERE owner=(SELECT id FROM users WHERE name='alice');`
</details>

## 5. How injection happens (and the fix), in code

```python
# VULNERABLE: the user's text becomes part of the query
name = input("name: ")
rows = db.execute(f"SELECT * FROM users WHERE name = '{name}'").fetchall()

# SAFE: the value travels separately from the query
rows = db.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()
```
Try both with the input `x' OR '1'='1`: the first returns every user, the second returns none. That one experiment explains why the fix is *parameterized queries*, not filtering quotes.

## 6. CTF reading tips

- Count columns before `UNION`: both SELECTs need the same number (and compatible types).
- Comments end a query early: `-- ` (with a space) and `#` in MySQL.
- Blind injection: if you only see a yes/no difference, ask one yes/no question at a time.
- Always find the table and column names first (metadata tables), then read the data.

## 7. Attempt loop

Attempt 1 (20 min, no notes) → compare with the answers → reread the table in section 3 → Attempt 2 two days later with a fresh database.
