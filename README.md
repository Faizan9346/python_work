# SQL Task Implementation

## Results Summary
![Query Results](Screenshot_2025-06-12_174900.png)

## Key Features
```sql
-- 1. Second highest salary
SELECT emp_name, salary FROM employees 
ORDER BY salary DESC LIMIT 1 OFFSET 1;

-- 2. Department salary analysis
SELECT emp_name, department, salary
FROM employees WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.department = employees.department);
```

## How to Reproduce
1. Run:
   ```bash
   python sql_queries.py
   ```
