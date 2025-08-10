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

-- Alter statements (if not already run)
ALTER TABLE innovations ADD innovationMediaType VARCHAR(10) DEFAULT 'video';
ALTER TABLE know ADD knowMediaType VARCHAR(10) DEFAULT 'video';

INSERT INTO servicesTable (service_head, service_desc) VALUES
('IoT & Embedded Systems Development', 'We design and build smart IoT solutions powered by efficient embedded systems, enabling seamless device connectivity, data collection, and automation for consumer and industrial applications. Our engineers specialize in microcontrollers, sensors, and wireless protocols for optimized performance.'),
('EEG Wearables & Biosensor Solutions', 'MindTune pioneers EEG-powered wearables and biosensor integrations, enabling real-time tracking of mental and physical states. From earbuds to headsets, we turn neuroscience into user-friendly products for health, productivity, and research markets.'),
('PCB Design & Hardware Prototyping', 'Our hardware team delivers PCB designs and rapid prototypes that meet high standards of performance, efficiency, and reliability. We handle every stage — from schematics to assembled boards.'),
('Firmware & Machine Learning Integration', 'We create efficient firmware optimized for real-time data and integrate machine learning algorithms to deliver intelligent, adaptive devices. Our systems enhance performance while enabling edge-level AI features.'),
('Mobile App & Cloud Development', 'We build scalable mobile apps and cloud platforms to connect devices, users, and data seamlessly. From Bluetooth integration to cloud dashboards, we bring IoT ecosystems to life.'),
('Product Design & Mechanical CAD', 'Our mechanical engineers create functional and aesthetically refined designs using advanced CAD tools. We design housings, enclosures, and product structures that are production-ready.'),
('Team & Culture', 'At MindTune Innovations, our culture thrives on collaboration, creativity, and technical excellence. Our multidisciplinary team of engineers, designers, and innovators works together to develop cutting-edge IoT, EEG, and smart tech solutions, fostering a culture where ideas grow into impactful products.');

