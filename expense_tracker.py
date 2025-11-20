import csv
from pathlib import Path
from datetime import datetime


# Define a class named ExpenseTracker to manage expenses
class ExpenseTracker:
    # Initialize the ExpenseTracker with an empty list to store expenses
    # and a CSV file to save/load data
    def __init__(self, filename="expenses.csv"):
        self.expenses = []
        self.file_path = Path(filename)
        self.load_expenses_from_file()

    # Load existing expenses from CSV file, if it exists
    def load_expenses_from_file(self):
        if not self.file_path.exists():
            return  # no file yet, start empty

        with self.file_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    amount = float(row["amount"])
                except (ValueError, KeyError):
                    continue
                self.expenses.append({
                    "date": row.get("date", ""),
                    "category": row.get("category", ""),
                    "description": row.get("description", ""),
                    "amount": amount
                })

    # Save all expenses to CSV file
    def save_expenses_to_file(self):
        with self.file_path.open("w", newline="", encoding="utf-8") as f:
            fieldnames = ["date", "category", "description", "amount"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for exp in self.expenses:
                writer.writerow({
                    "date": exp["date"],
                    "category": exp["category"],
                    "description": exp["description"],
                    "amount": f"{exp['amount']:.2f}"
                })

    # Method to add a new expense to the list
   # Method to add a new expense to the list
    def add_expense(self, date, category, description, amount):
        expense = {
            'date': date,
            'category': category,
            'description': description,
            'amount': amount
        }
        self.expenses.append(expense)
        self.save_expenses_to_file()

        # Calculate total of a list of expenses (or all)
    def total_expenses(self, expenses=None):
            if expenses is None:
                expenses = self.expenses
            return sum(e['amount'] for e in expenses)

        # Calculate totals by category
    def totals_by_category(self, expenses=None):
        if expenses is None:
            expenses = self.expenses
        totals = {}
        for e in expenses:
            cat = e['category']
            totals[cat] = totals.get(cat, 0.0) + e['amount']
        return totals
    
    def clear_all_expenses(self):
        """Remove all expenses from memory and wipe the CSV file."""
        # Clear the list in memory
        self.expenses = []

        with self.file_path.open("w", newline="", encoding="utf-8") as f:
            fieldnames = ["date", "category", "description", "amount"]
            writer = csv.DictWriter(f, fieldnames = fieldnames)
            writer.writeheader()

        print("\nAll expenses have been cleared.")

    # Filter expenses by category
    def filter_by_category(self, category):
        return [e for e in self.expenses
                if e['category'].lower() == category.lower()]

    # Filter expenses by exact date
    def filter_by_date(self, date):
        return [e for e in self.expenses if e['date'] == date]

    # Method to display expenses (all or a filtered list)
    def display_expenses(self, expenses=None):
        if expenses is None:
            expenses = self.expenses

        # Check if there are no expenses recorded
        if not expenses:
            print("\nNo expenses recorded.")
        else:
            # Display a table header for Date, Category, Description, and Amount
            print("\n{:<12} {:<15} {:<25} {:<15}".format(
                "Date", "Category", "Description", "Amount"))
            print("-" * 75)
            total_expense = 0
            # Iterate through each expense and display its details
            for expense in expenses:
                print("{:<12} {:<15} {:<25} ${:<13,.2f}".format(
                    expense['date'],
                    expense['category'],
                    expense['description'],
                    expense['amount']
                ))
                total_expense += expense['amount']
            print("-" * 75)
            # Display the total of all expenses
            print("{:<54} ${:<13,.2f}".format("Total Expenses:", total_expense))


# Function to run the main Expense Tracker program
def main():
    # Create an instance of the ExpenseTracker class
    expense_tracker = ExpenseTracker()

    # Main program loop
    while True:
        # Display the menu options
        print("\nExpense Tracker Menu:")
        print("\n1. Add Expense")
        print("2. Display All Expenses")
        print("3. View Totals (Overall & By Category)")
        print("4. Filter Expenses (By Category or Date)")
        print("5. Clear All Expenses")
        print("6. Exit")

        # Get user choice
        choice = input("\nEnter your choice: ")

        # Process user's choice
        if choice == '1':
            # Get user input for a new expense and add it to the tracker
            date = input("\nEnter the date (YYYY-MM-DD): ")
            category = input("Enter the category (Food, Entertainment, Rent, etc.): ")
            description = input("Enter a short description: ")
            amount_input = input("Enter the amount: $")

            # Check if any input is empty
            if not date or not category or not description or not amount_input:
                print("\nIncomplete input. Please provide values for date, category, description, and amount.")
            else:
                # First, validate the date format
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    print("\nInvalid date format. Please use YYYY-MM-DD (example: 2025-11-19).")
                    continue

                # Then, validate the amount
                try:
                    amount = float(amount_input)
                    if amount < 0:
                        print("\nAmount cannot be negative.")
                        continue
                except ValueError:
                    print("\nInvalid amount. Please enter a number.")
                    continue

                expense_tracker.add_expense(date, category, description, amount)
                print("\nExpense added successfully!")

        elif choice == '2':
            # Display all recorded expenses
            expense_tracker.display_expenses()

        elif choice == '3':
            # Show total and totals by category
            if not expense_tracker.expenses:
                print("\nNo expenses recorded.")
            else:
                total = expense_tracker.total_expenses()
                print(f"\nTotal expenses: ${total:.2f}")

                cat_totals = expense_tracker.totals_by_category()
                print("\nTotals by category:")
                for cat, amt in cat_totals.items():
                    print(f"  {cat}: ${amt:.2f}")

        elif choice == '4':
            # Filter by category or date
            if not expense_tracker.expenses:
                print("\nNo expenses recorded.")
                continue

            print("\nFilter by:")
            print("1. Category")
            print("2. Date")
            filter_choice = input("Choose filter type: ")

            if filter_choice == '1':
                cat = input("Enter category to filter by: ")
                filtered = expense_tracker.filter_by_category(cat)
                expense_tracker.display_expenses(filtered)
            elif filter_choice == '2':
                date = input("Enter date (YYYY-MM-DD) to filter by: ")
                filtered = expense_tracker.filter_by_date(date)
                expense_tracker.display_expenses(filtered)
            else:
                print("\nInvalid filter option.")

        elif choice == '5':
            # Clear all expenses
            confirm = input("\nAre you sure you want to delete ALL expenses? (y/n): ").lower()
            if confirm == 'y':
                expense_tracker.clear_all_expenses()
            else:
                print("\nCanceled. Expenses were not cleared.")
        
        elif choice == '6':
            # Exit the program
            print("\nExiting the Expense Tracker. Goodbye!")
            break

        else:
            # Handle invalid user input
            print("\nInvalid choice. Please enter a valid option.")


# Run the main function if this script is executed
if __name__ == "__main__":
    main()