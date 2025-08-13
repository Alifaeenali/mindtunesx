import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import json
import hashlib
from datetime import datetime
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, session, make_response, jsonify
from werkzeug.utils import secure_filename
import mysql.connector
from dotenv import load_dotenv
from io import StringIO
import csv
import re
import time
from flask import Flask

# Load environment variables
load_dotenv()
 
app = Flask(__name__)
# IMPORTANT: Use environment variables for sensitive data in production
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-change-this-in-production')

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
# Fixed: Hash the password properly
admin_password = os.getenv('ADMIN_PASSWORD_HASH', '12345')
ADMIN_PASSWORD = hashlib.sha256(admin_password.encode()).hexdigest()

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_FROM_NAME = os.getenv('EMAIL_FROM_NAME', 'MindTune Innovations')


# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'ogg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database configuration

CV_UPLOAD_FOLDER = 'static/uploads/cvs'
ALLOWED_CV_EXTENSIONS = {'pdf'}
app.config['CV_UPLOAD_FOLDER'] = CV_UPLOAD_FOLDER
app.config['MAX_CV_SIZE'] = 10 * 1024 * 1024  # 10MB max CV size

# Create CV upload directory if it doesn't exist
os.makedirs(CV_UPLOAD_FOLDER, exist_ok=True)

