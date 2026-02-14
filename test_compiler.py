"""
Test script for Mini SQL Compiler
Run this to verify the compiler works correctly before submission
"""

from sql_compiler import SQLCompiler

def test_compiler():
    print("=" * 60)
    print("Mini SQL Compiler - Test Suite")
    print("=" * 60)
    print()
    
    compiler = SQLCompiler()
    test_passed = 0
    test_failed = 0
    
    # Test 1: CREATE TABLE
    print("Test 1: CREATE TABLE")
    result = compiler.compile_and_execute(
        "CREATE TABLE students (id INT, name VARCHAR(50), age INT, grade VARCHAR(2))"
    )
    if result['success']:
        print("✓ PASSED")
        test_passed += 1
    else:
        print(f"✗ FAILED: {result['error']}")
        test_failed += 1
    print()
    
    # Test 2: INSERT
    print("Test 2: INSERT INTO")
    result = compiler.compile_and_execute(
        "INSERT INTO students VALUES (1, 'Alice', 20, 'A')"
    )
    if result['success']:
        print("✓ PASSED")
        test_passed += 1
    else:
        print(f"✗ FAILED: {result['error']}")
        test_failed += 1
    print()
    
    # Test 3: INSERT more data
    print("Test 3: INSERT Multiple Records")
    queries = [
        "INSERT INTO students VALUES (2, 'Bob', 21, 'B')",
        "INSERT INTO students VALUES (3, 'Charlie', 19, 'A')",
        "INSERT INTO students VALUES (4, 'Diana', 22, 'C')",
    ]
    all_success = True
    for q in queries:
        result = compiler.compile_and_execute(q)
        if not result['success']:
            all_success = False
            print(f"✗ FAILED: {result['error']}")
            break
    if all_success:
        print("✓ PASSED")
        test_passed += 1
    else:
        test_failed += 1
    print()
    
    # Test 4: SELECT ALL
    print("Test 4: SELECT * FROM students")
    result = compiler.compile_and_execute("SELECT * FROM students")
    if result['success'] and result['row_count'] == 4:
        print(f"✓ PASSED - Retrieved {result['row_count']} rows")
        print("Data:")
        for row in result['data']:
            print(f"  {row}")
        test_passed += 1
    else:
        print(f"✗ FAILED: Expected 4 rows, got {result.get('row_count', 0)}")
        test_failed += 1
    print()
    
    # Test 5: SELECT with specific columns
    print("Test 5: SELECT name, grade FROM students")
    result = compiler.compile_and_execute("SELECT name, grade FROM students")
    if result['success']:
        print("✓ PASSED")
        print("Data:")
        for row in result['data']:
            print(f"  {row}")
        test_passed += 1
    else:
        print(f"✗ FAILED: {result['error']}")
        test_failed += 1
    print()
    
    # Test 6: SELECT with WHERE
    print("Test 6: SELECT * FROM students WHERE age > 20")
    result = compiler.compile_and_execute("SELECT * FROM students WHERE age > 20")
    if result['success'] and result['row_count'] == 2:  # Bob (21) and Diana (22)
        print(f"✓ PASSED - Retrieved {result['row_count']} rows")
        print("Data:")
        for row in result['data']:
            print(f"  {row}")
        test_passed += 1
    else:
        print(f"✗ FAILED: Expected 2 rows, got {result.get('row_count', 0)}")
        test_failed += 1
    print()
    
    # Test 7: SELECT with WHERE AND
    print("Test 7: SELECT * FROM students WHERE age > 19 AND grade = 'A'")
    result = compiler.compile_and_execute(
        "SELECT * FROM students WHERE age > 19 AND grade = 'A'"
    )
    if result['success'] and result['row_count'] == 1:  # Only Alice
        print(f"✓ PASSED - Retrieved {result['row_count']} rows")
        print("Data:")
        for row in result['data']:
            print(f"  {row}")
        test_passed += 1
    else:
        print(f"✗ FAILED: Expected 1 row, got {result.get('row_count', 0)}")
        test_failed += 1
    print()
    
    # Test 8: UPDATE
    print("Test 8: UPDATE students SET grade = 'A+' WHERE name = 'Alice'")
    result = compiler.compile_and_execute(
        "UPDATE students SET grade = 'A+' WHERE name = 'Alice'"
    )
    if result['success']:
        print("✓ PASSED")
        # Verify update
        verify = compiler.compile_and_execute("SELECT * FROM students WHERE name = 'Alice'")
        if verify['data'][0]['grade'] == 'A+':
            print("  Update verified: Alice now has grade A+")
        test_passed += 1
    else:
        print(f"✗ FAILED: {result['error']}")
        test_failed += 1
    print()
    
    # Test 9: DELETE
    print("Test 9: DELETE FROM students WHERE age < 20")
    result = compiler.compile_and_execute("DELETE FROM students WHERE age < 20")
    if result['success']:
        print("✓ PASSED")
        # Verify deletion
        verify = compiler.compile_and_execute("SELECT * FROM students")
        print(f"  Remaining rows: {verify['row_count']}")
        test_passed += 1
    else:
        print(f"✗ FAILED: {result['error']}")
        test_failed += 1
    print()
    
    # Test 10: DROP TABLE
    print("Test 10: DROP TABLE students")
    result = compiler.compile_and_execute("DROP TABLE students")
    if result['success']:
        print("✓ PASSED")
        test_passed += 1
    else:
        print(f"✗ FAILED: {result['error']}")
        test_failed += 1
    print()
    
    # Test 11: Error handling - query non-existent table
    print("Test 11: Error Handling - SELECT from non-existent table")
    result = compiler.compile_and_execute("SELECT * FROM nonexistent")
    if not result['success']:
        print("✓ PASSED - Error correctly detected")
        print(f"  Error message: {result['error']}")
        test_passed += 1
    else:
        print("✗ FAILED - Should have thrown an error")
        test_failed += 1
    print()
    
    # Test 12: Complex query
    print("Test 12: Complex Table with Multiple Data Types")
    result = compiler.compile_and_execute(
        "CREATE TABLE employees (emp_id INT, name VARCHAR(100), salary FLOAT, dept VARCHAR(50))"
    )
    if result['success']:
        compiler.compile_and_execute("INSERT INTO employees VALUES (101, 'John Doe', 50000.50, 'IT')")
        compiler.compile_and_execute("INSERT INTO employees VALUES (102, 'Jane Smith', 60000.75, 'HR')")
        result = compiler.compile_and_execute("SELECT * FROM employees WHERE salary > 55000")
        if result['success'] and result['row_count'] == 1:
            print("✓ PASSED")
            test_passed += 1
        else:
            print(f"✗ FAILED: Expected 1 row, got {result.get('row_count', 0)}")
            test_failed += 1
    else:
        print(f"✗ FAILED: {result['error']}")
        test_failed += 1
    print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Total Tests: {test_passed + test_failed}")
    print(f"Passed: {test_passed}")
    print(f"Failed: {test_failed}")
    
    if test_failed == 0:
        print("\n✓ ALL TESTS PASSED! Compiler is working correctly.")
    else:
        print(f"\n✗ {test_failed} test(s) failed. Please check the implementation.")
    
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_compiler()
    except Exception as e:
        print(f"\n✗ CRITICAL ERROR: {e}")
        print("Please check the compiler implementation.")
