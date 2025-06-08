# md-exam-updates
Giving the updates of important dates of exams and couselling like: JEE Mains, JEE Advanced, JOSSA

1. Web Scraper Module

Purpose: Monitor JoSAA news-event page for new updates
Technology: Python with BeautifulSoup, Requests, Selenium (if needed)
Frequency: Every 15-30 minutes
Functions:

Scrape the main news page
Extract new document links
Download and process PDF files
Generate update summaries



2. Database Schema
-- Updates tracking table
CREATE TABLE josaa_updates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(500) NOT NULL,
    url VARCHAR(1000) NOT NULL,
    pdf_url VARCHAR(1000),
    pdf_content TEXT,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scraped_at TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    is_sent BOOLEAN DEFAULT FALSE
);

-- Authorization requests table
CREATE TABLE authorization_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    update_id INT,
    drafted_message TEXT,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    processed_by VARCHAR(100),
    FOREIGN KEY (update_id) REFERENCES josaa_updates(id)
);

-- WhatsApp groups configuration
CREATE TABLE whatsapp_groups (
    id INT PRIMARY KEY AUTO_INCREMENT,
    group_name VARCHAR(200),
    group_id VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


3. Authorization System

Admin Web Panel: Simple web interface for approval/rejection
Notification System: Email/SMS alerts to admin when new updates are detected
Manual Review: Admin can edit the drafted message before approval

4. WhatsApp Integration

WhatsApp Business API: For official business accounts
Alternative: WhatsApp Web automation (using libraries like whatsapp-web.js)
Message Format: Text + PDF attachment

Implementation Details
Phase 1: Web Scraper
Core Scraper Functions