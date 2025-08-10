from flask import Flask, render_template, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
# IMPORTANT: Replace with your actual MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',    # e.g., 'root'
    'password': '10,Aug_2023', # e.g., 'password'
    'database': 'mindtunes_db'
}

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
    cursor = conn.cursor(dictionary=True) # Returns data as dictionaries
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

def base_data():
    nav_data = fetch_data('navTable')
    footer_data = fetch_data('footer')

    base_data_dict = {
        'nav': nav_data[0] if nav_data else {},
        'footer': footer_data[0] if footer_data else {}
    }

    return base_data_dict

@app.route('/')
def index():
    """Renders the main index page with data from all tables."""
    # Fetch data from all tables
    nav_data = fetch_data('navTable')
    hero_data = fetch_data('heroTable')
    clients_data = fetch_data('Ourclients')
    innovations_data = fetch_data('innovations')
    know_data = fetch_data('know')
    statistics_data = fetch_data('statistics')
    footer_data = fetch_data('footer')

    # Create a dictionary to hold all data
    template_data = {
        'nav': nav_data[0] if nav_data else {},
        'hero': hero_data[0] if hero_data else {},
        'client': clients_data[0] if clients_data else {},
        'innovation': innovations_data[0] if innovations_data else {},
        'know': know_data[0] if know_data else {},
        'statistic': statistics_data[0] if statistics_data else {},
        'footer': footer_data[0] if footer_data else {}
    }

    # Pass the entire dictionary to the template using ** for unpacking
    return render_template('index.html', **template_data)

# Define other routes if needed by your navAnchors,
# for example, an 'about' page.
@app.route('/about')
def about():
    """Renders the about us page with data from the aboutUs table."""
    about_data = fetch_data('aboutUs')
    about_us = about_data[0] if about_data else {}
    base_data_dict = base_data()

    return render_template(
        'about.html',
        mainTitle=about_us.get('mainTitle'),
        subtitle=about_us.get('subtitle'),
        heroImage=about_us.get('heroImage'),
        aboutContent1=about_us.get('aboutContent1'),
        aboutContent2=about_us.get('aboutContent2'),
        teamWorkingImage=about_us.get('teamWorkingImage'),
        achievementTitle=about_us.get('achievementTitle'),
        achievementSubtitle=about_us.get('achievementSubtitle'),
        missionTitle=about_us.get('missionTitle'),
        missionContent=about_us.get('missionContent'),
        beliefsTitle=about_us.get('beliefsTitle'),
        belief1=about_us.get('belief1'),
        belief2=about_us.get('belief2'),
        belief3=about_us.get('belief3'),
        belief4=about_us.get('belief4'),
        whoWeWorkWithTitle=about_us.get('whoWeWorkWithTitle'),
        clientType1Icon=about_us.get('clientType1Icon'),
        clientType1Title=about_us.get('clientType1Title'),
        clientType1Desc=about_us.get('clientType1Desc'),
        clientType2Icon=about_us.get('clientType2Icon'),
        clientType2Title=about_us.get('clientType2Title'),
        clientType2Desc=about_us.get('clientType2Desc'),
        clientType3Icon=about_us.get('clientType3Icon'),
        clientType3Title=about_us.get('clientType3Title'),
        clientType3Desc=about_us.get('clientType3Desc'),
        clientType4Icon=about_us.get('clientType4Icon'),
        clientType4Title=about_us.get('clientType4Title'),
        clientType4Desc=about_us.get('clientType4Desc'),
        founder1Name=about_us.get('founder1Name'),
        founder1Role=about_us.get('founder1Role'),
        founder1Desc=about_us.get('founder1Desc'),
        founder1Image=about_us.get('founder1Image'),
        founder2Name=about_us.get('founder2Name'),
        founder2Role=about_us.get('founder2Role'),
        founder2Desc=about_us.get('founder2Desc'),
        founder2Image=about_us.get('founder2Image'), 
        **base_data_dict
    )



@app.route('/services')
def services():
    """Renders the services page with data from the servicesTable."""
    services_data = fetch_data('servicesTable')
    service_content = services_data[0] if services_data else {}
    base_data_dict = base_data()
    
    return render_template(
        'services.html',
        heroTitle=service_content.get('heroTitle'),
        heroSubtitle=service_content.get('heroSubtitle'),
        exploreButtonText=service_content.get('exploreButtonText'),
        sectionTitle=service_content.get('sectionTitle'),
        sectionSubtitle=service_content.get('sectionSubtitle'),
        serviceCard1Icon=service_content.get('serviceCard1Icon'),
        serviceCard1Title=service_content.get('serviceCard1Title'),
        serviceCard1Desc=service_content.get('serviceCard1Desc'),
        serviceCard2Icon=service_content.get('serviceCard2Icon'),
        serviceCard2Title=service_content.get('serviceCard2Title'),
        serviceCard2Desc=service_content.get('serviceCard2Desc'),
        serviceCard3Icon=service_content.get('serviceCard3Icon'),
        serviceCard3Title=service_content.get('serviceCard3Title'),
        serviceCard3Desc=service_content.get('serviceCard3Desc'),
        serviceCard4Icon=service_content.get('serviceCard4Icon'),
        serviceCard4Title=service_content.get('serviceCard4Title'),
        serviceCard4Desc=service_content.get('serviceCard4Desc'),
        serviceCard5Icon=service_content.get('serviceCard5Icon'),
        serviceCard5Title=service_content.get('serviceCard5Title'),
        serviceCard5Desc=service_content.get('serviceCard5Desc'),
        serviceCard6Icon=service_content.get('serviceCard6Icon'),
        serviceCard6Title=service_content.get('serviceCard6Title'),
        serviceCard6Desc=service_content.get('serviceCard6Desc'),
        statsSectionTitle=service_content.get('statsSectionTitle'),
        stat1Number=service_content.get('stat1Number'),
        stat1Desc=service_content.get('stat1Desc'),
        stat2Number=service_content.get('stat2Number'),
        stat2Desc=service_content.get('stat2Desc'),
        stat3Number=service_content.get('stat3Number'),
        stat3Desc=service_content.get('stat3Desc'),
        stat4Number=service_content.get('stat4Number'),
        stat4Desc=service_content.get('stat4Desc'),
        **base_data_dict
    )




if __name__ == '__main__':
    app.run(debug=True)
