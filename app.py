import streamlit as st
import pandas as pd
import plotly.express as px

# ---- BAIN COLORS ----
BAIN_RED = "#AF0A26"
BAIN_DARK = "#00294B"
BAIN_GREY = "#F7F7F7"

st.set_page_config(page_title="Cloud Cost Savings Dashboard", layout="wide")
st.markdown(f"""
    <style>
        html, body, [class*="css"]  {{ background-color: {BAIN_GREY} !important; }}
        .big-title {{ font-size: 2.7em; font-weight: bold; color: {BAIN_RED}; margin-bottom:0.2em; }}
        .bain-card {{
            background: #fff; border-radius: 22px;
            box-shadow: 0 8px 36px #e3c3c394;
            padding: 2.5em 2.5em 1.2em 2.5em; margin: 1em 0 2em 0;
            display: flex; align-items: center;
        }}
        .bain-red {{ color: {BAIN_RED}; }}
        .bain-dark {{ color: {BAIN_DARK}; }}
        .icon-title {{ vertical-align: middle; margin-right: 0.3em; }}
        .bain-subtitle {{ font-size:1.5em; color:{BAIN_DARK}; font-weight: 700; letter-spacing:-1px; }}
        .number-title {{ font-size:2.4em; font-weight:800; color:{BAIN_RED}; }}
        .provider-card {{ display:inline-block; background:#fff; border-radius:15px; box-shadow:0 2px 12px #ccc; margin:0.5em; padding:1em 2em; min-width:180px; }}
        .css-1q8dd3e, .stButton>button, .stDownloadButton>button {{ background-color: {BAIN_RED}; color: #fff; border-radius:10px; }}
        .stRadio>div>label>div[data-testid="stMarkdownContainer"] > p {{font-weight:bold;}}
    </style>
""", unsafe_allow_html=True)

# ---- DATA ----
data_folder = "data"
az = pd.read_excel(f'{data_folder}/Azure_Resource_Subscription_Cost_Estimate.xlsx')
gcp = pd.read_excel(f'{data_folder}/GCP_Resource_Project_Cost_Grouped.xlsx')
aws = pd.read_excel(f'{data_folder}/AWS_Merged.costs.xlsx')

# ---- AGGREGATION ----
az = az[az['name'] != "SUBSCRIPTION TOTAL"]
az_group = az.groupby(['subscriptionName'], as_index=False)['Service total'].sum()
az_group['Provider'] = 'Azure'
az_group = az_group.rename(columns={'subscriptionName': 'Account/Project', 'Service total':'Cost Saved'})
gcp = gcp[gcp['CLOUD_RESOURCE.Name'] != "PROJECT TOTAL"]
gcp_group = gcp.groupby(['SUBSCRIPTION.Name'], as_index=False)['Service total'].sum()
gcp_group['Provider'] = 'GCP'
gcp_group = gcp_group.rename(columns={'SUBSCRIPTION.Name': 'Account/Project', 'Service total':'Cost Saved'})
acct_col = [col for col in aws.columns if 'account' in col.lower()][0]
cost_col = [col for col in aws.columns if 'service total' in col.lower() or 'cost' in col.lower()][0]
aws_group = aws.groupby([acct_col], as_index=False)[cost_col].sum()
aws_group['Provider'] = 'AWS'
aws_group = aws_group.rename(columns={acct_col: 'Account/Project', cost_col: 'Cost Saved'})
all_data = pd.concat([az_group, gcp_group, aws_group], ignore_index=True)

# ---- HEADER ----
st.markdown(f'''
<div style="display:flex;align-items:center;gap:1em;margin-top:1em;">
    <img src="https://img.icons8.com/fluency/96/000000/globe.png" height="70" class="icon-title">
    <span class="big-title">
        Cloud Cost Savings from<br>Decommissioned Subscriptions/Accounts/Projects
    </span>
</div>
''', unsafe_allow_html=True)
st.markdown('<div class="bain-subtitle">See how temporary and permanent decommissioning actions across <span class="bain-red">Azure, AWS, and GCP</span> have cut cloud spend.</div>', unsafe_allow_html=True)

# ---- PROVIDER CARDS ----
total_savings = all_data['Cost Saved'].sum()
cols = st.columns(4)
icons = {"Azure":"https://img.icons8.com/color/48/000000/azure-1.png", "AWS":"https://img.icons8.com/color/48/000000/amazon-web-services.png", "GCP":"https://img.icons8.com/color/48/000000/google-cloud.png"}
for i, provider in enumerate(["Azure","AWS","GCP"]):
    cost = all_data[all_data["Provider"]==provider]["Cost Saved"].sum()
    cols[i].markdown(
        f'<div class="provider-card" style="text-align:center">'
        f'<img src="{icons[provider]}" width="38"><br>'
        f'<span style="font-size:1.25em;font-weight:700">{provider}</span><br>'
        f'<span class="number-title">${cost:,.0f}</span>'
        f'</div>', unsafe_allow_html=True)
