-- Database creation and selection
CREATE DATABASE IF NOT EXISTS mindtunes_db;
USE mindtunes_db;

-- Table for navigation links
CREATE TABLE IF NOT EXISTS navTable (
    nav_id INT AUTO_INCREMENT PRIMARY KEY,
    navLogo VARCHAR(200),
    navAnchor1 VARCHAR(200),
    navAnchor2 VARCHAR(200),
    navAnchor3 VARCHAR(200),
    navAnchor4 VARCHAR(200),
    navAnchor5 VARCHAR(200),
    navAnchor6 VARCHAR(200)
);

-- Table for the hero section
CREATE TABLE IF NOT EXISTS heroTable (
    hero_id INT AUTO_INCREMENT PRIMARY KEY,
    heroImg VARCHAR(200),
    heroHead VARCHAR(200),
    heroDesc TEXT
);

-- Table for the "Our Clients" section text
CREATE TABLE IF NOT EXISTS Ourclients (
    clients_id INT AUTO_INCREMENT PRIMARY KEY,
    clientHead VARCHAR(200),
    clientDesc TEXT
);

-- Table for the dynamic client logos
CREATE TABLE IF NOT EXISTS client_logos (
    logo_id INT AUTO_INCREMENT PRIMARY KEY,
    logo_url VARCHAR(255),
    logo_order INT
);

-- Table for the "Innovations" section
CREATE TABLE IF NOT EXISTS innovations (
    innovation_id INT AUTO_INCREMENT PRIMARY KEY,
    innovationSubHead VARCHAR(200),
    innovationHead VARCHAR(200),
    innovationDescp VARCHAR(500),
    innovationl1 TEXT,
    innovationl2 TEXT,
    innovationl3 TEXT,
    innovationl4 TEXT,
    innovationVideo VARCHAR(200),
    innovationImage VARCHAR(200)
);

-- Table for the "Know" section
CREATE TABLE IF NOT EXISTS know (
    know_id INT AUTO_INCREMENT PRIMARY KEY,
    knowHead VARCHAR(200),
    knowDescp VARCHAR(500),
    knowVideo VARCHAR(200),
    knowImage VARCHAR(200)
);

-- Table for the "Statistics" section
CREATE TABLE IF NOT EXISTS statistics (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    statHead VARCHAR(200),
    statDescp VARCHAR(500),
    headCard1 VARCHAR(200),
    headCard2 VARCHAR(200),
    headCard3 VARCHAR(200),
    DescCard1 VARCHAR(200),
    DescCard2 VARCHAR(200),
    DescCard3 VARCHAR(200),
    ImgCard1 VARCHAR(200),
    ImgCard2 VARCHAR(200),
    ImgCard3 VARCHAR(200)
);

-- Table for the footer
CREATE TABLE IF NOT EXISTS footer (
    ftr_id INT AUTO_INCREMENT PRIMARY KEY,
    ftr_link1 VARCHAR(200),
    ftr_link2 VARCHAR(200),
    ftr_link3 VARCHAR(200),
    ftr_link4 VARCHAR(200)
);

-- Table for the "About Us" page
CREATE TABLE IF NOT EXISTS aboutUs (
    about_id INT AUTO_INCREMENT PRIMARY KEY,
    about_head VARCHAR(200),
    about_desc TEXT,
    about_title VARCHAR(500),
    about_subtitle VARCHAR(500),
    about_secondary_desc TEXT,
    aboutHeroImage VARCHAR(200),
    achievement_title VARCHAR(200),
    achievement_subtitle TEXT,
    mission_text TEXT,
    belief1 VARCHAR(500),
    belief2 VARCHAR(500),
    belief3 VARCHAR(500),
    belief4 VARCHAR(500)
);

-- Table for dynamic founders section
CREATE TABLE IF NOT EXISTS founders (
    founder_id INT AUTO_INCREMENT PRIMARY KEY,
    founder_name VARCHAR(200),
    founder_role VARCHAR(200),
    founder_image VARCHAR(200),
    founder_description TEXT,
    founder_order INT
);

-- Table for dynamic "Who We Work With" section
CREATE TABLE IF NOT EXISTS who_we_work_with (
    work_id INT AUTO_INCREMENT PRIMARY KEY,
    work_icon VARCHAR(20),
    work_title VARCHAR(200),
    work_description TEXT,
    work_order INT
);

