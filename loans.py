from datetime import datetime

import mysql.connector

try:
    import library_db as db
except ImportError:
    import library_db


def ask_required(prompt, max_length):
    while True:
        value = input(prompt).strip()
        if not value:
            print("Kailangan itong punan.")
        elif len(value) > max_length:
            print(f"Hindi dapat lumampas sa {max_length} characters.")
        else:
            return value


def ask_positive_int(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and int(value) >= 1:
            return int(value)
        print("Dapat numero ito na higit sa 0.")


def is_valid_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def ask_date(prompt):
    while True:
        value = input(prompt).strip()
        if not is_valid_date_format(value):
            print("Gamitin ang format na YYYY-MM-DD (halimbawa: 2026-10-27).")
            continue
        return value


def display_record(record):
    print(
        f"\nLoan No.:        {record['loan_no']}\n"
        f"Borrower Name:   {record['borrower_name']}\n"
        f"Student/ID No.:  {record['student_id']}\n"
        f"Book Title:      {record['book_title']}\n"
        f"Author:          {record['author']}\n"
        f"Copies:          {record['copies']}\n"
        f"Loan Date:       {record['loan_date']}\n"
        f"Due Date:        {record['due_date']}\n"
        f"Return Date:     {record['return_date'] if record['return_date'] else 'N/A'}\n"
        f"Status:          {record['status']}\n"
        f"Encoded By:      {record['encoded_by']}\n"
        f"Created At:      {record['created_at']}"
    )


def borrow_book():
    print("\n--- Mag-record ng bagong Book Loan ---")
    loan_no = db.get_next_loan_no()
    print(f"Loan No.: {loan_no}")

    borrower_name = ask_required("Buong pangalan ng borrower: ", 150)
    student_id = ask_required("Student/Employee ID: ", 30)
    book_title = ask_required("Pamagat ng aklat: ", 150)
    author = ask_required("May-akda: ", 100)
    copies = ask_positive_int("Bilang ng kopya: ")
    loan_date = ask_date("Petsa ng paghiram (YYYY-MM-DD): ")
    due_date = ask_date("Petsa ng kapalit/pagtatapos ng hiram (YYYY-MM-DD): ")

    try:
        l_date = datetime.strptime(loan_date, "%Y-%m-%d").date()
        d_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        if d_date < l_date:
            print("Hindi pwedeng mas maaga ang due date kaysa sa loan date.")
            return
    except ValueError:
        print("Hindi wastong petsa.")
        return

    encoded_by = ask_required("In-record ni: ", 100)

    record = {
        "loan_no": loan_no,
        "borrower_name": borrower_name,
        "student_id": student_id,
        "book_title": book_title,
        "author": author,
        "copies": copies,
        "loan_date": loan_date,
        "due_date": due_date,
        "return_date": None,
        "status": "On Loan",
        "encoded_by": encoded_by,
    }

    try:
        record_id = db.insert_loan(record)
        print(f"Matagumpay na na-hiram ang aklat! ID: {record_id}")
    except mysql.connector.IntegrityError:
        print("May record na gamit ang loan number na ito.")
    except mysql.connector.Error as error:
        print(f"Hindi na-save ang record: {error}")


def show_all_loans():
    try:
        records = db.get_all_loans()
    except mysql.connector.Error as error:
        print(f"Hindi makuha ang mga book loan records: {error}")
        return

    print("\n--- Lahat ng Book Loans ---")
    if not records:
        print("Wala pang book loans.")
        return

    for record in records:
        display_record(record)


def search_loan():
    loan_no = ask_required("Loan No. na hahanapin: ", 20)
    try:
        record = db.get_loan_by_no(loan_no)
    except mysql.connector.Error as error:
        print(f"Hindi mahanap ang record: {error}")
        return

    if record is None:
        print("Walang record na may loan number na iyan.")
        return

    display_record(record)


def return_book():
    loan_no = ask_required("Loan No. na isasauli: ", 20)
    try:
        record = db.get_loan_by_no(loan_no)
    except mysql.connector.Error as error:
        print(f"Hindi makuha ang record: {error}")
        return

    if record is None:
        print("Walang record na may loan number na iyan.")
        return

    if record["status"] == "Returned":
        print("Ang libro ay naibalik na.")
        return

    display_record(record)
    return_date = ask_date("Petsa ng aktwal na pagsasauli (YYYY-MM-DD): ")

    try:
        l_date = datetime.strptime(str(record["loan_date"]), "%Y-%m-%d").date()
        r_date = datetime.strptime(return_date, "%Y-%m-%d").date()
        if r_date < l_date:
            print("Hindi pwedeng mas maaga ang return date kaysa sa loan date.")
            return
    except ValueError:
        print("Hindi wastong petsa.")
        return

    try:
        updated = db.mark_returned(loan_no, return_date)
    except mysql.connector.Error as error:
        print(f"Hindi ma-update ang record: {error}")
        return

    if updated:
        print("Matagumpay na naibalik ang libro!")
    else:
        print("Hindi na-update ang record.")


def remove_loan():
    loan_no = ask_required("Loan No. na buburahin: ", 20)
    try:
        record = db.get_loan_by_no(loan_no)
    except mysql.connector.Error as error:
        print(f"Hindi makuha ang record: {error}")
        return

    if record is None:
        print("Walang record na may loan number na iyan.")
        return

    display_record(record)
    confirmation = input("Sigurado ka bang buburahin ang record na ito? (o/h): ").strip().lower()
    if confirmation not in {"o", "oo", "y", "yes"}:
        print("Kinansela ang pagbura.")
        return

    try:
        deleted = db.delete_loan(loan_no)
    except mysql.connector.Error as error:
        print(f"Hindi nabura ang record: {error}")
        return

    if deleted:
        print("Matagumpay na nabura ang book loan record.")
    else:
        print("Wala nang record na buburahin.")


def remove_all_loans():
    confirmation = input(
        "Sigurado ka bang buburahin ang LAHAT ng book loan records? (o/h): "
    ).strip().lower()
    if confirmation not in {"o", "oo", "y", "yes"}:
        print("Kinansela ang pagbura ng lahat ng records.")
        return

    try:
        deleted_count = db.delete_all_loans()
    except mysql.connector.Error as error:
        print(f"Hindi nabura ang lahat ng records: {error}")
        return

    if deleted_count:
        print(f"Matagumpay na nabura ang {deleted_count} book loan records.")
    else:
        print("Walang book loan records na buburahin.")
