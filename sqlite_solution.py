"""
SQL Tasks Solution - Part 2
Author: [Your Name]
Date: 2025-06-12
Implements:
1. Second highest salary query
2. Department salary analysis
3. Sales running totals
4. Duplicate transaction detection
"""
import sqlite3
from datetime import date

def create_connection():
    """Create SQLite database connection"""
    conn = None
    try:
        conn = sqlite3.connect('company.db')
        print("SQLite connection established")
        return conn
    except sqlite3.Error as e:
        print(f"SQLite connection error: {e}")
    return conn

def setup_database(conn):
    """Create tables and insert data"""
    try:
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY,
            emp_name TEXT,
            department TEXT,
            job_name TEXT,
            manager_id INTEGER,
            hire_date TEXT,
            salary REAL,
            commission REAL
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            amount REAL NOT NULL
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            col1 TEXT NOT NULL,
            col2 TEXT NOT NULL,
            transaction_date TEXT,
            amount REAL
        )""")
        
        # Insert sample data
        employees_data = [
            (1, 'Faizan', 'IT', 'Developer', None, '2020-01-15', 85000, None),
            (2, 'Zain', 'IT', 'Senior Dev', 1, '2018-05-10', 95000, None),
            (3, 'Hyder Johnson', 'Sales', 'Manager', None, '2019-03-22', 75000, 15000)
        ]
        
        sales_data = [
            (1, '2023-01-05', 1500.00),
            (2, '2023-01-10', 2300.00),
            (3, '2023-01-15', 1800.00)
        ]
        
        transactions_data = [
            ('A100', 'B200', '2023-01-01', 100.00),
            ('A101', 'B201', '2023-01-02', 200.00),
            ('A100', 'B200', '2023-01-03', 150.00)
        ]
        
        cursor.executemany("INSERT INTO employees VALUES (?,?,?,?,?,?,?,?)", employees_data)
        cursor.executemany("INSERT INTO sales VALUES (?,?,?)", sales_data)
        cursor.executemany("INSERT INTO transactions (col1, col2, transaction_date, amount) VALUES (?,?,?,?)", transactions_data)
        
        conn.commit()
        print("Database setup complete")
        
    except sqlite3.Error as e:
        print(f"Database setup error: {e}")
        # In execute_queries() function:
print("## SQL Query Results\n")
print("### 1. Second Highest Salary")
print(f"`{result['emp_name']}`: ${result['salary']:,.2f}\n")

print("### 2. Above-Average Earners")
print("| Employee | Department | Salary |")
print("|----------|------------|--------|")
for row in cursor.fetchall():
    print(f"| {row['emp_name']} | {row['department']} | ${row['salary']:,.2f} |")
    # Add to sql_queries.py
assert len(employees) == 8, "Employee count mismatch"
assert total_sales == 5600.0, "Sales total incorrect"

def run_queries(conn):
    """Execute all required queries"""
    try:
        cursor = conn.cursor()
        
        print("\n=== Query Results ===")
        
        # 1. Second highest salary
        cursor.execute("SELECT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1")
        print("\n1. Second highest salary:", cursor.fetchone()[0])
        
        # 2. Employees earning above department average
        print("\n2. Above average earners:")
        cursor.execute("""
        SELECT e.emp_name, e.department, e.salary, d.avg_salary
        FROM employees e
        JOIN (
            SELECT department, AVG(salary) as avg_salary 
            FROM employees 
            GROUP BY department
        ) d ON e.department = d.department
        WHERE e.salary > d.avg_salary
        """)
        for row in cursor.fetchall():
            print(f"{row[0]} ({row[1]}): ${row[2]:.2f} (Avg: ${row[3]:.2f})")
        
        # 3. Sales running total (SQLite 3.25+ required for window functions)
        print("\n3. Sales running total:")
        cursor.execute("""
        SELECT date, amount, 
               SUM(amount) OVER (ORDER BY date) AS running_total
        FROM sales
        ORDER BY date
        """)
        for row in cursor.fetchall():
            print(f"{row[0]}: ${row[1]:.2f} (Total: ${row[2]:.2f})")
        
        # 4. Duplicate transactions
        print("\n4. Duplicate transactions:")
        cursor.execute("""
        SELECT col1, col2, COUNT(*) as count
        FROM transactions
        GROUP BY col1, col2
        HAVING COUNT(*) > 1
        """)
        for row in cursor.fetchall():
            print(f"{row[0]}-{row[1]}: {row[2]} duplicates")
            
    except sqlite3.Error as e:
        print(f"Query error: {e}")

def main():
    conn = create_connection()
    if conn:
        setup_database(conn)
        run_queries(conn)
        conn.close()

if __name__ == "__main__":
    main()