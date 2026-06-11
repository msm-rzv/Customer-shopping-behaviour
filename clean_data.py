"""
Customer Shopping Behaviour — Data Cleaning Script
Author: Masooma Rizvi
Date: June 2025

Steps:
    1. Load raw CSV
    2. Explore structure and check for missing values
    3. Impute missing Review Ratings using category median
    4. Standardise column names
    5. Engineer age_group feature
    6. Engineer purchase_frequency_days feature
    7. Drop redundant promo_code_used column
    8. Load cleaned data into PostgreSQL
"""

import pandas as pd
from sqlalchemy import create_engine


# ── 1. Load Data ──────────────────────────────────────────────
df = pd.read_csv('customer_shopping_behavior.csv')

print("Shape:", df.shape)
print("\nColumn names:", df.columns.tolist())


# ── 2. Explore & Check for Missing Values ─────────────────────
print("\n--- Data Types ---")
print(df.info())

print("\n--- Summary Statistics ---")
print(df.describe(include='all'))

print("\n--- Missing Values ---")
print(df.isnull().sum())


# ── 3. Impute Missing Review Ratings ──────────────────────────
# Fill nulls with the median rating within each product category
# This preserves category-level rating patterns rather than using a global median

df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(
    lambda x: x.fillna(x.median())
)

print("\n--- Missing Values After Imputation ---")
print(df.isnull().sum())


# ── 4. Standardise Column Names ───────────────────────────────
# Lowercase all column names and replace spaces with underscores for SQL compatibility
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})

print("\n--- Cleaned Column Names ---")
print(df.columns.tolist())


# ── 5. Engineer age_group Feature ─────────────────────────────
# Quartile-based age bands so each group has roughly equal customer counts
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

print("\n--- Age Group Distribution ---")
print(df['age_group'].value_counts().sort_index())


# ── 6. Engineer purchase_frequency_days Feature ───────────────
# Maps text frequency labels to numeric days for quantitative analysis
frequency_mapping = {
    'Weekly':          7,
    'Fortnightly':     14,
    'Bi-Weekly':       14,
    'Monthly':         30,
    'Quarterly':       90,
    'Every 3 Months':  90,
    'Annually':        365,
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

print("\n--- Purchase Frequency Days Sample ---")
print(df[['frequency_of_purchases', 'purchase_frequency_days']].drop_duplicates().sort_values('purchase_frequency_days'))


# ── 7. Drop Redundant Column ──────────────────────────────────
# promo_code_used is 100% identical to discount_applied — confirmed before dropping
identical = (df['discount_applied'] == df['promo_code_used']).all()
print(f"\npromo_code_used identical to discount_applied: {identical}")

df = df.drop('promo_code_used', axis=1)

print("\n--- Final Columns ---")
print(df.columns.tolist())
print("\nFinal shape:", df.shape)


# ── 8. Load to PostgreSQL ─────────────────────────────────────
# Update credentials as needed
username = "postgres"
password = "your_password"
host     = "localhost"
port     = "5432"
database = "customer_behaviour"

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

df.to_sql("customer", engine, if_exists="replace", index=False)
print(f"\nData successfully loaded into table 'customer' in database '{database}'.")
