# Customer Shopping Behaviour
### A Data Analysis Case Study

> *What are the key drivers of customer spending behaviour, and how can the business use purchase patterns, loyalty segmentation, and product performance to improve revenue and customer retention?*

---

## Overview

This project analyses a retail dataset of **3,900 customers across 18 variables** — covering demographics, purchase history, product preferences, shipping habits, subscription status, and review ratings.

| | |
|---|---|
| **Dataset** | 3,900 customers, 18 variables |
| **Tools** | PostgreSQL, Power BI |
| **Language** | SQL |
| **Date** | June 2025 |

---

## Summary Statistics

| Metric | Value |
|---|---|
| Total Customers | 3,900 |
| Average Purchase Amount | $59.76 |
| Average Review Rating | 3.75 / 5.0 |
| Average Previous Purchases | 25.4 |
| Subscribed Customers | 27% (1,053) |
| Loyal Customers (11+ purchases) | 79.9% (3,116) |
| Top Category by Revenue | Clothing ($104,264) |

---

## Key Findings

- **Male customers generate 67.7% of revenue** — reflecting customer base composition (68% male) rather than higher individual spend
- **Subscriptions don't drive spend** — subscribers and non-subscribers average virtually identical purchase amounts ($59.49 vs $59.87)
- **79.9% of customers are Loyal but only 2.1% are New** — strong retention but weak acquisition
- **72.4% of repeat buyers are not subscribed** — the clearest conversion opportunity in the dataset
- **Discounts are concentrated on top sellers** — Blouse (50.3% discount rate) rather than underperformers like Jeans (124 orders)
- **Gloves and Boots are top-rated but least purchased** — high satisfaction is not translating into sales volume

---

## Data Cleaning

Before loading the data into PostgreSQL, the raw CSV was cleaned using Python (`clean_data.py`). The following steps were performed:

| Step | What Was Done | Why |
|---|---|---|
| **Missing value imputation** | Filled null Review Ratings with the median per category | Preserves category-level rating patterns rather than using a global median |
| **Column standardisation** | Lowercased all column names, replaced spaces with underscores | SQL compatibility — avoids needing quotes on every column name |
| **Column rename** | `purchase_amount_(usd)` → `purchase_amount` | Cleaner, simpler name for queries |
| **Age group feature** | Created `age_group` using quartile-based bands | Enables demographic revenue analysis |
| **Frequency feature** | Created `purchase_frequency_days` mapping text to numeric days | Enables quantitative frequency analysis |
| **Dropped redundant column** | Removed `promo_code_used` | 100% identical to `discount_applied` — confirmed before dropping |

---

## Repository Structure

```
├── README.md
├── clean_data.py                            # Python data cleaning script
├── queries.sql                              # All 13 SQL queries used in the analysis
├── customer_shopping_behavior.csv           # Raw dataset
└── Customer_Shopping_Behaviour_Case_Study.pdf  # Full written report
```

---

## How to Run the Queries

### Prerequisites
- PostgreSQL installed (version 14+)
- pgAdmin or any SQL client

### Setup

**1. Create the table**
```sql
CREATE TABLE customer (
    customer_id INT PRIMARY KEY,
    age INT,
    gender VARCHAR(10),
    item_purchased VARCHAR(50),
    category VARCHAR(20),
    purchase_amount NUMERIC(6,2),
    location VARCHAR(50),
    size VARCHAR(5),
    color VARCHAR(30),
    season VARCHAR(10),
    review_rating VARCHAR(5),
    subscription_status VARCHAR(5),
    shipping_type VARCHAR(20),
    discount_applied VARCHAR(5),
    promo_code_used VARCHAR(5),
    previous_purchases INT,
    payment_method VARCHAR(20),
    frequency_of_purchases VARCHAR(20)
);
```

**2. Import the CSV**
```sql
COPY customer(customer_id, age, gender, item_purchased, category, purchase_amount,
    location, size, color, season, review_rating, subscription_status, shipping_type,
    discount_applied, promo_code_used, previous_purchases, payment_method, frequency_of_purchases)
FROM '/your/path/customer_shopping_behavior.csv'
DELIMITER ','
CSV HEADER;
```

**3. Add the age_group column used in queries**
```sql
ALTER TABLE customer ADD COLUMN age_group VARCHAR(20);

UPDATE customer SET age_group =
    CASE
        WHEN age < 25 THEN 'Young Adult'
        WHEN age BETWEEN 25 AND 39 THEN 'Adult'
        WHEN age BETWEEN 40 AND 54 THEN 'Middle-aged'
        ELSE 'Senior'
    END;
```

**4. Run the queries**

Open `queries.sql` in pgAdmin and run each query individually by highlighting it and pressing **F5**.

---

## Analysis Structure

The analysis is divided into four sections:

**Section 1 — Revenue & Demographics**
- Total revenue by gender
- Revenue contribution by age group

**Section 2 — Product & Category Performance**
- Top 5 products by review rating
- Top 5 and bottom 5 products by purchase volume
- Top 3 products per category
- Top selling product in each category

**Section 3 — Subscriptions & Customer Loyalty**
- Subscription vs non-subscription spend comparison
- Customer segmentation (New / Returning / Loyal)
- Subscription rates among repeat buyers

**Section 4 — Discounts, Shipping & Spend Patterns**
- High-spend discount users
- Products with highest discount rates
- Spend comparison by shipping type

---

## Recommendations

| Recommendation | Evidence |
|---|---|
| **Subscription conversion campaign** | 2,518 loyal non-subscribers — 20% conversion nearly doubles subscriber base |
| **Redirect discount strategy** | Discounts on top sellers; Jeans at 124 orders needs support |
| **Young adult acquisition** | 18–24 age group contributes significantly less revenue |
| **Promote high-rated low-volume products** | Gloves (3.86 rating, 140 orders) and Boots (3.82 rating, 144 orders) |

---

*© 2025 Masooma Rizvi*
