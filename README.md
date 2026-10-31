# Tech Hub Kenya – September 2026 Sales Analytics

## 1. Project Overview

This project analyses September 2026 sales data for Tech Hub Kenya, a retailer dealing in phones, laptops and electronic accessories.

The objective is to calculate total revenue, identify the best-performing products and stores, analyse payment methods, and identify high-value transactions.

The project uses Python's standard library for the main analysis, with pandas used independently to verify the headline results.

## 2. Project Structure

```text
tech_hub_sales_analytics/
│
├── data/
│   └── electronics_sales.csv
│
├── output/
│   └── sales_report.txt
│
├── sales_analysis.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 3. Technologies Used

- Python 3
- csv module
- pathlib
- pandas (verification)
- Git and GitHub

## 4. Data Cleaning and Preparation

The original dataset contained 50 sales records.

The following cleaning procedures were implemented:

- Removed unnecessary spaces from numerical values.
- Removed currency prefixes such as KES.
- Removed commas used as thousands separators.
- Converted numerical values into floating-point numbers.
- Handled missing and unparseable numerical values.
- Converted supported number words from one to ten into numerical values.
- Excluded records with invalid quantities or unit prices.
- Calculated transaction revenue using quantity multiplied by unit price.

### Data Quality Results

| Description | Records |
|---|---:|
| Original records | 50 |
| Valid records | 47 |
| Skipped records | 3 |

### Skipped Records

| Sale ID | Reason |
|---|---|
| S-3030 | Invalid unit price |
| S-3035 | Invalid quantity |
| S-3039 | Invalid unit price |

## 5. Analysis Performed

The project implemented the following functions:

1. `read_sales()` – reads the CSV file using `csv.DictReader`.
2. `parse_number()` – cleans and converts numerical values.
3. `convert_rows()` – separates valid and invalid records.
4. `total_revenue()` – calculates total sales revenue.
5. `revenue_by()` – groups revenue by product, store and payment method.
6. `top_n()` – identifies the highest-performing products.
7. `high_value()` – identifies transactions of KES 50,000 and above.
8. `mean()`, `median()` and `minimum_maximum()` – calculate descriptive statistics.
9. `verify_with_pandas()` – independently checks headline results using pandas.

## 6. Key Findings

### Overall Performance

| Metric | Result |
|---|---:|
| Total Revenue | KES 1,317,210.00 |
| Valid Transactions | 47 |
| Skipped Transactions | 3 |
| High-value Transactions | 5 |

### Top Three Products by Revenue

| Product | Revenue (KES) |
|---|---:|
| HP 15 Laptop | 389,994.00 |
| Hisense 43in Smart TV | 272,993.00 |
| Lenovo Tab M10 | 199,992.00 |

### Store Performance

Kisumu Mega Plaza recorded the highest revenue, generating KES 449,678.00.

### Payment Method Performance

M-Pesa generated the highest revenue at KES 738,568.00.

### High-value Transactions

A transaction was classified as high-value when its revenue was equal to or greater than KES 50,000.

Five transactions met this threshold.

### Descriptive Statistics

| Statistic | Revenue (KES) |
|---|---:|
| Mean | 28,025.74 |
| Median | 10,998.00 |
| Minimum | 1,499.00 |
| Maximum | 259,996.00 |

## 7. Pandas Verification

Pandas was used to independently load the original CSV, apply the numerical cleaning rules, recalculate transaction revenue and compare the results with the standard-library implementation.

| Verification | Result |
|---|---|
| Total Revenue | MATCH |
| Valid Transaction Count | MATCH |

Both implementations returned total revenue of KES 1,317,210.00 and 47 valid transactions.

## 8. How to Run the Project

Clone the repository:

```bash
git clone https://github.com/Wamweya-26/tech_hub_sales_analytics.git
```

Navigate into the project folder:

```bash
cd tech_hub_sales_analytics
```

Install the required dependency:

```bash
pip install -r requirements.txt
```

Run the analysis:

```bash
python sales_analysis.py
```

The analysis results are displayed in the terminal and saved to:

```text
output/sales_report.txt
```

## 9. Conclusion

The analysis successfully processed 50 sales records, retained 47 valid transactions and calculated total revenue of KES 1,317,210.00.

HP 15 Laptop was the highest revenue-generating product, Kisumu Mega Plaza was the highest-performing store, and M-Pesa was the leading payment method.

The successful pandas verification provides confidence in the accuracy of the headline results.
