from database import connect_db


# Replace 1 with your actual PostgreSQL user_id.
USER_ID = 1


def borrow_tracker():

    while True:

        print("\n===== BORROW TRACKER =====")
        print("1. Add Borrow/Lend Record")
        print("2. View Borrow/Lend Records")
        print("3. Update Payment Status")
        print("4. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_borrow_record()

        elif choice == "2":
            view_borrow_records()

        elif choice == "3":
            update_borrow_status()

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please try again.")


def add_borrow_record():

    print("\n===== ADD BORROW/LEND RECORD =====")

    person_name = input("Enter person's name: ").strip()

    if not person_name:
        print("Person's name cannot be empty.")
        return

    print("\n1. Borrowed (You received money)")
    print("2. Lent (You gave money)")

    choice = input("Enter record type: ")

    if choice == "1":
        record_type = "BORROWED"

    elif choice == "2":
        record_type = "LENT"

    else:
        print("Invalid record type.")
        return

    while True:

        try:
            amount = float(input("Enter amount: ₹"))

            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                break

        except ValueError:
            print("Please enter a valid amount.")

    description = input("Enter description (optional): ").strip()

    conn = connect_db()

    if conn is None:
        return

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO borrow_records
                    (user_id, person_name, amount, record_type,
                     status, description)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING record_id;
                """,
                (
                    USER_ID,
                    person_name,
                    amount,
                    record_type,
                    "Unpaid",
                    description or None
                )
            )

            record_id = cur.fetchone()[0]

        conn.commit()

        print("\nRecord added successfully!")
        print("Record ID:", record_id)

    except Exception as e:

        conn.rollback()
        print("Error adding record:", e)

    finally:
        conn.close()


def view_borrow_records():

    conn = connect_db()

    if conn is None:
        return

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT record_id, person_name, amount,
                       record_type, status, transaction_date,
                       due_date, description
                FROM borrow_records
                WHERE user_id = %s
                ORDER BY record_id DESC;
                """,
                (USER_ID,)
            )

            records = cur.fetchall()

        if not records:
            print("\nNo borrow/lend records found.")
            return

        print("\n========== BORROW/LEND RECORDS ==========")

        for record in records:

            print(f"\nRecord ID : {record[0]}")
            print(f"Person    : {record[1]}")
            print(f"Amount    : ₹{record[2]}")
            print(f"Type      : {record[3]}")
            print(f"Status    : {record[4]}")
            print(f"Date      : {record[5]}")
            print(f"Due Date  : {record[6]}")
            print(f"Description: {record[7]}")

    except Exception as e:
        print("Error retrieving records:", e)

    finally:
        conn.close()


def update_borrow_status():

    view_borrow_records()

    try:
        record_id = int(input("\nEnter record ID to update: "))

    except ValueError:
        print("Please enter a valid record ID.")
        return

    print("\n1. Unpaid")
    print("2. Partially Paid")
    print("3. Paid")

    choice = input("Select new status: ")

    statuses = {
        "1": "Unpaid",
        "2": "Partially Paid",
        "3": "Paid"
    }

    if choice not in statuses:
        print("Invalid status.")
        return

    new_status = statuses[choice]

    conn = connect_db()

    if conn is None:
        return

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                UPDATE borrow_records
                SET status = %s
                WHERE record_id = %s
                  AND user_id = %s
                RETURNING record_id;
                """,
                (new_status, record_id, USER_ID)
            )

            updated = cur.fetchone()

        conn.commit()

        if updated:
            print("\nPayment status updated successfully!")
        else:
            print("\nRecord not found.")

    except Exception as e:

        conn.rollback()
        print("Error updating status:", e)

    finally:
        conn.close()