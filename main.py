import config
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urlencode
import pandas as pd


def get_scrapeops_url(START_URL):
    payload = {'api_key': config.API_KEY, 'url': config.START_URL}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

def extract(page, START_URL):
    parsed_url = urlparse(START_URL)
    query_params = parsed_url.query

    if '&start=' in query_params:
        start_index = query_params.index('&start=')
        modified_query = query_params[:start_index + len('&start=')]
        modified_url = urlunparse(parsed_url._replace(query=modified_query))
    else:
        print('url not valid')

    url = f'{modified_url}+{page}'
    proxy_url = get_scrapeops_url(url)
    r = requests.get(proxy_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    #return r.status_code #to check the connection has been made
    return soup

def transform(soup):
    divs = soup.find_all('div', class_='job_seen_beacon')
    for item in divs:
        title_span = item.find('span', attrs={'title': True})
        #if title_span is not None:
        title = title_span.text.strip()
        company_span = item.find('span', attrs={'companyName'})
        company = company_span.text.strip()
        location_span = item.find('div', attrs={'companyLocation'})
        location = location_span.text.strip()
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
    return


joblist = []

for i in range(0,40,10):
    print(f"Getting page, {i}")
    c = extract(0, config.START_URL)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
#df.to_csv('indeed_data_jobs.csv')




