USE books_tracker;

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    price FLOAT,
    rating INT
);