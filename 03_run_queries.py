import sqlite3
import pandas as pd

conn = sqlite3.connect("skincare.db")

print("\n--- Category Summary ---")
print(pd.read_sql_query("""
    SELECT Category, COUNT(*) AS product_count, ROUND(AVG(Price),2) AS avg_price,
           ROUND(AVG(Rating),2) AS avg_rating
    FROM products GROUP BY Category ORDER BY product_count DESC;
""", conn).to_string(index=False))

print("\n--- Top Brands ---")
print(pd.read_sql_query("""
    SELECT Brand, COUNT(*) AS product_count, ROUND(AVG(Rating),2) AS avg_rating
    FROM products GROUP BY Brand HAVING COUNT(*) >= 10
    ORDER BY product_count DESC LIMIT 10;
""", conn).to_string(index=False))

print("\n--- Price Tier vs Rating ---")
print(pd.read_sql_query("""
    SELECT Price_Tier, COUNT(*) AS product_count, ROUND(AVG(Rating),3) AS avg_rating
    FROM products GROUP BY Price_Tier ORDER BY AVG(Price);
""", conn).to_string(index=False))

print("\n--- Top Ingredients ---")
print(pd.read_sql_query("""
    SELECT Ingredient, COUNT(*) AS product_count
    FROM ingredients GROUP BY Ingredient ORDER BY product_count DESC LIMIT 15;
""", conn).to_string(index=False))

conn.close()