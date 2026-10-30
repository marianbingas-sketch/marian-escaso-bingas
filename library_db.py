import os

import mysql.connector
from mysql.connector import Error


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "marian")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
    )


def test_connection():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM book_loans LIMIT 1")
            cursor.fetchone()
            return True, f"Nakakonekta sa MySQL database '{DB_NAME}'."
        return False, "Hindi makakonekta sa MySQL."
    except Error as error:
        return False, str(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_next_loan_no():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT loan_no FROM book_loans ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if not result:
            return "BL-001"
        last_no = result[0]
        try:
            num = int(last_no.split("-")[1]) + 1
            return f"BL-{num:03d}"
        except (IndexError, ValueError):
            return "BL-001"
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_all_loans():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, loan_no, borrower_name, student_id, book_title, author,
                   copies, loan_date, due_date, return_date, status, encoded_by, created_at
            FROM book_loans
            ORDER BY id DESC
            """
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_loan_by_no(loan_no):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, loan_no, borrower_name, student_id, book_title, author,
                   copies, loan_date, due_date, return_date, status, encoded_by, created_at
            FROM book_loans
            WHERE loan_no = %s
            """,
            (loan_no,),
        )
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def insert_loan(record):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO book_loans
                (loan_no, borrower_name, student_id, book_title, author,
                 copies, loan_date, due_date, return_date, status, encoded_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                record["loan_no"],
                record["borrower_name"],
                record["student_id"],
                record["book_title"],
                record["author"],
                record["copies"],
                record["loan_date"],
                record["due_date"],
                record["return_date"],
                record["status"],
                record["encoded_by"],
            ),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def mark_returned(loan_no, return_date):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE book_loans
            SET return_date = %s, status = %s
            WHERE loan_no = %s AND status = %s
            """,
            (return_date, "Returned", loan_no, "On Loan"),
        )
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_loan(loan_no):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM book_loans WHERE loan_no = %s", (loan_no,))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_all_loans():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM book_loans")
        connection.commit()
        return cursor.rowcount
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
