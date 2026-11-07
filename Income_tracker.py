from database import connect_db

# Replace 1 with your actual user_id from the users table.
USER_ID = 1


def income_tracker():
    while True:
        print("\n===================================")
        print("          INCOME TRACKER")
        print("===================================")
        print("1. Add Income")
        print("2. View Income Records")
        print("3. Calculate Total Income")
        print("4. Delete Income Record")
        print("5. Back to Main Menu")
        print("===================================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_income()

        elif choice == "2":
            view_income()

        elif choice == "3":
            calculate_total_income()

        elif choice == "4":
            delete_income()

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")


def add_income():
    print("\n========== ADD INCOME ==========")

    income_source = input(
        "Enter income source (Salary, Freelancing, Pocket Money, etc.): "
    ).strip()

    if not income_source:
        print("Income source cannot be empty.")
        return

    description = input("Enter description (optional): ").strip()

    while True:
        try:
            amount = float(input("Enter income amount: ₹"))

            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                break

        except ValueError:
            print("Please enter a valid numeric amount.")

    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO income
                    (user_id, income_source, description, amount)
                VALUES (%s, %s, %s, %s)
                RETURNING income_id;
                """,
                (
                    USER_ID,
                    income_source,
                    description or None,
                    amount
                )
            )

            income_id = cur.fetchone()[0]

        conn.commit()

        print("\nIncome added successfully!")
        print("Income ID:", income_id)

    except Exception as e:
        conn.rollback()
        print("Error adding income:", e)

    finally:
        conn.close()


def view_income():
    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT income_id, income_source, description,
                amount, income_date
                FROM income
                WHERE user_id = %s
                ORDER BY income_date DESC, income_id DESC;
                """,
                (USER_ID,)
            )

            records = cur.fetchall()

        if not records:
            print("\nNo income records found.")
            return

        print("\n========== INCOME RECORDS ==========")

        for record in records:
            print(f"\nIncome ID  : {record[0]}")
            print(f"Source     : {record[1]}")
            print(f"Description: {record[2] or '-'}")
            print(f"Amount     : ₹{record[3]:,.2f}")
            print(f"Date       : {record[4]}")

    except Exception as e:
        print("Error retrieving income:", e)

    finally:
        conn.close()


def calculate_total_income():
    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COALESCE(SUM(amount), 0)
                FROM income
                WHERE user_id = %s;
                """,
                (USER_ID,)
            )

            total = cur.fetchone()[0]

        print(f"\nTotal Income: ₹{total:,.2f}")

    except Exception as e:
        print("Error calculating total income:", e)

    finally:
        conn.close()


def delete_income():
    print("\n========== DELETE INCOME ==========")

    try:
        income_id = int(input("Enter the Income ID to delete: "))

        if income_id <= 0:
            print("Income ID must be positive.")
            return

    except ValueError:
        print("Please enter a valid Income ID.")
        return

    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM income
                WHERE income_id = %s
                  AND user_id = %s
                RETURNING income_id;
                """,
                (income_id, USER_ID)
            )

            deleted = cur.fetchone()

        conn.commit()

        if deleted:
            print("\nIncome record deleted successfully!")
        else:
            print("\nIncome record not found.")

    except Exception as e:
        conn.rollback()
        print("Error deleting income:", e)

    finally:
        conn.close()
