import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib
import PyPDF2
import re

class JoSAAScraper:
    def __init__(self):
        self.base_url = "https://josaa.nic.in"
        self.news_url = "https://josaa.nic.in/news-event/"
        self.session = requests.Session()
        
    def scrape_news_page(self):
        """Scrape the main news and events page"""
        response = self.session.get(self.news_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the "What's New" section
        whats_new_section = soup.find('h2', string='Whats New').parent
        links = whats_new_section.find_all('a')
        
        updates = []
        for link in links:
            update = {
                'title': link.get_text().strip(),
                'url': self.base_url + link.get('href') if link.get('href').startswith('/') else link.get('href'),
                'scraped_at': datetime.now()
            }
            updates.append(update)
        
        return updates
    
    def extract_pdf_from_page(self, page_url):
        """Extract PDF links from individual update pages"""
        response = self.session.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for PDF links
        pdf_links = []
        for link in soup.find_all('a'):
            href = link.get('href', '')
            if href.endswith('.pdf'):
                pdf_url = self.base_url + href if href.startswith('/') else href
                pdf_links.append(pdf_url)
        
        return pdf_links
    
    def download_and_extract_pdf_text(self, pdf_url):
        """Download PDF and extract text content"""
        try:
            response = self.session.get(pdf_url)
            # Save PDF temporarily and extract text
            with open('temp.pdf', 'wb') as f:
                f.write(response.content)
            
            # Extract text from PDF
            with open('temp.pdf', 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            return text
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""
    
    def generate_summary(self, title, pdf_content):
        """Generate a brief summary for WhatsApp message"""
        # Simple keyword-based summary generation
        important_keywords = [
            'schedule', 'date', 'admission', 'counselling', 'seat',
            'allocation', 'registration', 'documents', 'fee',
            'important', 'notice', 'update', 'change'
        ]
        
        summary_lines = []
        lines = pdf_content.split('\n')
        
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip()
            if any(keyword.lower() in line.lower() for keyword in important_keywords):
                if len(line) > 10 and len(line) < 200:
                    summary_lines.append(line)
        
        summary = '\n'.join(summary_lines[:3])  # Top 3 relevant lines
        
        return summary if summary else "New update available. Please check the attached document."
    


if __name__ == "__main__":
    scraper = JoSAAScraper()
    updates = scraper.scrape_news_page()
    
    for update in updates:
        print(f"Title: {update['title']}")
        print(f"URL: {update['url']}")
        print(f"Scraped At: {update['scraped_at']}")
        
        pdf_links = scraper.extract_pdf_from_page(update['url'])
        if pdf_links:
            print(f"PDF Links: {pdf_links}")
            pdf_content = scraper.download_and_extract_pdf_text(pdf_links[0])
            summary = scraper.generate_summary(update['title'], pdf_content)
            print(f"Summary: {summary}\n")
        else:
            print("No PDF links found.\n")