import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

# Initialize connection to Firestore using the service account key
cred = credentials.Certificate("firebase-credentials.json")
firebase_admin.initialize_app(cred)

# Get database client instance
db = firestore.client()

def initialize_categories():
    """
    Seeds the 'categories' collection with initial budget data.
    Prevents duplicates by checking if the category already exists.
    """
    default_categories = {
        "Food": 500.00,
        "Rent": 1200.00,
        "Entertainment": 200.00
    }
    
    categories_ref = db.collection("categories")
    for name, limit in default_categories.items():
        doc_ref = categories_ref.document(name.lower())
        if not doc_ref.get().exists:
            doc_ref.set({"category_name": name, "monthly_limit": limit})
            print(f"[SETUP] Created category: {name} with limit ${limit}")

def insert_expense(category_id, cost, description):
    """
    CREATE: Adds a new expense document to the 'expenses' collection.
    It verifies the linked category exists first to maintain data integrity.
    Returns the auto-generated document ID of the new expense.
    """
    category_id = category_id.lower()
    
    # Check if the relational category actually exists
    cat_ref = db.collection("categories").document(category_id)
    if not cat_ref.get().exists:
        print(f"[ERROR] Cannot add expense. Category '{category_id}' does not exist.")
        return None

    # Build the expense dictionary with a server timestamp
    new_expense = {
        "category_id": category_id,
        "cost": float(cost),
        "description": description,
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    
    # Push to the database
    update_time, doc_ref = db.collection("expenses").add(new_expense)
    print(f"[INSERT] Logged ${cost} for '{description}' under '{category_id}'. (ID: {doc_ref.id})")
    
    return doc_ref.id

def retrieve_expenses_by_category(category_id):
    """
    READ: Queries the 'expenses' collection to find all transactions 
    linked to a specific category. Calculates and prints the total spent.
    """
    category_id = category_id.lower()
    print(f"\n--- Retrieving Expenses for: {category_id.upper()} ---")
    
    # Query the database for matching category_id
    expenses_ref = db.collection("expenses")
    query = expenses_ref.where("category_id", "==", category_id).stream()
    
    total_spent = 0.0
    count = 0
    
    # Loop through the results and print them
    for doc in query:
        data = doc.to_dict()
        cost = data.get("cost", 0)
        desc = data.get("description", "No description")
        total_spent += cost
        count += 1
        print(f"  - ${cost:.2f} | {desc} | ID: {doc.id}")
        
    if count == 0:
        print("  No expenses found for this category.")
        
    print(f"Total spent in {category_id.upper()}: ${total_spent:.2f}\n")

def update_expense(expense_id, new_cost, new_description):
    """
    UPDATE: Modifies an existing expense document using its specific ID.
    Updates both the cost and the description.
    """
    doc_ref = db.collection("expenses").document(expense_id)
    
    # Verify the document exists before attempting to update
    if doc_ref.get().exists:
        doc_ref.update({
            "cost": float(new_cost),
            "description": new_description
        })
        print(f"[UPDATE] Expense {expense_id} updated to ${new_cost} ('{new_description}').")
    else:
        print(f"[ERROR] Cannot update. Expense {expense_id} does not exist.")

def delete_expense(expense_id):
    """
    DELETE: Removes a specific expense document entirely from the database
    using its unique document ID.
    """
    doc_ref = db.collection("expenses").document(expense_id)
    
    # Verify before deleting
    if doc_ref.get().exists:
        doc_ref.delete()
        print(f"[DELETE] Expense {expense_id} was successfully removed.")
    else:
        print(f"[ERROR] Cannot delete. Expense {expense_id} does not exist.")

# --- Execution Block to Demonstrate CRUD ---
if __name__ == "__main__":
    print("Starting Personal Expense Tracker...\n")
    
    # 1. Setup
    initialize_categories()
    
    # 2. CREATE (Insert data)
    print("\n--- Testing INSERT ---")
    expense1_id = insert_expense("food", 15.50, "Chipotle Burrito")
    expense2_id = insert_expense("food", 45.00, "Groceries")
    expense3_id = insert_expense("entertainment", 12.99, "Movie Ticket")
    
    # 3. READ (Retrieve data)
    retrieve_expenses_by_category("food")
    
    # 4. UPDATE (Modify data)
    print("--- Testing UPDATE ---")
    if expense1_id:
        # Correcting the price and description of the first food expense
        update_expense(expense1_id, 18.50, "Chipotle Burrito + Drink")
    
    # Read again to verify the update
    retrieve_expenses_by_category("food")
    
    # 5. DELETE (Remove data)
    print("--- Testing DELETE ---")
    if expense2_id:
        delete_expense(expense2_id)
        
    # Final Read to show the deleted item is gone
    retrieve_expenses_by_category("food")
    print("Demonstration complete.")