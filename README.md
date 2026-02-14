# Mini SQL Compiler - Compiler Design Project

A fully functional SQL compiler built from scratch for Compiler Design course (6th Semester). This project implements all phases of compilation: Lexical Analysis, Syntax Analysis (Parsing), and Code Execution.

## 🎯 Project Overview

This Mini SQL Compiler demonstrates the complete compilation pipeline:
1. **Lexical Analysis (Scanner)** - Tokenizes SQL queries
2. **Syntax Analysis (Parser)** - Builds Abstract Syntax Tree (AST)
3. **Semantic Analysis** - Validates query structure
4. **Execution Engine** - Executes queries on in-memory database

## ✨ Features

### Supported SQL Commands
- ✅ **CREATE TABLE** - Create new tables with column definitions
- ✅ **INSERT INTO** - Insert data into tables
- ✅ **SELECT** - Query data with column selection
- ✅ **UPDATE** - Modify existing records
- ✅ **DELETE** - Remove records from tables
- ✅ **DROP TABLE** - Delete entire tables
- ✅ **WHERE Clause** - Filter data with conditions (=, !=, <, >, <=, >=)
- ✅ **Logical Operators** - Combine conditions with AND/OR

### Technical Features
- ✅ Complete lexical analyzer with token recognition
- ✅ Recursive descent parser for SQL grammar
- ✅ Abstract Syntax Tree (AST) generation
- ✅ In-memory database with full CRUD operations
- ✅ Beautiful GUI with syntax highlighting
- ✅ Query history and sample queries
- ✅ Real-time results in tabular format
- ✅ Error handling with detailed messages

## 🖥️ System Requirements

### Windows Operating System
- Windows 10 or Windows 11
- Python 3.8 or higher

### Required Python Packages
- tkinter (usually comes with Python)
- No external dependencies required!

## 📦 Installation Guide

### Step 1: Install Python (if not installed)
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, **CHECK** "Add Python to PATH"
3. Click "Install Now"

### Step 2: Verify Python Installation
Open Command Prompt (cmd) and run:
```bash
python --version
```
You should see: `Python 3.x.x`

### Step 3: Extract Project Files
1. Extract the `mini-sql-compiler.zip` file
2. You should see these files:
   ```
   mini-sql-compiler/
   ├── gui.py              (Main GUI application)
   ├── sql_compiler.py     (Compiler core)
   ├── README.md           (This file)
   ├── RUN_COMPILER.bat    (Quick launcher for Windows)
   └── USER_GUIDE.pdf      (Detailed documentation)
   ```

### Step 4: Run the Compiler

**Option A: Using the Batch File (Easiest)**
1. Double-click `RUN_COMPILER.bat`
2. The GUI will open automatically

**Option B: Using Command Prompt**
1. Open Command Prompt
2. Navigate to project folder:
   ```bash
   cd path\to\mini-sql-compiler
   ```
3. Run:
   ```bash
   python gui.py
   ```

## 🚀 Quick Start Guide

### 1. Launch the Application
Run the compiler using either method above. You'll see:
- **Query Editor** (left panel) - Write your SQL queries here
- **Output Console** (right panel) - See execution results
- **Results Table** (bottom right) - View SELECT query results
- **Sample Queries** (bottom left) - Click to load examples

### 2. Try Your First Query

**Example 1: Create a Table**
```sql
CREATE TABLE students (id INT, name VARCHAR(50), age INT, grade VARCHAR(2))
```
Click "▶ Execute Query"

**Example 2: Insert Data**
```sql
INSERT INTO students VALUES (1, 'Alice', 20, 'A')
```

**Example 3: Query Data**
```sql
SELECT * FROM students
```

**Example 4: Filter Data**
```sql
SELECT name, grade FROM students WHERE age > 19
```

**Example 5: Update Data**
```sql
UPDATE students SET grade = 'A+' WHERE name = 'Alice'
```

**Example 6: Delete Data**
```sql
DELETE FROM students WHERE age < 20
```

### 3. Using Sample Queries
- Click any query in the "Sample Queries" section
- It will load into the editor
- Click "Execute Query" to run it

## 📚 Complete SQL Command Reference

### CREATE TABLE
```sql
CREATE TABLE table_name (
    column1 datatype,
    column2 datatype,
    ...
)
```
**Supported Data Types:** INT, VARCHAR(n), FLOAT, DATE

**Example:**
```sql
CREATE TABLE employees (
    emp_id INT,
    name VARCHAR(100),
    salary FLOAT,
    hire_date DATE
)
```

### INSERT INTO
```sql
INSERT INTO table_name VALUES (value1, value2, ...)
```
OR
```sql
INSERT INTO table_name (column1, column2) VALUES (value1, value2)
```

