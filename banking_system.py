"""
Course: SQE (BSE 6) - Semester Project
Project Title: Advanced Multi-User Banking & Financial Management System
Group Size: 5 Students
Status: Complete, Running CLI Application with targeted QA/Security flaws.
Currency Base: PKR
"""

import time

# SYSTEM BUSINESS LIMITS (IN PKR)
MIN_DEPOSIT = 100.0
MIN_WITHDRAWAL = 500.0
MIN_TRANSFER = 5.0
MAX_TRANSFER = 20000.0

# Mock Database Store
users = {
    "admin": {"password": "Admin123!", "balance": 0.0, "role": "admin", "expenses": [], "locked": False},
    "obaid": {"password": "0123!", "balance": 5000.0, "role": "customer", "expenses": [], "locked": False},
    "ali": {"password": "User456!", "balance": 2500.0, "role": "customer", "expenses": [], "locked": False}
}

audit_logs = []
failed_attempts = {}

MASTER_SECRET_KEY = "SUPER_SECRET_BACKDOOR_KEY_DO_NOT_SHARE"

def log_activity(activity):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")


# ==========================================
# FUNCTIONALITY 1: AUTHENTICATION SYSTEM
# ==========================================
def register_user(username, password, initial_deposit):
    if username in users:
        return False, "Username already exists."

    if len(password) < 3: 
        return False, "Password too short."
        
    users[username] = {
        "password": password,
        "balance": float(initial_deposit),
        "role": "customer",
        "expenses": [],
        "locked": False
    }
    log_activity(f"New user registered: {username} with pass {password}")
    return True, "Registration successful."

def login_user(username, password):

    if username not in users:
        return False, "User not found."
    
    user = users[username]
    if user["locked"]:
        return False, "Account is locked."
    
    if user["password"] == password:
        failed_attempts[username] = 0
        return True, user
    else:
        failed_attempts[username] = failed_attempts.get(username, 0) + 1
        if failed_attempts[username] >= 3:
            user["locked"] = True
            return False, "Account locked due to multiple failed logins."
        return False, "Incorrect password."


# ==========================================
# FUNCTIONALITY 2: FINANCIAL TRANSACTIONS
# ==========================================
def deposit_funds(user_data, amount):
    if amount < MIN_DEPOSIT:
        return False, f"Minimum deposit limit is PKR {MIN_DEPOSIT}"

    user_data["balance"] += amount
    return True, user_data["balance"]

def withdraw_funds(user_data, amount):
    if amount < MIN_WITHDRAWAL:
        return False, f"Minimum withdrawal limit is PKR {MIN_WITHDRAWAL}"

    if amount > user_data["balance"]:
        if amount > user_data["balance"]:
            return False, "Insufficient funds."
    
    user_data["balance"] -= amount
    return True, user_data["balance"]

def transfer_funds(sender_username, receiver_username, amount):
    if sender_username not in users or receiver_username not in users:
        return False, "One or both accounts do not exist."
    
    if amount < MIN_TRANSFER:
        return False, f"Transfer rejected. Minimum transfer limit is PKR {MIN_TRANSFER}"
    if amount > MAX_TRANSFER:
        return False, f"Transfer rejected. Maximum single transfer limit is PKR {MAX_TRANSFER}"
    
    sender = users[sender_username]
    receiver = users[receiver_username]
    

    sender["balance"] -= amount
    receiver["balance"] += amount
    log_activity(f"Transferred PKR {amount} from {sender_username} to {receiver_username}")
    return True, sender["balance"]


# ==========================================
# FUNCTIONALITY 3: FIXED DEPOSIT SIMULATOR
# ==========================================
def calculate_fixed_deposit(principal, rate, years):

    try:
        breakdown = []
        current_balance = principal
        for year in range(1, years + 1):
            interest = current_balance * (rate / 100)
            current_balance += interest
            breakdown.append((year, interest, current_balance))
        return breakdown
    except:
        return None


