import csv

def view_donors():
    print("=== View Donors ===")
    try:
        with open('database.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip header
            donors = list(reader)
            if not donors:
                print("No donors found.")
                return
            print("\nDonor List:")
            for i, donor in enumerate(donors, 1):
                print(f"{i}. Name: {donor[0]}, Age: {donor[1]}, Gender: {donor[2]}, Blood Group: {donor[3]}, Contact: {donor[4]}, Location: {donor[5]}, Last Donation: {donor[6] or 'None'}")
    except FileNotFoundError:
        print("Error: database.csv not found.")

def edit_donor():
    print("=== Edit Donor ===")
    try:
        with open('database.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            donors = list(reader)
            if not donors:
                print("No donors found.")
                return
            
            view_donors()
            try:
                index = int(input("Enter donor number to edit (1-{}): ".format(len(donors)))) - 1
                if index < 0 or index >= len(donors):
                    print("Invalid donor number.")
                    return
            except ValueError:
                print("Invalid input. Enter a number.")
                return
            
            donor = donors[index]
            print(f"Editing: {donor[0]}")
            name = input(f"Enter new name (current: {donor[0]}): ").strip() or donor[0]
            while not name.replace(" ", "").isalpha():
                print("Invalid name. Use letters only.")
                name = input(f"Enter new name (current: {donor[0]}): ").strip() or donor[0]
            
            try:
                age = input(f"Enter new age (current: {donor[1]}): ").strip() or donor[1]
                age = int(age)
                while age < 18 or age > 60:
                    print("Age must be between 18 and 60.")
                    age = int(input(f"Enter new age (current: {donor[1]}): ").strip() or donor[1])
            except ValueError:
                print("Invalid age. Keeping current value.")
                age = int(donor[1])
            
            gender = input(f"Enter new gender (M/F/O, current: {donor[2]}): ").strip().upper() or donor[2]
            while gender not in ['M', 'F', 'O']:
                print("Invalid gender. Enter M, F, or O.")
                gender = input(f"Enter new gender (M/F/O, current: {donor[2]}): ").strip().upper() or donor[2]
            
            blood_group = input(f"Enter new blood group (A+, A-, B+, B-, AB+, AB-, O+, O-, current: {donor[3]}): ").strip().upper() or donor[3]
            valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
            while blood_group not in valid_blood_groups:
                print("Invalid blood group.")
                blood_group = input(f"Enter new blood group (current: {donor[3]}): ").strip().upper() or donor[3]
            
            contact = input(f"Enter new contact number (current: {donor[4]}): ").strip() or donor[4]
            while not contact.isdigit() or len(contact) != 10:
                print("Invalid contact. Enter a 10-digit number.")
                contact = input(f"Enter new contact number (current: {donor[4]}): ").strip() or donor[4]
            
            location = input(f"Enter new location (current: {donor[5]}): ").strip() or donor[5]
            while not location.replace(" ", "").isalpha():
                print("Invalid location. Use letters only.")
                location = input(f"Enter new location (current: {donor[5]}): ").strip() or donor[5]
            
            last_donation = input(f"Enter new last donation date (YYYY-MM-DD or 'None', current: {donor[6] or 'None'}): ").strip() or donor[6]
            if last_donation.lower() == 'none':
                last_donation = ''
            else:
                try:
                    from datetime import datetime
                    datetime.strptime(last_donation, '%Y-%m-%d')
                except ValueError:
                    print("Invalid date format. Keeping current value.")
                    last_donation = donor[6]
            
            donors[index] = [name, age, gender, blood_group, contact, location, last_donation]
            
            with open('database.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(donors)
            print("Donor updated successfully!")
    except FileNotFoundError:
        print("Error: database.csv not found.")

def delete_donor():
    print("=== Delete Donor ===")
    try:
        with open('database.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            donors = list(reader)
            if not donors:
                print("No donors found.")
                return
            
            view_donors()
            try:
                index = int(input("Enter donor number to delete (1-{}): ".format(len(donors)))) - 1
                if index < 0 or index >= len(donors):
                    print("Invalid donor number.")
                    return
            except ValueError:
                print("Invalid input. Enter a number.")
                return
            
            donor = donors.pop(index)
            with open('database.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(donors)
            print(f"Donor {donor[0]} deleted successfully!")
    except FileNotFoundError:
        print("Error: database.csv not found.")

def admin_panel():
    while True:
        print("\n=== Admin Panel ===")
        print("1. View Donors")
        print("2. Edit Donor")
        print("3. Delete Donor")
        print("4. Back to Main Menu")
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == '1':
            view_donors()
        elif choice == '2':
            edit_donor()
        elif choice == '3':
            delete_donor()
        elif choice == '4':
            print("Returning to main menu...")
            break
        else:
            print("Invalid choice. Try again.")