def allowed_cv_file(filename):
    """Check if CV file has allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_CV_EXTENSIONS

# =================================================================================================
# Email Configuration using smtplib
# =================================================================================================

class EmailService:
    """Email service using smtplib for sending emails."""
    
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.email_user = EMAIL_USER
        self.email_password = EMAIL_PASSWORD
        self.from_name = EMAIL_FROM_NAME
    
    def test_connection(self):
        """Test SMTP connection and authentication."""
        try:
            # Create SMTP session
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable TLS encryption
            server.login(self.email_user, self.email_password)
            server.quit()
            return True, "Connection successful"
        except smtplib.SMTPAuthenticationError as e:
            return False, f"Authentication failed: {str(e)}"
        except smtplib.SMTPConnectError as e:
            return False, f"Connection failed: {str(e)}"
        except smtplib.SMTPException as e:
            return False, f"SMTP error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def send_email(self, to_emails, subject, body, html_body=None, attachments=None):
        """
        Send email using smtplib.
        
        Args:
            to_emails: List of email addresses or single email string
            subject: Email subject
            body: Plain text body
            html_body: Optional HTML body
            attachments: List of file paths to attach
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Ensure to_emails is a list
            if isinstance(to_emails, str):
                to_emails = [to_emails]
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.email_user}>"
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject
            
            # Add plain text part
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html', 'utf-8')
                msg.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for file_path in attachments:
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
            
            # Create SMTP session and send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable TLS encryption
            server.login(self.email_user, self.email_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.email_user, to_emails, text)
            server.quit()
            
            print(f"Email sent successfully to: {', '.join(to_emails)}")
            return True, "Email sent successfully"
            
        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"Authentication failed: {str(e)}"
            print(error_msg)
            return False, error_msg
        except smtplib.SMTPRecipientsRefused as e:
            error_msg = f"Recipients refused: {str(e)}"
            print(error_msg)
            return False, error_msg
        except smtplib.SMTPException as e:
            error_msg = f"SMTP error: {str(e)}"
            print(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(error_msg)
            return False, error_msg
    
    def send_html_email(self, to_emails, subject, html_content, plain_text_fallback=None):
        """Send HTML email with optional plain text fallback."""
        if plain_text_fallback is None:
            # Create simple plain text version by stripping HTML tags
            plain_text_fallback = re.sub('<[^<]+?>', '', html_content)
        
        return self.send_email(to_emails, subject, plain_text_fallback, html_content)

# Initialize email service
email_service = EmailService()

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

        query = "INSERT INTO servicesTable (service_head, service_icon, service_desc) VALUES (%s, %s, %s)"
        for service in services_list:
            cursor.execute(query, (
                service['service_head'], 
                service.get('service_icon', 'fas fa-cogs'),  # Default icon if not provided
                service['service_desc']
            ))
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
# ========================================================team members
def fetch_team_members():
    """Fetches all active team members from the database."""
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM team_members WHERE member_status = 'active' ORDER BY team_order")
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        print(f"Error fetching team members: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_team_members(team_members_list):
    """Updates the team members in the database by clearing existing and inserting new ones."""
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        # Clear existing active team members
        cursor.execute("DELETE FROM team_members WHERE member_status = 'active'")

        query = """INSERT INTO team_members 
                   (member_name, member_position, member_description, member_image, team_order, member_status) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        for i, member in enumerate(team_members_list, 1):
            cursor.execute(query, (
                member['member_name'], 
                member['member_position'], 
                member['member_description'], 
                member['member_image'], 
                i, 
                'active'
            ))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating team members: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# =================================================================================================
# Contact Form Database Functions
# =================================================================================================
def create_contact_submissions_table():
    """Creates the contact_submissions table if it doesn't exist."""
    conn = get_db_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_submissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                subject TEXT,
                message TEXT,
                submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status ENUM('new', 'read', 'replied', 'archived') DEFAULT 'new',
                priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
                assigned_to VARCHAR(255),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error creating contact_submissions table: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def add_contact_submission(name, email, subject, message, status='new', priority='medium'):
    """Adds a new contact form submission to the database."""
    conn = get_db_connection()
    if conn is None:
        print("Database connection failed")
        return False
    
    cursor = conn.cursor()
    try:
        # Use the correct table structure
        query = """INSERT INTO contact_submissions 
                   (name, email, subject, message, submission_date, status, priority) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (name, email, subject, message, datetime.now(), status, priority))
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

def fetch_contact_submissions():
    """Fetches all contact form submissions from the database."""
    conn = get_db_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""SELECT id, name, email, subject, message, submission_date, status, priority, notes 
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

def get_contact_submissions_stats():
    """Gets statistics about contact submissions."""
    conn = get_db_connection()
    if conn is None:
        return {'total': 0, 'this_week': 0, 'today': 0}
    
    cursor = conn.cursor(dictionary=True)
    try:
        # Get total submissions
        cursor.execute("SELECT COUNT(*) as total FROM contact_submissions")
        total = cursor.fetchone()['total']
        
        # Get this week's submissions
        cursor.execute("""
            SELECT COUNT(*) as this_week 
            FROM contact_submissions 
            WHERE submission_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        """)
        this_week = cursor.fetchone()['this_week']
        
        # Get today's submissions
        cursor.execute("""
            SELECT COUNT(*) as today 
            FROM contact_submissions 
            WHERE DATE(submission_date) = CURDATE()
        """)
        today = cursor.fetchone()['today']
        
        return {
            'total': total,
            'this_week': this_week,
            'today': today
        }
    except mysql.connector.Error as err:
        print(f"Error fetching contact submission stats: {err}")
        return {'total': 0, 'this_week': 0, 'today': 0}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_contact_submission(submission_id):
    """Deletes a contact form submission by ID."""
    conn = get_db_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM contact_submissions WHERE id = %s", (submission_id,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print(f"Error deleting contact submission: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_contact_submission_by_id(submission_id):
    """Fetches a single contact submission by ID."""
    conn = get_db_connection()
    if conn is None:
        return None
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM contact_submissions WHERE id = %s", (submission_id,))
        data = cursor.fetchone()
        return data
    except mysql.connector.Error as err:
        print(f"Error fetching contact submission: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_submission_status(submission_id, status, notes=''):
    """Updates the status and notes of a contact submission."""
    conn = get_db_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE contact_submissions 
            SET status = %s, notes = %s, updated_at = %s 
            WHERE id = %s
        """, (status, notes, datetime.now(), submission_id))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print(f"Error updating submission status: {err}")
        return False
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

# =================================================================================================
# Public Routes
# =================================================================================================
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
    team_members_data = fetch_team_members()

    return render_template('about.html',
                           aboutData=about_us,
                           founders=founders_data,
                           work_with=who_we_work_with_data,
                           team_members=team_members_data,
                           **base_data_dict)

@app.route('/services')
def services():
    """Renders the services page with data from the servicesTable."""
    services_data = fetch_data('servicesTable')
    base_data_dict = base_data()
    return render_template('services.html', servicesList=services_data, **base_data_dict)

# =================================================================================================
# Contact Form Route with Email Integration
# =================================================================================================
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Enhanced contact form with smtplib email handling."""
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
            return render_template('contact.html', **base_data_dict)

        # Combine first and last name
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
- Company Size: {num_employees}

Project Details:
{additional_details}
        """.strip()

        # Save to database first (so it's saved even if email fails)
        db_saved = add_contact_submission(full_name, email, subject_line, comprehensive_message)
        
        # Prepare admin email
        admin_subject = f"New Contact Submission: {subject_line}"
        admin_body = f"""
You have received a new contact form submission:

Name: {full_name}
Email: {email}
Phone: {phone_number}
Job Title: {job_title}
Company: {company_name}
Industry: {industry}
Company Size: {num_employees}

Project Details:
{additional_details}

---
This message was sent from the MindTune Innovations contact form.
Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()

        # Prepare user confirmation email
        user_subject = "Thank you for contacting MindTune Innovations"
        user_body = f"""
Dear {first_name},

Thank you for reaching out to MindTune Innovations. We have received your project inquiry and will get back to you within 24 hours.

Here's a summary of your submission:
- Project: {additional_details[:100]}{'...' if len(additional_details) > 100 else ''}
- Company: {company_name if company_name else 'Not specified'}
- Industry: {industry if industry else 'Not specified'}

Our team will review your request and contact you shortly to discuss how we can help bring your vision to life.

Best regards,
MindTune Innovations Team

---
If you have any urgent questions, feel free to reply to this email or call us directly.
        """.strip()

        # Send emails
        email_results = []
        
        # Send to admin
        admin_success, admin_msg = email_service.send_email(
            EMAIL_USER,  # Send to admin email
            admin_subject, 
            admin_body
        )
        email_results.append(('admin', admin_success, admin_msg))
        
        # Send confirmation to user
        user_success, user_msg = email_service.send_email(
            email, 
            user_subject, 
            user_body
        )
        email_results.append(('user', user_success, user_msg))

        # Determine final message based on results
        if db_saved and admin_success and user_success:
            flash('Your message has been sent successfully! We will get back to you within 24 hours.', 'success')
        elif db_saved and (admin_success or user_success):
            flash('Your message has been received and saved. We will contact you soon.', 'warning')
        elif db_saved:
            flash('Your message has been saved. We will contact you soon. (Email delivery issue - please check your email or contact us directly)', 'warning')
        else:
            flash('There was an error processing your message. Please try again or contact us directly.', 'error')
            
        # Log email results for debugging
        for recipient, success, msg in email_results:
            print(f"Email to {recipient}: {'SUCCESS' if success else 'FAILED'} - {msg}")

        return redirect(url_for('contact'))
    
    return render_template('contact.html', **base_data_dict)

# =================================================================================================
# API Route for Services Data
# =================================================================================================
@app.route('/api/services')
def show_services_data():
    """Fetches and displays all services data as JSON."""
    services_data = fetch_data('servicesTable')
    return jsonify(services_data)

# =================================================================================================
# Admin Routes
# =================================================================================================
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
        'contact_submissions': 'Contact Submissions'
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
        'contact_submissions': 'contact_submissions'
    }

    current_data = {}
    client_logos = []
    founders_data = []
    work_with_data = []
    team_members_data = []
    services_data = []
    contact_submissions_data = []
    contact_stats = {}

    if section and section in table_mapping:
        if section == 'contact_submissions':
            contact_submissions_data = fetch_contact_submissions()
            contact_stats = get_contact_submissions_stats()
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
                team_members_data = fetch_team_members() 

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
                           team_members=team_members_data,
                           services=services_data,
                           contact_submissions=contact_submissions_data,
                           contact_stats=contact_stats)

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
        service_heads = request.form.getlist('service_head')
        service_icons = request.form.getlist('service_icon')
        service_descs = request.form.getlist('service_desc')

        for i in range(len(service_heads)):
            if service_heads[i].strip() and service_descs[i].strip():
                services_to_update.append({
                    'service_head': service_heads[i].strip(),
                    'service_icon': service_icons[i].strip() if i < len(service_icons) and service_icons[i].strip() else 'fas fa-cogs',
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
        founder_names = request.form.getlist('founder_name') 
        founder_roles = request.form.getlist('founder_role')
        founder_descs = request.form.getlist('founder_description')
        existing_founder_images = request.form.getlist('existing_founder_image')

        for i in range(len(founder_names)):
            if founder_names[i].strip():  # Only process if name is provided
                # Check for uploaded file first, then existing hidden field
                founder_image = uploaded_files.get(f'founder_image_{i}')
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

        # Handle team members
        team_members_to_update = []
        team_names = request.form.getlist('team_member_name') 
        team_positions = request.form.getlist('team_member_position')
        team_descriptions = request.form.getlist('team_member_description')
        existing_team_images = request.form.getlist('existing_team_member_image')

        for i in range(len(team_names)):
            if team_names[i].strip():  # Only process if name is provided
                # Check for uploaded file first, then existing hidden field
                team_image = uploaded_files.get(f'team_member_image_{i}')
                if not team_image and i < len(existing_team_images):
                    team_image = existing_team_images[i]

                team_members_to_update.append({
                    'member_name': team_names[i],
                    'member_position': team_positions[i] if i < len(team_positions) else '',
                    'member_description': team_descriptions[i] if i < len(team_descriptions) else '',
                    'member_image': team_image or ''
                })

        if update_team_members(team_members_to_update):
            flash('Team members updated successfully!', 'success')
        else:
            flash('Error updating team members.', 'error')

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

# =================================================================================================
# Admin Email Test Route
# =================================================================================================
@app.route('/admin/test-email', methods=['GET', 'POST'])
@admin_required
def admin_test_email():
    """Test email configuration."""
    if request.method == 'POST':
        test_email = request.form.get('test_email', EMAIL_USER)
        
        # Test connection first
        conn_success, conn_msg = email_service.test_connection()
        
        if conn_success:
            # Send test email
            test_subject = "Test Email from MindTune Innovations"
            test_body = f"""
This is a test email to verify your email configuration is working correctly.

Email Configuration:
- SMTP Server: {SMTP_SERVER}
- SMTP Port: {SMTP_PORT}
- From Email: {EMAIL_USER}

Test sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

If you received this email, your configuration is working properly!
            """.strip()
            
            success, msg = email_service.send_email(
                test_email,
                test_subject,
                test_body
            )
            
            if success:
                flash(f'Test email sent successfully to {test_email}!', 'success')
            else:
                flash(f'Failed to send test email: {msg}', 'error')
        else:
            flash(f'Email connection test failed: {conn_msg}', 'error')
    
    # Get current configuration for display
    config_info = {
        'SMTP_SERVER': SMTP_SERVER,
        'SMTP_PORT': SMTP_PORT,
        'EMAIL_USER': EMAIL_USER,
        'EMAIL_PASSWORD': '****** (Set)' if EMAIL_PASSWORD else 'NOT SET',
        'FROM_NAME': EMAIL_FROM_NAME
    }
    
    return render_template('admin_test_email_smtp.html', config=config_info)

# =================================================================================================
# Contact Submission Management Routes
# =================================================================================================
@app.route('/admin/contact/<int:submission_id>/delete', methods=['POST'])
@admin_required
def delete_contact_submission_route(submission_id):
    """Delete a contact submission."""
    if delete_contact_submission(submission_id):
        flash('Contact submission deleted successfully!', 'success')
    else:
        flash('Error deleting contact submission.', 'error')
    
    return redirect(url_for('admin', section='contact_submissions'))

@app.route('/admin/contact/<int:submission_id>/view')
@admin_required
def view_contact_submission(submission_id):
    """View a single contact submission (AJAX endpoint)."""
    submission = get_contact_submission_by_id(submission_id)
    if not submission:
        return {'error': 'Submission not found'}, 404
    
    # Format the submission data for JSON response
    submission_data = {
        'id': submission['id'],
        'name': submission['name'],
        'email': submission['email'],
        'subject': submission['subject'],
        'message': submission['message'],
        'submission_date': submission['submission_date'].strftime('%Y-%m-%d %H:%M:%S') if submission['submission_date'] else None,
        'status': submission.get('status', 'new'),
        'priority': submission.get('priority', 'medium'),
        'notes': submission.get('notes', '')
    }
    
    return jsonify(submission_data)

@app.route('/admin/contact/<int:submission_id>/status', methods=['POST'])
@admin_required
def update_contact_status(submission_id):
    """Update contact submission status."""
    status = request.form.get('status')
    notes = request.form.get('notes', '')
    
    if update_submission_status(submission_id, status, notes):
        flash('Submission status updated successfully!', 'success')
    else:
        flash('Error updating submission status.', 'error')
    
    return redirect(url_for('admin', section='contact_submissions'))

@app.route('/admin/contact/export')
@admin_required
def export_contact_submissions():
    """Export contact submissions as CSV."""
    submissions = fetch_contact_submissions()
    
    # Create CSV content
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'ID', 'Name', 'Email', 'Subject', 'Company', 'Industry', 
        'Phone', 'Job Title', 'Company Size', 'Project Details', 'Status', 
        'Priority', 'Notes', 'Submission Date'
    ])
    
    # Write data
    for submission in submissions:
        # Parse message to extract structured data
        message = submission['message']
        company = ''
        industry = ''
        phone = ''
        job_title = ''
        company_size = ''
        project_details = ''
        
        # Extract data from message using simple string parsing
        lines = message.split('\n')
        in_project_section = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('- Company:'):
                company = line.replace('- Company:', '').strip()
            elif line.startswith('- Industry:'):
                industry = line.replace('- Industry:', '').strip()
            elif line.startswith('- Phone:'):
                phone = line.replace('- Phone:', '').strip()
            elif line.startswith('- Job Title:'):
                job_title = line.replace('- Job Title:', '').strip()
            elif line.startswith('- Number of Employees:') or line.startswith('- Company Size:'):
                company_size = line.split(':', 1)[1].strip() if ':' in line else ''
            elif line == 'Project Details:':
                in_project_section = True
            elif in_project_section and line:
                project_details += line + ' '
        
        writer.writerow([
            submission['id'],
            submission['name'],
            submission['email'],
            submission['subject'],
            company,
            industry,
            phone,
            job_title,
            company_size,
            project_details.strip(),
            submission.get('status', 'new'),
            submission.get('priority', 'medium'),
            submission.get('notes', ''),
            submission['submission_date'].strftime('%Y-%m-%d %H:%M:%S') if submission['submission_date'] else ''
        ])
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=contact_submissions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response

@app.route('/admin/contact/bulk-delete', methods=['POST'])
@admin_required
def bulk_delete_contact_submissions():
    """Bulk delete contact submissions."""
    submission_ids = request.form.getlist('submission_ids')
    
    if not submission_ids:
        flash('No submissions selected for deletion.', 'warning')
        return redirect(url_for('admin', section='contact_submissions'))
    
    conn = get_db_connection()
    if conn is None:
        flash('Database connection error.', 'error')
        return redirect(url_for('admin', section='contact_submissions'))
    
    cursor = conn.cursor()
    deleted_count = 0
    
    try:
        for submission_id in submission_ids:
            cursor.execute("DELETE FROM contact_submissions WHERE id = %s", (submission_id,))
            if cursor.rowcount > 0:
                deleted_count += 1
        conn.commit()
        
        if deleted_count > 0:
            flash(f'Successfully deleted {deleted_count} submission(s).', 'success')
        else:
            flash('No submissions were deleted.', 'warning')
            
    except mysql.connector.Error as err:
        print(f"Error bulk deleting submissions: {err}")
        flash('Error deleting submissions.', 'error')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return redirect(url_for('admin', section='contact_submissions'))

# =================================================================================================
# Blog Management Functions and Routes (if needed)
# =================================================================================================
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

# =================================================================================================
# Career/Job Management Functions and Routes
# =================================================================================================
def fetch_job_postings(status='active'):
    """Fetches job postings from the database."""
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        if status:
            cursor.execute("SELECT * FROM job_postings WHERE job_status = %s ORDER BY posted_date DESC", (status,))
        else:
            cursor.execute("SELECT * FROM job_postings ORDER BY posted_date DESC")
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        print(f"Error fetching job postings: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_job_posting_by_id(job_id):
    """Fetches a single job posting by ID."""
    conn = get_db_connection()
    if conn is None:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM job_postings WHERE job_id = %s", (job_id,))
        data = cursor.fetchone()
        return data
    except mysql.connector.Error as err:
        print(f"Error fetching job posting: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_job_posting(job_data):
    """Creates a new job posting."""
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        query = """INSERT INTO job_postings 
                   (job_title, job_type, department, location, salary_range, 
                    job_description, requirements, responsibilities, benefits, 
                    application_deadline, job_status) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (
            job_data['job_title'],
            job_data['job_type'],
            job_data['department'],
            job_data['location'],
            job_data.get('salary_range', ''),
            job_data['job_description'],
            job_data['requirements'],
            job_data['responsibilities'],
            job_data.get('benefits', ''),
            job_data.get('application_deadline'),
            job_data.get('job_status', 'active')
        ))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error creating job posting: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_job_posting(job_id, job_data):
    """Updates an existing job posting."""
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        # Filter out empty values
        filtered_data = {k: v for k, v in job_data.items() if v}
        
        if not filtered_data:
            return False
        
        set_clause = ', '.join([f"{key} = %s" for key in filtered_data.keys()])
        values = list(filtered_data.values())
        values.append(job_id)
        
        query = f"UPDATE job_postings SET {set_clause} WHERE job_id = %s"
        cursor.execute(query, values)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating job posting: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_job_posting(job_id):
    """Deletes a job posting."""
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM job_postings WHERE job_id = %s", (job_id,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error deleting job posting: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_job_application(application_data):
    """Creates a new job application."""
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        query = """INSERT INTO job_applications 
                   (job_id, applicant_name, applicant_email, applicant_phone, 
                    cover_letter, cv_filename, cv_path, linkedin_profile, 
                    portfolio_website, expected_salary, availability_date, 
                    application_status) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (
            application_data['job_id'],
            application_data['applicant_name'],
            application_data['applicant_email'],
            application_data.get('applicant_phone', ''),
            application_data.get('cover_letter', ''),
            application_data['cv_filename'],
            application_data['cv_path'],
            application_data.get('linkedin_profile', ''),
            application_data.get('portfolio_website', ''),
            application_data.get('expected_salary', ''),
            application_data.get('availability_date'),
            'pending'
        ))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error creating job application: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_job_applications():
    """Fetches all job applications with job details."""
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        query = """SELECT ja.*, jp.job_title, jp.department 
                   FROM job_applications ja 
                   JOIN job_postings jp ON ja.job_id = jp.job_id 
                   ORDER BY ja.applied_date DESC"""
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        print(f"Error fetching job applications: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_application_status(application_id, status, notes=''):
    """Updates job application status."""
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        query = "UPDATE job_applications SET application_status = %s, notes = %s WHERE application_id = %s"
        cursor.execute(query, (status, notes, application_id))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating application status: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Public Career Routes
@app.route('/careers')
def careers():
    """Renders the careers page with active job postings."""
    job_postings = fetch_job_postings('active')
    base_data_dict = base_data()
    return render_template('careers.html', job_postings=job_postings, **base_data_dict)

@app.route('/careers/<int:job_id>')
def job_detail(job_id):
    """Renders job detail page."""
    job_posting = fetch_job_posting_by_id(job_id)
    if not job_posting:
        flash('Job posting not found.', 'error')
        return redirect(url_for('careers'))
    
    base_data_dict = base_data()
    return render_template('job_detail.html', job=job_posting, **base_data_dict)

@app.route('/apply/<int:job_id>', methods=['POST'])
def apply_for_job(job_id):
    """Handle job application submission with smtplib."""
    job_posting = fetch_job_posting_by_id(job_id)
    if not job_posting:
        flash('Job posting not found.', 'error')
        return redirect(url_for('careers'))
    
    # Get form data
    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    applicant_phone = request.form.get('applicant_phone', '').strip()
    cover_letter = request.form.get('cover_letter', '').strip()
    linkedin_profile = request.form.get('linkedin_profile', '').strip()
    portfolio_website = request.form.get('portfolio_website', '').strip()
    expected_salary = request.form.get('expected_salary', '').strip()
    availability_date = request.form.get('availability_date', '').strip()
    
    # Validation
    if not applicant_name or not applicant_email:
        flash('Please fill in all required fields.', 'error')
        return redirect(url_for('job_detail', job_id=job_id))
    
    # Handle CV upload
    if 'cv_file' not in request.files:
        flash('CV file is required.', 'error')
        return redirect(url_for('job_detail', job_id=job_id))
    
    cv_file = request.files['cv_file']
    if cv_file.filename == '':
        flash('No CV file selected.', 'error')
        return redirect(url_for('job_detail', job_id=job_id))
    
    if not allowed_cv_file(cv_file.filename):
        flash('Only PDF files are allowed for CV upload.', 'error')
        return redirect(url_for('job_detail', job_id=job_id))
    
    # Save CV file
    try:
        filename = secure_filename(cv_file.filename)
        timestamp = str(int(time.time()))
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        cv_path = os.path.join(app.config['CV_UPLOAD_FOLDER'], filename)
        cv_file.save(cv_path)
        cv_url = f"/static/uploads/cvs/{filename}"
        
        # Create application
        application_data = {
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'applicant_phone': applicant_phone,
            'cover_letter': cover_letter,
            'cv_filename': filename,
            'cv_path': cv_url,
            'linkedin_profile': linkedin_profile,
            'portfolio_website': portfolio_website,
            'expected_salary': expected_salary,
            'availability_date': availability_date if availability_date else None
        }
        
        if create_job_application(application_data):
            # Send email notification to admin
            admin_subject = f"New Job Application: {job_posting['job_title']}"
            admin_body = f"""
