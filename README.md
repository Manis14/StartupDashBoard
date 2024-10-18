# 📊 Startup Funding Analysis Dashboard

Welcome to the **Startup Funding Analysis** dashboard, a Streamlit application that provides a comprehensive analysis of startup funding trends using a dataset of startup investments in India. This project leverages the power of Streamlit and Plotly to deliver an interactive experience for exploring funding data.

## 🛠 Features

- **Overall Analysis**: Get a bird’s-eye view of the startup ecosystem with key metrics like total funding, max funding, average funding, and the number of funded startups.
- **Month-over-Month Analysis**: Visualize funding trends month-over-month using line charts.
- **Funding Types Overview**: Explore different types of funding rounds and their frequency.
- **City-wise Investment Count**: Understand which cities attract the most investments with a bar chart visualization.
- **Yearly Maximum Funding Analysis**: View startups that received the highest funding each year.
- **Top Investors**: Discover the top 5 investors based on their total funding amount.

### 🏢 Startup Details
- Comprehensive information about a specific startup, including:
  - Location
  - Industry and Sub-Industry
  - Investment Details (dates, investors, and funding rounds)
  - Similar companies in the same industry

### 💼 Investor Details
- View detailed information about an investor, including:
  - Recent investments
  - Biggest investments
  - Sector investment distribution
  - Yearly investment trends

## 🚀 Getting Started

### Prerequisites
Ensure you have Python installed. This project uses:
- `Streamlit`
- `pandas`
- `plotly`

### Install the dependencies using:
```bash
pip install streamlit pandas plotly
```
### Running the App
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/your-username/startup-funding-analysis.git
cd startup-funding-analysis
```
### Run the Streamlit app:
```bash
streamlit run app.py
```
### Dataset
The app uses a dataset **startup_cleaned.csv**. Ensure the dataset is in the root directory of the project. The dataset includes:
- Date
- Startup name
- Investors
- Funding amount
- City, industry, and other related information


## 📦 File Structure

  