**Examples:**
```sql
INSERT INTO employees VALUES (101, 'John Doe', 50000.50, '2024-01-15')
INSERT INTO employees (emp_id, name) VALUES (102, 'Jane Smith')
```

### SELECT
```sql
SELECT * FROM table_name
SELECT column1, column2 FROM table_name
SELECT * FROM table_name WHERE condition
```

**Examples:**
```sql
SELECT * FROM employees
SELECT name, salary FROM employees
SELECT * FROM employees WHERE salary > 45000
SELECT name FROM employees WHERE emp_id = 101
```

### UPDATE
```sql
UPDATE table_name SET column1 = value1 WHERE condition
UPDATE table_name SET column1 = value1, column2 = value2 WHERE condition
```

**Examples:**
```sql
UPDATE employees SET salary = 55000 WHERE emp_id = 101
UPDATE employees SET name = 'John Smith', salary = 60000 WHERE emp_id = 101
```

### DELETE
```sql
DELETE FROM table_name WHERE condition
DELETE FROM table_name  -- Deletes all records
```

**Examples:**
```sql
DELETE FROM employees WHERE emp_id = 101
DELETE FROM employees WHERE salary < 30000
```

### DROP TABLE
```sql
DROP TABLE table_name
```

**Example:**
```sql
DROP TABLE employees
```

### WHERE Clause with Operators
**Comparison Operators:** =, !=, <, >, <=, >=

**Examples:**
```sql
SELECT * FROM students WHERE age = 20
SELECT * FROM students WHERE age > 18
SELECT * FROM students WHERE grade != 'F'
```

**Logical Operators:** AND, OR

**Examples:**
```sql
SELECT * FROM students WHERE age > 18 AND grade = 'A'
SELECT * FROM students WHERE age < 20 OR grade = 'A+'
SELECT * FROM students WHERE age > 18 AND grade = 'A' OR grade = 'B'
```

## 🎨 GUI Features

### Query Editor
- Syntax-aware text editor
- Copy/paste support
- Large text area for complex queries

### Output Console
- Color-coded output
- Success/error indicators
- Timestamp for each execution
- Scrollable history

### Results Table
- Professional table display
- Column headers
- Row highlighting
- Scrollable for large datasets

### Buttons
- **▶ Execute Query** - Run the SQL query
- **🗑 Clear** - Clear the editor
- **📊 Show Tables** - View all database tables

## 🔧 Compiler Architecture

### 1. Lexical Analyzer (Lexer)
**File:** `sql_compiler.py` - Class `Lexer`

**Function:** Converts SQL query string into tokens
```python
Input:  "SELECT * FROM students"
Output: [SELECT, *, FROM, IDENTIFIER(students)]
```

**Token Types:**
- Keywords: SELECT, FROM, WHERE, INSERT, UPDATE, etc.
- Identifiers: table names, column names
- Literals: strings ('text'), numbers (123, 45.67)
- Operators: =, !=, <, >, <=, >=
- Symbols: (, ), *, ,, ;

### 2. Syntax Analyzer (Parser)
**File:** `sql_compiler.py` - Class `Parser`

**Function:** Validates syntax and builds Abstract Syntax Tree (AST)
```python
Input:  [SELECT, *, FROM, IDENTIFIER(students)]
Output: SelectNode(columns=['*'], table='students')
```

**AST Node Types:**
- CreateTableNode
- InsertNode
- SelectNode
- UpdateNode
- DeleteNode
- DropTableNode
- WhereClause

### 3. Execution Engine
**File:** `sql_compiler.py` - Class `QueryExecutor`

**Function:** Executes the AST on the in-memory database
```python
Input:  SelectNode
Output: Query results (rows of data)
```

### 4. Database Manager
**File:** `sql_compiler.py` - Class `Database`

**Function:** Manages tables and data in memory
- Table storage
- Row operations (CRUD)
- WHERE clause evaluation

## 🧪 Testing the Compiler

### Test Case 1: Complete Student Management
```sql
-- Create table
CREATE TABLE students (id INT, name VARCHAR(50), age INT, grade VARCHAR(2))

-- Insert multiple records
INSERT INTO students VALUES (1, 'Alice', 20, 'A')
INSERT INTO students VALUES (2, 'Bob', 21, 'B')
INSERT INTO students VALUES (3, 'Charlie', 19, 'A')
INSERT INTO students VALUES (4, 'Diana', 22, 'C')
INSERT INTO students VALUES (5, 'Eve', 20, 'B')

-- Query all data
SELECT * FROM students

-- Query with filter
SELECT name, grade FROM students WHERE age > 19

-- Query with AND condition
SELECT * FROM students WHERE age > 19 AND grade = 'A'

-- Update records
UPDATE students SET grade = 'A+' WHERE name = 'Alice'

-- Verify update
SELECT * FROM students WHERE name = 'Alice'

-- Delete records
DELETE FROM students WHERE age < 20

-- Verify deletion
SELECT * FROM students

-- Clean up
DROP TABLE students
```

