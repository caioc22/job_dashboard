import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from job_utils import *


st.set_page_config(layout="wide")

st.title("Overview")


import matplotlib.pyplot as plt
import pandas as pd

def make_fig(data):
    """
    Creates a grouped bar chart of skills segmented by city.

    Args:
        data (pd.DataFrame): DataFrame with columns ['skill', 'city', 'total'].

    Returns:
        matplotlib.figure.Figure: The generated figure.
    """
    # Pivot the data for grouped bars
    pivot_data = data.pivot(index='skill', columns='location', values='total')
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot grouped bars
    pivot_data.plot(kind='bar', ax=ax, width=0.8, colormap='viridis')
    
    # Customize the plot
    ax.set_title('Skill Distribution by Location', pad=20, fontsize=16)
    ax.set_xlabel('Skills', labelpad=15, fontsize=12)
    ax.set_ylabel('Count', labelpad=15, fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    ax.legend(title='Location', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    return fig


import plotly.express as px
import pandas as pd

def make_stacked_bar(data):

    fig = px.bar(
        data,
        x='skill',
        y='total',
        color='location',
        # title='Skill Distribution by Location',
        labels={'total': 'Count', 'skill': 'Skills'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Customize layout
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=100, b=20),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        xaxis=dict(tickangle=45)
    )
    
    # Add interactive hover data
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>City: %{fullData.name}<br>Count: %{y}<extra></extra>"
    )
    
    return fig


col1, col2 = st.columns([1,1])

with col1:
    st.header("Skills")

    with st.spinner("Loading..."):

        df = pd.read_csv("jobs.csv")
        
        st.session_state["df"] = df

        df = format_df(df)
        
        dfsk = count_skills(df)
        
        fig = make_stacked_bar(dfsk)

        st.plotly_chart(fig, use_container_width=True)

# Helper function to convert figure to PNG
# def fig_to_png(fig):
#     import io
#     buf = io.BytesIO()
#     fig.savefig(buf, format='png', dpi=300)
#     buf.seek(0)
#     return buf


