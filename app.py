from flask import Flask, render_template, request, redirect, url_for, flash
from donor_registration import register_donor
from request_blood import request_blood
from search_donor import search_donor
from admin_panel import view_donors, edit_donor, delete_donor
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for flash messages

@app.route('/')
def index():
    return render_template('main.html', page='index')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        try:
            age = int(request.form['age'])
            if age < 18 or age > 60:
                flash('Age must be between 18 and 60.')
                return redirect(url_for('register'))
        except ValueError:
            flash('Invalid age. Please enter a number.')
            return redirect(url_for('register'))
        
        gender = request.form['gender'].upper()
        if gender not in ['M', 'F', 'O']:
            flash('Invalid gender. Select M, F, or O.')
            return redirect(url_for('register'))
        
        blood_group = request.form['blood_group'].upper()
        valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if blood_group not in valid_blood_groups:
            flash('Invalid blood group.')
            return redirect(url_for('register'))
        
        contact = request.form['contact']
        if not contact.isdigit() or len(contact) != 10:
            flash('Invalid contact. Enter a 10-digit number.')
            return redirect(url_for('register'))
        
        location = request.form['location']
        if not location.replace(' ', '').isalpha():
            flash('Invalid location. Use letters only.')
            return redirect(url_for('register'))
        
        last_donation = request.form['last_donation']
        if last_donation.lower() == 'none':
            last_donation = ''
        else:
            try:
                datetime.strptime(last_donation, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format. Use YYYY-MM-DD or None.')
                return redirect(url_for('register'))
        
        try:
            with open('database.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, age, gender, blood_group, contact, location, last_donation])
            flash('Donor registered successfully!')
        except Exception as e:
            flash(f'Error registering donor: {str(e)}')
        return redirect(url_for('register'))
    
    return render_template('main.html', page='register')

@app.route('/request', methods=['GET', 'POST'])
def request_blood_route():
    if request.method == 'POST':
        blood_group = request.form['blood_group'].upper()
        valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if blood_group not in valid_blood_groups:
            flash('Invalid blood group.')
            return redirect(url_for('request_blood_route'))
        
        location = request.form['location']
        if not location.replace(' ', '').isalpha():
            flash('Invalid location. Use letters only.')
            return redirect(url_for('request_blood_route'))
        
        try:
            units = int(request.form['units'])
            if units < 1 or units > 5:
                flash('Units must be between 1 and 5.')
                return redirect(url_for('request_blood_route'))
        except ValueError:
            flash('Invalid input. Enter a number for units.')
            return redirect(url_for('request_blood_route'))
        
        hospital = request.form['hospital']
        if not hospital.replace(' ', '').isalnum():
            flash('Invalid hospital name. Use letters and numbers only.')
            return redirect(url_for('request_blood_route'))
        
        request_date = request.form['request_date']
        try:
            request_date = datetime.strptime(request_date, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD.')
            return redirect(url_for('request_blood_route'))
        
        matching_donors = []
        try:
            with open('database.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) < 7:
                        continue
                    donor_blood_group, donor_location, last_donation = row[3], row[5], row[6]
                    if donor_blood_group == blood_group and donor_location.lower() == location.lower():
                        if last_donation:
                            last_donation_date = datetime.strptime(last_donation, '%Y-%m-%d')
                            if (request_date - last_donation_date).days < 90:
                                continue
                        matching_donors.append(row)
        except FileNotFoundError:
            flash('Error: database.csv not found.')
            return redirect(url_for('request_blood_route'))
        
        try:
            with open('requests.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([blood_group, location, units, hospital, request_date.strftime('%Y-%m-%d')])
            flash('Blood request recorded successfully!')
        except FileNotFoundError:
            flash('Error: requests.csv not found.')
            return redirect(url_for('request_blood_route'))
        
        return render_template('main.html', page='request_result', donors=matching_donors)
    
    return render_template('main.html', page='request')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        blood_group = request.form['blood_group'].upper()
        valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if blood_group not in valid_blood_groups:
            flash('Invalid blood group.')
            return redirect(url_for('search'))
        
        location = request.form['location']
        if not location.replace(' ', '').isalpha():
            flash('Invalid location. Use letters only.')
            return redirect(url_for('search'))
        
        current_date = datetime.now()
        matching_donors = []
        try:
            with open('database.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) < 7:
                        continue
                    donor_blood_group, donor_location, last_donation = row[3], row[5], row[6]
                    if donor_blood_group == blood_group and donor_location.lower() == location.lower():
                        if last_donation:
                            last_donation_date = datetime.strptime(last_donation, '%Y-%m-%d')
                            if (current_date - last_donation_date).days < 90:
                                continue
                        matching_donors.append(row)
        except FileNotFoundError:
            flash('Error: database.csv not found.')
            return redirect(url_for('search'))
        
        return render_template('main.html', page='search_result', donors=matching_donors)
    
    return render_template('main.html', page='search')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    donors = []
    try:
        with open('database.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            donors = list(reader)
    except FileNotFoundError:
        flash('Error: database.csv not found.')
    
    # Create enumerated list for template (1-based index)
    enumerated_donors = [(i + 1, donor) for i, donor in enumerate(donors)]
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'edit':
            try:
                # Adjust index to 0-based for internal use
                index = int(request.form.get('index', -1)) - 1
                if index < 0 or index >= len(donors):
                    flash('Invalid donor number.')
                    return redirect(url_for('admin'))
                
                # Safely get form fields, default to current donor values
                name = request.form.get('name', donors[index][0]).strip()
                if not name or not name.replace(' ', '').isalpha():
                    flash('Invalid name. Use letters only.')
                    return redirect(url_for('admin'))
                
                try:
                    age_input = request.form.get('age', donors[index][1])
                    age = int(age_input)
                    if age < 18 or age > 60:
                        flash('Age must be between 18 and 60.')
                        return redirect(url_for('admin'))
                except ValueError:
                    flash('Invalid age. Keeping current value.')
                    age = int(donors[index][1])
                
                gender = request.form.get('gender', donors[index][2]).upper()
                if gender not in ['M', 'F', 'O']:
                    flash('Invalid gender. Select M, F, or O.')
                    return redirect(url_for('admin'))
                
                blood_group = request.form.get('blood_group', donors[index][3]).upper()
                valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
                if blood_group not in valid_blood_groups:
                    flash('Invalid blood group.')
                    return redirect(url_for('admin'))
                
                contact = request.form.get('contact', donors[index][4]).strip()
                if not contact.isdigit() or len(contact) != 10:
                    flash('Invalid contact. Enter a 10-digit number.')
                    return redirect(url_for('admin'))
                
                location = request.form.get('location', donors[index][5]).strip()
                if not location or not location.replace(' ', '').isalpha():
                    flash('Invalid location. Use letters only.')
                    return redirect(url_for('admin'))
                
                last_donation = request.form.get('last_donation', donors[index][6]).strip()
                if last_donation.lower() == 'none':
                    last_donation = ''
                elif last_donation:
                    try:
                        datetime.strptime(last_donation, '%Y-%m-%d')
                    except ValueError:
                        flash('Invalid date format. Use YYYY-MM-DD or None.')
                        return redirect(url_for('admin'))
                
                # Update donor data
                donors[index] = [name, str(age), gender, blood_group, contact, location, last_donation]
                try:
                    with open('database.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['name', 'age', 'gender', 'blood_group', 'contact', 'location', 'last_donation_date'])
                        writer.writerows(donors)
                    flash(f'Donor {name} updated successfully!')
                except Exception as e:
                    flash(f'Error updating donor: {str(e)}')
            except Exception as e:
                flash(f'Error processing edit: {str(e)}')
        elif action == 'delete':
            try:
                index = int(request.form.get('index', -1)) - 1
                if index < 0 or index >= len(donors):
                    flash('Invalid donor number.')
                    return redirect(url_for('admin'))
                donor = donors.pop(index)
                try:
                    with open('database.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['name', 'age', 'gender', 'blood_group', 'contact', 'location', 'last_donation_date'])
                        writer.writerows(donors)
                    flash(f'Donor {donor[0]} deleted successfully!')
                except Exception as e:
                    flash(f'Error deleting donor: {str(e)}')
            except ValueError:
                flash('Invalid donor number.')
        
        return redirect(url_for('admin'))
    
    return render_template('main.html', page='admin', enumerated_donors=enumerated_donors)

if __name__ == '__main__':
    app.run(debug=True)
