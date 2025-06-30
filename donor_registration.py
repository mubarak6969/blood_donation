import csv
from datetime import datetime

def register_donor():
    print("=== Donor Registration ===")
    name = input("Enter name: ").strip()
    while not name.replace(" ", "").isalpha():
        print("Invalid name. Use letters only.")
        name = input("Enter name: ").strip()
    
    try:
        age = int(input("Enter age (18-60): "))
        while age < 18 or age > 60:
            print("Age must be between 18 and 60.")
            age = int(input("Enter age (18-60): "))
    except ValueError:
        print("Invalid age. Please enter a number.")
        return
    
    gender = input("Enter gender (M/F/O): ").strip().upper()
    while gender not in ['M', 'F', 'O']:
        print("Invalid gender. Enter M, F, or O.")
        gender = input("Enter gender (M/F/O): ").strip().upper()
    
    blood_group = input("Enter blood group (A+, A-, B+, B-, AB+, AB-, O+, O-): ").strip().upper()
    valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    while blood_group not in valid_blood_groups:
        print("Invalid blood group.")
        blood_group = input("Enter blood group (A+, A-, B+, B-, AB+, AB-, O+, O-): ").strip().upper()
    
    contact = input("Enter contact number: ").strip()
    while not contact.isdigit() or len(contact) != 10:
        print("Invalid contact. Enter a 10-digit number.")
        contact = input("Enter contact number: ").strip()
    
    location = input("Enter location: ").strip()
    while not location.replace(" ", "").isalpha():
        print("Invalid location. Use letters only.")
        location = input("Enter location: ").strip()
    
    last_donation = input("Enter last donation date (YYYY-MM-DD, or 'None' if never): ").strip()
    if last_donation.lower() == 'none':
        last_donation = ''
    else:
        try:
            datetime.strptime(last_donation, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD or 'None'.")
            return
    
    # Save to CSV
    with open('database.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, age, gender, blood_group, contact, location, last_donation])
    print("Donor registered successfully!")

if __name__ == "__main__":
    register_donor()