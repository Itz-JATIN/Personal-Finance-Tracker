from database import connect_db
from datetime import datetime

USER_ID = 1


def budget_tracker():
    while True:
        print("\n===================================")
        print("          BUDGET TRACKER")
        print("===================================")
        print("1. Add Budget")
        print("2. View Budgets")
        print("3. Update Budget")
        print("4. Delete Budget")
        print("5. Check Budget Status")
        print("6. Back to Main Menu")
        print("===================================")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_budget()

        elif choice == "2":
            view_budgets()

        elif choice == "3":
            update_budget()

        elif choice == "4":
            delete_budget()

        elif choice == "5":
            check_budget_status()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")


def get_date_input(message):
    while True:
        date_value = input(message).strip()

        try:
            return datetime.strptime(date_value, "%Y-%m-%d").date()

        except ValueError:
            print("Invalid date! Use YYYY-MM-DD format.")


def get_positive_amount(message):
    while True:
        try:
            amount = float(input(message))

            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                return amount

        except ValueError:
            print("Please enter a valid amount.")


def add_budget():
    print("\n========== ADD BUDGET ==========")

    category = input("Enter budget category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    budget_amount = get_positive_amount("Enter budget amount: ₹")

    start_date = get_date_input("Enter start date (YYYY-MM-DD): ")
    end_date = get_date_input("Enter end date (YYYY-MM-DD): ")

    if end_date < start_date:
        print("End date cannot be before start date.")
        return

    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO budgets
                (user_id, category, budget_amount, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING budget_id;
            """, (
                USER_ID,
                category,
                budget_amount,
                start_date,
                end_date
            ))

            budget_id = cur.fetchone()[0]

        conn.commit()

        print("\nBudget added successfully!")
        print("Budget ID:", budget_id)

    except Exception as e:
        conn.rollback()
        print("Error adding budget:", e)

    finally:
        conn.close()


def view_budgets():
    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT budget_id, category, budget_amount,
                       start_date, end_date
                FROM budgets
                WHERE user_id = %s
                ORDER BY start_date DESC;
            """, (USER_ID,))

            records = cur.fetchall()

        if not records:
            print("\nNo budgets found.")
            return

        print("\n========== YOUR BUDGETS ==========")

        for record in records:
            print(f"\nBudget ID : {record[0]}")
            print(f"Category  : {record[1]}")
            print(f"Amount    : ₹{record[2]:,.2f}")
            print(f"Start Date: {record[3]}")
            print(f"End Date  : {record[4]}")

    except Exception as e:
        print("Error retrieving budgets:", e)

    finally:
        conn.close()


def update_budget():
    print("\n========== UPDATE BUDGET ==========")

    try:
        budget_id = int(input("Enter Budget ID: "))

        if budget_id <= 0:
            print("Budget ID must be positive.")
            return

    except ValueError:
        print("Please enter a valid Budget ID.")
        return

    new_amount = get_positive_amount("Enter new budget amount: ₹")

    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE budgets
                SET budget_amount = %s
                WHERE budget_id = %s AND user_id = %s
                RETURNING budget_id;
            """, (new_amount, budget_id, USER_ID))

            updated = cur.fetchone()

        conn.commit()

        if updated:
            print("\nBudget updated successfully!")
        else:
            print("\nBudget not found.")

    except Exception as e:
        conn.rollback()
        print("Error updating budget:", e)

    finally:
        conn.close()


def delete_budget():
    print("\n========== DELETE BUDGET ==========")

    try:
        budget_id = int(input("Enter Budget ID: "))

        if budget_id <= 0:
            print("Budget ID must be positive.")
            return

    except ValueError:
        print("Please enter a valid Budget ID.")
        return

    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM budgets
                WHERE budget_id = %s AND user_id = %s
                RETURNING budget_id;
            """, (budget_id, USER_ID))

            deleted = cur.fetchone()

        conn.commit()

        if deleted:
            print("\nBudget deleted successfully!")
        else:
            print("\nBudget not found.")

    except Exception as e:
        conn.rollback()
        print("Error deleting budget:", e)

    finally:
        conn.close()


def check_budget_status():
    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    b.budget_id,
                    b.category,
                    b.budget_amount,
                    b.start_date,
                    b.end_date,
                    COALESCE(SUM(e.amount), 0) AS total_spent
                FROM budgets b
                LEFT JOIN expenses e
                    ON LOWER(TRIM(e.expense_type)) =
                       LOWER(TRIM(b.category))
                    AND e.user_id = b.user_id
                    AND e.expense_date BETWEEN
                        b.start_date AND b.end_date
                WHERE b.user_id = %s
                GROUP BY
                    b.budget_id,
                    b.category,
                    b.budget_amount,
                    b.start_date,
                    b.end_date
                ORDER BY b.start_date DESC;
            """, (USER_ID,))

            records = cur.fetchall()

        if not records:
            print("\nNo budgets available.")
            return

        print("\n========== BUDGET STATUS ==========")

        for record in records:
            budget_id, category, budget, start, end, spent = record

            remaining = budget - spent
            usage = (spent / budget) * 100

            print(f"\nBudget ID : {budget_id}")
            print(f"Category  : {category}")
            print(f"Budget    : ₹{budget:,.2f}")
            print(f"Spent     : ₹{spent:,.2f}")
            print(f"Remaining : ₹{remaining:,.2f}")
            print(f"Usage     : {usage:.2f}%")

            if usage >= 100:
                print("ALERT: Budget exceeded!")

            elif usage >= 90:
                print("WARNING: You have used 90% or more of your budget!")

            else:
                print("Status: Budget is under control.")

            print("-----------------------------------")

    except Exception as e:
        print("Error checking budget status:", e)

    finally:
        conn.close()