import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Set the Streamlit page configuration
st.set_page_config(layout='wide', page_title='StartUp Analysis')

# Load and preprocess the data
df = pd.read_csv("startup_cleaned (1).csv")
def fix_year(date_str):
    # Check if the date string has exactly two '/' characters
    if date_str.count("/") == 2:
        parts = date_str.split("/")
        if len(parts[2]) == 3:  # If the year has only 3 digits, fix it
            parts[2] = parts[2].zfill(4)  # Pad the year with a leading zero
        return "/".join(parts)
    else:
        return date_str  # Return the date as is if it's not in the expected format

# Apply the function to fix the date format in the DataFrame
df['date'] = df['date'].apply(fix_year)

# Convert the date column to datetime with dayfirst=True
df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

def load_investor_detail(invest):
    st.title(invest)
    # Load the recent 5 investments of the investor
    name = invest
    last5_df = df[df['investors'].str.contains(name, na=False)].sort_values(by='date', ascending=False).head()[[
        'date', 'startup', 'city', 'vertical', 'round', 'amount'
    ]]
    st.subheader('Most Recent Investment')
    st.dataframe(last5_df)

    # Biggest Investment
    big_series = df[df['investors'].str.contains(name, na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False)
    col1, col2 = st.columns(2)

    with col1:
        big_investments_df = big_series.reset_index()
        st.subheader('Biggest Investments Graph')
        fig = px.bar(big_investments_df, x='startup', y='amount',
                     title='Biggest Investments by ' + name,
                     labels={'startup': 'Startup', 'amount': 'Total Investment (in currency)'},
                     color='amount',
                     color_continuous_scale='Blues')

        # Rotate x-axis labels for better readability
        fig.update_layout(xaxis_tickangle=-45)

        # Display the plot in Streamlit
        st.plotly_chart(fig)



        # fig, ax = plt.subplots(figsize=(6, 4))  # Set the figure size
        # ax.bar(big_series.index, big_series.values)
        # ax.set_xlabel('Startup')
        # ax.set_ylabel('Total Investment (in currency)')
        # ax.set_title('Biggest Investments')
        # plt.xticks(rotation=45)
        # st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(name, na=False)].groupby('vertical')['amount'].sum()
        st.subheader('Sector Invested in')

        vertical_investments_df = vertical_series.reset_index()

        # Create a pie chart using Plotly
        fig2 = px.pie(vertical_investments_df, names='vertical', values='amount',
                      title='Investment Distribution by Sector',
                      labels={'vertical': 'Sector', 'amount': 'Total Investment (in currency)'},
                      hole=0.3)  # If you want a donut chart, set hole to a value between 0 and 1

        # Display the plot in Streamlit
        st.plotly_chart(fig2)


        # fig2, ax2 = plt.subplots(figsize=(6, 4))  # Set the figure size
        # ax2.pie(vertical_series, labels=vertical_series.index, autopct="%0.1f%%")
        # ax2.set_title('Investment Distribution by Sector')
        # st.pyplot(fig2)

    # YOY Investment
    df['year'] = df['date'].dt.year

    # Filter the DataFrame and group by year to get the total investment
    year_series = df[df['investors'].str.contains(name, na=False)].groupby('year')['amount'].sum().reset_index()

    # Create a subheader for the graph
    st.subheader('YOY Investment')

    # Create a line chart using Plotly
    fig3 = px.line(year_series, x='year', y='amount',
                    title='Year Over Year (YOY) Investment',
                    labels={'year': 'Year', 'amount': 'Total Investment (in currency)'},
                    markers=True)

    # Display the plot in Streamlit
    st.plotly_chart(fig3)


    # Similar Investors

    st.title("Similar Investors")

    def find_similar_investors(df, investor_name):
        # Get the unique sectors where the specified investor has invested
        sectors = list(set(df[df['investors'].str.contains(investor_name, na=False)]['vertical']))
        if not sectors:
            st.write(f"No sectors found for the investor '{investor_name}'.")
            # print(f"No sectors found for the investor '{investor_name}'.")
            return

        sectors_dict = {}

        for i in range(len(sectors)):
            each_sector = df[df['vertical'].str.contains(sectors[i], na=False)]
            #         print(f"Sector name is {sectors[i]}")
            investors_names = each_sector['investors'].dropna()  # Drop any NaN values to avoid issues

            # Ensure that each value is a string before splitting
            unique_values = set()
            for names in investors_names:
                if isinstance(names, str):
                    unique_values.update(names.split(','))

            # Create a dictionary where the key is the sector name and the value is the set of unique investors
            sectors_dict[sectors[i]] = unique_values

        # Dictionary to count the occurrences of each investor across all sectors
        investor_count = {}

        # Count the occurrences of each investor across the sectors
        for sector, investors in sectors_dict.items():
            for investor in investors:
                if investor.strip() != investor_name:  # Exclude the original investor name (with stripped whitespace)
                    investor_count[investor.strip()] = investor_count.get(investor.strip(), 0) + 1

        # Check if there are any other investors in these sectors
        if not investor_count:
            st.write(f"No other investors found in the same sectors as '{investor_name}'.")
            # print(f"No other investors found in the same sectors as '{investor_name}'.")
            return

        # Find the maximum number of sectors any other investor has invested in
        max_invested_sectors = max(investor_count.values())
        investors_with_max_sectors = [inv for inv, count in investor_count.items() if count == max_invested_sectors]

        # Print the results
        st.subheader(f"Investors who have invested in the most number of sectors where '{investor_name}' is active:")
        # print(f"\nInvestors who have invested in the most number of sectors where '{investor_name}' is active:")
        for investor in investors_with_max_sectors:
            st.write(f"Investor: {investor}, Number of sectors: {max_invested_sectors}")
            # print(f"Investor: {investor}, Number of sectors: {max_invested_sectors}")

    # Example usage:
    find_similar_investors(df, name)


def load_overall_analysis():
    st.title('OverAll Analysis')

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        # Total invested Amount
        total = round(df['amount'].sum())
        st.metric('Total', str(total)+' Cr')
    with col2:
        # Max amount infused in a start
        maximum_fund = df.groupby('startup')['amount'].max().sort_values(ascending = False).head(1).values[0]
        st.metric('Maximum Funing',str(maximum_fund)+' Cr')
    with col3:
        mean_fund = round(df.groupby('startup')['amount'].sum().mean())
        st.metric('Mean Funing', str(mean_fund) + ' Cr')
    with col4:
        num_startup= df['startup'].nunique()
        st.metric('Funded Startups ', str(num_startup) + ' Cr')

    st.header('MoM Graph')
    selected_option=st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3 = px.line(temp_df, x='x_axis', y='amount',
                   title=f'{selected_option} Amount by Month and Year',
                   labels={'x_axis': 'Month-Year', 'amount': selected_option + ' Amount'},
                   markers=True)

    # Display the plot in Streamlit
    st.plotly_chart(fig3)

    # Extract unique funding types from the DataFrame
    types = df["round"].unique()
    lists1 = []
    lists2 = []

    # Convert all types to lowercase and store in lists1
    for i in range(len(types)):
        lists1.append(types[i].lower())

    # Process each element in lists1 to clean and normalize
    for i in range(len(lists1)):
        if '/' in lists1[i]:
            # Split by '/' and add both parts separately
            a, b = lists1[i].split('/')
            lists2.append(a.strip())
            lists2.append(b.strip())
        else:
            # Replace '-' with space and add to lists2 if '/' is not present
            lists2.append(lists1[i].replace('-', ' ').strip())

    # Further clean and deduplicate lists2
    cleaned_types = []
    for item in lists2:
        # Normalize separators and spaces
        item = item.replace('/', ' and ').replace('  ', ' ')
        item = item.strip()  # Remove any extra spaces

        # Add the cleaned type if it's not already in the cleaned list
        if item not in cleaned_types:
            cleaned_types.append(item)

    # Output the cleaned and deduplicated funding types
    # Display the cleaned and deduplicated list on Streamlit
    st.header("Funding Types:")
    st.write(cleaned_types)

    city_date_counts = df.groupby('city')['date'].count().reset_index()

    # Rename the columns for clarity
    city_date_counts.columns = ['City', 'Date Count']

    # Create a bar chart using Plotly
    fig = px.bar(city_date_counts, x='City', y='Date Count',
                 title='Count of Investment by City',
                 labels={'City': 'City', 'Date Count': 'Total Invest'},
                 color='Date Count',
                 color_continuous_scale='Blues')

    # Display the graph in Streamlit
    # st.write("Count of Dates by City:")
    st.plotly_chart(fig)


st.sidebar.title("Startup Funding Analysis ")
option= st.sidebar.selectbox("Select One",['OverAll Analysis','StartUp','Investor'])

if option =='OverAll Analysis':
    # st.title('OverAll Analysis')
    # btn0 = st.sidebar.button("Show OverAll Analysis")

    # if btn0:
    load_overall_analysis()


elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    st.title('StartUp Analysis')
else :
    selected_investor = st.sidebar.selectbox('Select Funding',sorted(set(df['investors'].str.split(',').sum())))
    btn2  = st.sidebar.button('Find Investor Detail')

    if btn2:
        load_investor_detail(selected_investor)
    # st.title()


