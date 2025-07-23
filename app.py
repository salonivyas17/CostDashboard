import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---- CUSTOM STYLING FOR "BAINIFIED" LOOK ----
st.set_page_config(page_title="Cloud Cost Savings Dashboard", layout="wide")
st.markdown("""
<style>
.big-title { font-size: 2.6em; font-weight: bold; color: #AF0A26; margin-bottom:0.2em; }
.bain-card { background: #fff; border-radius: 16px; box-shadow: 0 4px 20px #E6E6E6; padding: 2em 2em 1em 2em; margin: 0.5em 0; }
.bain-red { color: #AF0A26; }
.bain-blue { color: #00294B; }
.bain-btn { background:#AF0A26; color:#fff; font-weight:bold; border:none; padding:0.7em 1.2em; border-radius:10px; cursor:pointer; }
hr { border: 1.5px solid #AF0A26; }
</style>
""", unsafe_allow_html=True)

# ---- DATA FOLDER PATH (Cross-platform compatible) ----
data_folder = "data"

# ---- READ ALL DATA ----
@st.cache_data(show_spinner=False)
def load_data():
    # Azure
    az = pd.read_excel(f'{data_folder}/Azure_Resource_Subscription_Cost_Estimate.xlsx')
    az = az[az['name'] != "SUBSCRIPTION TOTAL"]  # Remove subtotal rows
    az_group = az.groupby(['subscriptionName'], as_index=False)['Service total'].sum()
    az_group['Provider'] = 'Azure'
    az_group = az_group.rename(columns={'subscriptionName': 'Account/Project', 'Service total':'Cost Saved'})
    
    # GCP
    gcp = pd.read_excel(f'{data_folder}/GCP_Resource_Project_Cost_Grouped.xlsx')
    gcp = gcp[gcp['CLOUD_RESOURCE.Name'] != "PROJECT TOTAL"]
    gcp_group = gcp.groupby(['SUBSCRIPTION.Name'], as_index=False)['Service total'].sum()
    gcp_group['Provider'] = 'GCP'
    gcp_group = gcp_group.rename(columns={'SUBSCRIPTION.Name': 'Account/Project', 'Service total':'Cost Saved'})
    
    # AWS (sheet auto-detects account col, see note)
    aws = pd.read_excel(f'{data_folder}/AWS_Merged.costs.xlsx')
    acct_col = [col for col in aws.columns if 'account' in col.lower()][0]
    cost_col = [col for col in aws.columns if 'service total' in col.lower() or 'cost' in col.lower()][0]
    aws_group = aws.groupby([acct_col], as_index=False)[cost_col].sum()
    aws_group['Provider'] = 'AWS'
    aws_group = aws_group.rename(columns={acct_col: 'Account/Project', cost_col: 'Cost Saved'})
    
    all_data = pd.concat([az_group, gcp_group, aws_group], ignore_index=True)
    return az, gcp, aws, all_data

az, gcp, aws, all_data = load_data()

# ---- MAIN DASHBOARD ----
st.markdown('<div class="big-title">🌏 Cloud Cost Savings from Decommissioned Subscriptions/Accounts/Projects</div>', unsafe_allow_html=True)
st.write("**See how temporary and permanent decommissioning actions across Azure, AWS, and GCP have cut cloud spend.**")

# 1. Total savings headline (all clouds)
total_savings = all_data['Cost Saved'].sum()
st.markdown(f"""
<div class="bain-card" style="text-align:center">
    <span style="font-size:1.2em; color:#333;">Total Estimated Cost Saved</span>
    <br><span class="big-title">${total_savings:,.0f}</span>
</div>
""", unsafe_allow_html=True)

# 2. Provider selector
clouds = ['All', 'Azure', 'AWS', 'GCP']
provider = st.selectbox('Filter by Cloud Provider', clouds)

filtered = all_data if provider == 'All' else all_data[all_data['Provider'] == provider]

