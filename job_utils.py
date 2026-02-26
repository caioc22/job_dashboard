import csv
import sys, os
import re, json
import pandas as pd
from jobspy import scrape_jobs
from tqdm import tqdm

SEARCH_BASES = ["indeed", "linkedin"]#, "google"] #, "glassdoor"] #, "bayt", "naukri", "bdjobs"
CITIES = [
    "São Paulo, SP",
    "Campinas, SP",
    "São José dos Campos, SP",
    "Belo Horizonte, MG",
    "Rio de Janeiro, RJ",
    "Uberlândia, MG",
    "Florianópolis, SC",
    "Blumenau, SC",
    "Curitiba, PR",
    "Porto Alegre, RS",
    "Recife, PE",
    "Fortaleza, CE",
    "Salvador, BA",
    "Brasília, DF",
    "Goiânia, GO",
    "Manaus, AM"
]

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


def format_df(df):

    df["tech_skills"] = df["description"].apply(lambda x: extract_skills(x))

    cols = ['title','company','tech_skills','location','job_url','company_industry', 'site','salary_source', 'date_posted', 'description', 'job_type']
    df = df[cols]

    return df


def count_skills(df):

    # df_counts = df['tech_skills'] \
    #         .apply(lambda x: list(set(x)) if isinstance(x, list) else []) \
    #         .explode() \
    #         .value_counts() \
    #         .reset_index()

    # df_counts.columns = ['skill', 'total']

    print("columns",df.columns)
    
    df_exploded = df.explode('tech_skills')
    
    skill_counts = (
        df_exploded.groupby(['location', 'tech_skills'])
        .size()
        .reset_index(name='total')
        .rename(columns={'tech_skills': 'skill'})
    )
    
    return skill_counts

    return df_counts

    skill_counts = count_skills(df)

    skill_counts.set_index('skill')['total'].plot(kind='bar', figsize=(10, 6), color='skyblue')


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

    all_jobs["tech_skills"] = all_jobs
    
    all_jobs.to_csv(f"jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
    
    print(f"--- DONE ---")


if __name__ == "__main__":
    
    op = sys.argv[1]
    
    if op == "all":
        get_massive_data()
