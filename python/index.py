import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

connection_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="brinda$arvind10",
    host="localhost",
    database="da_project"
)
engine = create_engine(connection_url)

# Basic info
df = pd.read_csv(r"C:\Users\admin\OneDrive\Pictures\Documents\DA-Project\Customer-Shopping-Behavior-Analysis\data\customer_shopping_behavior.csv")

print(df.head())
print(df.info())
print(df.describe(include="all"))
print(df.isnull().sum())


# Fill missing Review Rating using median of each Category
df["Review Rating"] = df.groupby("Category")["Review Rating"].transform(
    lambda x: x.fillna(x.median())
)


# Change column names to snake_case
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ", "_")


# Rename purchase amount column
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})


# Create age_group
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']

df['age_group'] = pd.qcut(
    df['age'],
    q=4,
    labels=labels
)


# Purchase frequency days
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}


# Map purchase frequency to days
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(
    frequency_mapping
)


# Check both columns
print(
    df[['purchase_frequency_days', 'frequency_of_purchases']].head(10)
)


# Check whether discount and promo code are the same
print(df[['discount_applied', 'promo_code_used']].head(10))

print(
    (df['discount_applied'] == df['promo_code_used']).all()
)


# If both are the same, remove one column
df = df.drop('promo_code_used', axis=1)


# Check final columns
print(df.columns)


# Upload DataFrame to MySQL
df.to_sql(
    name="customer",
    con=engine,
    if_exists="replace",
    index=False
)
print("Customer table uploaded successfully!")