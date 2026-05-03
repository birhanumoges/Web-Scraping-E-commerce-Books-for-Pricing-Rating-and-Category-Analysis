-- Use your database
USE book_tracker;

-- See all books inserted
SELECT * FROM books;

-- Count how many books you've scraped
SELECT COUNT(*) as total_books FROM books;

-- See the first 10 books
SELECT id, title, price, rating FROM books LIMIT 10;

-- Main requirement: Average price per rating
SELECT 
    rating,
    COUNT(*) as number_of_books,
    ROUND(AVG(price), 2) as average_price,
    ROUND(MIN(price), 2) as cheapest_book,
    ROUND(MAX(price), 2) as most_expensive
FROM books_tracker.books
WHERE rating IS NOT NULL
GROUP BY rating
ORDER BY rating DESC;