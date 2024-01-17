import json 

file = open('indeed_jobs.json')
data = json.load(file)

for job in data:
    job_title = job['positionName']
    company = job['company']
    job_description = job['description']
    job_url = job['url']
    print(f'Position name: {job_title}')
    print(f'Company: {company}')
    print(f'Job description: {job_description}')
    print(f'URL: {job_url}')
    break