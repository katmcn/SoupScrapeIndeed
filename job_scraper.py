
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re

def proxy_url_generator(api_key, url):
    """Generates an url to connect to a proxy server"""
    payload = {'api_key': api_key, 'url': url}
    proxy_url = 'https://scrape.abstractapi.com/v1/?' + urlencode(payload)
    return proxy_url


def soup_generator(api_key, base_url, url_page):
    """Creates a soup object (a searchable and navigable representation of the HTML code)"""
    url = f'{base_url}+{url_page}'
    proxy_url = proxy_url_generator(api_key, url)
    r = requests.get(proxy_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def extract_total_search_results(soup):
    """Returns an integer value from the 'results', if listed on the website"""
    job_count_element = soup.find('div', class_='jobsearch-JobCountAndSortPane-jobCount css-1af0d6o eu4oa1w0')
    if job_count_element is not None:
        job_count_string = job_count_element.find('span').text.strip()
        numbers = re.findall(r'\d+', job_count_string)  # searches for and combines digits into one item in a list
        if numbers:
            return int(numbers[0])  # converts the first (and only in this instance) item in the list to an integer
        else:
            return None


def extract_job_data(soup, joblist):
    """Returns a list of dictionaries, containing the desired data from the given website"""
    if joblist is None:
        joblist = []
    divs = soup.find_all('div', class_='job_seen_beacon')
    for item in divs:
        title = item.find('span', attrs={'title': True}).text.strip()
        company = item.find('span', attrs={'companyName'}).text.strip()
        location = item.find('div', attrs={'companyLocation'}).text.strip()
        salary_element = item.find('div', class_='attribute_snippet', attrs={'Salary'})
        salary_text = salary_element.text.strip() if salary_element is not None else ''
        if '£' in salary_text:
            salary = salary_text
        else:
            salary = ''
        summary = item.find('div', class_='job-snippet').text.strip().replace('\n', '')

        job = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)
    return joblist
