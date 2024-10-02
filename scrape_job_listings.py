import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_job_listings(url):
    # Send a request to the specified URL
    response = requests.get(url)
    # Check if the request was successful
    response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)

    # Parse the content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    job_listings = []
    # Find all job postings on the page
    for job in soup.find_all('div', class_='job_seen_beacon'):
        title = job.find('h2').text.strip()
        company = job.find('span', class_='companyName').text.strip()
        location = job.find('div', class_='companyLocation').text.strip()
        date_posted = job.find('span', class_='date').text.strip()
        job_link = job.find('a')['href']

        # Append the extracted details to the job_listings list
        job_listings.append({
            'Title': title,
            'Company': company,
            'Location': location,
            'Date Posted': date_posted,
            'Job Link': job_link
        })

    return job_listings

def save_to_csv(job_listings, filename='job_listings.csv'):
    # Convert the job listings to a DataFrame and save to CSV
    df = pd.DataFrame(job_listings)
    df.to_csv(filename, index=False)

if __name__ == '__main__':
    # Define the URL for the job search
    url = 'https://www.indeed.com/jobs?q=Python+Developer&l=New+York'
    # Scrape job listings from the URL
    job_listings = scrape_job_listings(url)
    # Save the listings to a CSV file
    save_to_csv(job_listings)
    print(f"Scraped {len(job_listings)} job listings.")
