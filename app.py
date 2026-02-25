import streamlit as st
import pandas as pd
from scrape_jobs import *


st.set_page_config(layout="wide")

col1, col2, col3 = st.columns([1, 3, 2])  # Adjust the ratio as needed

with col1:
    st.header("Jobs Search")
    keyword = st.text_input("Enter job keyword (e.g., 'software engineer')")
    city = st.text_input("Enter location (e.g., 'New York, NY')", value="São Paulo, SP")
    country = st.text_input("Enter country (e.g., 'USA')", value="Brazil")
    num_jobs = st.number_input("Total jobs to scrape", min_value=1, max_value=100, value=10)
    days_ago = st.number_input("Days ago", min_value=0, max_value=60, value=1)
    if st.button("Scrape Jobs"):
        with st.spinner("Scraping jobs..."):
            jobs = get_jobs(keyword, city, country, days_ago, num_jobs)

            df = pd.DataFrame(jobs)

            df["tech_skills"] = df["description"].apply(lambda x: extract_skills(x))

            cols = ['title','company','tech_skills','location','job_url','company_industry', 'site','salary_source', 'date_posted', 'description', 'job_type']
            df = df[cols]
            
            st.session_state.df = df  # Save dataframe to session state
            st.success("Scraped successfully!")


with col2:
    if "df" in st.session_state:
        st.header("Jobs Results")

        skills = []
        st.session_state.df["tech_skills"].apply(lambda s: skills.extend(s))
        skills = list(set(skills))
        # print("skills",skills)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Skills", options=skills)

        event = st.dataframe(
            st.session_state.df, 
            on_select="rerun", 
            selection_mode="single-row",
            height=600
        )

        # 3. Pegar os dados da linha selecionada
        selected_index = None
        if event.selection.rows:
            selected_index = event.selection.rows[0]
        
        # Option to download the data
        # csv = st.session_state.df.to_csv(index=False)
        # st.download_button(
        #     label="Download CSV",
        #     data=csv,
        #     file_name="jobs.csv",
        #     mime="text/csv"
        # )

with col3:
    
    if "df" in st.session_state:
        if selected_index:
            job = st.session_state.df.iloc[selected_index]

            # info
            st.markdown(f"### {job["title"]}")
            st.markdown(f"#### {job["company"]}")
            st.markdown(f"Skills: {job["tech_skills"]}")
            st.markdown(f"{job["job_url"]} (Posted at {job["date_posted"]})")
            
            # description
            job_desc = job["description"]
            
            if isinstance(job_desc, str):
                job_desc = re.sub(r'\*{3}(.+?)\*{3}', r'### \1', job_desc)
                job_desc = re.sub(r'\*{2}(.+?)\*{2}', r'**\1**', job_desc)
                # Remove excessive blank lines (3+ newlines → 2)
                job_desc = re.sub(r'\n{3,}', '\n\n', job_desc)
                
                with st.container(height=600):
                    st.markdown(job_desc)

    