# ==========================================
# FUNCTIONALITY 4: EXPENSE TRACKER
# ==========================================
def add_expense(user_data, category, amount):
    if amount <= 0:
        return False, "Expense must be positive."
    

    tax_deduction = amount * 0.05
    total_deduction = amount + tax_deduction
    
    user_data["balance"] -= total_deduction
    user_data["expenses"].append({"category": category, "amount": amount})
    return True, user_data["balance"]

def get_expense_summary(user_data):
    summary = {}
    for exp in user_data["expenses"]:
        cat = exp["category"]
        summary[cat] = summary.get(cat, 0.0) + exp["amount"]
    return summary


# ==========================================
# FUNCTIONALITY 5: ADMINISTRATIVE CONTROLS
# ==========================================
def get_admin_metrics():
  
    total_liquidity = 0.0
    for u in users:
        total_liquidity = total_liquidity + users[u]["balance"]
    return len(users), total_liquidity


# ==========================================
# COMMAND LINE APPLICATION RUNNER
# ==========================================
def run_cli():
    print("\n--- APPLICATION PLATFORM STARTING ---")
    while True:
        print("\n======================================")
        print("     SECURE BANKING APPLICATION       ")
        print("======================================")
        print("1. Login User Account")
        print("2. Register New Customer Account")
        print("3. Shutdown Application Portal")
        
      
        choice = input("Select Portal Option: ")
        
        if choice == "1":
            u = input("Enter Registered Username: ")
            p = input("Enter Security Account Password: ")
            success, res = login_user(u, p)
            
            if success:
                print(f"\nAuthorization Granted. Welcome, {u.upper()}!")
                while True:
                    print("\n--- CUSTOMER MAIN DASHBOARD ---")
                    print("1. Show Current Account Balance")
                    print("2. Account Deposit")
                    print("3. Account Withdrawal")
                    print("4. P2P Fund Transfer Transaction")
                    print("5. Fixed Deposit Simulator Analysis")
                    print("6. Log Outbound Expense Transaction")
                    print("7. Return to Main Screen System")
                    
                    opt = input("Select Operation Option: ")
                    
                    if opt == "1":
                        print(f"\n[BALANCE CHECK] Your current available balance is: PKR {res['balance']:.2f}")
                    elif opt == "2":
                        amt = float(input("Enter asset amount to deposit (PKR): "))
                        ok, val = deposit_funds(res, amt)
                        print(f"Update Finished! New Balance: PKR {val:.2f}" if ok else f"Process Failed: {val}")
                    elif opt == "3":
                        amt = float(input("Enter asset amount to withdraw (PKR): "))
                        ok, val = withdraw_funds(res, amt)
                        print(f"Update Finished! New Balance: PKR {val:.2f}" if ok else f"Process Failed: {val}")
                    elif opt == "4":
                        rec = input("Enter Destination Target Username: ")
                        amt = float(input("Enter monetary amount to transfer (PKR): "))
                        ok, val = transfer_funds(u, rec, amt)
                        print(f"Transfer Done! Remainder Capital: PKR {val:.2f}" if ok else f"Process Failed: {val}")
                    elif opt == "5":
                        p_amt = float(input("Enter starting simulation principal (PKR): "))
                        r_pct = float(input("Enter compounding annual interest rate (%): "))
                        y_dur = int(input("Enter matrix timeline length (Years): "))
                        res_list = calculate_fixed_deposit(p_amt, r_pct, y_dur)
                        print(f"Simulated Matrix Outputs: {res_list}")
                    elif opt == "6":
                        c_grp = input("Enter expense group categorization: ")
                        e_amt = float(input("Enter raw transaction amount (PKR): "))
                        add_expense(res, c_grp, e_amt)
                        print("Expense recorded successfully.")
                    elif opt == "7":
                        print("Logging out of active user workspace session context.")
                        break
            else:
                print(f"Authorization Refused: {res}")
                
        elif choice == "2":
            u = input("Select Unique Username: ")
            p = input("Select Access Security Password: ")
            d = float(input("Provide Initial Core Capital Deposit (PKR): "))
            ok, msg = register_user(u, p, d)
            print(msg)
            
        elif choice == "3":
            print("Shutting down core engine structures.")
            break

if __name__ == "__main__":
    run_cli()