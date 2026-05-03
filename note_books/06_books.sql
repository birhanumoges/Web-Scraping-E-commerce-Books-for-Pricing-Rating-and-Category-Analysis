-- ============================================
-- CORRECT BASIC QUERIES (USE THESE)
-- ============================================

-- 1. Use correct database name
USE books_tracker;  -- NOT book_tracker (notice the 's'!)

-- 2. See all books
SELECT * FROM books;

-- 3. Count total books
SELECT COUNT(*) as total_books FROM books;

-- 4. First 10 books
SELECT id, title, price, rating FROM books LIMIT 10;

-- 5. MAIN REQUIREMENT: Average price per rating (FIXED)
SELECT 
    rating,
    COUNT(*) as number_of_books,
    ROUND(AVG(price), 2) as average_price,
    ROUND(MIN(price), 2) as cheapest_book,
    ROUND(MAX(price), 2) as most_expensive
FROM books  -- Removed the incorrect alias
WHERE rating IS NOT NULL
GROUP BY rating
ORDER BY rating DESC;

-- 6. Your project requirement (simplified)
SELECT 
    rating, 
    COUNT(*) as book_count, 
    ROUND(AVG(price), 2) as avg_price
FROM books
WHERE rating IS NOT NULL
GROUP BY rating
ORDER BY rating DESC;