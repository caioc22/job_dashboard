import csv
from jobspy import scrape_jobs

SEARCH_BASES = ["indeed", "linkedin", "zip_recruiter", "google", "glassdoor"] #, "bayt", "naukri", "bdjobs"


def get_jobs(role, location, country, total_results):

    jobs = scrape_jobs(
        site_name=SEARCH_BASES,
        search_term=role,
        google_search_term=f"{role} jobs near {location} since yesterday",
        location=location,
        results_wanted=total_results,
        hours_old=72,
        country_indeed=country,
        # linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
        # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
    )

    print(f"Found {len(jobs)} jobs")
    print(jobs.head(), jobs.columns)

    return jobs

    # jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel