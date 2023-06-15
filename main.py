import config
from job_scraper import soup_generator, extract_total_search_results, extract_job_data
import pandas as pd

API = config.API_KEY
BASE_URL = config.START_URL
soup = soup_generator(API, BASE_URL, 0)
joblist = []
total_jobs = extract_total_search_results(soup)
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
        c = soup_generator(API, BASE_URL, url_number)
        joblist = extract_job_data(c, joblist)
        print(f'Jobs collected: {len(joblist)}')
        url_number += 10
print('Scrape completed')
print(f'A total of {len(joblist)} jobs have been gathered')
df = pd.DataFrame(joblist)
print(df)
# df.to_csv('indeed_jobs_14_06_23.csv')



