import sys
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
from dotenv import load_dotenv

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables from .env file
load_dotenv()

# --- Database Connection ---
def get_connection():
    """Return a MySQL connection or None on error."""
    try:
        # Ensure required variables are set
        password = os.getenv('DB_PASSWORD')
        if password is None:
            print("DB_PASSWORD not set in .env file.")
            return None

        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=password,
            database=os.getenv('DB_NAME', 'expense_tracker')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# --- Setup Table ---
def init_db():
    """Create the expenses table if it doesn't exist."""
    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    description TEXT
                )
            ''')
            conn.commit()
            print("MySQL Database connected and table ready!\n")
    except Error as e:
        print(f"Database initialization error: {e}")
    finally:
        conn.close()

# --- Helper Functions ---
def parse_date(date_str):
    """Validate DD/MM/YYYY and return a datetime.date object."""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        return None

def add_expense():
    conn = get_connection()
    if not conn:
        return

    date_str = input("Enter date (DD/MM/YYYY): ")
    date_obj = parse_date(date_str)
    if not date_obj:
        print("Invalid date format. Please use DD/MM/YYYY.\n")
        conn.close()
        return

    category = input("Enter category (e.g., Food, Transport): ")
    try:
        amount = float(input("Enter amount: R"))
    except ValueError:
        print("Invalid amount.\n")
        conn.close()
        return

    description = input("Enter description (optional): ")

    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO expenses (date, category, amount, description)
                VALUES (%s, %s, %s, %s)
            ''', (date_obj, category, amount, description))
            conn.commit()
            print("Expense added successfully!\n")
    except Error as e:
        print(f"Error adding expense: {e}")
    finally:
        conn.close()

def view_expenses():
    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, date, category, amount, description FROM expenses ORDER BY date')
            rows = cursor.fetchall()

            if not rows:
                print("No expenses found.\n")
                return

            print("\n" + "-" * 70)
            print(f"{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
            print("-" * 70)
            for row in rows:
                # row[1] is a date object, format it
                date_str = row[1].strftime("%d/%m/%Y")
                print(f"{row[0]:<5} {date_str:<12} {row[2]:<15} R{row[3]:<10.2f} {row[4]}")
            print("-" * 70 + "\n")
    except Error as e:
        print(f"Error retrieving expenses: {e}")
    finally:
        conn.close()

def delete_expense():
    view_expenses()  # shows list and closes its own connection

    try:
        exp_id = int(input("Enter the ID of the expense to delete: "))
    except ValueError:
        print("Invalid ID.\n")
        return

    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM expenses WHERE id = %s', (exp_id,))
            conn.commit()
            if cursor.rowcount > 0:
                print("Expense deleted!\n")
            else:
                print("ID not found.\n")
    except Error as e:
        print(f"Error deleting expense: {e}")
    finally:
        conn.close()

def show_total():
    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT SUM(amount) FROM expenses')
            total = cursor.fetchone()[0]
            total = total if total else 0.0
            print(f"\nTotal spending: R{total:.2f}\n")
    except Error as e:
        print(f"Error calculating total: {e}")
    finally:
        conn.close()

# --- Main Program ---
def main():
    init_db()
    print("\n" + "="*30)
    print(" PYTHON EXPENSE TRACKER")
    print("="*30)

    while True:
        print("\n--- MENU ---")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Delete Expense")
        print("4. Show Total Spending")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            delete_expense()
        elif choice == '4':
            show_total()
        elif choice == '5':
            print(" Goodbye!")
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()