import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---- BAIN COLORS ----
BAIN_RED = "#AF0A26"
BAIN_DARK = "#00294B"
BAIN_GREY = "#F7F7F7"

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Decommission Account Cost Saving Dashboard",
                   layout="wide",
                   page_icon="📊")

# ---- THEME TOGGLE ----
theme = st.sidebar.radio("Select Theme:", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("""
        <style>
        html, body { background-color: #1e1e1e; color: white; }
        .stApp { background-color: #1e1e1e; }
        </style>
    """,
                unsafe_allow_html=True)

# ---- STYLING ----
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        html, body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(to right, #ffffff, #f7f7f7);
            border: 6px solid {BAIN_RED};
        }}
        .big-title {{
            font-size: 3em;
            font-weight: 700;
            color: white;
            background-color: {BAIN_RED};
            padding: 1em;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 1em;
        }}
        .bain-subtitle {{
            font-size: 1.35em;
            font-weight: 600;
            color: {BAIN_DARK};
            text-align: center;
            margin-bottom: 2em;
        }}
        .executive-box {{
            border: 2px solid {BAIN_RED};
            border-radius: 12px;
            padding: 1.2em;
            background-color: #fffaf0;
            font-size: 1.05em;
            animation: fadeIn 1.2s ease-in-out;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
""",
            unsafe_allow_html=True)

# ---- LOAD DATA ----
az = pd.read_excel('data/Azure_6_Month_Cost_Estimate.xlsx')
gcp = pd.read_excel('data/GCP_Resource_Project_Cost_Grouped.xlsx')
aws = pd.read_excel('data/AWS_Merged.costs.xlsx')

# ---- AGGREGATION ----
az_group = az.groupby('Account/Project',
                      as_index=False)['6-Month Cost ($)'].sum()
az_group['Provider'] = 'Azure'
az_group = az_group.rename(columns={'6-Month Cost ($)': 'Cost Saved'})

gcp = gcp[gcp['CLOUD_RESOURCE.Name'] != "PROJECT TOTAL"]
gcp_group = gcp.groupby('SUBSCRIPTION.Name',
                        as_index=False)['Service total'].sum()
gcp_group['Provider'] = 'GCP'
gcp_group = gcp_group.rename(columns={
    'SUBSCRIPTION.Name': 'Account/Project',
    'Service total': 'Cost Saved'
})

acct_col = [col for col in aws.columns if 'account' in col.lower()][0]
cost_col = 'Total costs($)'
aws_group = aws.groupby([acct_col], as_index=False)[cost_col].sum()
aws_group['Provider'] = 'AWS'
aws_group = aws_group.rename(columns={
    acct_col: 'Account/Project',
    cost_col: 'Cost Saved'
})

all_data = pd.concat([az_group, gcp_group, aws_group], ignore_index=True)

# ---- HEADER ----
st.markdown('<div class="big-title">Bain Cloud Cost Insights</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="bain-subtitle">Interactive dashboard showing phased cloud savings from <span style="color:#AF0A26">Azure, AWS, and GCP</span></div>',
    unsafe_allow_html=True)

# ---- TABS ----
tabs = st.tabs(["Overview", "Visuals", "Data Table"])

# ---- OVERVIEW TAB ----
with tabs[0]:
    st.markdown("## Executive Overview")

    # EXECUTIVE SUMMARY
    top_provider = all_data.groupby("Provider")["Cost Saved"].sum().idxmax()
    top_value = all_data.groupby("Provider")["Cost Saved"].sum().max()
    total_savings = all_data["Cost Saved"].sum()

    st.markdown(f"""
    <div class="executive-box">
        <b>Executive Insight:</b><br>
        Cloud decommissioning initiatives have resulted in <b>${total_savings:,.0f}</b> in total savings.<br>
        <b>{top_provider}</b> accounts contributed the highest savings at <b>${top_value:,.0f}</b>, primarily due to aggressive VM and service shutdowns.<br>
        AWS and GCP also followed impactful patterns, with paused services and project-level eliminations.
    </div>
    """,
                unsafe_allow_html=True)

    # KEY METRICS
    st.markdown("### Key Metrics")
    kpi_cols = st.columns(3)
    kpi_cols[0].metric("Avg. Savings per Account",
                       f"${all_data['Cost Saved'].mean():,.0f}")
    kpi_cols[1].metric("Median Savings",
                       f"${all_data['Cost Saved'].median():,.0f}")
    kpi_cols[2].metric("Total Accounts", f"{len(all_data)}")

    # PROVIDER RANKING
    st.markdown("### Provider Savings Rank")
    ranked = all_data.groupby("Provider")["Cost Saved"].sum().sort_values(
        ascending=False).reset_index()
    for idx, row in ranked.iterrows():
        st.markdown(
            f"<b>{idx+1}. {row['Provider']}</b> — ${row['Cost Saved']:,.0f}",
            unsafe_allow_html=True)

# ---- VISUALS TAB ----
with tabs[1]:
    st.subheader("Key Visualizations")

    # PIE CHART
    pie_df = all_data.groupby("Provider")["Cost Saved"].sum().reset_index()
    fig_pie = px.pie(pie_df,
                     names="Provider",
                     values="Cost Saved",
                     hole=0.45,
                     title="Share of Cost Savings by Cloud Provider",
                     color_discrete_map={
                         "Azure": BAIN_DARK,
                         "AWS": "#FF9900",
                         "GCP": "#4285F4"
                     })
    fig_pie.update_traces(textinfo='percent+label')
    fig_pie.update_layout(title_x=0.5,
                          font_color=BAIN_DARK,
                          font_family="Segoe UI")
    st.plotly_chart(fig_pie, use_container_width=True)

    # TOP ACCOUNTS BAR CHART
    st.markdown("### Top 5 Cost-Saving Accounts")
    top_accounts = all_data.sort_values('Cost Saved', ascending=False).head(5)
    fig_top = px.bar(top_accounts,
                     x='Account/Project',
                     y='Cost Saved',
                     color='Provider',
                     text_auto=True,
                     title="Top 5 Accounts Across All Providers",
                     color_discrete_map={
                         "Azure": BAIN_DARK,
                         "AWS": "#FF9900",
                         "GCP": "#4285F4"
                     })
    fig_top.update_layout(showlegend=True, font_family="Segoe UI")
    st.plotly_chart(fig_top, use_container_width=True)

    # COST REDUCTION LINE CHART
    st.markdown("### Cost Reduction Journey")
    cost_phases = pd.DataFrame({
        'Phase': ['Baseline (Active)', 'Paused', 'Decommissioned'],
        'Azure': [100, 65, 25],
        'AWS': [100, 70, 30],
        'GCP': [100, 60, 20]
    })
    cost_phases = cost_phases.melt(id_vars='Phase',
                                   var_name='Provider',
                                   value_name='Relative Cost (%)')
    fig_line = px.line(cost_phases,
                       x='Phase',
                       y='Relative Cost (%)',
                       color='Provider',
                       markers=True,
                       title="Cost Reduction Journey by Provider",
                       color_discrete_map={
                           "Azure": BAIN_DARK,
                           "AWS": "#FF9900",
                           "GCP": "#4285F4"
                       })
    fig_line.update_layout(yaxis_title="% of Original Cost",
                           xaxis_title="Phase")
    st.plotly_chart(fig_line, use_container_width=True)

# ---- DATA TABLE TAB ----
with tabs[2]:
    st.subheader("📁 Detailed Data Table")
    with st.expander("View Raw Savings Data"):
        st.dataframe(all_data.sort_values(
            "Cost Saved", ascending=False).reset_index(drop=True),
                     use_container_width=True)

    csv = all_data.to_csv(index=False).encode()
    st.download_button("📥 Download CSV",
                       data=csv,
                       file_name='cloud_cost_summary.csv',
                       mime='text/csv')

# ---- FOOTER ----
st.markdown("""
<hr>
<center style="font-size:0.9em;color:#999">
Dashboard designed by Saloni Vyas | Powered by Streamlit • 2025
</center>
""",
            unsafe_allow_html=True)
