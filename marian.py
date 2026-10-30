try:
    import library_db as db
except ImportError:
    import loans


import loans


def main():
    connected, message = db.test_connection()
    if not connected:
        print(f"Hindi makakonekta sa XAMPP MySQL: {message}")
        print("Siguruhin na naka-start ang MySQL at na-import ang schema_library.sql.")
        return
    print(message)

    print("\n=== LIBRARY BOOK BORROWING SYSTEM ===")
    while True:
        print("\n[1] Mag-record ng bagong Book Loan")
        print("[2] Tingnan ang Lahat ng Book Loans")
        print("[3] Hanapin ang Book Loan (by Loan No.)")
        print("[4] I-mark bilang Returned")
        print("[5] Burahin ang Book Loan Record")
        print("[6] Burahin ang Lahat ng Book Loan Records")
        print("[0] Lumabas")
        choice = input("Piliin: ").strip()

        if choice == "1":
            loans.borrow_book()
        elif choice == "2":
            loans.show_all_loans()
        elif choice == "3":
            loans.search_loan()
        elif choice == "4":
            loans.return_book()
        elif choice == "5":
            loans.remove_loan()
        elif choice == "6":
            loans.remove_all_loans()
        elif choice == "0":
            print("Salamat! Paalam.")
            break
        else:
            print("Hindi wastong pagpili. Pumili ng 1, 2, 3, 4, 5, 6, o 0.")


if __name__ == "__main__":
    main()
