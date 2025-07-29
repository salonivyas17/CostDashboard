# Cloud Cost Savings Dashboard

A comprehensive Streamlit-based dashboard that visualizes cloud cost savings from decommissioned subscriptions, accounts, and projects across **Azure**, **AWS**, and **GCP**. Built with Bain & Company branding and modern UI design.

##  Features

### Core Functionality
- **Multi-cloud cost analysis** - View savings across Azure, AWS, and GCP in one unified interface
- **Interactive visualizations** - Pie charts, bar charts, and timeline graphs with Plotly
- **Provider filtering** - Filter data by specific cloud providers
- **Cost breakdown** - Detailed view of savings by account/project
- **Download functionality** - Export filtered data as CSV
- **Theme toggle** - Switch between light and dark themes

### Dashboard Sections
- **Overview Tab** - Executive summary with key metrics and provider rankings
- **Visuals Tab** - Interactive charts including:
  - Cost savings distribution by provider (donut chart)
  - Top 5 cost-saving accounts (bar chart)
  - Cost reduction journey timeline (line chart)
- **Data Table Tab** - Raw data view with CSV export capability

### Key Metrics Displayed
- Total cost savings across all providers
- Average savings per account
- Median savings
- Provider-specific rankings
- Top performing accounts

### Data Requirements

The dashboard expects Excel files in the `data/` folder with the following structure:

### Azure Data (`Azure_6_Month_Cost_Estimate.xlsx`)
- Columns: `Account/Project`, `6-Month Cost ($)`
- Contains decommissioned Azure subscriptions and their cost estimates

### GCP Data (`GCP_Resource_Project_Cost_Grouped.xlsx`)
- Columns: `SUBSCRIPTION.Name`, `Service total`, `CLOUD_RESOURCE.Name`
- Contains GCP project costs and resource information

### AWS Data (`AWS_Merged.costs.xlsx`)
- Columns: Account column (auto-detected), `Total costs($)`
- Contains AWS account cost data

##  Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd Cost-Dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or using the project configuration:
   ```bash
   pip install -e .
   ```

3. **Prepare your data:**
   - Place your Excel files in the `data/` folder
   - Ensure file names match the expected format
   - Verify data structure matches requirements above

4. **Run the dashboard:**
   ```bash
   streamlit run app.py
   ```

5. **Access the dashboard:**
   - Open your browser to `http://localhost:8501`
   - The dashboard will load automatically

### Alternative Deployment Options

#### For Replit Deployment
- The `.replit` file is configured for automatic deployment
- Simply click "Run" in Replit
- No additional setup required

#### For Production Deployment
```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run with specific port
streamlit run app.py --server.port 8501
```

##  Design Features

### Bain & Company Branding
- Custom color scheme using Bain red (`#AF0A26`) and dark blue (`#00294B`)
- Professional typography with Inter font family
- Executive-style layout with gradient backgrounds
- Animated elements for enhanced user experience

### Responsive Design
- Wide layout optimized for desktop viewing
- Responsive charts that adapt to screen size
- Clean, modern interface with proper spacing

##  Usage Guide

### Navigation
1. **Overview Tab** - Start here for executive summary and key metrics
2. **Visuals Tab** - Explore interactive charts and data visualizations
3. **Data Table Tab** - Access raw data and download capabilities

### Key Interactions
- **Theme Toggle** - Switch between light and dark themes using the sidebar
- **Chart Interactions** - Hover over charts for detailed information
- **Data Export** - Download filtered data as CSV from the Data Table tab
- **Responsive Charts** - All charts are interactive and responsive

##  Technologies Used

### Core Framework
- **Streamlit** (>=1.28.0) - Web app framework and UI components

### Data Processing
- **Pandas** (>=1.5.0) - Data manipulation and analysis
- **OpenPyXL** (>=3.0.0) - Excel file reading and processing

### Visualization
- **Plotly** (>=5.15.0) - Interactive charts and graphs

### Development Tools
- **pytest** - Testing framework
- **black** - Code formatting
- **flake8** - Linting

##  Project Structure

```
Cost-Dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── README.md            # This file
└── data/                # Data files directory
    ├── Azure_6_Month_Cost_Estimate.xlsx
    ├── GCP_Resource_Project_Cost_Grouped.xlsx
    └── AWS_Merged.costs.xlsx
```

##  Configuration

### Customization Options
- **Colors**: Modify Bain color constants in `app.py`
- **Charts**: Adjust chart configurations in the visualization sections
- **Data Sources**: Update file paths and column mappings as needed

### Environment Variables
- No environment variables required for basic operation
- Configure Streamlit settings in `.streamlit/config.toml` if needed

##  Performance Tips

- Ensure Excel files are properly formatted and optimized
- For large datasets, consider pre-processing data
- Use appropriate data types for cost columns (numeric)
- Regular data updates recommended for accurate insights

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Format code: `black .`
6. Submit a pull request

##  License

This project is proprietary and confidential. All rights reserved.

##  Author

**Saloni Vyas** - 2025

---
 