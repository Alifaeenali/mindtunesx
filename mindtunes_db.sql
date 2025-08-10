create database if not exists mindtunes_db;  
use mindtunes_db; 

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
create table if not exists heroTable(
hero_id int auto_increment primary key, 
heroImg varchar(200), 
heroHead varchar(200), 
heroDesc text
); 

create table if not exists Ourclients(
clients_id int auto_increment primary key, 
clientHead varchar(200), 
clientDesc text, 
client1 varchar(200), 
client2 varchar(200), 
client3 varchar(200)
); 

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

 
create table if not exists know(
know_id int auto_increment primary key, 
knowHead varchar(200),
knowDescp varchar(500),
knowVideo varchar(200), 
knowImage varchar(200)

); 
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

create table if not exists footer(
ftr_id int auto_increment primary key, 
ftr_link1 varchar(200),
ftr_link2 varchar(200),
ftr_link3 varchar(200),
ftr_link4 varchar(200)
);

-- Insert dummy data into navTable
INSERT INTO navTable (navLogo, navAnchor1, navAnchor2, navAnchor3, navAnchor4, navAnchor5, navAnchor6) VALUES
('static/assets/images/updatedMindtuneLogo.png', 'Home', 'About', 'Services', 'News', 'Contact Us', 'Careers');

-- Insert dummy data into heroTable
INSERT INTO heroTable (heroImg, heroHead, heroDesc) VALUES
('static/assets/images/hero.png', 'We Engineer Next-Gen Wearables, Smart IoT Products & Full-Stack Tech Solutions', 'At MindTune Innovations, we help you bring bold product ideas to life. From connected devices to powerful software, our team handles every step including hardware, firmware, mobile apps, and mechanical design all under one roof.Whether you’re a startup, research team, or enterprise, we deliver complete and ready-to-deploy solutions that are reliable, scalable, and user-friendly.');

-- Insert dummy data into Ourclients
INSERT INTO Ourclients (clientHead, clientDesc, client1, client2, client3) VALUES
('Trusted by Leading Innovators', 'Our clientele includes a diverse range of companies, from tech startups to healthcare providers, all seeking to leverage the power of sound for human flourishing.', 'static/assets/images/client1.png', 'static/assets/images/client2.png', 'static/assets/images/client3.png');

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