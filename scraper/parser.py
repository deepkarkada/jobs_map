import json 
import sqlalchemy
from database import jobs, connect_and_create, commit

def get_data():
    file = open('indeed_jobs.json')
    data = json.load(file)
    return data

if __name__ == '__main__':
    ## Get the parsed jobs data from dataset
    data = get_data()

    ## Create and connect to the database
    engine, session = connect_and_create()
    table = jobs

    ## Add to database
    for job in data:
        try:
            # If the record already doesn't exist
            #if session.query(table).filter_by(**filter_logic).scalar() is None:
            job_id = job['id']
            posting_date = job['postingDateParsed']
            job_title = job['positionName']
            company = job['company']
            job_description = job['description'][:9999]
            job_url = job['url']

            # Create a new database entry
            entry = jobs(id=job_id, date=posting_date, title=job_title, company=company, description=job_description, url=job_url)
            commit(session = session, entry = entry)

            print(f'Inserted into database: {entry}')
        
        except sqlalchemy.exc.IntegrityError:
            continue
        
        except sqlalchemy.exc.InvalidRequestError:
            continue
