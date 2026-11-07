import pandas as pd
import matplotlib.pyplot as plt
from database import connect_db

USER_ID = 1

def income_source_analysis():
    conn = connect_db()

    if conn is None:
        return

    try:
        query = """
            SELECT
                income_source,
                SUM(amount) AS total_income
            FROM income
            WHERE user_id = %s
            GROUP BY income_source
            ORDER BY total_income DESC;
        """

        df = pd.read_sql_query(query, conn, params=(USER_ID,))

        if df.empty:
            print("\nNo income records found.")
            return

        print("\n========== INCOME SOURCE ANALYSIS ==========")
        print(df.to_string(index=False))

        plt.figure(figsize=(8, 6))

        plt.pie(
            df["total_income"],
            labels=df["income_source"],
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Income Source Analysis")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("Error generating income analysis:", e)

    finally:
        conn.close()


def income_vs_expense_analysis():
    conn = connect_db()

    if conn is None:
        return

    try:
        query = """
            SELECT
                (SELECT COALESCE(SUM(amount), 0)
                 FROM income
                 WHERE user_id = %s) AS total_income,

                (SELECT COALESCE(SUM(amount), 0)
                 FROM expenses
                 WHERE user_id = %s) AS total_expenses;
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(USER_ID, USER_ID)
        )

        total_income = float(df["total_income"][0])
        total_expenses = float(df["total_expenses"][0])

        balance = total_income - total_expenses

        print("\n========== FINANCIAL ANALYSIS ==========")
        print(f"Total Income   : ₹{total_income:.2f}")
        print(f"Total Expenses : ₹{total_expenses:.2f}")
        print(f"Remaining      : ₹{balance:.2f}")

        # Bar Chart
        categories = ["Income", "Expenses"]
        amounts = [total_income, total_expenses]

        plt.figure(figsize=(8, 6))

        plt.bar(categories, amounts)

        plt.title("Income vs Expenses Analysis")
        plt.xlabel("Category")
        plt.ylabel("Amount (₹)")

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("Error generating financial analysis:", e)

    finally:
        conn.close()