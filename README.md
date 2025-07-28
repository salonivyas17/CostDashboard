# Cloud Cost Savings Dashboard

A Streamlit-based dashboard that visualizes cloud cost savings from decommissioned subscriptions, accounts, and projects across Azure, AWS, and GCP.

## Features

- **Multi-cloud cost analysis** - View savings across Azure, AWS, and GCP
- **Interactive visualizations** - Pie charts, bar charts, and timeline graphs
- **Provider filtering** - Filter data by specific cloud providers
- **Cost breakdown** - Detailed view of savings by account/project
- **Download functionality** - Export filtered data as CSV

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the dashboard:**
   ```bash
   streamlit run app.py
   ```

3. **For Replit deployment:**
   - The `.replit` file is configured for automatic deployment
   - Simply click "Run" in Replit

## Data Structure

The dashboard expects Excel files in the `data/` folder:
- `Azure_Resource_Subscription_Cost_Estimate.xlsx`
- `GCP_Resource_Project_Cost_Grouped.xlsx`
- `AWS_Merged.costs.xlsx`

## Technologies Used

- **Streamlit** - Web app framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **OpenPyXL** - Excel file reading

## Author

Saloni Vyas - 2025 