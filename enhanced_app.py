
import streamlit as st
import pandas as pd
import plotly.express as px

# Set the Streamlit page configuration with an icon and title
st.set_page_config(layout='wide', page_title='📊 Startup Funding Analysis')

# Cache the data loading to improve performance
@st.cache_data
def load_data():
    df = pd.read_csv("startup_cleaned (1).csv")

    # Fix years in the date column
    def fix_year(date_str):
        if date_str.count("/") == 2:
            parts = date_str.split("/")
            if len(parts[2]) == 3:  # If the year has only 3 digits, fix it
                parts[2] = parts[2].zfill(4)
            return "/".join(parts)
        return date_str

    df['date'] = df['date'].apply(fix_year)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    return df

# Load data
df = load_data()

# Add a header for the page
st.header('📈 Overall Startup Funding Analysis')

# Introductory text explaining the purpose of the app
st.write('Welcome to the Startup Funding Analysis dashboard! Here, we explore key metrics and trends in startup funding over the years. Use the navigation on the side to dive into specific aspects.')

# Define the function for overall analysis
def load_overall_analysis():
    st.title('Overall Startup Funding Analysis')
    st.write('This section provides a high-level view of startup funding trends, including total funding amounts, funding rounds, and investment patterns over time.')

    # Example Plotly chart for visualizing startup funding by year
    funding_by_year = df.groupby('year').agg({'amount': 'sum'}).reset_index()
    fig = px.bar(funding_by_year, x='year', y='amount', labels={'year': 'Year', 'amount': 'Funding Amount'},
                 title='💸 Total Funding by Year', template='plotly_dark')
    st.plotly_chart(fig)

    # Additional icons and headers
    st.subheader('📅 Funding by Month')
    st.write('Analyze the distribution of funding across different months of the year.')

    # Example visualization for funding by month
    funding_by_month = df.groupby('month').agg({'amount': 'sum'}).reset_index()
    fig2 = px.bar(funding_by_month, x='month', y='amount', labels={'month': 'Month', 'amount': 'Funding Amount'},
                  title='📆 Total Funding by Month', template='plotly_dark')
    st.plotly_chart(fig2)

# Call the overall analysis function
load_overall_analysis()
