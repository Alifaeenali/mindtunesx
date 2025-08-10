create database if not exists mindtunes_db;  
use mindtunes_db; 

-- Table for navigation links
create table if not exists navTable(
    nav_id int auto_increment primary key, 
    navLogo varchar(200), 
    navAnchor1 varchar(200), 
    navAnchor2 varchar(200), 
    navAnchor3 varchar(200), 
    navAnchor4 varchar(200), 
    navAnchor5 varchar(200), 
    navAnchor6 varchar(200)
); 

-- Table for the hero section
create table if not exists heroTable(
    hero_id int auto_increment primary key, 
    heroImg varchar(200), 
    heroHead varchar(200), 
    heroDesc text
); 

-- Table for the "Our Clients" section text
create table if not exists Ourclients(
    clients_id int auto_increment primary key, 
    clientHead varchar(200), 
    clientDesc text
); 

-- Table for the dynamic client logos
create table if not exists client_logos (
    logo_id int auto_increment primary key,
    logo_url varchar(255),
    logo_order int
);

-- Table for the "Innovations" section
create table if not exists innovations (
    innovation_id int auto_increment primary key, 
    innovationSubHead varchar(200), 
    innovationHead varchar(200), 
    innovationDescp varchar(500), 
    innovationl1 text, 
    innovationl2 text, 
    innovationl3 text, 
    innovationl4 text, 
    innovationVideo varchar(200), 
    innovationImage varchar(200)
);

-- Table for the "Know" section
create table if not exists know(
    know_id int auto_increment primary key, 
    knowHead varchar(200),
    knowDescp varchar(500),
    knowVideo varchar(200), 
    knowImage varchar(200)
); 

-- Table for the "Statistics" section
create table if not exists statistics (
    stat_id int auto_increment primary key, 
    statHead varchar(200),
    statDescp varchar(500),
    headCard1 varchar(200),
    headCard2 varchar(200),
    headCard3 varchar(200),
    DescCard1 varchar(200),
    DescCard2 varchar(200),
    DescCard3 varchar(200),
    ImgCard1 varchar(200),
    ImgCard2 varchar(200),
    ImgCard3 varchar(200)
); 

-- Table for the footer
create table if not exists footer(
    ftr_id int auto_increment primary key, 
    ftr_link1 varchar(200),
    ftr_link2 varchar(200),
    ftr_link3 varchar(200),
    ftr_link4 varchar(200)
);

-- Table for the "About Us" page - UPDATED COLUMNS
create table if not exists aboutUs(
    about_id int auto_increment primary key,
    about_head varchar(200),
    about_desc text,
    about_title varchar(500),
    about_subtitle varchar(500)
);

-- NEW Table for dynamic founders section
create table if not exists founders (
    founder_id int auto_increment primary key,
    founder_name varchar(200),
    founder_role varchar(200),
    founder_image varchar(200),
    founder_description text,
    founder_order int
);

-- NEW Table for dynamic "Who We Work With" section
create table if not exists who_we_work_with (
    work_id int auto_increment primary key,
    work_icon varchar(20), -- Store emojis or icon classes
    work_title varchar(200),
    work_description text,
    work_order int
);

-- Table for the "Services" page
create table if not exists servicesTable(
    service_id int auto_increment primary key,
    service_head varchar(200),
    service_desc text
);

-- Insert dummy data into navTable
INSERT INTO navTable (navLogo, navAnchor1, navAnchor2, navAnchor3, navAnchor4, navAnchor5, navAnchor6) VALUES
('static/assets/images/updatedMindtuneLogo.png', 'Home', 'About', 'Services', 'News', 'Contact Us', 'Careers');

-- Insert dummy data into heroTable
INSERT INTO heroTable (heroImg, heroHead, heroDesc) VALUES
('static/assets/images/hero.png', 'We Engineer Next-Gen Wearables, Smart IoT Products & Full-Stack Tech Solutions', 'At MindTune Innovations, we help you bring bold product ideas to life. From connected devices to powerful software, our team handles every step including hardware, firmware, mobile apps, and mechanical design all under one roof.Whether you’re a startup, research team, or enterprise, we deliver complete and ready-to-deploy solutions that are reliable, scalable, and user-friendly.');

