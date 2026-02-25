def detect_provider(columns):
    if "UsageDate" in columns:
        return "AZURE"
    if "Total costs($)" in columns:
        return "AWS"
    if "Service description" in columns:
        return "GCP"
    return "SNOWFLAKE"

import pandas as pd

def normalize_azure(df, account):
    df["UsageDate"] = pd.to_datetime(df["UsageDate"])
    df["year"] = df["UsageDate"].dt.year
    df["month"] = df["UsageDate"].dt.month

    result = (
        df.groupby(["year", "month"])
        .agg(cost_amount=("CostUSD", "sum"))
        .reset_index()
    )

    result["cloud_provider"] = "AZURE"
    result["account_name"] = account
    result["service"] = "ALL"

    return result

def normalize_aws(df, account):
    df = df[df.iloc[:, 0] != "Service total"]
    df.rename(columns={df.columns[0]: "date"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"])

    service_cols = [c for c in df.columns if c.endswith("($)")]

    melted = df.melt(
        id_vars=["date"],
        value_vars=service_cols,
        var_name="service",
        value_name="cost_amount"
    )

    melted["year"] = melted["date"].dt.year
    melted["month"] = melted["date"].dt.month
    melted["cloud_provider"] = "AWS"
    melted["account_name"] = account
    melted["service"] = melted["service"].str.replace("($)", "", regex=False)

    return melted[melted["cost_amount"] > 0]

def normalize_gcp(df, account, year, month):
    df["cloud_provider"] = "GCP"
    df["account_name"] = account
    df["service"] = df["Service description"]
    df["year"] = year
    df["month"] = month
    df["cost_amount"] = df["Subtotal ($)"]

    return df[[
        "cloud_provider",
        "account_name",
        "service",
        "year",
        "month",
        "cost_amount"
    ]]
