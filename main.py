import config
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import pandas as pd
import re


# AbstractAPI
def get_scrapeops_url(api_key, url):
    payload = {'api_key': api_key, 'url': url}
    proxy_url = 'https://scrape.abstractapi.com/v1/?' + urlencode(payload)
    return proxy_url


def extract(api_key, base_url, url_page):
    url = f'{base_url}+{url_page}'
    proxy_url = get_scrapeops_url(api_key, url)
    r = requests.get(proxy_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    #return r.status_code #to check the connection has been made
    return soup


def extract_job_count(soup):
    job_count_element = soup.find('div', class_='jobsearch-JobCountAndSortPane-jobCount css-1af0d6o eu4oa1w0')
    if job_count_element is not None:
        job_count_string = job_count_element.find('span').text.strip()
        numbers = re.findall(r'\d+', job_count_string)  # searches for and combines digits into one item in a list
        if numbers:
            return int(numbers[0])  # converts the first (and only in this instance) item in the list to an integer
        else:
            return None


def transform(soup):
    divs = soup.find_all('div', class_='job_seen_beacon')
    for item in divs:
        title = item.find('span', attrs={'title': True}).text.strip()
        # if title_span is not None:
        # title = title_span.text.strip()
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

# this was my attempt to automatically scrape until the last page
# while next_page_exists:
#     navigation = soup.find_all('div', class_='css-tvvxwd ecydgvn1')
#     for i in navigation:
#         href_element = i.find('a', attrs={'href': True})
#         a_element = i.find('a', attrs={'data-testid': True})
#         data_testid = a_element['data-testid'] if a_element is not None else None
#         # print(a_element)
#         # print(data_testid)
#         if data_testid == 'pagination-page-next':
#             next_page_num = int(next_url[-2:]) + 10 #takes the page number from the last url and manually adds 10
#             next_url = f'{config.START_URL}{str(next_page_num)}'
#             print(next_url)
#         elif href_element is not None and href_element.get('href'):
#             href = href_element['href']
#             next_url = f'https://uk.indeed.com/' + href  # can also use: href['href']
#             print(next_url)
#             c = extract(next_url)
#             transform(c)


API = config.API_KEY
BASE_URL = config.START_URL
soup = extract(API, BASE_URL, 0)
joblist = []
# next_page_exists = True
total_jobs = extract_job_count(soup)
page_number = 0
url_number = 0
jobs_left = True


print(f'There are currently {total_jobs} jobs on Indeed')
print(f'{len(joblist)} have been scraped')
while jobs_left:
    if len(joblist) >= total_jobs:
        jobs_left = False
    else:
        page_number += 1
        print(f"Getting page {page_number}")
        # url = f'{config.START_URL}{url_number}'
        # print(url)
        c = extract(API, BASE_URL, url_number)
        joblist = transform(c)
        # print(f'{len(joblist)}/{total_jobs} have been scraped')
        print(len(joblist))
        url_number += 10
print('Scrape completed')
print(f'{len(joblist)} jobs have been gathered')
df = pd.DataFrame(joblist)
print(df)
df.to_csv('indeed_jobs_14_06_23.csv')

# for i in range(0,40,10):
#     url = f'{config.START_URL}{i}'
#     print(url)
#     c = extract(url)
#     transform(c)
#     print(len(joblist))


