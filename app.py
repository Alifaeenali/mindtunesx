from flask import Flask, render_template, url_for, request, redirect, flash, session
import mysql.connector
from functools import wraps
import hashlib
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production

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

def update_data(table_name, data_dict):
    """Updates data in a specified table."""
    conn = get_db_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    try:
        # Build the SET clause dynamically
        set_clause = ', '.join([f"{key} = %s" for key in data_dict.keys()])
        values = list(data_dict.values())
        
        # Assuming each table has only one row (id = 1)
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
            id_field = 'footer_id'
        elif table_name == 'aboutUs':
            id_field = 'about_id'
        elif table_name == 'servicesTable':
            id_field = 'service_id'
        else:
            id_field = 'id'
        
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
        'about_us': 'About Us Page'
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
        'about_us': 'aboutUs'
    }
    
    current_data = {}
    client_logos = []
    founders_data = []
    work_with_data = []
    
    if section and section in table_mapping:
        data = fetch_data(table_mapping[section])
        current_data = data[0] if data else {}
        
        # Special handling for clients section to get logos
        if section == 'clients':
            client_logos = fetch_client_logos()
        
        # Special handling for about_us section to get founders and 'who we work with'
        if section == 'about_us':
            founders_data = fetch_founders()
            work_with_data = fetch_who_we_work_with()
    
    return render_template('admin.html', 
                         current_section=section,
                         section_titles=section_titles,
                         data=current_data,
                         client_logos=client_logos,
                         founders=founders_data,
                         work_with=work_with_data)

# Handle POST requests for admin updates
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
        'about_us': 'About Us Page'
    }
    
    table_mapping = {
        'nav': 'navTable',
        'hero': 'heroTable',
        'clients': 'Ourclients',
        'innovations': 'innovations',
        'know': 'know',
        'statistics': 'statistics',
        'footer': 'footer',
        'about_us': 'aboutUs'
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
    
    # Special handling for client logos
    if section == 'clients':
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
            elif i - 1 < len(existing_logos_from_form):
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
        # Separate data for different tables
        about_us_data = {
            'about_head': form_data.get('about_head'),
            'about_desc': form_data.get('about_desc'),
            'about_title': form_data.get('about_title'),
            'about_subtitle': form_data.get('about_subtitle')
        }
        about_us_data = {k: v for k, v in about_us_data.items() if v}
        
        # Handle founders
        founders_to_update = []
        founder_names = request.form.getlist('founderName')
        founder_roles = request.form.getlist('founderRole')
        founder_descs = request.form.getlist('founderDescription')
        existing_founder_images = request.form.getlist('existingFounderImage')
        
        for i in range(len(founder_names)):
            founder_image = uploaded_files.get(f'founderImage{i+1}') or existing_founder_images[i]
            founders_to_update.append({
                'founder_name': founder_names[i],
                'founder_role': founder_roles[i],
                'founder_description': founder_descs[i],
                'founder_image': founder_image
            })
            
        if update_founders(founders_to_update):
            flash('Founders updated successfully!', 'success')
        else:
            flash('Error updating founders.', 'error')
            
        # Handle 'who we work with'
        work_with_to_update = []
        work_icons = request.form.getlist('workIcon')
        work_titles = request.form.getlist('workTitle')
        work_descs = request.form.getlist('workDescription')
        
        for i in range(len(work_icons)):
            work_with_to_update.append({
                'work_icon': work_icons[i],
                'work_title': work_titles[i],
                'work_description': work_descs[i]
            })
            
        if update_who_we_work_with(work_with_to_update):
            flash('"Who We Work With" section updated successfully!', 'success')
        else:
            flash('Error updating "Who We Work With" section.', 'error')

        # Update the main `aboutUs` table
        if about_us_data and update_data(table_mapping[section], about_us_data):
            flash('About Us page content updated successfully!', 'success')
        
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

# Error handlers
# @app.errorhandler(404)
# def not_found(error):
#     flash('Page not found.', 'error')
#     return redirect(url_for('index'))


@app.errorhandler(500)
def internal_error(error):
    flash('An internal error occurred. Please try again later.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)