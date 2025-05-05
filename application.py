# Optimal Retirement Portfolio Planner (Merged Version)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import io

# --- App Metadata ---
st.set_page_config(page_title="Optimal Retirement Portfolio", layout="wide")
st.sidebar.markdown("### ✨ Built by Akash D")

# ------------------------ Sidebar: User Inputs ------------------------
st.sidebar.header("🔧 User Configuration")
age = st.sidebar.slider("Current Age", 20, 60, 30)
retirement_age = st.sidebar.slider("Expected Retirement Age", 50, 70, 60)
monthly_expenses = st.sidebar.number_input("Current Monthly Expenses (₹)", 1000, 200000, 30000)
inflation_rate = st.sidebar.slider("Expected Inflation Rate (%)", 2.0, 10.0, 6.0)
investment_duration = retirement_age - age
risk_profile = st.sidebar.selectbox("Select Risk Profile", ["Conservative", "Balanced", "Aggressive"])

# --- Retirement Calculation Inputs ---
monthly_investment = st.sidebar.number_input("Monthly Investment (₹)", min_value=500, value=5000)
estimated_return_equity = st.sidebar.slider("Equity Return Rate (p.a.)", 5.0, 15.0, 12.0)
estimated_return_traditional = st.sidebar.slider("Traditional Return Rate (p.a.)", 4.0, 9.0, 7.0)

# ------------------------ 1. Investment Portfolio Builder ------------------------
st.title(":bar_chart: Optimal Retirement Portfolio Planner")
st.header("📌 1. Investment Portfolio Builder")

if risk_profile == "Conservative":
    allocation = {"Equity MFs": 10, "Debt MFs": 30, "PPF": 30, "SCSS": 15, "NPS": 10, "EPF": 5}
elif risk_profile == "Balanced":
    allocation = {"Equity MFs": 30, "Debt MFs": 25, "PPF": 15, "SCSS": 10, "NPS": 15, "EPF": 5}
else:
    allocation = {"Equity MFs": 50, "Debt MFs": 20, "PPF": 10, "SCSS": 5, "NPS": 10, "EPF": 5}

alloc_df = pd.DataFrame({"Instrument": allocation.keys(), "Allocation (%)": allocation.values()})
fig1 = px.pie(alloc_df, names='Instrument', values='Allocation (%)', title='Asset Allocation Based on Risk Profile')
st.plotly_chart(fig1)

# ------------------------ 2. 10-Year Debt vs Equity Returns ------------------------
st.header("\ud83d\udcc9 2. 10-Year Debt vs Equity Returns")
years = list(range(2014, 2024))
equity_returns = [12, 10, 15, 18, 11, -3, 8, 20, 13, 16]
debt_returns = [7, 6.5, 6.8, 7.2, 6.9, 6.5, 6.7, 7, 6.8, 6.6]
returns_df = pd.DataFrame({"Year": years, "Equity Returns (%)": equity_returns, "Debt Returns (%)": debt_returns})
st.bar_chart(returns_df.set_index("Year"))

# ------------------------ 3. Retirement Portfolio Summary ------------------------
st.header("\ud83d\udcbc 3. Retirement Portfolio Summary")
months = investment_duration * 12
total_investment = monthly_investment * months
future_value_equity = monthly_investment * (((1 + estimated_return_equity/100/12) ** months - 1) / (estimated_return_equity/100/12))
future_value_traditional = monthly_investment * (((1 + estimated_return_traditional/100/12) ** months - 1) / (estimated_return_traditional/100/12))

st.write(f"**Total Investment:** ₹{total_investment:,.0f}")
st.write(f"**Future Value (Equity-Based):** ₹{future_value_equity:,.0f}")
st.write(f"**Future Value (Traditional):** ₹{future_value_traditional:,.0f}")

if st.checkbox("\ud83d\udcca Show Year-by-Year Growth"):
    years = list(range(age, retirement_age + 1))
    equity_growth = [monthly_investment * (((1 + estimated_return_equity/100/12) ** (i*12) - 1) / (estimated_return_equity/100/12)) for i in range(len(years))]
    traditional_growth = [monthly_investment * (((1 + estimated_return_traditional/100/12) ** (i*12) - 1) / (estimated_return_traditional/100/12)) for i in range(len(years))]
    df_growth = pd.DataFrame({"Year": years, "Equity-Based": equity_growth, "Traditional": traditional_growth})
    st.line_chart(df_growth.set_index("Year"))