-- Insert dummy data into Ourclients (text data only)
INSERT INTO Ourclients (clientHead, clientDesc) VALUES
('Trusted by Leading Innovators', 'Our clientele includes a diverse range of companies, from tech startups to healthcare providers, all seeking to leverage the power of sound for human flourishing.');

-- Insert dummy data into client_logos (logo images)
INSERT INTO client_logos (logo_url, logo_order) VALUES
('static/assets/images/client1.png', 1),
('static/assets/images/client2.png', 2),
('static/assets/images/client3.png', 3);

-- Insert dummy data into innovations
INSERT INTO innovations (innovationSubHead, innovationHead, innovationDescp, innovationl1, innovationl2, innovationl3, innovationl4, innovationVideo, innovationImage) VALUES
('Pioneering the Future', 'Neuro-Acoustic Innovations', 'Discover how our proprietary algorithms and sound frequencies are revolutionizing mental performance and relaxation. We integrate the latest neuroscience with artistic sound design.',
'Personalized Brainwave Entrainment for focus and calm.',
'Adaptive Soundscapes that respond to your real-time biometric data.',
'Gamified Cognitive Training modules for enhanced learning.',
'Proprietary AI-driven sound generation for unique experiences.',
'static/assets/videos/a_new_course.webm', 'static/assets/images/hero.png');

-- Insert dummy data into know
INSERT INTO know (knowHead, knowDescp, knowVideo, knowImage) VALUES
('Deep Dive into Neuro-Acoustics', 'Learn more about the science behind MindTunes. Our expert-led content explains how specific sound frequencies influence brain activity and promote desired mental states.',
'static/assets/videos/get-to-know.webm', 'static/assets/images/hero.png');

-- Insert dummy data into statistics
INSERT INTO statistics (statHead, statDescp, headCard1, headCard2, headCard3, DescCard1, DescCard2, DescCard3, ImgCard1, ImgCard2, ImgCard3) VALUES
('Impact and Achievements', 'See the measurable difference MindTunes is making in people\'s lives and in various industries. Our data speaks volumes.',
'90% Improvement', '20K+ Users', '15+ Patents',
'Users report significant improvement in focus and sleep quality.',
'Global community benefiting from MindTunes daily.',
'Cutting-edge technology protected by intellectual property.',
'static/assets/images/hero.png', 'static/assets/images/hero.png', 'static/assets/images/hero.png');

-- Insert dummy data into footer
INSERT INTO footer (ftr_link1, ftr_link2, ftr_link3, ftr_link4) VALUES
('Privacy Policy', 'Terms of Service', 'Support', 'Careers');

-- Insert dummy data for aboutUs page - UPDATED DATA
INSERT INTO aboutUs (about_head, about_desc, about_title, about_subtitle) VALUES
('About MindTune Innovations', 'Building intelligent products that connect hardware, software, and people', 
'About Us', 'MindTune Innovations is a technology company based in Pakistan, focused on building intelligent products that connect hardware, software, and people. We bring together expertise in IoT, embedded systems, wearable tech, PCB design, and mobile app development — all within one team.');

-- Insert dummy data for founders
INSERT INTO founders (founder_name, founder_role, founder_image, founder_description, founder_order) VALUES
('Abdul Basit', 'CEO & DIRECTOR', 'static/assets/images/abbasit.png', 'Abdul Basit is an Electrical Engineer and technology innovator with a proven track record in developing high-performance IoT and smart electronic solutions. At MindTune Innovations, he leads the company\'s product development strategy, combining technical depth in hardware and embedded systems with a clear vision for scalable, market-ready solutions. His focus is on building products that deliver measurable value and position MindTune as a leader in EEG and IoT-driven technologies.', 1),
('Ryan Ahmed', 'COO & DIRECTOR', 'static/assets/images/rayanAhmed.png', 'Ryan Ahmed is the Co-Founder of Niura and a strategic leader in wearable neuroscience technologies. With a background in launching and scaling consumer tech ventures, Ryan has positioned Niura as a pioneer in EEG-powered earbuds designed for mental performance tracking. His expertise in bridging neuroscience with consumer technology allows Niura and MindTune to capture emerging market opportunities and drive significant growth potential in the wearable tech space.', 2);

