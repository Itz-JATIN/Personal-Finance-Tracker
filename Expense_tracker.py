from database import connect_db


# Replace 1 with the actual user_id from your database.
USER_ID = 1


def add_expense():
    while True:
        print("\n===== ADD NEW EXPENSE =====")

        expense_type = input("Enter expense type: ").strip()
        description = input("Enter description: ").strip()
        payment_method = input("Method of payment: ").strip()

        while True:
            try:
                amount = float(input("Enter amount: ₹"))

                if amount <= 0:
                    print("Amount must be greater than 0.")
                else:
                    break

            except ValueError:
                print("Please enter a valid amount.")

        conn = connect_db()

        if conn is None:
            return

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO expenses
                        (user_id, expense_type, description,
                         amount, payment_method)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING expense_id;
                    """,
                    (
                        USER_ID,
                        expense_type,
                        description,
                        amount,
                        payment_method
                    )
                )

                expense_id = cur.fetchone()[0]

            conn.commit()
            print(f"\nExpense added successfully! ID: {expense_id}")

        except Exception as e:
            conn.rollback()
            print("Error adding expense:", e)

        finally:
            conn.close()

        choice = input("\nAdd another expense? (y/n): ").lower()

        if choice != "y":
            break


def get_expenses():
    conn = connect_db()

    if conn is None:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT expense_id, expense_type, description,
                       amount, payment_method, expense_date
                FROM expenses
                WHERE user_id = %s
                ORDER BY expense_id;
                """,
                (USER_ID,)
            )

            return cur.fetchall()

    except Exception as e:
        print("Error retrieving expenses:", e)
        return None

    finally:
        conn.close()


def view_expenses():
    expenses = get_expenses()

    if expenses is None:
        return

    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n========== EXPENSES ==========")

    for expense in expenses:
        print(f"\nExpense ID : {expense[0]}")
        print(f"Type       : {expense[1]}")
        print(f"Description: {expense[2]}")
        print(f"Amount     : ₹{expense[3]}")
        print(f"Payment    : {expense[4]}")
        print(f"Date       : {expense[5]}")


def create_expense():
    print("\n===== CREATE EXPENSE =====")

    expense_type = input("Enter expense type: ").strip()
    description = input("Enter description: ").strip()
    payment_method = input("Method of payment: ").strip()

    while True:
        try:
            amount = float(input("Enter amount: ₹"))

            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                break

        except ValueError:
            print("Enter a valid amount.")

    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO expenses
                    (user_id, expense_type, description,
                     amount, payment_method)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING expense_id;
                """,
                (
                    USER_ID,
                    expense_type,
                    description,
                    amount,
                    payment_method
                )
            )

            expense_id = cur.fetchone()[0]

        conn.commit()
        print(f"\nExpense created successfully! ID: {expense_id}")

    except Exception as e:
        conn.rollback()
        print("Error creating expense:", e)

    finally:
        conn.close()


def update_expense():
    view_expenses()

    try:
        expense_id = int(input("\nEnter expense ID to update: "))
    except ValueError:
        print("Enter a valid expense ID.")
        return

    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT expense_type, description,
                       amount, payment_method
                FROM expenses
                WHERE expense_id = %s AND user_id = %s;
                """,
                (expense_id, USER_ID)
            )

            expense = cur.fetchone()

            if expense is None:
                print("Expense not found.")
                return

            print("\n===== UPDATE EXPENSE =====")

            expense_type = input(
                f"Enter new type [{expense[0]}]: "
            ).strip() or expense[0]

            description = input(
                f"Enter new description [{expense[1] or ''}]: "
            ).strip() or expense[1]

            payment_method = input(
                f"Enter new payment method [{expense[3] or ''}]: "
            ).strip() or expense[3]

            while True:
                try:
                    amount = input(
                        f"Enter new amount [{expense[2]}]: ₹"
                    ).strip()

                    amount = float(amount) if amount else expense[2]

                    if amount <= 0:
                        print("Amount must be greater than 0.")
                    else:
                        break

                except ValueError:
                    print("Enter a valid amount.")

            cur.execute(
                """
                UPDATE expenses
                SET expense_type = %s,
                    description = %s,
                    amount = %s,
                    payment_method = %s
                WHERE expense_id = %s AND user_id = %s;
                """,
                (
                    expense_type,
                    description,
                    amount,
                    payment_method,
                    expense_id,
                    USER_ID
                )
            )

        conn.commit()
        print("\nExpense updated successfully!")

    except Exception as e:
        conn.rollback()
        print("Error updating expense:", e)

    finally:
        conn.close()


def delete_expense():
    view_expenses()

    try:
        expense_id = int(input("\nEnter expense ID to delete: "))
    except ValueError:
        print("Enter a valid expense ID.")
        return

    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM expenses
                WHERE expense_id = %s AND user_id = %s
                RETURNING expense_id;
                """,
                (expense_id, USER_ID)
            )

            deleted = cur.fetchone()

        conn.commit()

        if deleted:
            print("\nExpense deleted successfully!")
        else:
            print("\nExpense not found.")

    except Exception as e:
        conn.rollback()
        print("Error deleting expense:", e)

    finally:
        conn.close()


def calculate_total_expenses():
    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COALESCE(SUM(amount), 0)
                FROM expenses
                WHERE user_id = %s;
                """,
                (USER_ID,)
            )

            total = cur.fetchone()[0]

        print(f"\nTotal Expense: ₹{total}")

    except Exception as e:
        print("Error calculating total:", e)

    finally:
        conn.close()


def load_existing_expense():
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Create Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Show Total Expense")
        print("6. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            update_expense()

        elif choice == "4":
            delete_expense()

        elif choice == "5":
            calculate_total_expenses()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")