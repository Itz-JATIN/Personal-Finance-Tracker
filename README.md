# Personal Finance Tracker

A Python-based Personal Finance Tracker that helps users manage their income, expenses, budgets and borrow/lend records using PostgreSQL.

The application provides a command-line interface (CLI) and financial analytics to help users understand and manage their finances.

## Features

### 1. Expense Tracker
- Add new expenses.
- View existing expenses.
- Update expense records.
- Delete expenses.
- Calculate total expenses.

### 2. Borrow / Lend Tracker
- Record borrowed and lent money.
- View borrow/lend records.
- Update payment status.
- Track unpaid and paid amounts.

### 3. Income Tracker
- Add income records.
- View income history.
- Delete income records.
- Calculate total income.

### 4. Financial Summary
- Calculate total income.
- Calculate total expenses.
- Display remaining balance.

### 5. Budget Management
- Create budgets for different categories.
- View, update and delete budgets.
- Monitor budget usage.
- Receive alerts when 90% of the budget is used.

### 6. Financial Analytics
- Category-wise expense analysis.
- Income source analysis.
- Income vs expenses comparison.
- Graphical representation using Matplotlib.

## Technologies Used

- **Programming Language:** Python
- **Database:** PostgreSQL
- **Database Connector:** Psycopg
- **Data Analysis:** Pandas
- **Data Visualization:** Matplotlib
- **Environment Variables:** Python-dotenv
- **Interface:** Command Line Interface (CLI)

## Project Structure

```text
FinanceTracker/
│
├── main.py
├── database.py
│
├── Expense_tracker.py
├── Borrow_tracker.py
├── Income_tracker.py
├── Financial_summary.py
├── Budget_tracker.py
├── Financial_analytics.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd FinanceTracker
```

### 3. Create a virtual environment

```bash
python3 -m venv venv
```

### 4. Activate the virtual environment

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure PostgreSQL

Create a PostgreSQL database named `finance_tracker` and configure your database credentials in a `.env` file.

Example `.env` structure:

```env
DB_NAME=finance_tracker
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

Create the required database tables using the project's PostgreSQL schema.

### 7. Run the application

```bash
python3 main.py
```

## Future Scope

The current project focuses on a Python CLI and PostgreSQL backend. Future improvements could include:

- FastAPI-based REST API.
- Web-based frontend.
- User authentication and authorization.
- Cloud deployment.

## Author

**Jatin Kumar**

BTech Computer Science Engineering Student

GitHub: [Itz-JATIN](https://github.com/Itz-JATIN)