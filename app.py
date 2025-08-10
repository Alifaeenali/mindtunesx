from flask import Flask, render_template, url_for, request, redirect, flash, session
import mysql.connector
from functools import wraps
import hashlib
import os
from werkzeug.utils import secure_filename
import json
from flask_mail import Mail, Message 
from datetime import datetime 
from dotenv import load_dotenv  # You'll need to install python-dotenv

# Load environment variables
load_dotenv()
 
app = Flask(__name__)
# IMPORTANT: Use environment variables for sensitive data in production
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-change-this-in-production')

# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'ogg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '10,Aug_2023',
    'database': 'mindtunes_db'
}

# Admin credentials (in production, store in database with hashed passwords)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = hashlib.sha256('admin123'.encode()).hexdigest()  # Change this password

# =================================================================================================
# NEW: Email Configuration
# =================================================================================================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Example: Gmail SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER', 'your_email@example.com')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS', 'your_email_password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER', 'ah5288317@example.com')

mail = Mail(app)

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def fetch_data(table_name):
    """Fetches all data from a specified table."""
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        print(f"Error fetching data from {table_name}: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_client_logos():
    """Fetch client logos from database."""
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM client_logos ORDER BY logo_order")
        data = cursor.fetchall()
        return [row['logo_url'] for row in data]
    except mysql.connector.Error as err:
        print(f"Error fetching client logos: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_client_logos(logos):
    """Update client logos in database."""
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # Clear existing logos
        cursor.execute("DELETE FROM client_logos")

        # Insert new logos
        for i, logo_url in enumerate(logos, 1):
            cursor.execute("INSERT INTO client_logos (logo_url, logo_order) VALUES (%s, %s)",
                           (logo_url, i))

        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating client logos: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_founders():
    """Fetches all founders from the database."""
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM founders ORDER BY founder_order")
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        print(f"Error fetching founders: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_founders(founders_list):
    """Updates the founders in the database by clearing existing and inserting new ones."""
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM founders")

        query = "INSERT INTO founders (founder_name, founder_role, founder_image, founder_description, founder_order) VALUES (%s, %s, %s, %s, %s)"
        for i, founder in enumerate(founders_list, 1):
            cursor.execute(query, (founder['founder_name'], founder['founder_role'], founder['founder_image'], founder['founder_description'], i))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating founders: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_who_we_work_with():
    """Fetches all 'Who We Work With' entries from the database."""
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM who_we_work_with ORDER BY work_order")
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        print(f"Error fetching 'who we work with' data: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_who_we_work_with(work_with_list):
    """Updates the 'Who We Work With' entries in the database."""
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM who_we_work_with")

        query = "INSERT INTO who_we_work_with (work_icon, work_title, work_description, work_order) VALUES (%s, %s, %s, %s)"
        for i, work_item in enumerate(work_with_list, 1):
            cursor.execute(query, (work_item['work_icon'], work_item['work_title'], work_item['work_description'], i))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating 'who we work with' data: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_services(services_list):
    """Updates the services in the database by clearing existing and inserting new ones."""
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM servicesTable")

        query = "INSERT INTO servicesTable (service_head, service_desc) VALUES (%s, %s)"
        for service in services_list:
            cursor.execute(query, (service['service_head'], service['service_desc']))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating services: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    print("WARNING: Email configuration incomplete. Set MAIL_USERNAME and MAIL_PASSWORD environment variables.")

def update_data(table_name, data_dict):
    """Updates data in a specified table, handling missing columns gracefully."""
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # First, get existing columns in the table
        cursor.execute(f"DESCRIBE {table_name}")
        existing_columns = [row[0] for row in cursor.fetchall()]

        # Filter data_dict to only include existing columns
        filtered_data = {}
        for key, value in data_dict.items():
            if key in existing_columns:
                filtered_data[key] = value
            else:
                print(f"Warning: Column '{key}' does not exist in table '{table_name}'. Skipping...")

        if not filtered_data:
            print(f"No valid columns to update in table '{table_name}'")
            return False

        # Build the SET clause dynamically with filtered data
        set_clause = ', '.join([f"{key} = %s" for key in filtered_data.keys()])
        values = list(filtered_data.values())

        # Determine the primary key field name based on table name
        id_field = 'id'
        if table_name == 'navTable':
            id_field = 'nav_id'
        elif table_name == 'heroTable':
            id_field = 'hero_id'
        elif table_name == 'Ourclients':
            id_field = 'clients_id'
        elif table_name == 'innovations':
            id_field = 'innovation_id'
        elif table_name == 'know':
            id_field = 'know_id'
        elif table_name == 'statistics':
            id_field = 'stat_id'
        elif table_name == 'footer':
            id_field = 'ftr_id'
        elif table_name == 'aboutUs':
            id_field = 'about_id'
        elif table_name == 'servicesTable':
            id_field = 'service_id'

        query = f"UPDATE {table_name} SET {set_clause} WHERE {id_field} = 1"

        cursor.execute(query, values)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating data in {table_name}: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# =================================================================================================
# NEW: Function to add contact form submission to the database
# =================================================================================================
def add_contact_submission(name, email, subject, message):
    """Adds a new contact form submission to the database."""
    conn = get_db_connection()
    if conn is None:
        print("Database connection failed")
        return False
    
    cursor = conn.cursor()
    try:
        # Use the correct table structure
        query = """INSERT INTO contact_submissions 
                   (name, email, subject, message, submission_date) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (name, email, subject, message, datetime.now()))
        conn.commit()
        print(f"Contact submission saved successfully for {name}")
        return True
    except mysql.connector.Error as err:
        print(f"Error adding contact submission: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# =================================================================================================
# NEW: Function to fetch contact submissions for admin panel
# =================================================================================================
def fetch_contact_submissions():
    """Fetches all contact form submissions from the database."""
    conn = get_db_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""SELECT id, name, email, subject, message, submission_date 
                         FROM contact_submissions 
                         ORDER BY submission_date DESC""")
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        print(f"Error fetching contact submissions: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def base_data():
    """Get base navigation and footer data."""
    nav_data = fetch_data('navTable')
    footer_data = fetch_data('footer')

    return {
        'nav': nav_data[0] if nav_data else {},
        'footer': footer_data[0] if footer_data else {}
    }

def admin_required(f):
    """Decorator to require admin authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please log in to access the admin panel.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Public Routes
@app.route('/')
def index():
    """Renders the main index page with data from all tables."""
    nav_data = fetch_data('navTable')
    hero_data = fetch_data('heroTable')
    clients_data = fetch_data('Ourclients')
    client_logos = fetch_client_logos()
    innovations_data = fetch_data('innovations')
    know_data = fetch_data('know')
    statistics_data = fetch_data('statistics')
    footer_data = fetch_data('footer')

    template_data = {
        'nav': nav_data[0] if nav_data else {},
        'hero': hero_data[0] if hero_data else {},
        'client': clients_data[0] if clients_data else {},
        'client_logos': client_logos,
        'innovation': innovations_data[0] if innovations_data else {},
        'know': know_data[0] if know_data else {},
        'statistic': statistics_data[0] if statistics_data else {},
        'footer': footer_data[0] if footer_data else {}
    }

    return render_template('index.html', **template_data)

@app.route('/about')
def about():
    """Renders the about us page with data from the aboutUs table."""
    about_data = fetch_data('aboutUs')
    about_us = about_data[0] if about_data else {}
    base_data_dict = base_data()
    founders_data = fetch_founders()
    who_we_work_with_data = fetch_who_we_work_with()

    return render_template('about.html',
                           aboutData=about_us,
                           founders=founders_data,
                           work_with=who_we_work_with_data,
                           **base_data_dict)

@app.route('/services')
def services():
    """Renders the services page with data from the servicesTable."""
    services_data = fetch_data('servicesTable')
    base_data_dict = base_data()
    return render_template('services.html', servicesList=services_data, **base_data_dict)


# =================================================================================================
# NEW: Contact form and email submission route
# =================================================================================================
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handles contact form display and submission."""
    base_data_dict = base_data()
    
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        job_title = request.form.get('job_title', '').strip()
        company_name = request.form.get('company_name', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        email = request.form.get('email', '').strip()
        industry = request.form.get('industry', '').strip()
        num_employees = request.form.get('num_employees', '').strip()
        additional_details = request.form.get('additional_details', '').strip()

        # Validation
        if not first_name or not last_name or not email or not additional_details:
            flash('Please fill in all the required fields: First Name, Last Name, Email, and Project Details.', 'error')
            return render_template('index.html', **base_data_dict)

        # Combine first and last name for database
        full_name = f"{first_name} {last_name}"
        
        # Create subject line
        subject_line = f"Project Inquiry from {full_name}"
        if company_name:
            subject_line += f" ({company_name})"

        # Build comprehensive message for database
        comprehensive_message = f"""
Contact Details:
- Name: {full_name}
- Email: {email}
- Phone: {phone_number}
- Job Title: {job_title}
- Company: {company_name}
- Industry: {industry}
- Number of Employees: {num_employees}

Project Details:
{additional_details}
        """.strip()

        try:
            # Send email to admin
            admin_subject = f"New Contact Submission: {subject_line}"
            admin_body = f"""
You have received a new contact form submission:

Name: {full_name}
Email: {email}
Phone: {phone_number}
Job Title: {job_title}
Company: {company_name}
Industry: {industry}
Number of Employees: {num_employees}

Project Details:
{additional_details}

---
This message was sent from the MindTune Innovations contact form.
            """.strip()

            # Send email to admin
            admin_msg = Message(
                subject=admin_subject,
                recipients=[app.config['MAIL_USERNAME']],
                body=admin_body
            )
            mail.send(admin_msg)

            # Send confirmation email to user
            user_subject = "Thank you for contacting MindTune Innovations"
            user_body = f"""
Dear {first_name},

Thank you for reaching out to MindTune Innovations. We have received your project inquiry and will get back to you within 24 hours.

Here's a summary of your submission:
- Project: {additional_details[:100]}{'...' if len(additional_details) > 100 else ''}
- Company: {company_name}
- Industry: {industry}

We look forward to discussing your project with you.

Best regards,
MindTune Innovations Team
            """.strip()

            user_msg = Message(
                subject=user_subject,
                recipients=[email],
                body=user_body
            )
            mail.send(user_msg)

            # Save to database
            if add_contact_submission(full_name, email, subject_line, comprehensive_message):
                flash('Your message has been sent successfully! We will get back to you shortly.', 'success')
            else:
                flash('Your message has been sent but there was an issue saving it. We will still contact you.', 'warning')

        except Exception as e:
            print(f"Error sending email: {e}")
            # Still try to save to database even if email fails
            if add_contact_submission(full_name, email, subject_line, comprehensive_message):
                flash('Your message has been received and saved. We will contact you soon. (Email service temporarily unavailable)', 'warning')
            else:
                flash('There was an error processing your message. Please try again or contact us directly.', 'error')

        return redirect(url_for('index'))
    
    # For GET request, render the index page
    return render_template('index.html', **base_data_dict)
# =================================================================================================
# NEW: Data Showing - A simple route to display all service data as JSON for API-like access
# =================================================================================================
@app.route('/api/services')
def show_services_data():
    """Fetches and displays all services data as JSON."""
    services_data = fetch_data('servicesTable')
    return json.dumps(services_data)


# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Hash the provided password
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if username == ADMIN_USERNAME and password_hash == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('admin_login.html')

@app.route('/admin/logout')
@admin_required
def admin_logout():
    """Admin logout."""
    session.pop('admin_logged_in', None)
    flash('Successfully logged out.', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/<section>')
@admin_required
def admin(section=None):
    """Admin panel main page."""

    # Section titles for display
    section_titles = {
        'nav': 'Navigation Settings',
        'hero': 'Hero Section',
        'clients': 'Our Clients',
        'innovations': 'Innovations Section',
        'know': 'Know Section',
        'statistics': 'Statistics Section',
        'footer': 'Footer Links',
        'about_us': 'About Us Page',
        'services': 'Services Management',
        'contact_submissions': 'Contact Submissions' # Add this for contact submissions
    }

    # Table mapping
    table_mapping = {
        'nav': 'navTable',
        'hero': 'heroTable',
        'clients': 'Ourclients',
        'innovations': 'innovations',
        'know': 'know',
        'statistics': 'statistics',
        'footer': 'footer',
        'about_us': 'aboutUs',
        'services': 'servicesTable',
        'contact_submissions': 'contact_submissions' # Add this for contact submissions
    }

    current_data = {}
    client_logos = []
    founders_data = []
    work_with_data = []
    services_data = []
    contact_submissions_data = [] # Initialize for contact submissions

    if section and section in table_mapping:
        if section == 'contact_submissions': # Special handling for contact submissions
            contact_submissions_data = fetch_contact_submissions()
        else:
            data = fetch_data(table_mapping[section])
            current_data = data[0] if data else {}

            # Special handling for clients section to get logos
            if section == 'clients':
                client_logos = fetch_client_logos()

            # Special handling for about_us section to get founders and 'who we work with'
            if section == 'about_us':
                founders_data = fetch_founders()
                work_with_data = fetch_who_we_work_with()

            # Special handling for services section to get all services
            if section == 'services':
                services_data = data

    return render_template('admin.html',
                           current_section=section,
                           section_titles=section_titles,
                           data=current_data,
                           client_logos=client_logos,
                           founders=founders_data,
                           work_with=work_with_data,
                           services=services_data,
                           contact_submissions=contact_submissions_data) # Pass contact submissions

@app.route('/admin/<section>', methods=['POST'])
@admin_required
def admin_update(section):
    """Handle admin form submissions."""

    section_titles = {
        'nav': 'Navigation Settings',
        'hero': 'Hero Section',
        'clients': 'Our Clients',
        'innovations': 'Innovations Section',
        'know': 'Know Section',
        'statistics': 'Statistics Section',
        'footer': 'Footer Links',
        'about_us': 'About Us Page',
        'services': 'Services Management',
        'contact_submissions': 'Contact Submissions'
    }

    table_mapping = {
        'nav': 'navTable',
        'hero': 'heroTable',
        'clients': 'Ourclients',
        'innovations': 'innovations',
        'know': 'know',
        'statistics': 'statistics',
        'footer': 'footer',
        'about_us': 'aboutUs',
        'services': 'servicesTable',
        'contact_submissions': 'contact_submissions'
    }

    if section not in table_mapping:
        flash('Invalid section specified.', 'error')
        return redirect(url_for('admin', section=section))

    form_data = request.form.to_dict()

    # Handle file uploads
    uploaded_files = {}
    for field_name in request.files:
        file = request.files[field_name]
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to prevent filename conflicts
            import time
            timestamp = str(int(time.time()))
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{timestamp}{ext}"

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploaded_files[field_name] = f"/static/uploads/{filename}"

    # Special handling for hero section
    if section == 'hero':
        # Handle hero image - keep existing if no new upload
        if 'heroImg' in uploaded_files:
            form_data['heroImg'] = uploaded_files['heroImg']
        elif 'existingHeroImg' in form_data and form_data['existingHeroImg']:
            form_data['heroImg'] = form_data['existingHeroImg']

        # Remove the helper fields
        form_data.pop('existingHeroImg', None)

        # Clean up empty values
        form_data = {k: v for k, v in form_data.items() if v}

        if form_data and update_data(table_mapping[section], form_data):
            flash('Hero section updated successfully!', 'success')
        elif not form_data:
            flash('No changes to update.', 'warning')
        else:
            flash('Error updating hero section. Please try again.', 'error')

        return redirect(url_for('admin', section=section))

    # Special handling for services section
    if section == 'services':
        services_to_update = []
        service_heads = request.form.getlist('service_head') # Corrected name
        service_descs = request.form.getlist('service_desc') # Corrected name

        for i in range(len(service_heads)):
            if service_heads[i].strip() and service_descs[i].strip():
                services_to_update.append({
                    'service_head': service_heads[i].strip(),
                    'service_desc': service_descs[i].strip()
                })

        if update_services(services_to_update):
            flash('Services updated successfully!', 'success')
        else:
            flash('Error updating services.', 'error')

        return redirect(url_for('admin', section=section))

    # Special handling for client logos
    elif section == 'clients':
        # Get data for the Ourclients table
        client_section_data = {
            'clientHead': form_data.get('clientHead'),
            'clientDesc': form_data.get('clientDesc')
        }

        # Clean up empty values
        client_section_data = {k: v for k, v in client_section_data.items() if v}

        # Update the main Ourclients table
        if client_section_data and update_data(table_mapping[section], client_section_data):
            flash('Client section details updated successfully!', 'success')
        elif not client_section_data:
            flash('No changes to update for client section details.', 'warning')
        else:
            flash(f'Error updating {section_titles.get(section, "section")} details. Please try again.', 'error')

        # Now handle logos separately
        new_logos = []

        # Collect existing logos from hidden fields
        existing_logos_from_form = request.form.getlist('existingLogoUrl')

        # Process new uploads and existing logos
        i = 1
        while True:
            file_field_name = f'clientLogo{i}'
            if file_field_name in uploaded_files:
                new_logos.append(uploaded_files[file_field_name])
            elif i - 1 < len(existing_logos_from_form) and existing_logos_from_form[i - 1]:
                new_logos.append(existing_logos_from_form[i - 1])
            else:
                break
            i += 1

        # Update client logos in a separate table
        if new_logos:
            if update_client_logos(new_logos):
                flash('Client logos updated successfully!', 'success')
            else:
                flash('Error updating client logos.', 'error')
        else:
            # If all logos are removed, the list is empty, and we clear the table
            if update_client_logos([]):
                flash('All client logos deleted successfully!', 'success')
            else:
                flash('Error deleting client logos.', 'error')

        return redirect(url_for('admin', section=section))

    # Special handling for About Us section
    elif section == 'about_us':
        # Handle aboutHeroImage - keep existing if no new upload
        if 'aboutHeroImage' in uploaded_files:
            form_data['aboutHeroImage'] = uploaded_files['aboutHeroImage']
        elif 'existingAboutHeroImage' in form_data and form_data['existingAboutHeroImage']:
            form_data['aboutHeroImage'] = form_data['existingAboutHeroImage']

        # Remove helper fields
        form_data.pop('existingAboutHeroImage', None)

        # Separate data for different tables
        about_us_data = {
            'about_head': form_data.get('about_head'),
            'about_desc': form_data.get('about_desc'),
            'aboutHeroImage': form_data.get('aboutHeroImage'),
            'about_title': form_data.get('about_title'),
            'about_subtitle': form_data.get('about_subtitle'),
            'about_secondary_desc': form_data.get('about_secondary_desc'),
            'achievement_title': form_data.get('achievement_title'),
            'achievement_subtitle': form_data.get('achievement_subtitle'),
            'mission_text': form_data.get('mission_text'),
            'belief1': form_data.get('belief1'),
            'belief2': form_data.get('belief2'),
            'belief3': form_data.get('belief3'),
            'belief4': form_data.get('belief4')
        }

        # Clean up empty values to avoid overwriting existing data with blanks
        about_us_data = {k: v for k, v in about_us_data.items() if v}

        # Update the main `aboutUs` table
        if about_us_data and update_data(table_mapping[section], about_us_data):
            flash('About Us page content updated successfully!', 'success')
        elif not about_us_data:
            flash('No changes to update for About Us content.', 'warning')
        else:
            flash('Error updating About Us content.', 'error')

        # Handle founders
        founders_to_update = []
        # Corrected field names for form.getlist
        founder_names = request.form.getlist('founder_name') 
        founder_roles = request.form.getlist('founder_role')
        founder_descs = request.form.getlist('founder_description')
        existing_founder_images = request.form.getlist('existing_founder_image')


        for i in range(len(founder_names)):
            if founder_names[i].strip():  # Only process if name is provided
                # Check for uploaded file first, then existing hidden field
                founder_image = uploaded_files.get(f'founder_image_{i}') # Adjusted name for multiple files
                if not founder_image and i < len(existing_founder_images):
                    founder_image = existing_founder_images[i]

                founders_to_update.append({
                    'founder_name': founder_names[i],
                    'founder_role': founder_roles[i] if i < len(founder_roles) else '',
                    'founder_description': founder_descs[i] if i < len(founder_descs) else '',
                    'founder_image': founder_image or ''
                })

        if update_founders(founders_to_update):
            flash('Founders updated successfully!', 'success')
        else:
            flash('Error updating founders.', 'error')

        # Handle 'who we work with'
        work_with_to_update = []
        # Corrected field names for form.getlist
        work_icons = request.form.getlist('work_icon') 
        work_titles = request.form.getlist('work_title')
        work_descs = request.form.getlist('work_description')

        for i in range(len(work_icons)):
            if work_icons[i].strip():  # Only process if icon is provided
                work_with_to_update.append({
                    'work_icon': work_icons[i],
                    'work_title': work_titles[i] if i < len(work_titles) else '',
                    'work_description': work_descs[i] if i < len(work_descs) else ''
                })

        if update_who_we_work_with(work_with_to_update):
            flash('"Who We Work With" section updated successfully!', 'success')
        else:
            flash('Error updating "Who We Work With" section.', 'error')

        return redirect(url_for('admin', section=section))

    # Update form_data with uploaded file paths
    for field_name, file_path in uploaded_files.items():
        form_data[field_name] = file_path

    # Remove empty values to prevent overwriting existing data with blanks
    form_data = {k: v for k, v in form_data.items() if v}

    # Special handling for media type selection
    if section in ['innovations', 'know']:
        media_type_field = f"{section[:-1] if section.endswith('s') else section}MediaType"
        if section == 'innovations':
            media_type_field = "innovationMediaType"
        elif section == 'know':
            media_type_field = "knowMediaType"

        if media_type_field in form_data:
            if form_data[media_type_field] == 'video':
                image_field = f"{section[:-1] if section.endswith('s') else section}Image"
                if section == 'innovations':
                    image_field = "innovationImage"
                elif section == 'know':
                    image_field = "knowImage"
                if image_field in form_data: del form_data[image_field]
            elif form_data[media_type_field] == 'image':
                video_field = f"{section[:-1] if section.endswith('s') else section}Video"
                if section == 'innovations':
                    video_field = "innovationVideo"
                elif section == 'know':
                    video_field = "knowVideo"
                if video_field in form_data: del form_data[video_field]

    if form_data and update_data(table_mapping[section], form_data):
        flash(f'{section_titles.get(section, "Section")} updated successfully!', 'success')
    elif not form_data:
        flash('No changes to update.', 'warning')
    else:
        flash(f'Error updating {section_titles.get(section, "section")}. Please try again.', 'error')

    return redirect(url_for('admin', section=section))
# Add these functions and routes to your app.py file

def fetch_blog_posts(status='published', limit=None):
    """Fetches blog posts from the database."""
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        if limit:
            cursor.execute("SELECT * FROM blog_posts WHERE blog_status = %s ORDER BY blog_date DESC LIMIT %s", (status, limit))
        else:
            cursor.execute("SELECT * FROM blog_posts WHERE blog_status = %s ORDER BY blog_date DESC", (status,))
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        print(f"Error fetching blog posts: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_blog_post_by_id(blog_id):
    """Fetches a single blog post by ID."""
    conn = get_db_connection()
    if conn is None:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM blog_posts WHERE blog_id = %s", (blog_id,))
        data = cursor.fetchone()
        return data
    except mysql.connector.Error as err:
        print(f"Error fetching blog post: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_blog_post(post_data):
    """Creates a new blog post."""
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        query = """INSERT INTO blog_posts 
                   (blog_title, blog_subtitle, blog_author, blog_date, blog_image, 
                    blog_excerpt, blog_content, blog_status) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (
            post_data['blog_title'],
            post_data['blog_subtitle'],
            post_data['blog_author'],
            post_data['blog_date'],
            post_data.get('blog_image', ''),
            post_data['blog_excerpt'],
            post_data['blog_content'],
            post_data.get('blog_status', 'published')
        ))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error creating blog post: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_blog_post(blog_id, post_data):
    """Updates an existing blog post."""
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        # Filter out empty values
        filtered_data = {k: v for k, v in post_data.items() if v}
        
        if not filtered_data:
            return False
        
        set_clause = ', '.join([f"{key} = %s" for key in filtered_data.keys()])
        values = list(filtered_data.values())
        values.append(blog_id)
        
        query = f"UPDATE blog_posts SET {set_clause} WHERE blog_id = %s"
        cursor.execute(query, values)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating blog post: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_blog_post(blog_id):
    """Deletes a blog post."""
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM blog_posts WHERE blog_id = %s", (blog_id,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error deleting blog post: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Public Blog Routes
@app.route('/news')
def news():
    """Renders the news/blog listing page."""
    blog_posts = fetch_blog_posts()
    base_data_dict = base_data()
    return render_template('news.html', blog_posts=blog_posts, **base_data_dict)

@app.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    """Renders a single blog post detail page."""
    blog_post = fetch_blog_post_by_id(blog_id)
    if not blog_post:
        flash('Blog post not found.', 'error')
        return redirect(url_for('news'))
    
    base_data_dict = base_data()
    # Get related posts (exclude current post)
    related_posts = fetch_blog_posts(limit=3)
    related_posts = [post for post in related_posts if post['blog_id'] != blog_id][:3]
    
    return render_template('blog_detail.html', 
                         blog_post=blog_post, 
                         related_posts=related_posts,
                         **base_data_dict)

# Admin Blog Routes
@app.route('/admin/blogs')
@admin_required
def admin_blogs():
    """Admin blog management page."""
    blog_posts = fetch_blog_posts(status='published')
    draft_posts = fetch_blog_posts(status='draft')
    return render_template('admin_blogs.html', 
                         blog_posts=blog_posts, 
                         draft_posts=draft_posts)

@app.route('/admin/blogs/create', methods=['GET', 'POST'])
@admin_required
def admin_blog_create():
    """Create new blog post."""
    if request.method == 'POST':
        # Handle file upload
        blog_image = ''
        if 'blog_image' in request.files:
            file = request.files['blog_image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                import time
                timestamp = str(int(time.time()))
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{timestamp}{ext}"
                
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                blog_image = f"/static/uploads/{filename}"
        
        post_data = {
            'blog_title': request.form.get('blog_title'),
            'blog_subtitle': request.form.get('blog_subtitle'),
            'blog_author': request.form.get('blog_author'),
            'blog_date': request.form.get('blog_date'),
            'blog_image': blog_image,
            'blog_excerpt': request.form.get('blog_excerpt'),
            'blog_content': request.form.get('blog_content'),
            'blog_status': request.form.get('blog_status', 'published')
        }
        
        if create_blog_post(post_data):
            flash('Blog post created successfully!', 'success')
            return redirect(url_for('admin_blogs'))
        else:
            flash('Error creating blog post.', 'error')
    
    return render_template('admin_blog_form.html', action='create')

@app.route('/admin/blogs/<int:blog_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_blog_edit(blog_id):
    """Edit existing blog post."""
    blog_post = fetch_blog_post_by_id(blog_id)
    if not blog_post:
        flash('Blog post not found.', 'error')
        return redirect(url_for('admin_blogs'))
    
    if request.method == 'POST':
        # Handle file upload
        blog_image = blog_post.get('blog_image', '')
        if 'blog_image' in request.files:
            file = request.files['blog_image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                import time
                timestamp = str(int(time.time()))
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{timestamp}{ext}"
                
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                blog_image = f"/static/uploads/{filename}"
        
        post_data = {
            'blog_title': request.form.get('blog_title'),
            'blog_subtitle': request.form.get('blog_subtitle'),
            'blog_author': request.form.get('blog_author'),
            'blog_date': request.form.get('blog_date'),
            'blog_image': blog_image,
            'blog_excerpt': request.form.get('blog_excerpt'),
            'blog_content': request.form.get('blog_content'),
            'blog_status': request.form.get('blog_status', 'published')
        }
        
        if update_blog_post(blog_id, post_data):
            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('admin_blogs'))
        else:
            flash('Error updating blog post.', 'error')
    
    return render_template('admin_blog_form.html', action='edit', blog_post=blog_post)

@app.route('/admin/blogs/<int:blog_id>/delete', methods=['POST'])
@admin_required
def admin_blog_delete(blog_id):
    """Delete blog post."""
    if delete_blog_post(blog_id):
        flash('Blog post deleted successfully!', 'success')
    else:
        flash('Error deleting blog post.', 'error')
    
    return redirect(url_for('admin_blogs'))

@app.errorhandler(500)
def internal_error(error):
    flash('An internal error occurred. Please try again later.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