-- Insert dummy data for who_we_work_with
INSERT INTO who_we_work_with (work_icon, work_title, work_description, work_order) VALUES
('🏥', 'Health-Tech Startups', 'Building wearable products and health monitoring solutions', 1),
('⚙️', 'Engineering Teams', 'Embedded systems and PCB development support', 2),
('🔬', 'Research Labs', 'Developing biomedical and IoT research tools', 3),
('🏢', 'Enterprise Companies', 'Custom hardware with mobile and cloud integration', 4);

ALTER TABLE aboutUs 
ADD COLUMN about_secondary_desc TEXT,
ADD COLUMN aboutHeroImage VARCHAR(200),
ADD COLUMN achievement_title VARCHAR(200),
ADD COLUMN achievement_subtitle TEXT,
ADD COLUMN mission_text TEXT,
ADD COLUMN belief1 VARCHAR(500),
ADD COLUMN belief2 VARCHAR(500),
ADD COLUMN belief3 VARCHAR(500),
ADD COLUMN belief4 VARCHAR(500);

-- Update existing record with sample data (optional)
UPDATE aboutUs SET 
    about_secondary_desc = 'MindTune Innovations is a technology company based in Pakistan, focused on building intelligent products that connect hardware, software, and people. We bring together expertise in IoT, embedded systems, wearable tech, PCB design, and mobile app development — all within one team.',
    aboutHeroImage = 'static/assets/images/hero.png',
    achievement_title = 'Innovation & Excellence',
    achievement_subtitle = 'Leading the way in wearable technology and IoT solutions with cutting-edge research and development.',
    mission_text = 'Our mission is to bridge the gap between advanced technology and everyday life by creating intelligent, user-friendly products that enhance human capabilities and well-being.',
    belief1 = 'Innovation drives progress',
    belief2 = 'Quality over quantity',
    belief3 = 'User-centered design',
    belief4 = 'Collaborative excellence'
WHERE about_id = 1;

-- Table for contact form submissions
create table if not exists contact_submissions(
    id int auto_increment primary key,
    name varchar(255) not null,
    email varchar(255) not null,
    subject varchar(255),
    message text,
    submission_date datetime default current_timestamp
);

-- Add this to your existing mindtunes_db.sql file

