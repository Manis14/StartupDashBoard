import streamlit as st
import pandas as pd
import plotly.express as px

# Set the Streamlit page configuration
st.set_page_config(layout='wide', page_title='Startup Funding Analysis')


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


# Define the function for overall analysis
def load_overall_analysis():
    st.title('Overall Startup Funding Analysis')

    # Metrics Display
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total = round(df['amount'].sum())
        st.metric('💰 Total Funding', f'{total} Cr')

    with col2:
        max_fund = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('🚀 Max Funding', f'{max_fund} Cr')

    with col3:
        mean_fund = round(df.groupby('startup')['amount'].sum().mean())
        st.metric('📊 Average Funding', f'{mean_fund} Cr')

    with col4:
        num_startups = df['startup'].nunique()
        st.metric('🏢 Funded Startups', num_startups)

    # Month-over-Month Funding Analysis
    st.header('📅 Month-over-Month Funding Analysis')
    selected_option = st.selectbox('Select Analysis Type', ['Total', 'Count'])

    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3 = px.line(temp_df, x='x_axis', y='amount',
                   title=f'{selected_option} Funding Amount by Month and Year',
                   labels={'x_axis': 'Month-Year', 'amount': f'{selected_option} Amount'},
                   markers=True)
    st.plotly_chart(fig3, use_container_width=True)

    # Funding Types Overview
    st.header("📊 Funding Types Overview")
    types = df["round"].unique()
    cleaned_types = []
    for type_ in types:
        type_ = type_.lower().replace('-', ' ').replace('/', ' and ').strip()
        if type_ not in cleaned_types:
            cleaned_types.append(type_)
    st.write("🔍 **Funding Types:** " + ", ".join(cleaned_types))

    # City-wise Investment Count
    st.header("🌆 City-wise Investment Count")
    city_date_counts = df.groupby('city')['date'].count().reset_index()
    city_date_counts.columns = ['City', 'Investment Count']

    fig = px.bar(city_date_counts, x='City', y='Investment Count',
                 title='Investment Count by City',
                 labels={'City': 'City', 'Investment Count': 'Count'},
                 color='Investment Count',
                 color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

    # Year-wise Maximum Funding Analysis
    st.header("📈 Year-wise Analysis of Maximum Funding Received")
    top = df.loc[df.groupby("year")["amount"].idxmax()][["year", "startup", "amount"]].reset_index(drop=True)
    st.dataframe(top)

    # Top Investors
    st.header("🏆 Top 5 Investors Based on Funding Amount")
    top_investor = df.groupby("investors")["amount"].sum().sort_values(ascending=False).reset_index().head(5)

    # Display the top investors in a table
    st.dataframe(top_investor)

    # Bar chart for top investors
    fig = px.bar(top_investor,
                 x='investors',
                 y='amount',
                 title='Top 5 Investors by Funding Amount',
                 labels={'amount': 'Total Investment Amount', 'investors': 'Investors'},
                 color='amount',
                 color_continuous_scale='Viridis')

    # Display the chart in Streamlit
    st.plotly_chart(fig)


# Define function for investor detail
def load_investor_detail(investor_name):
    st.title(f'📊 Investor Analysis: {investor_name}')

    # Filter data for the selected investor
    investor_data = df[df['investors'].str.contains(investor_name, na=False)]

    if investor_data.empty:
        st.write("🚫 No investment data found for this investor.")
        return

    # Recent Investments
    st.subheader('🆕 Recent Investments')
    recent_investments = investor_data.sort_values(by='date', ascending=False).head(5)[
        ['date', 'startup', 'city', 'vertical', 'round', 'amount']]
    st.dataframe(recent_investments)

    # Biggest Investments
    st.subheader('💰 Biggest Investments')
    big_series = investor_data.groupby('startup')['amount'].sum().sort_values(ascending=False).reset_index()

    fig = px.bar(big_series, x='startup', y='amount',
                 title=f'Biggest Investments by {investor_name}',
                 labels={'startup': 'Startup', 'amount': 'Total Investment'},
                 color='amount', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

    # Sector Investment Distribution
    st.subheader('📈 Sector Investment Distribution')
    vertical_series = investor_data.groupby('vertical')['amount'].sum().reset_index()

    fig2 = px.pie(vertical_series, names='vertical', values='amount',
                  title='Investment Distribution by Sector', hole=0.3)
    st.plotly_chart(fig2, use_container_width=True)

    # Yearly Investment Trend
    st.subheader('📅 Yearly Investment Trend')
    year_series = investor_data.groupby('year')['amount'].sum().reset_index()

    fig3 = px.line(year_series, x='year', y='amount',
                   title='Year Over Year Investment',
                   labels={'year': 'Year', 'amount': 'Total Investment'},
                   markers=True)
    st.plotly_chart(fig3, use_container_width=True)


def load_startup_detail(startup):
    st.title(f"Comprehensive Details of the {startup} Company")



    # Location of Startup
    name = startup
    location = df[df['startup'].str.contains(name, case=False, na=False)]['city'].reset_index()

    if not location.empty:
        st.subheader(f"📍 Location Details for {startup}")
        st.write(f"**City:** {location.loc[0]['city']}")
        st.write(
            "🔍 _Note: This is based on available records. If the city name is not as expected, it might be due to variations in the dataset._")
    else:
        st.subheader(f"🚫 No Location Data Found for {startup}")
        st.write(
            "Unfortunately, we couldn't find the location details for this startup based on the current dataset. Please check the startup name for any typos or variations.")

#     Industry and Sub Industry

    # Fetch industry details
    industry = df[df['startup'].str.contains(name, case=False, na=False)]['vertical'].reset_index()

    # Fetch sub-industry details
    subindustry = df[df['startup'].str.contains(name, case=False, na=False)]['subvertical'].reset_index()

    # Display industry and sub-industry information
    if not industry.empty and not subindustry.empty:
        st.subheader(f"🏢 Industry Details for {startup}")
        st.write(f"**Industry:** {industry.loc[0]['vertical']}")
        st.write(f"**Sub-Industry:** {subindustry.loc[0]['subvertical']}")
        st.write("📌 _These details are based on the available data. If the information seems incomplete, it may be due to dataset variations._")
    elif not industry.empty:
        st.subheader(f"🏢 Industry Details for {startup}")
        st.write(f"**Industry:** {industry.loc[0]['vertical']}")
        st.write("⚠️ _Sub-Industry information is not available._")
    elif not subindustry.empty:
        st.subheader(f"🏢 Sub-Industry Details for {startup}")
        st.write(f"**Sub-Industry:** {subindustry.loc[0]['subvertical']}")
        st.write("⚠️ _Industry information is not available._")
    else:
        st.subheader(f"🚫 No Industry Data Found for {startup}")
        st.write("We couldn't find any industry or sub-industry information for this startup. Please check the startup name for accuracy or variations in spelling.")

    # Funding Rounds
    # Fetch investment details: date, investors, and round information
    investment_details = df[df['startup'].str.contains(name, case=False, na=False)][
        ['date', 'investors', 'round']].reset_index()

    # Display the investment details
    if not investment_details.empty:
        st.subheader(f"💼 Investment Details for {startup}")
        st.write("Here are the details of the investment rounds for this startup:")

        for i in range(len(investment_details)):
            st.write(f"**Date:** {investment_details.loc[i]['date']}")
            st.write(f"**Investors:** {investment_details.loc[i]['investors']}")
            st.write(f"**Round:** {investment_details.loc[i]['round']}")
            st.markdown("---")  # Divider between entries

        st.write(
            "🔍 _Note: The information above is based on available records. If details appear missing or inconsistent, it may be due to data variations._")
    else:
        st.subheader(f"🚫 No Investment Data Found for {startup}")
        st.write(
            "We couldn't find any investment information for this startup. Please check the startup name for accuracy or variations in spelling.")

    # Fetch the industry (vertical) details for the startup
    industry = df[df['startup'].str.contains(name, case=False, na=False)][['vertical']].reset_index()

    if not industry.empty:
        vertical = industry.loc[0]['vertical']
        # Find other startups in the same vertical
        similar_companies = df[df['vertical'].str.contains(vertical, case=False, na=False)]['startup'].reset_index()

        # Filter out the current startup and get up to 5 similar companies
        similar_companies_list = [similar_companies.loc[i]['startup'] for i in range(len(similar_companies))
                                  if similar_companies.loc[i]['startup'].lower() != name.lower()][:5]

        if not similar_companies_list:
            st.subheader(f"🔍 No Other Similar Companies Found for {startup}")
            st.write(f"There are no other companies listed under the vertical **{vertical}** similar to {startup}.")
        else:
            st.subheader(f"🏢 Similar Companies in the Same Industry as {startup}")
            st.write(f"Here are up to 5 other companies operating in the **{vertical}** industry:")

            for company in similar_companies_list:
                st.write(f"- {company}")

            st.write(
                "🔍 _Note: These companies are based on available records in the dataset. There may be more companies in this vertical not listed here._")
    else:
        st.subheader(f"🚫 No Industry Data Found for {startup}")
        st.write(
            "We couldn't find the industry information for this startup. Please verify the startup name for any typos or spelling variations.")


# Sidebar navigation
st.sidebar.title("Startup Funding Dashboard")
option = st.sidebar.radio("Choose an Option", ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Investor':
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    if st.sidebar.button('Show Investor Details'):
        load_investor_detail(selected_investor)
else:
    selected_startup = st.sidebar.selectbox('Select StartUp', sorted(set(df['startup'])))
    if st.sidebar.button('Show StartUp Details'):
        load_startup_detail(selected_startup)