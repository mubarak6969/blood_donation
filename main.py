from donor_registration import register_donor
from request_blood import request_blood
from search_donor import search_donor
from admin_panel import admin_panel

def main():
    while True:
        print("\n=== Blood Donation Request System ===")
        print("1. Register Donor")
        print("2. Request Blood")
        print("3. Search Donors")
        print("4. Admin Panel")
        print("5. Exit")
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            register_donor()
        elif choice == '2':
            request_blood()
        elif choice == '3':
            search_donor()
        elif choice == '4':
            admin_panel()
        elif choice == '5':
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()