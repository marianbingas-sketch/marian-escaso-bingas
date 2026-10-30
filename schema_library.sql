CREATE DATABASE IF NOT EXISTS marian
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE marian;

CREATE TABLE IF NOT EXISTS book_loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    loan_no VARCHAR(20) NOT NULL UNIQUE,
    borrower_name VARCHAR(150) NOT NULL,
    student_id VARCHAR(30) NOT NULL,
    book_title VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    copies INT UNSIGNED NOT NULL,
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE NULL,
    status VARCHAR(20) NOT NULL,
    encoded_by VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
