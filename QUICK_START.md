# 🚀 QUICK START GUIDE - Mini SQL Compiler

## Installation (3 Steps)
1. Extract the ZIP file
2. Double-click `RUN_COMPILER.bat`
3. Start coding!

---

## First Query (Copy & Paste These)

### Create a Table
```sql
CREATE TABLE students (id INT, name VARCHAR(50), age INT, grade VARCHAR(2))
```

### Add Data
```sql
INSERT INTO students VALUES (1, 'Alice', 20, 'A')
INSERT INTO students VALUES (2, 'Bob', 21, 'B')
INSERT INTO students VALUES (3, 'Charlie', 19, 'A')
```

### View Data
```sql
SELECT * FROM students
```

### Filter Data
```sql
SELECT * FROM students WHERE age > 19
```

### Update Data
```sql
UPDATE students SET grade = 'A+' WHERE name = 'Alice'
```

### Delete Data
```sql
DELETE FROM students WHERE age < 20
```

---

## SQL Syntax Quick Reference

| Command | Example |
|---------|---------|
| CREATE  | `CREATE TABLE users (id INT, name VARCHAR(100))` |
| INSERT  | `INSERT INTO users VALUES (1, 'John')` |
| SELECT  | `SELECT * FROM users` |
| SELECT WHERE | `SELECT name FROM users WHERE id > 5` |
| UPDATE  | `UPDATE users SET name = 'Jane' WHERE id = 1` |
| DELETE  | `DELETE FROM users WHERE id = 1` |
| DROP    | `DROP TABLE users` |

---

## Operators

### Comparison
- `=` Equal to
- `!=` Not equal to
- `<` Less than
- `>` Greater than
- `<=` Less than or equal
- `>=` Greater than or equal

### Logical
- `AND` Both conditions must be true
- `OR` Either condition can be true

**Example**: `SELECT * FROM students WHERE age > 18 AND grade = 'A'`

---

## Data Types
- `INT` - Integers (1, 2, 100)
- `VARCHAR(n)` - Text up to n characters
- `FLOAT` - Decimals (3.14, 99.99)
- `DATE` - Dates ('2024-01-15')

---

## Buttons
- ▶ **Execute Query** - Run your SQL query
- 🗑 **Clear** - Clear the editor
- 📊 **Show Tables** - View all database tables

---

## Complete Example Workflow

```sql
-- 1. Create table
CREATE TABLE products (id INT, name VARCHAR(100), price FLOAT, stock INT)

-- 2. Add products
INSERT INTO products VALUES (1, 'Laptop', 999.99, 50)
INSERT INTO products VALUES (2, 'Mouse', 29.99, 200)
INSERT INTO products VALUES (3, 'Keyboard', 79.99, 150)

-- 3. View all
SELECT * FROM products

-- 4. Find expensive items
SELECT name, price FROM products WHERE price > 50

-- 5. Update price
UPDATE products SET price = 899.99 WHERE id = 1

-- 6. Check low stock
SELECT * FROM products WHERE stock < 100

-- 7. Remove item
DELETE FROM products WHERE id = 2

-- 8. Final check
SELECT * FROM products
```

---

## Troubleshooting

**Problem**: Can't open the program
**Solution**: Install Python from python.org (check "Add to PATH")

**Problem**: Syntax Error
**Solution**: Check spelling of keywords (SELECT not SELCT)

**Problem**: Table doesn't exist
**Solution**: Create the table first with CREATE TABLE

**Problem**: GUI looks broken
**Solution**: Make sure you're using Windows and have tkinter installed

---

## Tips
✅ Use sample queries to learn
✅ Start simple, then add complexity
✅ Check Output Console for errors
✅ Use "Show Tables" to see what tables exist
✅ Don't include semicolon at end (optional)

---

## Need Help?
- Read README.md for detailed instructions
- Read USER_GUIDE.txt for complete manual
- Run test_compiler.py to verify installation

---

**Have fun learning compiler design! 🎓**