else:
    df_growth = pd.DataFrame()

# ------------------------ 4. Investment Option Comparison ------------------------
st.header("\ud83d\udd04 4. Comparison of Investment Options")
data = {
    "Option": ["Equity Mutual Fund", "Public Provident Fund (PPF)", "Employees Provident Fund (EPF)", "National Pension Scheme (NPS)"],
    "Expected Returns (p.a.)": [12, 7.1, 8.1, 9],
    "Risk Level": ["High", "Low", "Low", "Moderate"],
    "Liquidity": ["High (after 1 year)", "Low", "Low", "Moderate"]
}
df_comparison = pd.DataFrame(data)
st.dataframe(df_comparison)

# ------------------------ 5. SIP Simulation ------------------------
st.header("\ud83d\udd2e 5. SIP-Based Investment Simulation")
def sip_simulation(monthly_investment, annual_return_rate, years):
    total_invested = monthly_investment * 12 * years
    future_value = 0
    monthly_rate = annual_return_rate / 12 / 100
    months = years * 12
    for i in range(1, months + 1):
        future_value += monthly_investment * (1 + monthly_rate) ** (months - i + 1)
    return total_invested, future_value

monthly = st.number_input("SIP Monthly Investment (₹)", 1000, 100000, 5000, key="sip")
rate = st.number_input("Expected Annual Return (%)", 1.0, 20.0, 12.0, key="sip_rate")
years = st.slider("Investment Duration (Years)", 1, 40, 20, key="sip_years")
if st.button("\ud83e\uddf2 Calculate SIP Growth"):
    invested, value = sip_simulation(monthly, rate, years)
    st.success(f"Total Invested: ₹{invested:,.0f}, Future Value: ₹{value:,.0f}")
    st.bar_chart(pd.DataFrame({"Future Value": [value], "Invested": [invested]}))

# ------------------------ 6. Tax Benefit Estimation ------------------------
st.header("\ud83d\udcb0 6. Tax Benefit Estimation")
def tax_benefits(investment_amount):
    sec_80c_limit = 150000
    eligible = min(investment_amount, sec_80c_limit)
    tax_saved = eligible * 0.3
    return eligible, tax_saved

investment = st.number_input("Annual Investment for Tax Saving (₹)", 0, 500000, 100000)
eligible, saved = tax_benefits(investment)
if investment:
    st.info(f"Eligible under Sec 80C: ₹{eligible:,.0f}\nPotential Tax Saved: ₹{saved:,.0f}")

# ------------------------ 7. Post-Retirement Income Simulation ------------------------
st.header("\ud83c\udfe6 7. Post-Retirement Income Simulation")
def post_retirement_income_models(total_corpus, annuity_rate, swp_amount):
    annual_annuity = total_corpus * annuity_rate / 100
    years_swp = total_corpus / (swp_amount * 12)
    return annual_annuity, years_swp

corpus = st.number_input("Total Corpus at Retirement (₹)", 100000, 100000000, 1000000)
annuity_rate = st.slider("Annuity Rate (%)", 1, 10, 6)
swp_amount = st.number_input("SWP Monthly Amount (₹)", 1000, 100000, 10000)
if st.button("\ud83d\udcc8 Simulate Income Models"):
    annuity, swp_years = post_retirement_income_models(corpus, annuity_rate, swp_amount)
    st.success(f"Annual Annuity Income: ₹{annuity:,.0f}\nSWP Duration: {swp_years:.1f} years")

# ------------------------ 8. Excel Export ------------------------
if st.button("\ud83d\udcc5 Download Excel Summary"):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame({
            "Summary": ["Total Investment", "Equity FV", "Traditional FV"],
            "Amount": [total_investment, future_value_equity, future_value_traditional]
        }).to_excel(writer, sheet_name='Summary', index=False)
        if not df_growth.empty:
            df_growth.to_excel(writer, sheet_name='Growth Over Time', index=False)
        df_comparison.to_excel(writer, sheet_name='Option Comparison', index=False)
        alloc_df.to_excel(writer, sheet_name='Risk Allocation', index=False)
    st.download_button("\ud83d\udcc4 Click to Download Excel File", data=output.getvalue(), file_name="optimal_retirement_portfolio.xlsx")