cols[3].markdown(
    f'<div class="provider-card" style="text-align:center">'
    f'<img src="https://img.icons8.com/emoji/48/000000/money-mouth-face.png" width="38"><br>'
    f'<span style="font-size:1.1em;font-weight:700">Total Saved</span><br>'
    f'<span class="number-title">${total_savings:,.0f}</span>'
    f'</div>', unsafe_allow_html=True
)

# ---- PIE/DONUT CHART ----
pie_df = all_data.groupby("Provider")["Cost Saved"].sum().reset_index()
fig_pie = px.pie(pie_df, names="Provider", values="Cost Saved", hole=0.45,
                 color_discrete_map={"Azure":BAIN_DARK,"AWS":"#FF9900","GCP":"#4285F4"},
                 title="Share of Cost Savings by Cloud Provider")
fig_pie.update_traces(textinfo='percent+label', pull=[0.05,0,0])
fig_pie.update_layout(title_x=0.5, font_color=BAIN_DARK, font_family="Inter", showlegend=True)
st.plotly_chart(fig_pie, use_container_width=True)

# ---- BAR CHART BY PROVIDER ----
provider = st.selectbox('Filter by Cloud Provider', ['All', 'Azure', 'AWS', 'GCP'], key="bar-select")
filtered = all_data if provider == 'All' else all_data[all_data['Provider'] == provider]
bar = filtered.groupby('Provider')['Cost Saved'].sum().reset_index()
fig = px.bar(bar, x='Provider', y='Cost Saved', color='Provider',
    color_discrete_map={'Azure': BAIN_DARK, 'AWS': "#FF9900", 'GCP': "#4285F4"},
    text_auto=True, title="Cost Savings by Cloud Provider")
fig.update_layout(showlegend=False, plot_bgcolor='#fff', font_family='Inter', font_color=BAIN_DARK)
st.plotly_chart(fig, use_container_width=True)

# ---- AREA CHART: Timeline ----
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
trend_provider = st.radio('Show monthly cost trend for:', ['All','Azure','AWS','GCP'], horizontal=True)
trend_data = timeline if trend_provider == "All" else timeline[timeline["Provider"] == trend_provider]
trend = trend_data.groupby(['Month', 'Provider'])['Cost'].sum().reset_index()
fig2 = px.area(trend, x='Month', y='Cost', color='Provider',
    color_discrete_map={'Azure':BAIN_DARK, 'AWS':'#FF9900', 'GCP':'#4285F4'},
    markers=True, title="Cloud Cost Reduction Timeline (Decommissioned Accounts Only)")
fig2.update_traces(line_shape='spline', mode="lines+markers", marker=dict(size=8, symbol='circle'))
fig2.update_layout(yaxis_title="Monthly Cost Saved ($)", font_family='Inter', font_color=BAIN_DARK, plot_bgcolor="#fff")
st.plotly_chart(fig2, use_container_width=True)

# ---- TABLE ----
with st.expander("Show all decommissioned subscriptions/accounts/projects and savings"):
    st.dataframe(filtered.sort_values("Cost Saved", ascending=False).reset_index(drop=True), use_container_width=True)

# ---- STORY ----
st.markdown(f"""
<div class="bain-card">
<b>Decommissioning Journey:</b><br>
<ul>
<li> <b>April-May:</b> Temporary decommissioning (manual pausing/stopping of safe resources).</li>
<li> <b>By July:</b> Completed full decommission of targeted subscriptions/accounts/projects.</li>
</ul>
Result: <span class="bain-red">Significant, ongoing monthly cloud cost savings</span> with no negative impact on business continuity.
</div>
""", unsafe_allow_html=True)

# ---- DOWNLOAD BUTTON ----
csv = filtered.to_csv(index=False).encode()
st.download_button(
    label="Download detailed savings data as CSV",
    data=csv,
    file_name='cloud_cost_savings_summary.csv',
    mime='text/csv',
    help="Download the current filtered data"
)

st.markdown('<center><img src="https://www.bain.com/contentassets/72eae12bfa234408a76596b86f668d90/bain_red_logo.svg" width="120"></center>', unsafe_allow_html=True)
st.markdown('<center style="font-size:0.95em;color:#999">Dashboard by Saloni Vyas, powered by Streamlit • 2025</center>', unsafe_allow_html=True)
