import streamlit as st
import pandas as pd
from job_utils import *


overview_pg = st.Page("pages/overview.py", title="Overview")
search_pg = st.Page("pages/search.py", title="Search")

pg = st.navigation([overview_pg, search_pg], position="top")

pg.run()