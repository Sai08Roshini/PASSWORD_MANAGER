# PASSWORD MANAGER PROJECT
# STEP 1:Install the necessary modules.
import os
import json
import re
from cryptography.fernet import Fernet
from getpass import getpass
# STEP 2 :Generate and Store Encryption Key
# Generate a key and store it in a file
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Load the key from the file
def load_key():
    return open("key.key", "rb").read()

# Generate a key if it does not exist
if not os.path.exists("key.key"):
    generate_key()

key = load_key()
cipher_suite = Fernet(key)
# STEP 3: Implement Password Storage and Retrieval
# File to store passwords
PASSWORD_FILE = "passwords.json"
# Load passwords from the file
def load_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            return json.load(file)
    return []

# Save passwords to the file
def save_passwords(passwords):
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file)
# Check password strength
def check_password_strength(password):
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None

    errors = {
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }

    return not any(errors.values()), errors
# Add a new password
def add_password():
    site = input("Enter the site name: ")
    user = input("Enter the username: ")
    while True:
        password = getpass("Enter the password: ")
        is_strong, errors = check_password_strength(password)

        if is_strong:
            break
        else:
            print("Password is not strong enough. Please ensure the password meets the following criteria:")
            if errors['length_error']:
                print(" - At least 8 characters long")
            if errors['digit_error']:
                print(" - Contains at least one digit")
            if errors['uppercase_error']:
                print(" - Contains at least one uppercase letter")
            if errors['lowercase_error']:
                print(" - Contains at least one lowercase letter")
            if errors['symbol_error']:
                print(" - Contains at least one special character (!@#$%^&*(), etc.)")
    
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    passwords.append({"site": site, "user": user, "password": encrypted_password})
    save_passwords(passwords)
    print("Password added successfully!")

# View all passwords
def view_passwords():
    for idx, pw in enumerate(passwords, start=1):
        print(f"{idx}. Site: {pw['site']}, User: {pw['user']}")

# Show a specific password
def show_password():
    try:
        index = int(input("Enter the number of the password to view: ")) - 1
        selected_password = passwords[index]
        decrypted_password = cipher_suite.decrypt(selected_password['password'].encode()).decode()
        print(f"Site: {selected_password['site']}\nUser: {selected_password['user']}\nPassword: {decrypted_password}")
    except (IndexError, ValueError):
        print("Invalid selection.")

# Delete a specific password
def delete_password():
    try:
        index = int(input("Enter the number of the password to delete: ")) - 1
        deleted_password = passwords.pop(index)
        save_passwords(passwords)
        print(f"Deleted password for site: {deleted_password['site']}")
    except (IndexError, ValueError):
        print("Invalid selection.")
# STEP 4: Create the Command-Line Interface
def menu():
    print("\nPassword Vault Menu")
    print("1. Add a new password")
    print("2. View all passwords")
    print("3. Show a specific password")
    print("4. Delete a password")
    print("5. Exit")

# Main loop
passwords = load_passwords()

while True:
    menu()
    choice = input("Choose an option: ")

    if choice == '1':
        add_password()
    elif choice == '2':
        view_passwords()
    elif choice == '3':
        show_password()
    elif choice == '4':
        delete_password()
    elif choice == '5':
        print("Exiting Password Vault. Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option.")