-- Table for the "Services" page
CREATE TABLE IF NOT EXISTS servicesTable (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_head VARCHAR(200),
    service_desc TEXT
);

-- Table for blog posts
CREATE TABLE IF NOT EXISTS blog_posts (
    blog_id INT AUTO_INCREMENT PRIMARY KEY,
    blog_title VARCHAR(255) NOT NULL,
    blog_subtitle VARCHAR(255),
    blog_author VARCHAR(100) NOT NULL,
    blog_date DATE NOT NULL,
    blog_image VARCHAR(255),
    blog_excerpt TEXT,
    blog_content LONGTEXT NOT NULL,
    blog_status ENUM('draft', 'published') DEFAULT 'published',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table for job postings
CREATE TABLE IF NOT EXISTS job_postings (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(255) NOT NULL,
    job_type ENUM('full-time', 'part-time', 'internship', 'contract') NOT NULL,
    department VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    salary_range VARCHAR(100),
    job_description LONGTEXT NOT NULL,
    requirements LONGTEXT NOT NULL,
    responsibilities LONGTEXT NOT NULL,
    benefits TEXT,
    application_deadline DATE,
    job_status ENUM('active', 'closed', 'draft') DEFAULT 'active',
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table for job applications
CREATE TABLE IF NOT EXISTS job_applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    applicant_name VARCHAR(255) NOT NULL,
    applicant_email VARCHAR(255) NOT NULL,
    applicant_phone VARCHAR(20),
    cover_letter TEXT,
    cv_filename VARCHAR(255) NOT NULL,
    cv_path VARCHAR(500) NOT NULL,
    linkedin_profile VARCHAR(255),
    portfolio_website VARCHAR(255),
    expected_salary VARCHAR(100),
    availability_date DATE,
    application_status ENUM('pending', 'reviewed', 'shortlisted', 'interviewed', 'hired', 'rejected') DEFAULT 'pending',
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (job_id) REFERENCES job_postings(job_id) ON DELETE CASCADE
);

ALTER TABLE servicesTable 
ADD COLUMN service_icon VARCHAR(255) DEFAULT 'fas fa-cogs' AFTER service_head;

UPDATE servicesTable 
SET service_icon = 'fas fa-cogs' 
WHERE service_icon IS NULL OR service_icon = '';

-- Table for contact form submissions
CREATE TABLE IF NOT EXISTS contact_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(255),
    message TEXT,
    submission_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- SQL Table for Team Members
CREATE TABLE IF NOT EXISTS team_members (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    member_name VARCHAR(255) NOT NULL,
    member_position VARCHAR(255) NOT NULL,
    member_description TEXT NOT NULL,
    member_image VARCHAR(500) NOT NULL,
    team_order INT DEFAULT 1,
    member_status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO team_members (member_name, member_position, member_description, member_image, team_order) VALUES
('John Smith', 'Lead Developer', 'Experienced full-stack developer with expertise in modern web technologies and system architecture.', '/static/uploads/default-avatar.jpg', 1),
('Sarah Johnson', 'UI/UX Designer', 'Creative designer focused on user experience and interface design with a passion for creating intuitive solutions.', '/static/uploads/default-avatar.jpg', 2),
('Mike Chen', 'Project Manager', 'Skilled project manager ensuring smooth delivery of projects while maintaining quality and client satisfaction.', '/static/uploads/default-avatar.jpg', 3);
-- Indexes for performance
CREATE INDEX idx_submission_date ON contact_submissions (submission_date);
-- NOTE: The 'status' column does not exist in contact_submissions, so this index is incorrect and has been removed.
-- CREATE INDEX idx_status ON contact_submissions (status);

-- Data Insertion
INSERT INTO navTable (navLogo, navAnchor1, navAnchor2, navAnchor3, navAnchor4, navAnchor5, navAnchor6) VALUES
('static/assets/images/updatedMindtuneLogo.png', 'Home', 'About', 'Services', 'News', 'Contact Us', 'Careers');

INSERT INTO heroTable (heroImg, heroHead, heroDesc) VALUES
('static/assets/images/hero.png', 'We Engineer Next-Gen Wearables, Smart IoT Products & Full-Stack Tech Solutions', 'At MindTune Innovations, we help you bring bold product ideas to life. From connected devices to powerful software, our team handles every step including hardware, firmware, mobile apps, and mechanical design all under one roof. Whether you’re a startup, research team, or enterprise, we deliver complete and ready-to-deploy solutions that are reliable, scalable, and user-friendly.');

INSERT INTO Ourclients (clientHead, clientDesc) VALUES
('Trusted by Leading Innovators', 'Our clientele includes a diverse range of companies, from tech startups to healthcare providers, all seeking to leverage the power of sound for human flourishing.');
ALTER TABLE innovations
ADD COLUMN innovationMediaType VARCHAR(50);
ALTER TABLE know
ADD COLUMN knowMediaType VARCHAR(50);

ALTER TABLE know
ADD COLUMN knowFile VARCHAR(200);
INSERT INTO client_logos (logo_url, logo_order) VALUES
('static/assets/images/client1.png', 1),
('static/assets/images/client2.png', 2),
('static/assets/images/client3.png', 3);

INSERT INTO innovations (innovationSubHead, innovationHead, innovationDescp, innovationl1, innovationl2, innovationl3, innovationl4, innovationVideo, innovationImage) VALUES
('Pioneering the Future', 'Neuro-Acoustic Innovations', 'Discover how our proprietary algorithms and sound frequencies are revolutionizing mental performance and relaxation. We integrate the latest neuroscience with artistic sound design.',
'Personalized Brainwave Entrainment for focus and calm.',
'Adaptive Soundscapes that respond to your real-time biometric data.',
'Gamified Cognitive Training modules for enhanced learning.',
'Proprietary AI-driven sound generation for unique experiences.',
'static/assets/videos/a_new_course.webm', 'static/assets/images/hero.png');

INSERT INTO know (knowHead, knowDescp, knowVideo, knowImage) VALUES
('Deep Dive into Neuro-Acoustics', 'Learn more about the science behind MindTunes. Our expert-led content explains how specific sound frequencies influence brain activity and promote desired mental states.',
'static/assets/videos/get-to-know.webm', 'static/assets/images/hero.png');

INSERT INTO statistics (statHead, statDescp, headCard1, headCard2, headCard3, DescCard1, DescCard2, DescCard3, ImgCard1, ImgCard2, ImgCard3) VALUES
('Impact and Achievements', 'See the measurable difference MindTunes is making in people\'s lives and in various industries. Our data speaks volumes.',
'90% Improvement', '20K+ Users', '15+ Patents',
'Users report significant improvement in focus and sleep quality.',
'Global community benefiting from MindTunes daily.',
'Cutting-edge technology protected by intellectual property.',
'static/assets/images/hero.png', 'static/assets/images/hero.png', 'static/assets/images/hero.png');

INSERT INTO footer (ftr_link1, ftr_link2, ftr_link3, ftr_link4) VALUES
('Privacy Policy', 'Terms of Service', 'Support', 'Careers');

INSERT INTO aboutUs (about_head, about_desc, about_title, about_subtitle, about_secondary_desc, aboutHeroImage, achievement_title, achievement_subtitle, mission_text, belief1, belief2, belief3, belief4) VALUES
('About MindTune Innovations', 'Building intelligent products that connect hardware, software, and people', 'About Us', 'MindTune Innovations is a technology company based in Pakistan, focused on building intelligent products that connect hardware, software, and people. We bring together expertise in IoT, embedded systems, wearable tech, PCB design, and mobile app development — all within one team.',
'MindTune Innovations is a technology company based in Pakistan, focused on building intelligent products that connect hardware, software, and people. We bring together expertise in IoT, embedded systems, wearable tech, PCB design, and mobile app development — all within one team.',
'static/assets/images/hero.png', 'Innovation & Excellence', 'Leading the way in wearable technology and IoT solutions with cutting-edge research and development.',
'Our mission is to bridge the gap between advanced technology and everyday life by creating intelligent, user-friendly products that enhance human capabilities and well-being.',
'Innovation drives progress',
'Quality over quantity',
'User-centered design',
'Collaborative excellence');

INSERT INTO founders (founder_name, founder_role, founder_image, founder_description, founder_order) VALUES
('Abdul Basit', 'CEO & DIRECTOR', 'static/assets/images/abbasit.png', 'Abdul Basit is an Electrical Engineer and technology innovator with a proven track record in developing high-performance IoT and smart electronic solutions. At MindTune Innovations, he leads the company\'s product development strategy, combining technical depth in hardware and embedded systems with a clear vision for scalable, market-ready solutions. His focus is on building products that deliver measurable value and position MindTune as a leader in EEG and IoT-driven technologies.', 1),
('Ryan Ahmed', 'COO & DIRECTOR', 'static/assets/images/rayanAhmed.png', 'Ryan Ahmed is the Co-Founder of Niura and a strategic leader in wearable neuroscience technologies. With a background in launching and scaling consumer tech ventures, Ryan has positioned Niura as a pioneer in EEG-powered earbuds designed for mental performance tracking. His expertise in bridging neuroscience with consumer technology allows Niura and MindTune to capture emerging market opportunities and drive significant growth potential in the wearable tech space.', 2);

INSERT INTO who_we_work_with (work_icon, work_title, work_description, work_order) VALUES
('🏥', 'Health-Tech Startups', 'Building wearable products and health monitoring solutions', 1),
('⚙️', 'Engineering Teams', 'Embedded systems and PCB development support', 2),
('🔬', 'Research Labs', 'Developing biomedical and IoT research tools', 3),
('🏢', 'Enterprise Companies', 'Custom hardware with mobile and cloud integration', 4);

INSERT INTO servicesTable (service_head, service_desc) VALUES
('IoT & Embedded Systems Development', 'We design and build smart IoT solutions powered by efficient embedded systems, enabling seamless device connectivity, data collection, and automation for consumer and industrial applications. Our engineers specialize in microcontrollers, sensors, and wireless protocols for optimized performance.'),
('EEG Wearables & Biosensor Solutions', 'MindTune pioneers EEG-powered wearables and biosensor integrations, enabling real-time tracking of mental and physical states. From earbuds to headsets, we turn neuroscience into user-friendly products for health, productivity, and research markets.'),
('PCB Design & Hardware Prototyping', 'Our hardware team delivers PCB designs and rapid prototypes that meet high standards of performance, efficiency, and reliability. We handle every stage — from schematics to assembled boards.'),
('Firmware & Machine Learning Integration', 'We create efficient firmware optimized for real-time data and integrate machine learning algorithms to deliver intelligent, adaptive devices. Our systems enhance performance while enabling edge-level AI features.'),
('Mobile App & Cloud Development', 'We build scalable mobile apps and cloud platforms to connect devices, users, and data seamlessly. From Bluetooth integration to cloud dashboards, we bring IoT ecosystems to life.'),
('Product Design & Mechanical CAD', 'Our mechanical engineers create functional and aesthetically refined designs using advanced CAD tools. We design housings, enclosures, and product structures that are production-ready.');

INSERT INTO blog_posts (blog_title, blog_subtitle, blog_author, blog_date, blog_image, blog_excerpt, blog_content, blog_status) VALUES
('The Future of EEG Wearables in Healthcare', 'How Brain-Computer Interfaces are Revolutionizing Patient Care', 'Abdul Basit', '2024-12-15', 'static/uploads/blog1.jpg', 'Explore how EEG wearables are transforming healthcare by providing real-time brain monitoring capabilities for better patient outcomes.', '<p>The healthcare industry is experiencing a revolutionary transformation with the advent of EEG (Electroencephalography) wearables. These innovative devices are opening new frontiers in patient care, mental health monitoring, and neurological disorder management.</p><h3>What are EEG Wearables?</h3><p>EEG wearables are portable, non-invasive devices that can monitor brain activity in real-time. Unlike traditional EEG systems that require clinical settings and multiple electrodes, modern wearables integrate seamlessly into everyday life through headbands, earbuds, or caps.</p><h3>Applications in Healthcare</h3><ul><li><strong>Seizure Detection:</strong> Real-time monitoring can alert patients and caregivers to impending seizures</li><li><strong>Sleep Disorders:</strong> Continuous monitoring of sleep patterns and brain waves during rest</li><li><strong>Mental Health:</strong> Tracking stress levels, anxiety, and depression markers</li><li><strong>Cognitive Assessment:</strong> Monitoring cognitive decline in aging populations</li></ul><h3>The Technology Behind the Innovation</h3><p>Modern EEG wearables utilize advanced signal processing, machine learning algorithms, and miniaturized electronics to deliver clinical-grade data. The integration of IoT connectivity allows for continuous data streaming to healthcare providers.</p><p>At MindTune Innovations, we are at the forefront of this technology, developing next-generation EEG wearables that combine accuracy, comfort, and affordability.</p>', 'published'),
('IoT in Smart Healthcare: Connecting Devices for Better Outcomes', 'Building the Connected Healthcare Ecosystem of Tomorrow', 'Ryan Ahmed', '2024-12-10', 'static/uploads/blog2.jpg', 'Discover how Internet of Things (IoT) technology is creating interconnected healthcare systems that improve patient care and operational efficiency.', '<p>The Internet of Things (IoT) is reshaping healthcare delivery by creating interconnected ecosystems of smart devices, sensors, and applications that work together to improve patient outcomes and streamline healthcare operations.</p><h3>The Connected Healthcare Landscape</h3><p>IoT in healthcare encompasses a vast network of connected devices including wearable sensors, smart medical equipment, environmental monitors, and mobile health applications. These devices collect, transmit, and analyze health data in real-time.</p><h3>Key Benefits of IoT in Healthcare</h3><ul><li><strong>Remote Patient Monitoring:</strong> Continuous tracking of vital signs and health metrics</li><li><strong>Preventive Care:</strong> Early detection of health issues before they become critical</li><li><strong>Medication Management:</strong> Smart pill dispensers and adherence monitoring</li><li><strong>Emergency Response:</strong> Automatic alerts for medical emergencies</li></ul><h3>Challenges and Solutions</h3><p>While IoT offers tremendous benefits, it also presents challenges such as data security, device interoperability, and regulatory compliance. Our team at MindTune Innovations addresses these challenges through:</p><ul><li>End-to-end encryption for data security</li><li>Standardized protocols for device communication</li><li>Compliance with healthcare regulations like HIPAA</li></ul><p>The future of healthcare lies in seamlessly connected systems that put patients at the center of care delivery.</p>', 'published'),
('PCB Design Best Practices for Wearable Devices', 'Engineering Challenges and Solutions in Miniaturized Electronics', 'MindTune Engineering Team', '2024-12-05', 'static/uploads/blog3.jpg', 'Learn about the critical considerations and best practices for designing PCBs for wearable devices, from power management to signal integrity.', '<p>Designing printed circuit boards (PCBs) for wearable devices presents unique challenges that require specialized knowledge and careful consideration of multiple factors including size constraints, power efficiency, and user comfort.</p><h3>Key Design Considerations</h3><p>When designing PCBs for wearables, engineers must balance numerous competing requirements:</p><h4>Size and Form Factor</h4><ul><li>Miniaturization without compromising functionality</li><li>Flexible and rigid-flex PCB options</li><li>Component placement optimization</li></ul><h4>Power Management</h4><ul><li>Ultra-low power consumption design</li><li>Battery life optimization</li><li>Efficient power conversion circuits</li><li>Sleep mode implementations</li></ul><h3>Signal Integrity in Compact Designs</h3><p>Maintaining signal integrity becomes increasingly challenging as PCB real estate decreases. Key strategies include:</p><ul><li>Careful impedance control</li><li>Minimizing electromagnetic interference (EMI)</li><li>Proper grounding techniques</li><li>Strategic component placement</li></ul><h3>Manufacturing Considerations</h3><p>Wearable PCBs often require specialized manufacturing processes:</p><ul><li>Fine-pitch components and micro-vias</li><li>Flexible materials for comfort</li><li>Environmental sealing for durability</li><li>Cost-effective high-volume production</li></ul><p>At MindTune Innovations, our PCB design expertise enables us to create compact, efficient, and reliable circuit boards that form the foundation of innovative wearable products.</p>', 'published');

INSERT INTO job_postings (job_title, job_type, department, location, salary_range, job_description, requirements, responsibilities, benefits, application_deadline, job_status) VALUES
('Senior Hardware Engineer', 'full-time', 'Engineering', 'Rawalpindi, Pakistan / Remote', 'PKR 150,000 - 250,000/month', 'Join our innovative team as a Senior Hardware Engineer and help design next-generation wearable devices and IoT products. You will work on cutting-edge EEG technology and contribute to revolutionary brain-computer interfaces.', '• Bachelor''s or Master''s degree in Electrical Engineering, Electronics Engineering, or related field\n• 5+ years of experience in hardware design and development\n• Proficiency in PCB design tools (Altium Designer, KiCad, Eagle)\n• Experience with microcontrollers (ESP32, STM32, Arduino)\n• Knowledge of analog and digital circuit design\n• Experience with EEG or biomedical device development (preferred)\n• Understanding of signal processing and embedded systems\n• Experience with wireless communication protocols (Bluetooth, WiFi, LoRa)', '• Design and develop hardware solutions for wearable and IoT devices\n• Create PCB layouts and manage the manufacturing process\n• Collaborate with firmware and software teams for system integration\n• Conduct testing and validation of hardware prototypes\n• Optimize designs for performance, power consumption, and cost\n• Prepare technical documentation and specifications\n• Work with suppliers and manufacturers for component sourcing\n• Troubleshoot and resolve hardware-related issues', '• Competitive salary and performance bonuses\n• Health insurance coverage\n• Professional development opportunities\n• Flexible working hours\n• Remote work options\n• Latest technology and tools\n• Collaborative and innovative work environment', '2025-09-15', 'active'),
('Mobile App Developer (React Native)', 'full-time', 'Software Development', 'Rawalpindi, Pakistan / Hybrid', 'PKR 120,000 - 200,000/month', 'We are seeking a talented Mobile App Developer to create user-friendly mobile applications that connect with our innovative wearable devices and IoT products.', '• Bachelor''s degree in Computer Science, Software Engineering, or related field\n• 3+ years of experience in mobile app development\n• Strong proficiency in React Native and JavaScript/TypeScript\n• Experience with native iOS and Android development\n• Knowledge of RESTful APIs and GraphQL\n• Experience with Bluetooth Low Energy (BLE) integration\n• Familiarity with state management (Redux, Context API)\n• Understanding of mobile app deployment processes\n• Experience with Git version control', '• Develop cross-platform mobile applications using React Native\n• Integrate mobile apps with hardware devices via Bluetooth and WiFi\n• Implement user authentication and data synchronization\n• Create intuitive user interfaces and user experiences\n• Optimize app performance and battery usage\n• Collaborate with hardware and backend teams\n• Conduct testing and debugging of mobile applications\n• Maintain and update existing mobile applications', '• Competitive salary package\n• Health and dental insurance\n• Annual performance bonuses\n• Learning and development budget\n• Flexible work arrangements\n• Modern office environment\n• Team building activities', '2025-08-30', 'active'),
('Firmware Engineer Intern', 'internship', 'Engineering', 'Rawalpindi, Pakistan', 'PKR 30,000 - 50,000/month', 'Join our team as a Firmware Engineer Intern and gain hands-on experience in developing embedded software for innovative wearable devices and IoT products.', '• Currently pursuing Bachelor''s or Master''s degree in Computer Engineering, Electrical Engineering, or related field\n• Strong programming skills in C/C++\n• Basic knowledge of microcontrollers and embedded systems\n• Familiarity with development environments (Arduino IDE, PlatformIO, etc.)\n• Understanding of communication protocols (UART, SPI, I2C)\n• Basic knowledge of version control systems (Git)\n• Eagerness to learn and work in a fast-paced environment\n• Good problem-solving and analytical skills', '• Assist in developing firmware for wearable devices and IoT products\n• Write and test embedded software code\n• Help with hardware-software integration tasks\n• Participate in debugging and troubleshooting activities\n• Document development processes and test results\n• Collaborate with senior engineers on various projects\n• Learn about signal processing and data acquisition\n• Assist in prototype testing and validation', '• Mentorship from experienced engineers\n• Hands-on experience with cutting-edge technology\n• Certificate of completion\n• Potential for full-time employment\n• Flexible internship duration (3-6 months)\n• Learning stipend\n• Access to company resources and tools', '2025-09-01', 'active');