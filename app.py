import streamlit as st
import pandas as pd
from scrape_jobs import *


st.set_page_config(layout="wide")

# Create two columns for layout
col1, col2 = st.columns([1, 3])  # Adjust the ratio as needed

# Input fields in the left column
with col1:
    st.header("Job Scraper")
    keyword = st.text_input("Enter job keyword (e.g., 'software engineer')", value="software engineer")
    location = st.text_input("Enter location (e.g., 'New York, NY')", value="New York, NY")
    num_jobs = st.number_input("Number of jobs to scrape", min_value=1, max_value=100, value=10)
    if st.button("Scrape Jobs"):
        with st.spinner("Scraping jobs..."):
            jobs = get_jobs(keyword, location, "us", num_jobs)

            df = pd.DataFrame(jobs)
            st.session_state.df = df  # Save dataframe to session state
            st.success("Scraped successfully!")

# Display dataframe in the right column
with col2:
    st.header("Job Results")
    if "df" in st.session_state:
        st.dataframe(st.session_state.df)

        # Option to download the data
        csv = st.session_state.df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="jobs.csv",
            mime="text/csv"
        )
