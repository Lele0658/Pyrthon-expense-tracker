# Python Expense Tracker

A simple command-line Expense Tracker built with Python and MySQL that helps users record, manage, and organize their daily expenses. The application provides an easy way to store expense records in a MySQL database while demonstrating Python database connectivity and CRUD operations.

## Features

- Add new expenses
- View all recorded expenses
- Update existing expenses
- Delete expenses
- Store data in a MySQL database
- Simple command-line interface
- Secure database configuration using environment variables

## Technologies Used

- Python 3
- MySQL
- mysql-connector-python
- python-dotenv

## Project Structure

```
Python-expense-tracker/
│
├── expense_tracker_mysql.py    # Main application
├── requirements.txt            # Python dependencies
├── .gitignore                  # Ignored files
└── README.md                   # Project documentation
```

## Prerequisites

Before running the project, install:

- Python 3.10 or newer
- MySQL Server
- pip

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Lele0658/Pyrthon-expense-tracker.git
```

### 2. Navigate into the project

```bash
cd Python-expense-tracker
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a file named `.env` in the project folder and add your MySQL credentials.

Example:

```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=expense_tracker
```

### 5. Run the application

```bash
python expense_tracker_mysql.py
```

## Requirements

Install all required packages using:

```bash
pip install -r requirements.txt
```

Example requirements:

```
mysql-connector-python
python-dotenv
```

## Learning Objectives

This project demonstrates:

- Python programming fundamentals
- CRUD operations
- MySQL database integration
- Database security using environment variables
- Organizing a Python project
- Working with external packages

## Future Improvements

- User authentication
- Expense categories
- Monthly reports
- Budget tracking
- Charts and data visualization
- CSV and PDF export
- Graphical User Interface (GUI)
- Receipt attachment support

## Author

**Leoneigh**

GitHub: https://github.com/Lele0658

## License

This project is intended for educational and portfolio purposes.
