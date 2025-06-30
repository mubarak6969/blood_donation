import csv
from datetime import datetime, timedelta

def request_blood():
    print("=== Blood Request ===")
    blood_group = input("Enter required blood group (A+, A-, B+, B-, AB+, AB-, O+, O-): ").strip().upper()
    valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    while blood_group not in valid_blood_groups:
        print("Invalid blood group.")
        blood_group = input("Enter blood group (A+, A-, B+, B-, AB+, AB-, O+, O-): ").strip().upper()
    
    location = input("Enter location: ").strip()
    while not location.replace(" ", "").isalpha():
        print("Invalid location. Use letters only.")
        location = input("Enter location: ").strip()
    
    try:
        units = int(input("Enter number of units needed (1-5): "))
        while units < 1 or units > 5:
            print("Units must be between 1 and 5.")
            units = int(input("Enter number of units needed (1-5): "))
    except ValueError:
        print("Invalid input. Enter a number.")
        return
    
    hospital = input("Enter hospital name: ").strip()
    while not hospital.replace(" ", "").isalnum():
        print("Invalid hospital name. Use letters and numbers only.")
        hospital = input("Enter hospital name: ").strip()
    
    request_date = input("Enter request date (YYYY-MM-DD): ").strip()
    try:
        request_date = datetime.strptime(request_date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return
    
    # Search for matching donors
    matching_donors = []
    try:
        with open('database.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) < 7:
                    continue
                donor_blood_group, donor_location, last_donation = row[3], row[5], row[6]
                # Check blood group and location match
                if donor_blood_group == blood_group and donor_location.lower() == location.lower():
                    # Check 90-day donation gap
                    if last_donation:
                        last_donation_date = datetime.strptime(last_donation, '%Y-%m-%d')
                        if (request_date - last_donation_date).days < 90:
                            continue
                    matching_donors.append(row)
    except FileNotFoundError:
        print("Error: database.csv not found.")
        return
    
    # Display results
    if matching_donors:
        print("\nMatching Donors Found:")
        for donor in matching_donors:
            print(f"Name: {donor[0]}, Age: {donor[1]}, Gender: {donor[2]}, Contact: {donor[4]}")
    else:
        print("\nNo matching donors found.")
    
    # Save request
    try:
        with open('requests.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([blood_group, location, units, hospital, request_date.strftime('%Y-%m-%d')])
        print("Blood request recorded successfully!")
    except FileNotFoundError:
        print("Error: requests.csv not found.")