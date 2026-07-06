import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Database Connection ---
def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD'),  
            database=os.getenv('DB_NAME', 'expense_tracker')
        )
        return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

# --- Setup Table ---
def init_db():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date VARCHAR(20) NOT NULL,
                category VARCHAR(50) NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ MySQL Database connected and table ready!\n")

# --- Helper Functions ---
def add_expense():
    conn = get_connection()
    if not conn: return
    
    date = input("Enter date (DD/MM/YYYY): ")
    category = input("Enter category (e.g., Food, Transport): ")
    try:
        amount = float(input("Enter amount: R"))
    except ValueError:
        print("Invalid amount.\n")
        conn.close()
        return
    description = input("Enter description (optional): ")
    
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, category, amount, description)
        VALUES (%s, %s, %s, %s)
    ''', (date, category, amount, description))
    conn.commit()
    print("✅ Expense added successfully!\n")
    conn.close()

def view_expenses():
    conn = get_connection()
    if not conn: return
    
    cursor = conn.cursor()
    cursor.execute('SELECT id, date, category, amount, description FROM expenses')
    rows = cursor.fetchall()
    
    if not rows:
        print("📭 No expenses found.\n")
        conn.close()
        return
    
    print("\n" + "-" * 60)
    print(f"{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<12} {row[2]:<15} R{row[3]:<10.2f} {row[4]}")
    print("-" * 60 + "\n")
    conn.close()

def delete_expense():
    view_expenses()
    try:
        exp_id = int(input("Enter the ID of the expense to delete: "))
    except ValueError:
        print("Invalid ID.\n")
        return
    
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = %s', (exp_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print("🗑️ Expense deleted!\n")
    else:
        print("❌ ID not found.\n")
    conn.close()

def show_total():
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM expenses')
    total = cursor.fetchone()[0]
    total = total if total else 0.0
    print(f"\n💰 Total spending: R{total:.2f}\n")
    conn.close()

# --- Main Program ---
def main():
    init_db()
    print("\n" + "="*30)
    print(" PYTHON EXPENSE TRACKER (MySQL)")
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
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.\n")

if __name__ == "__main__":
    main()