### Test Case 2: Employee Database
```sql
-- Create employees table
CREATE TABLE employees (
    emp_id INT,
    name VARCHAR(100),
    salary INT,
    department VARCHAR(50)
)

-- Insert employees
INSERT INTO employees VALUES (101, 'John Doe', 50000, 'IT')
INSERT INTO employees VALUES (102, 'Jane Smith', 60000, 'HR')
INSERT INTO employees VALUES (103, 'Bob Johnson', 55000, 'IT')
INSERT INTO employees VALUES (104, 'Alice Williams', 65000, 'Finance')

-- Query IT department
SELECT * FROM employees WHERE department = 'IT'

-- Query high earners
SELECT name, salary FROM employees WHERE salary > 55000

-- Give raises
UPDATE employees SET salary = 70000 WHERE department = 'Finance'

-- Verify
SELECT * FROM employees WHERE department = 'Finance'
```

## ❗ Common Issues & Solutions

### Issue 1: "Python is not recognized"
**Solution:** 
- Reinstall Python and check "Add Python to PATH"
- OR manually add Python to PATH in System Environment Variables

### Issue 2: "tkinter not found"
**Solution:**
- tkinter comes with Python. Reinstall Python with "tcl/tk" option checked

### Issue 3: GUI doesn't open
**Solution:**
- Run from Command Prompt to see error messages:
  ```bash
  python gui.py
  ```
- Check if both `gui.py` and `sql_compiler.py` are in the same folder

### Issue 4: "Syntax Error" on valid SQL
**Solution:**
- Don't include semicolon (;) at the end - it's optional
- Check for typos in keywords (SELECT, not SELCT)
- Ensure proper spacing around operators (age > 20, not age>20)

### Issue 5: Table doesn't show data
**Solution:**
- Make sure you executed the INSERT statements successfully
- Check the output console for errors
- Use "Show Tables" button to verify table exists

## 📊 Project Structure Explanation

```
mini-sql-compiler/
│
├── sql_compiler.py          # Core compiler implementation
│   ├── TokenType           (Enum for token types)
│   ├── Token               (Token class)
│   ├── Lexer               (Lexical analyzer)
│   ├── ASTNode             (Base class for AST nodes)
│   ├── Parser              (Syntax analyzer)
│   ├── Database            (In-memory database)
│   ├── QueryExecutor       (Execution engine)
│   └── SQLCompiler         (Main compiler class)
│
├── gui.py                   # Graphical user interface
│   └── SQLCompilerGUI      (Main GUI class)
│
├── README.md               # This documentation
├── RUN_COMPILER.bat        # Windows launcher
└── USER_GUIDE.pdf          # Detailed documentation
```

## 🎓 Academic Notes

### Compiler Design Concepts Demonstrated
1. **Lexical Analysis**
   - Token recognition
   - Pattern matching
   - Character scanning

2. **Syntax Analysis**
   - Grammar rules implementation
   - Recursive descent parsing
   - AST construction

3. **Semantic Analysis**
   - Type checking
   - Table/column validation
   - Operator validation

4. **Code Generation/Execution**
   - Direct execution (interpretation)
   - Query optimization basics
   - Result generation

### Key Learning Outcomes
- Understanding compilation phases
- Token design and implementation
- Grammar rules and parsing
- Abstract syntax tree creation
- Symbol table management (table storage)
- Error handling and reporting

## 💡 Extending the Project

### Easy Extensions
1. Add more data types (BOOLEAN, TEXT)
2. Implement ORDER BY clause
3. Add aggregate functions (COUNT, SUM, AVG)
4. Support for LIMIT clause

### Moderate Extensions
1. JOIN operations
2. Subqueries
3. CREATE INDEX
4. Transaction support

### Advanced Extensions
1. Query optimization
2. Persistent storage (file-based)
3. Multi-user support
4. Network connectivity

## 🤝 Support

If you encounter any issues:
1. Check the "Common Issues" section above
2. Verify Python installation: `python --version`
3. Ensure all files are in the same directory
4. Run from command prompt to see detailed errors

## 📄 License

This project is created for academic purposes for the Compiler Design course (6th Semester).

## 👨‍💻 Author

Created as a Compiler Design Project
Subject: Compiler Design
Semester: 6th

---

**Enjoy learning compiler design! 🚀**
