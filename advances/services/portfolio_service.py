from decimal import Decimal
import pandas as pd
from ..models import Portfolio, PortfolioMetrics


def calculate_mrr(df):
    """
    Calculate Monthly Recurring Revenue (MRR) from a CSV file containing client data.

    :param csv_file: The path to the CSV file with 'ID_CLIENTE', 'MONTO (USD)', 'AÑO', 'MES' columns
    :return: A DataFrame with MRR calculated for each month
    """
    df.columns = df.columns.str.strip()

    # Calculate MRR of every month
    mrr = df.groupby(['AÑO', 'MES'])['MONTO (USD)'].sum().reset_index()

    # Rename columns to 'year', 'month', 'mrr' for clarity
    mrr.columns = ['Year', 'Month', 'MRR']

    return mrr

def calculate_churn_rate(df):
    """
    Calculate Churn Rate from a CSV file containing client data.

    :param csv_file: The path to the CSV file with 'ID_CLIENTE', 'MONTO (USD)', 'AÑO', 'MES' columns
    :return: A DataFrame with Churn Rate calculated for each month
    """
    df.columns = df.columns.str.strip()
    df_clients = df.groupby(['AÑO', 'MES'])['ID_CLIENTE'].unique().reset_index()

    churn_rates = []
    # Loop over the months
    for i in range(1, len(df_clients)):
        previous_month_clients = set(df_clients.iloc[i-1]['ID_CLIENTE'])
        current_month_clients = set(df_clients.iloc[i]['ID_CLIENTE'])

        # Calculate churn (clients who were present last month but not this month)
        churned_clients = previous_month_clients - current_month_clients
        churn_rate = len(churned_clients) / len(previous_month_clients) * 100

        churn_rates.append({
            'Year': df_clients.iloc[i]['AÑO'],
            'Month': df_clients.iloc[i]['MES'],
            'Churn Rate': churn_rate
        })

    churn_df = pd.DataFrame(churn_rates)
    return churn_df

def save_portfolio_to_db(mrr_df, churn_df):
    # Merging MRR and Churn dataFrames
    merged_df = pd.merge(mrr_df, churn_df, on=['Year', 'Month'], how='left')

    # Calculate the average MRR and churn rate for the entire portfolio
    avg_mrr = merged_df['MRR'].mean()
    avg_churn_rate = merged_df['Churn Rate'].mean()

    portfolio = Portfolio.objects.create(avg_mrr=avg_mrr, avg_churn_rate=avg_churn_rate)

    for _, row in merged_df.iterrows():
        churn_rate = row['Churn Rate'] if pd.notna(row['Churn Rate']) else None
        PortfolioMetrics.objects.create(
            portfolio=portfolio,
            year=row['Year'],
            month=row['Month'],
            mrr=row['MRR'],
            churn_rate=churn_rate
        )
    return portfolio.id

def process_portfolio(csv_file):
    df = pd.read_csv(csv_file)

    mrr_df = calculate_mrr(df)
    churn_df = calculate_churn_rate(df)

    portfolio_id = save_portfolio_to_db(mrr_df, churn_df)
    return portfolio_id

def calculate_score_of_portfolio(portfolio_id):
    """
    Calculate the average MRR and churn rate for all portfolio data,
    and return the score based on these averages.
    
    :param portfolio_id: ID of portfolio
    :return: The score of the portfolio
    """
    portfolio = Portfolio.objects.get(id=portfolio_id)
    avg_mrr = portfolio.avg_mrr
    avg_churn_rate = portfolio.avg_churn_rate

    if avg_mrr is None or avg_churn_rate is None:
        return {"error": "Could not calculate score. Missing data."}

    # Calculate score using the formula
    score = (avg_mrr / 1000) - (avg_churn_rate * 10)
    return {"score": round(score, 2)}

def calculate_max_advance(portfolio_id):
    """
    Calculate whether a client is eligible to ask for a loan and the max loan advance based on MRR and churn rate.
    
    :param mrr: Monthly Recurring Revenue of the company
    :param churn_rate: The churn rate of the company (as a percentage)
    :return: A tuple of max_advance (0 if not eligible), and a boolean representing if company is eligible for loan or not
    """
    portfolio = Portfolio.objects.get(id=portfolio_id)
    avg_mrr = portfolio.avg_mrr
    avg_churn_rate = portfolio.avg_churn_rate

    if avg_mrr is None or avg_churn_rate is None:
        return {"error": "Missing data."}
    
    score = calculate_score_of_portfolio(portfolio_id)["score"]
    
    # Eligibility threshold
    eligibility_threshold = 70
    
    if score <= eligibility_threshold:
        return 0, False
    
    # Define loan multipliers based on the score
    if score > eligibility_threshold and score <= 85:
        loan_multiplier = Decimal(1.2)
    elif score > 85:
        loan_multiplier = Decimal(1.4)
    
    # Calculate the maximum loan advance
    max_advance = avg_mrr * loan_multiplier
    
    return round(max_advance, 2), True

def process_and_calculate_max_advance(csv_file):
    """
    Processes the portfolio (calculates MRR and churn rates) and calculates the max loan advance.
    """
    # Process and save portfolio data
    portfolio_id = process_portfolio(csv_file)

    # Calculate the max advance
    max_advance, is_eligible_for_loan = calculate_max_advance(portfolio_id)

    if not is_eligible_for_loan:
        message = "The company is not eligible to ask for a loan based on the current data."
    else:
        message = "The company is eligible to ask for a loan."

    return {
        "portfolio": {
            "portfolio_id": portfolio_id,
            "max_advance": max_advance
        },
        "message": message
    }