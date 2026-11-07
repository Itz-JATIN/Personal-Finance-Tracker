from database import connect_db

USER_ID = 1


def financial_summary():
    conn = connect_db()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:

            # Calculate total income
            cur.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM income
                WHERE user_id = %s;
            """, (USER_ID,))

            total_income = cur.fetchone()[0]

            # Calculate total expenses
            cur.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM expenses
                WHERE user_id = %s;
            """, (USER_ID,))

            total_expenses = cur.fetchone()[0]

        # Calculate remaining balance
        remaining_balance = total_income - total_expenses

        # Display financial summary
        print("\n========================================")
        print("          FINANCIAL SUMMARY")
        print("========================================")

        print(f"Total Income       : ₹{total_income:,.2f}")
        print(f"Total Expenses     : ₹{total_expenses:,.2f}")

        print("----------------------------------------")

        print(f"Remaining Balance  : ₹{remaining_balance:,.2f}")

        print("========================================")

        if remaining_balance > 0:
            print("Financial Status: Positive Balance")
        elif remaining_balance < 0:
            print("Financial Status: Expenses Exceed Income")
        else:
            print("Financial Status: Break-even")

        print("========================================")

    except Exception as e:
        print("Error generating financial summary:", e)

    finally:
        conn.close()