New job application received:

Position: {job_posting['job_title']}
Applicant: {applicant_name}
Email: {applicant_email}
Phone: {applicant_phone}

Cover Letter:
{cover_letter}

LinkedIn: {linkedin_profile}
Portfolio: {portfolio_website}
Expected Salary: {expected_salary}
Availability: {availability_date}

The CV has been uploaded to the system. Please check the admin panel for the complete application.
            """.strip()
            
            admin_success, admin_msg = email_service.send_email(
                EMAIL_USER,  # Send to admin
                admin_subject,
                admin_body
            )
            
            # Send confirmation email to applicant
            user_subject = f"Application Received: {job_posting['job_title']}"
            user_body = f"""
Dear {applicant_name},

Thank you for your interest in the {job_posting['job_title']} position at MindTune Innovations.

We have received your application and will review it carefully. If your qualifications match our requirements, we will contact you within 1-2 weeks to discuss the next steps.

Best regards,
MindTune Innovations HR Team
            """.strip()
            
            user_success, user_msg = email_service.send_email(
                applicant_email,
                user_subject,
                user_body
            )
            
            # Log results
            print(f"Admin notification: {'SUCCESS' if admin_success else 'FAILED'} - {admin_msg}")
            print(f"User confirmation: {'SUCCESS' if user_success else 'FAILED'} - {user_msg}")
            
            flash('Your application has been submitted successfully! We will contact you soon.', 'success')
        else:
            flash('Error submitting application. Please try again.', 'error')
            
    except Exception as e:
        print(f"Error in job application: {e}")
        flash('Error processing application. Please try again.', 'error')
    
    return redirect(url_for('careers'))

# Admin Job Management Routes
@app.route('/admin/jobs')
@admin_required
def admin_jobs():
    """Admin job postings management page."""
    active_jobs = fetch_job_postings('active')
    draft_jobs = fetch_job_postings('draft')
    closed_jobs = fetch_job_postings('closed')
    return render_template('admin_jobs.html', 
                         active_jobs=active_jobs, 
                         draft_jobs=draft_jobs,
                         closed_jobs=closed_jobs)

@app.route('/admin/jobs/create', methods=['GET', 'POST'])
@admin_required
def admin_job_create():
    """Create new job posting."""
    if request.method == 'POST':
        job_data = {
            'job_title': request.form.get('job_title'),
            'job_type': request.form.get('job_type'),
            'department': request.form.get('department'),
            'location': request.form.get('location'),
            'salary_range': request.form.get('salary_range'),
            'job_description': request.form.get('job_description'),
            'requirements': request.form.get('requirements'),
            'responsibilities': request.form.get('responsibilities'),
            'benefits': request.form.get('benefits'),
            'application_deadline': request.form.get('application_deadline'),
            'job_status': request.form.get('job_status', 'active')
        }
        
        if create_job_posting(job_data):
            flash('Job posting created successfully!', 'success')
            return redirect(url_for('admin_jobs'))
        else:
            flash('Error creating job posting.', 'error')
    
    return render_template('admin_job_form.html', action='create')

@app.route('/admin/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_job_edit(job_id):
    """Edit existing job posting."""
    job_posting = fetch_job_posting_by_id(job_id)
    if not job_posting:
        flash('Job posting not found.', 'error')
        return redirect(url_for('admin_jobs'))
    
    if request.method == 'POST':
        job_data = {
            'job_title': request.form.get('job_title'),
            'job_type': request.form.get('job_type'),
            'department': request.form.get('department'),
            'location': request.form.get('location'),
            'salary_range': request.form.get('salary_range'),
            'job_description': request.form.get('job_description'),
            'requirements': request.form.get('requirements'),
            'responsibilities': request.form.get('responsibilities'),
            'benefits': request.form.get('benefits'),
            'application_deadline': request.form.get('application_deadline'),
            'job_status': request.form.get('job_status')
        }
        
        if update_job_posting(job_id, job_data):
            flash('Job posting updated successfully!', 'success')
            return redirect(url_for('admin_jobs'))
        else:
            flash('Error updating job posting.', 'error')
    
    return render_template('admin_job_form.html', action='edit', job=job_posting)

@app.route('/admin/jobs/<int:job_id>/delete', methods=['POST'])
@admin_required
def admin_job_delete(job_id):
    """Delete job posting."""
    if delete_job_posting(job_id):
        flash('Job posting deleted successfully!', 'success')
    else:
        flash('Error deleting job posting.', 'error')
    
    return redirect(url_for('admin_jobs'))

@app.route('/admin/applications')
@admin_required
def admin_applications():
    """Admin job applications management page."""
    applications = fetch_job_applications()
    return render_template('admin_applications.html', applications=applications)

@app.route('/admin/applications/<int:application_id>/status', methods=['POST'])
@admin_required
def update_application_status_route(application_id):
    """Update application status."""
    status = request.form.get('status')
    notes = request.form.get('notes', '')
    
    if update_application_status(application_id, status, notes):
        flash('Application status updated successfully!', 'success')
    else:
        flash('Error updating application status.', 'error')
    
    return redirect(url_for('admin_applications'))

# =================================================================================================
# Debug and Utility Functions
# =================================================================================================
def debug_email_config():
    """Debug email configuration."""
    print("\n=== SMTPLIB EMAIL CONFIGURATION DEBUG ===")
    print(f"SMTP_SERVER: {SMTP_SERVER}")
    print(f"SMTP_PORT: {SMTP_PORT}")
    print(f"EMAIL_USER: {EMAIL_USER}")
    print(f"EMAIL_PASSWORD: {'***' if EMAIL_PASSWORD else 'NOT SET'}")
    print(f"EMAIL_FROM_NAME: {EMAIL_FROM_NAME}")
    
    if not EMAIL_USER:
        print("❌ EMAIL_USER not set!")
    if not EMAIL_PASSWORD:
        print("❌ EMAIL_PASSWORD not set!")
    
    # Test connection
    success, msg = email_service.test_connection()
    print(f"Connection test: {'✅ SUCCESS' if success else '❌ FAILED'} - {msg}")
    print("=== END EMAIL DEBUG ===\n")

# =================================================================================================
# Error Handlers
# =================================================================================================
@app.errorhandler(404)
def not_found_error(error):
    flash('Page not found.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    flash('An internal error occurred. Please try again later.', 'error')
    return redirect(url_for('index'))

# =================================================================================================
# Application Initialization
# =================================================================================================
if __name__ == '__main__':
    # Debug email configuration
    debug_email_config()
    create_contact_submissions_table()
    app.run(debug=True)