-- Table for blog posts
CREATE TABLE IF NOT EXISTS blog_posts (
    blog_id INT AUTO_INCREMENT PRIMARY KEY,
    blog_title VARCHAR(255) NOT NULL,
    blog_subtitle VARCHAR(255),
    blog_author VARCHAR(100) NOT NULL,
    blog_date DATE NOT NULL,
    blog_image VARCHAR(255),
    blog_excerpt TEXT, -- Short description for the blog list page
    blog_content LONGTEXT NOT NULL, -- Full blog content
    blog_status ENUM('draft', 'published') DEFAULT 'published',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample blog data
INSERT INTO blog_posts (blog_title, blog_subtitle, blog_author, blog_date, blog_image, blog_excerpt, blog_content, blog_status) VALUES
(
    'The Future of EEG Wearables in Healthcare',
    'How Brain-Computer Interfaces are Revolutionizing Patient Care',
    'Abdul Basit',
    '2024-12-15',
    'static/uploads/blog1.jpg',
    'Explore how EEG wearables are transforming healthcare by providing real-time brain monitoring capabilities for better patient outcomes.',
    '<p>The healthcare industry is experiencing a revolutionary transformation with the advent of EEG (Electroencephalography) wearables. These innovative devices are opening new frontiers in patient care, mental health monitoring, and neurological disorder management.</p>

<h3>What are EEG Wearables?</h3>
<p>EEG wearables are portable, non-invasive devices that can monitor brain activity in real-time. Unlike traditional EEG systems that require clinical settings and multiple electrodes, modern wearables integrate seamlessly into everyday life through headbands, earbuds, or caps.</p>

<h3>Applications in Healthcare</h3>
<ul>
<li><strong>Seizure Detection:</strong> Real-time monitoring can alert patients and caregivers to impending seizures</li>
<li><strong>Sleep Disorders:</strong> Continuous monitoring of sleep patterns and brain waves during rest</li>
<li><strong>Mental Health:</strong> Tracking stress levels, anxiety, and depression markers</li>
<li><strong>Cognitive Assessment:</strong> Monitoring cognitive decline in aging populations</li>
</ul>

<h3>The Technology Behind the Innovation</h3>
<p>Modern EEG wearables utilize advanced signal processing, machine learning algorithms, and miniaturized electronics to deliver clinical-grade data. The integration of IoT connectivity allows for continuous data streaming to healthcare providers.</p>

<p>At MindTune Innovations, we are at the forefront of this technology, developing next-generation EEG wearables that combine accuracy, comfort, and affordability.</p>',
    'published'
),
(
    'IoT in Smart Healthcare: Connecting Devices for Better Outcomes',
    'Building the Connected Healthcare Ecosystem of Tomorrow',
    'Ryan Ahmed',
    '2024-12-10',
    'static/uploads/blog2.jpg',
    'Discover how Internet of Things (IoT) technology is creating interconnected healthcare systems that improve patient care and operational efficiency.',
    '<p>The Internet of Things (IoT) is reshaping healthcare delivery by creating interconnected ecosystems of smart devices, sensors, and applications that work together to improve patient outcomes and streamline healthcare operations.</p>

<h3>The Connected Healthcare Landscape</h3>
<p>IoT in healthcare encompasses a vast network of connected devices including wearable sensors, smart medical equipment, environmental monitors, and mobile health applications. These devices collect, transmit, and analyze health data in real-time.</p>

<h3>Key Benefits of IoT in Healthcare</h3>
<ul>
<li><strong>Remote Patient Monitoring:</strong> Continuous tracking of vital signs and health metrics</li>
<li><strong>Preventive Care:</strong> Early detection of health issues before they become critical</li>
<li><strong>Medication Management:</strong> Smart pill dispensers and adherence monitoring</li>
<li><strong>Emergency Response:</strong> Automatic alerts for medical emergencies</li>
</ul>

<h3>Challenges and Solutions</h3>
<p>While IoT offers tremendous benefits, it also presents challenges such as data security, device interoperability, and regulatory compliance. Our team at MindTune Innovations addresses these challenges through:</p>
<ul>
<li>End-to-end encryption for data security</li>
<li>Standardized protocols for device communication</li>
<li>Compliance with healthcare regulations like HIPAA</li>
</ul>

<p>The future of healthcare lies in seamlessly connected systems that put patients at the center of care delivery.</p>',
    'published'
),
(
    'PCB Design Best Practices for Wearable Devices',
    'Engineering Challenges and Solutions in Miniaturized Electronics',
    'MindTune Engineering Team',
    '2024-12-05',
    'static/uploads/blog3.jpg',
    'Learn about the critical considerations and best practices for designing PCBs for wearable devices, from power management to signal integrity.',
    '<p>Designing printed circuit boards (PCBs) for wearable devices presents unique challenges that require specialized knowledge and careful consideration of multiple factors including size constraints, power efficiency, and user comfort.</p>

<h3>Key Design Considerations</h3>
<p>When designing PCBs for wearables, engineers must balance numerous competing requirements:</p>

<h4>Size and Form Factor</h4>
<ul>
<li>Miniaturization without compromising functionality</li>
<li>Flexible and rigid-flex PCB options</li>
<li>Component placement optimization</li>
</ul>

<h4>Power Management</h4>
<ul>
<li>Ultra-low power consumption design</li>
<li>Battery life optimization</li>
<li>Efficient power conversion circuits</li>
<li>Sleep mode implementations</li>
</ul>

<h3>Signal Integrity in Compact Designs</h3>
<p>Maintaining signal integrity becomes increasingly challenging as PCB real estate decreases. Key strategies include:</p>
<ul>
<li>Careful impedance control</li>
<li>Minimizing electromagnetic interference (EMI)</li>
<li>Proper grounding techniques</li>
<li>Strategic component placement</li>
</ul>

<h3>Manufacturing Considerations</h3>
<p>Wearable PCBs often require specialized manufacturing processes:</p>
<ul>
<li>Fine-pitch components and micro-vias</li>
<li>Flexible materials for comfort</li>
<li>Environmental sealing for durability</li>
<li>Cost-effective high-volume production</li>
</ul>

<p>At MindTune Innovations, our PCB design expertise enables us to create compact, efficient, and reliable circuit boards that form the foundation of innovative wearable products.</p>',
    'published'
);