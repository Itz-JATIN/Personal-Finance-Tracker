import Expense_tracker
import Borrow_tracker
import Income_tracker
import Financial_summary
import Budget_tracker
import Financial_analytics


def financial_analytics_menu():

    while True:
        print("\n========== FINANCIAL ANALYTICS ==========")
        print("1. Income Source Analysis")
        print("2. Income vs Expenses Analysis")
        print("3. BAck to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            Financial_analytics.income_source_analysis()

        elif choice == "2":
            Financial_analytics.income_vs_expense_analysis()

        elif choice == "3":
            break

        else:
            print("\nInvalid choice! Please try again.")


def main():

    while True:
        print("\n========== PERSONAL FINANCE TRACKER ==========")
        print("1. Expense Tracker")
        print("2. Borrow / Lend Tracker")
        print("3. Income Tracker")
        print("4. Financial Summary")
        print("5. Budget Tracker")
        print("6. Financial Analytics")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            Expense_tracker.load_existing_expense()

        elif choice == "2":
            Borrow_tracker.borrow_tracker()

        elif choice == "3":
            Income_tracker.income_tracker()

        elif choice == "4":
            Financial_summary.financial_summary()

        elif choice == "5":
            Budget_tracker.budget_tracker()

        elif choice == "6":
            financial_analytics_menu()

        elif choice == "7":
            print("\nThank you for using Personal Finance Tracker!")
            break

        else:
            print("\nInvalid choice! Please try again.")


if __name__ == "__main__":
    main()