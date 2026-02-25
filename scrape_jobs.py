import csv
import sys, os
import re, json
import pandas as pd
from jobspy import scrape_jobs
from tqdm import tqdm

SEARCH_BASES = ["indeed", "linkedin"]#, "google"] #, "glassdoor"] #, "bayt", "naukri", "bdjobs"
CITIES = ["Campinas, SP","São Paulo, SP","Florianópolis, SC","Curitiba, PR","worldwide"]
ROLES = ["Data Scientist","Machine Learning","Data Analyst","Data Engineer","AI Engineer"]

def get_jobs(role, location, country, days, total_results):

    jobs = scrape_jobs(
        site_name=SEARCH_BASES,
        search_term=role,
        google_search_term=f"{role} jobs near {location} since {days} days ago",
        location=location,
        results_wanted=total_results,
        hours_old=72,
        country_indeed=country,
        # linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
        # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
    )

    # print(f"Found {len(jobs)} jobs")
    # print(jobs.head(), jobs.columns)
    # jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel

    return jobs



def get_massive_data():
    print("Getting massive jobs data...")

    all_jobs = pd.DataFrame([])
    
    pbar = tqdm(total=len(ROLES) * len(CITIES))

    for role in ROLES:
        for city in CITIES:
            try:
                country = "worldwide" if city == "worldwide" else "Brazil"
                jobs = get_jobs(role, city, country, 100)
                all_jobs = pd.concat([all_jobs, jobs], ignore_index=True)
                print(len(all_jobs))
            
            except Exception as e:
                print(f"ERROR: {country} - {role} in {city}: {e}")
                continue

            pbar.update(1)
            
    print(f"Total of {len(all_jobs)} jobs found!")
    
    all_jobs.to_csv(f"jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
    
    print(f"--- DONE ---")


COLS = ["title","company","job_url","location","company_industry","site","salary_source","date_posted","description","job_type"]

def extract_skills(text):
    with open("skills.json","r") as f:
        skills = json.load(f)

    # print(f"Total skills: {len(skills)}")
    match_pattern = r'\b(?:' + '|'.join(re.escape(word) for word in skills) + r')\b'
    
    try:
        if not isinstance(text, str):
            text = str(text) if text is not None else ""
        
        return re.findall(match_pattern, text, re.IGNORECASE)
    except Exception as e:
        print(e)
        return None
    
    
if __name__ == "__main__":
    
    op = sys.argv[1]
    
    if op == "all":
        get_massive_data()
