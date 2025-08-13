#!/usr/bin/env python3
"""
Simple MindTunes Database Setup Script
Creates database, tables and inserts initial data
"""

import os
import mysql.connector
from datetime import datetime, date
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration from environment variables
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT', 3306)
}

# Database name from environment
database_name = os.getenv('DB_DATABASE')

def setup_database():
    print("🚀 Starting MindTunes Database Setup...")
    print(f"🌐 Host: {db_config['host']}")
    print(f"👤 User: {db_config['user']}")
    print(f"📁 Database to create: {database_name}")
    
    if not database_name:
        print("❌ Error: DB_DATABASE not found in environment variables")
        return
    
    try:
        # First, connect to MySQL server without specifying a database
        print("🔌 Connecting to MySQL server...")
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        print("✅ Connected to MySQL server successfully")
        
        # Create database if it doesn't exist
        print(f"🏗️ Creating database '{database_name}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
        print(f"✅ Database '{database_name}' created/verified")
        
        # Close the initial connection
        cursor.close()
        connection.close()
        
        # Now connect to the specific database
        print(f"🔌 Connecting to database '{database_name}'...")
        db_config_with_db = db_config.copy()
        db_config_with_db['database'] = database_name
        
        connection = mysql.connector.connect(**db_config_with_db)
        cursor = connection.cursor()
        print(f"✅ Connected to database '{database_name}' successfully")
        
        # Create tables
        create_tables(cursor)
        
        # Insert initial data
        insert_initial_data(cursor, connection)
        
        cursor.close()
        connection.close()
        print("🎉 Database setup completed successfully!")
        
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

def create_tables(cursor):
    print("📋 Creating tables...")
    
    # About Us table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aboutus (
            about_id INT PRIMARY KEY AUTO_INCREMENT,
            about_head VARCHAR(255),
            about_desc TEXT,
            about_title VARCHAR(255),
            about_subtitle TEXT,
            about_secondary_desc TEXT,
            aboutHeroImage VARCHAR(500),
            achievement_title VARCHAR(255),
            achievement_subtitle TEXT,
            mission_text TEXT,
            belief1 VARCHAR(255),
            belief2 VARCHAR(255),
            belief3 VARCHAR(255),
            belief4 VARCHAR(255)
        )
    """)
    
    # Blog Posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_posts (
            blog_id INT PRIMARY KEY AUTO_INCREMENT,
            blog_title VARCHAR(500),
            blog_subtitle TEXT,
            blog_author VARCHAR(255),
            blog_date DATE,
            blog_image VARCHAR(500),
            blog_excerpt TEXT,
            blog_content LONGTEXT,
            blog_status VARCHAR(20) DEFAULT 'published',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    
    # Client Logos table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS client_logos (
            logo_id INT PRIMARY KEY AUTO_INCREMENT,
            logo_url VARCHAR(500),
            logo_order INT DEFAULT 0
        )
    """)
    
    # Contact Submissions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_submissions (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255),
            email VARCHAR(255),
            subject VARCHAR(500),
            message TEXT,
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) DEFAULT 'new',
            priority VARCHAR(20) DEFAULT 'medium',
            assigned_to VARCHAR(255),
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    
    # Footer table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS footer (
            ftr_id INT PRIMARY KEY AUTO_INCREMENT,
            ftr_link1 VARCHAR(255),
            ftr_link2 VARCHAR(255),
            ftr_link3 VARCHAR(255),
            ftr_link4 VARCHAR(255)
        )
    """)
    
    # Founders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS founders (
            founder_id INT PRIMARY KEY AUTO_INCREMENT,
            founder_name VARCHAR(255),
            founder_role VARCHAR(255),
            founder_image VARCHAR(500),
            founder_description TEXT,
            founder_order INT DEFAULT 0
        )
    """)
    
    # Hero table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS herotable (
            hero_id INT PRIMARY KEY AUTO_INCREMENT,
            heroImg VARCHAR(500),
            heroHead TEXT,
            heroDesc TEXT
        )
    """)
    
    # Innovations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS innovations (
            innovation_id INT PRIMARY KEY AUTO_INCREMENT,
            innovationSubHead VARCHAR(255),
            innovationHead VARCHAR(255),
            innovationDescp TEXT,
            innovationl1 TEXT,
            innovationl2 TEXT,
            innovationl3 TEXT,
            innovationl4 TEXT,
            innovationVideo VARCHAR(500),
            innovationImage VARCHAR(500),
            innovationMediaType VARCHAR(20) DEFAULT 'video'
        )
    """)
    
    # Job Applications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            application_id INT PRIMARY KEY AUTO_INCREMENT,
            job_id INT,
            applicant_name VARCHAR(255),
            applicant_email VARCHAR(255),
            applicant_phone VARCHAR(20),
            cover_letter TEXT,
            cv_filename VARCHAR(500),
            cv_path VARCHAR(500),
            linkedin_profile VARCHAR(500),
            portfolio_website VARCHAR(500),
            expected_salary VARCHAR(100),
            availability_date DATE,
            application_status VARCHAR(20) DEFAULT 'pending',
            applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    """)
    
    # Job Postings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_postings (
            job_id INT PRIMARY KEY AUTO_INCREMENT,
            job_title VARCHAR(255),
            job_type VARCHAR(50),
            department VARCHAR(100),
            location VARCHAR(255),
            salary_range VARCHAR(100),
            job_description TEXT,
            requirements TEXT,
            responsibilities TEXT,
            benefits TEXT,
            application_deadline DATE,
            job_status VARCHAR(20) DEFAULT 'active',
            posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    
    # Know table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS know (
            know_id INT PRIMARY KEY AUTO_INCREMENT,
            knowHead VARCHAR(255),
            knowDescp TEXT,
            knowVideo VARCHAR(500),
            knowImage VARCHAR(500),
            knowMediaType VARCHAR(20),
            knowFile VARCHAR(500)
        )
    """)
    
    # Navigation table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS navtable (
            nav_id INT PRIMARY KEY AUTO_INCREMENT,
            navLogo VARCHAR(500),
            navAnchor1 VARCHAR(50),
            navAnchor2 VARCHAR(50),
            navAnchor3 VARCHAR(50),
            navAnchor4 VARCHAR(50),
            navAnchor5 VARCHAR(50),
            navAnchor6 VARCHAR(50)
        )
    """)
    
    # Our Clients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ourclients (
            clients_id INT PRIMARY KEY AUTO_INCREMENT,
            clientHead VARCHAR(255),
            clientDesc TEXT
        )
    """)
    
    # Services table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicestable (
            service_id INT PRIMARY KEY AUTO_INCREMENT,
            service_head VARCHAR(255),
            service_icon VARCHAR(100),
            service_desc TEXT
        )
    """)
    
    # Statistics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statistics (
            stat_id INT PRIMARY KEY AUTO_INCREMENT,
            statHead VARCHAR(255),
            statDescp TEXT,
            headCard1 VARCHAR(100),
            headCard2 VARCHAR(100),
            headCard3 VARCHAR(100),
            DescCard1 TEXT,
            DescCard2 TEXT,
            DescCard3 TEXT,
            ImgCard1 VARCHAR(500),
            ImgCard2 VARCHAR(500),
            ImgCard3 VARCHAR(500)
        )
    """)
    
    # Team Members table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_members (
            team_id INT PRIMARY KEY AUTO_INCREMENT,
            member_name VARCHAR(255),
            member_position VARCHAR(255),
            member_description TEXT,
            member_image VARCHAR(500),
            team_order INT DEFAULT 0,
            member_status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    
    # Who We Work With table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS who_we_work_with (
            work_id INT PRIMARY KEY AUTO_INCREMENT,
            work_icon VARCHAR(10),
            work_title VARCHAR(255),
            work_description TEXT,
            work_order INT DEFAULT 0
        )
    """)
    
    print("✅ All tables created successfully")

def insert_initial_data(cursor, connection):
    print("📝 Inserting initial data...")
    
    # Insert About Us data
    cursor.execute("""
        INSERT INTO aboutus (about_head, about_desc, about_title, about_subtitle, about_secondary_desc, 
                           aboutHeroImage, achievement_title, achievement_subtitle, mission_text, 
                           belief1, belief2, belief3, belief4) VALUES
        ('About MindTune Innovations', 'Building intelligent products that connect hardware, software, and people',
         'About Us', 'MindTune Innovations is a technology company based in Pakistan, focused on building intelligent products that connect hardware, software, and people. We bring together expertise in IoT, embedded systems, wearable tech, PCB design, and mobile app development — all within one team.',
         'MindTune Innovations is a technology company based in Pakistan, focused on building intelligent products that connect hardware, software, and people. We bring together expertise in IoT, embedded systems, wearable tech, PCB design, and mobile app development — all within one team.',
         '/static/uploads/mindtuneteam_1754838288_1754898947.png', 'Innovation & Excellence',
         'Leading the way in wearable technology and IoT solutions with cutting-edge research and development.',
         'Our mission is to bridge the gap between advanced technology and everyday life by creating intelligent, user-friendly products that enhance human capabilities and well-being.',
         'Innovation drives progress', 'Quality over quantity', 'User-centered design', 'Collaborative excellence')
    """)
    
    # Insert Blog Posts data
    cursor.execute("""
        INSERT INTO blog_posts (blog_title, blog_subtitle, blog_author, blog_date, blog_image, blog_excerpt, blog_content, blog_status) VALUES
        ('The Future of EEG Wearables in Healthcare', 'How Brain-Computer Interfaces are Revolutionizing Patient Care', 
         'Abdul Basit', '2024-12-15', '/static/uploads/istockphoto-2153478836-1024x1024_1754978312.jpg',
         'Explore how EEG wearables are transforming healthcare by providing real-time brain monitoring capabilities for better patient outcomes.',
         '<p>The healthcare industry is experiencing a revolutionary transformation with the advent of EEG (Electroencephalography) wearables. These innovative devices are opening new frontiers in patient care, mental health monitoring, and neurological disorder management.</p><h3>What are EEG Wearables?</h3><p>EEG wearables are portable, non-invasive devices that can monitor brain activity in real-time. Unlike traditional EEG systems that require clinical settings and multiple electrodes, modern wearables integrate seamlessly into everyday life through headbands, earbuds, or caps.</p>',
         'published'),
        ('IoT in Smart Healthcare: Connecting Devices for Better Outcomes', 'Building the Connected Healthcare Ecosystem of Tomorrow',
         'Ryan Ahmed', '2024-12-10', 'static/uploads/blog2.jpg',
         'Discover how Internet of Things (IoT) technology is creating interconnected healthcare systems that improve patient care and operational efficiency.',
         '<p>The Internet of Things (IoT) is reshaping healthcare delivery by creating interconnected ecosystems of smart devices, sensors, and applications that work together to improve patient outcomes and streamline healthcare operations.</p>',
         'published'),
        ('PCB Design Best Practices for Wearable Devices', 'Engineering Challenges and Solutions in Miniaturized Electronics',
         'MindTune Engineering Team', '2024-12-05', 'static/uploads/blog3.jpg',
         'Learn about the critical considerations and best practices for designing PCBs for wearable devices, from power management to signal integrity.',
         '<p>Designing printed circuit boards (PCBs) for wearable devices presents unique challenges that require specialized knowledge and careful consideration of multiple factors including size constraints, power efficiency, and user comfort.</p>',
         'published')
    """)
    
    # Insert Client Logos data
    cursor.execute("""
        INSERT INTO client_logos (logo_url, logo_order) VALUES
        ('/static/uploads/client1_1754991075.png', 1),
        ('/static/uploads/client2_1754991075.png', 2),
        ('/static/uploads/mindtunes_1_1755010632.png', 3)
    """)
    
    # Insert Footer data
    cursor.execute("""
        INSERT INTO footer (ftr_link1, ftr_link2, ftr_link3, ftr_link4) VALUES
        ('Privacy Policy', 'Terms of Service', 'Info@mindtuneinnovation.tech', 'https://www.linkedin.com/company/mindtune-innovations')
    """)
    
    # Insert Founders data
    cursor.execute("""
        INSERT INTO founders (founder_name, founder_role, founder_image, founder_description, founder_order) VALUES
        ('Abdul Basit', 'CEO & DIRECTOR', 'static/assets/images/abbasit.png',
         'Abdul Basit is an Electrical Engineer and technology innovator with a proven track record in developing high-performance IoT and smart electronic solutions. At MindTune Innovations, he leads the company''s product development strategy, combining technical depth in hardware and embedded systems with a clear vision for scalable, market-ready solutions.',
         1),
        ('Ryan Ahmed', 'COO & DIRECTOR', 'static/assets/images/rayanAhmed.png',
         'Ryan Ahmed is the Co-Founder of Niura and a strategic leader in wearable neuroscience technologies. With a background in launching and scaling consumer tech ventures, Ryan has positioned Niura as a pioneer in EEG-powered earbuds designed for mental performance tracking.',
         2)
    """)
    
    # Insert Hero data
    cursor.execute("""
        INSERT INTO herotable (heroImg, heroHead, heroDesc) VALUES
        ('/static/uploads/hero_1755007641.png', 
         'We Engineer Next-Gen Wearables, Smart IoT Products & Full-Stack Tech Solutions updated',
         'At MindTune Innovations, we help you bring bold product ideas to life. From connected devices to powerful software, our team handles every step including hardware, firmware, mobile apps, and mechanical design all under one roof. Whether you''re a startup, research team, or enterprise, we deliver complete and ready-to-deploy solutions that are reliable, scalable, and user-friendly. updated')
    """)
    
    # Insert Innovations data
    cursor.execute("""
        INSERT INTO innovations (innovationSubHead, innovationHead, innovationDescp, innovationl1, innovationl2, innovationl3, innovationl4, innovationVideo, innovationImage, innovationMediaType) VALUES
        ('Pioneering the Future', 'Neuro-Acoustic Innovations',
         'Discover how our proprietary algorithms and sound frequencies are revolutionizing mental performance and relaxation. We integrate the latest neuroscience with artistic sound design.',
         'Personalized Brainwave Entrainment for focus and calm.',
         'Adaptive Soundscapes that respond to your real-time biometric data.',
         'Gamified Cognitive Training modules for enhanced learning.',
         'Proprietary AI-driven sound generation for unique experiences.',
         'static/assets/videos/a_new_course.webm', 'static/assets/images/hero.png', 'video')
    """)
    
    # Insert Job Postings data
    cursor.execute("""
        INSERT INTO job_postings (job_title, job_type, department, location, salary_range, job_description, requirements, responsibilities, benefits, application_deadline, job_status) VALUES
        ('Senior Hardware Engineer', 'full-time', 'Engineering', 'Rawalpindi, Pakistan / Remote', 'PKR 150,000 - 250,000/month',
         'Join our innovative team as a Senior Hardware Engineer and help design next-generation wearable devices and IoT products.',
         '• Bachelor''s or Master''s degree in Electrical Engineering\\n• 5+ years of experience in hardware design\\n• Proficiency in PCB design tools',
         '• Design and develop hardware solutions for wearable and IoT devices\\n• Create PCB layouts and manage manufacturing process',
         '• Competitive salary and performance bonuses\\n• Health insurance coverage\\n• Professional development opportunities',
         '2025-09-15', 'active'),
        ('Mobile App Developer (React Native)', 'full-time', 'Software Development', 'Rawalpindi, Pakistan / Hybrid', 'PKR 120,000 - 200,000/month',
         'We are seeking a talented Mobile App Developer to create user-friendly mobile applications that connect with our innovative wearable devices.',
         '• Bachelor''s degree in Computer Science\\n• 3+ years of experience in mobile app development\\n• Strong proficiency in React Native',
         '• Develop cross-platform mobile applications using React Native\\n• Integrate mobile apps with hardware devices',
         '• Competitive salary package\\n• Health and dental insurance\\n• Annual performance bonuses',
         '2025-08-30', 'active'),
        ('Firmware Engineer Intern', 'internship', 'Engineering', 'Rawalpindi, Pakistan', 'PKR 30,000 - 50,000/month',
         'Join our team as a Firmware Engineer Intern and gain hands-on experience in developing embedded software.',
         '• Currently pursuing Bachelor''s or Master''s degree\\n• Strong programming skills in C/C++\\n• Basic knowledge of microcontrollers',
         '• Assist in developing firmware for wearable devices\\n• Write and test embedded software code',
         '• Mentorship from experienced engineers\\n• Hands-on experience with cutting-edge technology',
         '2025-09-01', 'active')
    """)
    
    # Insert Know data
    cursor.execute("""
        INSERT INTO know (knowHead, knowDescp, knowVideo, knowImage, knowMediaType, knowFile) VALUES
        ('Deep Dive into Neuro-Acoustics ',
         'Learn more about the science behind MindTunes. Our expert-led content explains how specific sound frequencies influence brain activity and promote desired mental states.',
         'static/assets/videos/get-to-know.webm', 'static/assets/images/hero.png', 'video',
         '/static/uploads/a_new_course_1755018621.webm')
    """)
    
    # Insert Navigation data
    cursor.execute("""
        INSERT INTO navtable (navLogo, navAnchor1, navAnchor2, navAnchor3, navAnchor4, navAnchor5, navAnchor6) VALUES
        ('/static/uploads/WhatsApp_Image_2025-03-25_at_14.06.11_4d5129c4-removebg-preview_1_1755060269.png',
         'Home ', 'About ', 'Services ', 'News ', 'Contact Us ', 'Careers ')
    """)
    
    # Insert Our Clients data
    cursor.execute("""
        INSERT INTO ourclients (clientHead, clientDesc) VALUES
        ('Trusted by Leading Innovators ',
         'Our clientele includes a diverse range of companies, from tech startups to healthcare providers, all seeking to leverage the power of sound for human flourishing.')
    """)
    
    # Insert Services data
    services_data = [
        ('IoT & Embedded Systems Development', 'fa-solid fa-laptop', 'We design and build smart IoT solutions powered by efficient embedded systems, enabling seamless device connectivity, data collection, and automation for consumer and industrial applications.'),
        ('EEG Wearables & Biosensor Solutions', 'fa-solid fa-microchip', 'MindTune pioneers EEG-powered wearables and biosensor integrations, enabling real-time tracking of mental and physical states.'),
        ('PCB Design & Hardware Prototyping', 'fa-solid fa-wrench', 'Our hardware team delivers PCB designs and rapid prototypes that meet high standards of performance, efficiency, and reliability.'),
        ('Firmware & Machine Learning Integration', 'fa-solid fa-robot', 'We create efficient firmware optimized for real-time data and integrate machine learning algorithms to deliver intelligent, adaptive devices.'),
        ('Mobile App & Cloud Development', 'fas fa-mobile-alt', 'We build scalable mobile apps and cloud platforms to connect devices, users, and data seamlessly.'),
        ('Product Design & Mechanical CAD', 'fa-solid fa-hard-drive', 'Our mechanical engineers create functional and aesthetically refined designs using advanced CAD tools.')
    ]
    
    for service in services_data:
        cursor.execute("""
            INSERT INTO servicestable (service_head, service_icon, service_desc) VALUES (%s, %s, %s)
        """, service)
    
    # Insert Statistics data
    cursor.execute("""
        INSERT INTO statistics (statHead, statDescp, headCard1, headCard2, headCard3, DescCard1, DescCard2, DescCard3, ImgCard1, ImgCard2, ImgCard3) VALUES
        ('Impact and Achievements',
         'See the measurable difference MindTunes is making in people''s lives and in various industries. Our data speaks volumes.',
         '90% Improvement', '20K+ Users', '15+ Patents',
         'Users report significant improvement in focus and sleep quality.',
         'Global community benefiting from MindTunes daily.',
         'Cutting-edge technology protected by intellectual property.',
         '/static/uploads/stats1_1754841602_1754898914.png',
         '/static/uploads/stats2_1754841602_1754898914.png',
         '/static/uploads/stats3_1754841602_1754898914.png')
    """)
    
    # Insert Team Members data
    team_data = [
        ('John Smith', 'Lead Developer', 'Experienced full-stack developer with expertise in modern web technologies and system architecture.', '/static/uploads/usericon_1754982255.png', 1),
        ('Sarah Johnson', 'UI/UX Designer', 'Creative designer focused on user experience and interface design with a passion for creating intuitive solutions.', '/static/uploads/usericon_1754982255.png', 2),
        ('Mike Chen', 'Project Manager', 'Skilled project manager ensuring smooth delivery of projects while maintaining quality and client satisfaction.', '/static/uploads/usericon_1754982255.png', 3)
    ]
    
    for member in team_data:
        cursor.execute("""
            INSERT INTO team_members (member_name, member_position, member_description, member_image, team_order) VALUES (%s, %s, %s, %s, %s)
        """, member)
    
    # Insert Who We Work With data
    work_data = [
        ('🏥', 'Health-Tech Startups', 'Building wearable products and health monitoring solutions', 1),
        ('⚙️', 'Engineering Teams', 'Embedded systems and PCB development support', 2),
        ('🔬', 'Research Labs', 'Developing biomedical and IoT research tools', 3),
        ('🏢', 'Enterprise Companies', 'Custom hardware with mobile and cloud integration', 4)
    ]
    
    for work in work_data:
        cursor.execute("""
            INSERT INTO who_we_work_with (work_icon, work_title, work_description, work_order) VALUES (%s, %s, %s, %s)
        """, work)
    
    connection.commit()
    print("✅ All initial data inserted successfully")

if __name__ == "__main__":
    setup_database()