# 3. Show per-provider bar
bar = filtered.groupby('Provider')['Cost Saved'].sum().reset_index()
fig = px.bar(bar, x='Provider', y='Cost Saved', color='Provider',
    color_discrete_map={'Azure': '#00294B', 'AWS': '#FF9900', 'GCP': '#4285F4'},
    text_auto=True, title="Cost Savings by Cloud Provider")
fig.update_layout(showlegend=False, plot_bgcolor='#fff', font_family='Inter', font_color='#333')
st.plotly_chart(fig, use_container_width=True)

# 4. Details by account/project
with st.expander("Show all decommissioned subscriptions/accounts/projects and savings"):
    st.dataframe(filtered.sort_values("Cost Saved", ascending=False).reset_index(drop=True), use_container_width=True)

st.markdown("---")

# 5. Cost savings over months (if available)
def extract_months(df, id_col, monthly_cols):
    result = []
    for _, row in df.iterrows():
        for m in monthly_cols:
            if m in row:
                result.append({
                    'Account/Project': row[id_col],
                    'Provider': df.name,
                    'Month': m,
                    'Cost': row[m]
                })
    return pd.DataFrame(result)

az_months = [col for col in az.columns if col.startswith('202')]
gcp_months = [col for col in gcp.columns if col.startswith('202')]
aws_months = [col for col in aws.columns if col.startswith('202')]

az_month_df = extract_months(az, 'subscriptionName', az_months)
gcp_month_df = extract_months(gcp, 'SUBSCRIPTION.Name', gcp_months)
aws_month_df = extract_months(aws, [c for c in aws.columns if 'account' in c.lower()][0], aws_months)
az_month_df.name, gcp_month_df.name, aws_month_df.name = "Azure", "GCP", "AWS"

timeline = pd.concat([az_month_df, gcp_month_df, aws_month_df], ignore_index=True)
timeline['Month'] = pd.to_datetime(timeline['Month'], errors='coerce')
timeline = timeline.dropna(subset=['Month'])

trend_provider = st.radio('Show monthly cost trend for:', clouds, horizontal=True)
trend_data = timeline if trend_provider == "All" else timeline[timeline["Provider"] == trend_provider]
trend = trend_data.groupby(['Month', 'Provider'])['Cost'].sum().reset_index()

fig2 = px.area(trend, x='Month', y='Cost', color='Provider',
    color_discrete_map={'Azure': '#00294B', 'AWS': '#FF9900', 'GCP': '#4285F4'},
    markers=True, title="Cloud Cost Reduction Timeline (Decommissioned Accounts Only)")
fig2.update_traces(line_shape='spline')
fig2.update_layout(yaxis_title="Monthly Cost Saved ($)", font_family='Inter', font_color='#333', plot_bgcolor="#fff")
st.plotly_chart(fig2, use_container_width=True)

# 6. Story of "temporary decommission" (April/May) vs "full decommission" (July)
st.markdown("""
<div class="bain-card">
<b>Decommissioning Journey:</b><br>
<ul>
<li> <b>April-May:</b> Started temporary decommissioning (manual pausing/stopping of safe resources).</li>
<li> <b>By July:</b> Completed full decommission of targeted subscriptions/accounts/projects.</li>
</ul>
Result: <span class="bain-red">Significant, ongoing monthly cloud cost savings</span> with no negative impact on business continuity.
</div>
""", unsafe_allow_html=True)

# 7. Download button for the combined savings table
csv = filtered.to_csv(index=False).encode()
st.download_button(
    label="Download detailed savings data as CSV",
    data=csv,
    file_name='cloud_cost_savings_summary.csv',
    mime='text/csv',
    help="Download the current filtered data"
)

st.markdown('<center><img src="https://www.bain.com/contentassets/72eae12bfa234408a76596b86f668d90/bain_red_logo.svg" width="120"></center>', unsafe_allow_html=True)
