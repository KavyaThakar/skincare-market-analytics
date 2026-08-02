-- Category-level summary
SELECT Category, COUNT(*) AS product_count, ROUND(AVG(Price),2) AS avg_price,
       ROUND(AVG(Rating),2) AS avg_rating
FROM products GROUP BY Category ORDER BY product_count DESC;

-- Top 10 brands by product count
SELECT Brand, COUNT(*) AS product_count, ROUND(AVG(Rating),2) AS avg_rating
FROM products GROUP BY Brand HAVING COUNT(*) >= 10
ORDER BY product_count DESC LIMIT 10;

-- Rank brands by avg price WITHIN each category (window function)
WITH brand_cat AS (
    SELECT Category, Brand, AVG(Price) AS avg_price, COUNT(*) AS n
    FROM products GROUP BY Category, Brand HAVING COUNT(*) >= 3
)
SELECT Category, Brand, ROUND(avg_price,2) AS avg_price,
       RANK() OVER (PARTITION BY Category ORDER BY avg_price DESC) AS price_rank
FROM brand_cat ORDER BY Category, price_rank;

-- Most common ingredients
SELECT Ingredient, COUNT(*) AS product_count
FROM ingredients GROUP BY Ingredient ORDER BY product_count DESC LIMIT 20;

-- Does price tier affect rating?
SELECT Price_Tier, COUNT(*) AS product_count, ROUND(AVG(Rating),3) AS avg_rating
FROM products GROUP BY Price_Tier ORDER BY AVG(Price);

-- Top 3 highest-rated products per category (window function)
WITH ranked AS (
    SELECT Category, Brand, Name, Price, Rating,
           DENSE_RANK() OVER (PARTITION BY Category ORDER BY Rating DESC, Price ASC) AS rnk
    FROM products
)
SELECT Category, Brand, Name, Price, Rating FROM ranked WHERE rnk <= 3;