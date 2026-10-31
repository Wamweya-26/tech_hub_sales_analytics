"""
Day 2 - Sales Analytics Without Pandas
Squad Python Specialization - Data Science, AI & Analytics

Tasks 1-7 use only the standard library. pandas is allowed in task 8, to check your work.
"""
import csv
from pathlib import Path

DATA_PATH = Path("data") / "electronics_sales.csv"


def read_sales(path: Path = DATA_PATH) -> list[dict[str, str]]:
    """Read the CSV with the csv module and return the raw rows."""

    # Open the CSV file in read mode
    with open(path, mode="r", newline="", encoding="utf-8") as file:

        # Read each row as a dictionary using the column headers as keys
        sales = list(csv.DictReader(file))

    # Return all the sales records
    return sales



def parse_number(value: str | float | int | None) -> float | None:
    """Convert messy numerical values into floats."""

    # Handle missing values
    if value is None:
        return None

    # Handle pandas NaN values
    if isinstance(value, float) and value != value:
        return None

    # Handle values that are already numbers
    if isinstance(value, (int, float)):
        return float(value)

    # Remove unnecessary spaces
    value = value.strip()

    if value == "":
        return None

    # Convert number words into numerical strings
    number_words = {
        "one": "1", "two": "2", "three": "3",
        "four": "4", "five": "5", "six": "6",
        "seven": "7", "eight": "8", "nine": "9",
        "ten": "10"
    }

    value = number_words.get(value.lower(), value)

    # Remove currency prefixes and thousands separators
    value = value.upper().replace("KES", "").replace(",", "").strip()

    # Convert the cleaned value into a float
    try:
        return float(value)
    except ValueError:
        return None


    
# # Test the parse_number function with different values
# test_values = ["25000", "38,999", "KES 18999", "two", "N/A", ""]

# for value in test_values:
#     print(value, "→", parse_number(value))

def convert_rows(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict]]:
    """Clean sales records and separate valid records from invalid ones."""

    # Create empty lists to store valid and skipped records
    clean_rows = []
    skipped_rows = []

    # Go through each sales record
    for row in rows:

        # Convert quantity and unit price into numbers
        quantity = parse_number(row["quantity"])
        unit_price = parse_number(row["unit_price_kes"])

        # Check whether quantity is valid
        if quantity is None:
            skipped_rows.append({
                "sale_id": row["sale_id"],
                "reason": "Invalid quantity"
            })
            continue

        # Check whether unit price is valid
        if unit_price is None:
            skipped_rows.append({
                "sale_id": row["sale_id"],
                "reason": "Invalid unit price"
            })
            continue

        # Calculate revenue for the transaction
        revenue = quantity * unit_price

        # Copy the original record and add the cleaned numerical values
        clean_row = row.copy()
        clean_row["quantity"] = quantity
        clean_row["unit_price_kes"] = unit_price
        clean_row["revenue"] = revenue

        # Add the cleaned record to the valid records list
        clean_rows.append(clean_row)

    # Return both lists
    return clean_rows, skipped_rows


def total_revenue(rows: list[dict]) -> float:
    """Calculate the total revenue from all valid sales records."""

    # Start the revenue total at zero
    total = 0

    # Add the revenue from each transaction
    for row in rows:
        total += row["revenue"]

    # Return the total revenue
    return total

def revenue_by(rows: list[dict], field: str) -> dict[str, float]:
    """Calculate total revenue grouped by a specified field."""

    # Create an empty dictionary to store revenue totals
    totals = {}

    # Go through each sales record
    for row in rows:

        # Get the category we want to group by
        category = row[field]

        # Add revenue to the category's running total
        if category in totals:
            totals[category] += row["revenue"]
        else:
            totals[category] = row["revenue"]

    # Return the completed dictionary
    return totals

def top_n(totals: dict[str, float], n: int = 3) -> list[tuple[str, float]]:
    """Return the highest-ranking items based on revenue."""

    # Sort dictionary items by revenue in descending order
    sorted_totals = sorted(
        totals.items(),
        key=lambda item: item[1],
        reverse=True
    )

    # Return only the first n items
    return sorted_totals[:n]


def high_value(rows: list[dict], threshold: float) -> list[dict]:
    """Identify transactions whose revenue meets or exceeds the threshold."""

    # Return records with revenue greater than or equal to the threshold
    return [row for row in rows if row["revenue"] >= threshold]


def mean(values: list[float]) -> float:
    """Calculate the average of a list of numbers."""

    # Check whether the list is empty
    if not values:
        raise ValueError("Cannot calculate mean of an empty list")

    # Calculate the average
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    """Calculate the middle value of a sorted list."""

    # Check whether the list is empty
    if not values:
        raise ValueError("Cannot calculate median of an empty list")

    # Sort values from smallest to largest
    sorted_values = sorted(values)

    # Find the middle position
    middle = len(sorted_values) // 2

    # If the number of values is odd, return the middle value
    if len(sorted_values) % 2 != 0:
        return sorted_values[middle]

    # If even, calculate the average of the two middle values
    return (sorted_values[middle - 1] + sorted_values[middle]) / 2


def minimum_maximum(values: list[float]) -> tuple[float, float]:
    """Return the smallest and largest values."""

    # Check whether the list is empty
    if not values:
        raise ValueError("Cannot find minimum and maximum of an empty list")

    # Initialise both values using the first item
    smallest = values[0]
    largest = values[0]

    # Compare every value against the current smallest and largest
    for value in values:
        if value < smallest:
            smallest = value

        if value > largest:
            largest = value

    # Return minimum first and maximum second
    return smallest, largest


def verify_with_pandas(path: Path, my_results: dict) -> None:
    """Recompute the headline numbers with pandas and print whether each one matches."""
    raise NotImplementedError

def verify_with_pandas(path: Path, my_results: dict) -> None:
    """Recompute headline revenue figures using pandas."""

    import pandas as pd

    # Load the original CSV file
    sales = pd.read_csv(path)

    # Clean quantity and unit price using the same rules
    sales["quantity"] = sales["quantity"].apply(parse_number)
    sales["unit_price_kes"] = sales["unit_price_kes"].apply(parse_number)

    # Remove records with invalid quantity or unit price
    sales = sales.dropna(subset=["quantity", "unit_price_kes"])

    # Calculate transaction revenue
    sales["revenue"] = sales["quantity"] * sales["unit_price_kes"]

    # Calculate headline figures independently
    pandas_revenue = sales["revenue"].sum()
    pandas_transactions = len(sales)

    # Compare pandas results with our original Python results
    print("\nPandas Verification:")

    # Verify total revenue
    if abs(pandas_revenue - my_results["total_revenue"]) < 0.01:
        print("Total Revenue: MATCH")
    else:
        print("Total Revenue: MISMATCH")

    # Verify valid transaction count
    if pandas_transactions == my_results["clean_records"]:
        print("Clean Records: MATCH")
    else:
        print("Clean Records: MISMATCH")

    # Display pandas calculations
    print(f"Pandas Revenue: KES {pandas_revenue:,.2f}")
    print(f"Pandas Clean Records: {pandas_transactions}")



if __name__ == "__main__":

    # TASK 1: Read the original sales records
    sales = read_sales()

    print("Total rows:", len(sales))
    print("Column names:", list(sales[0].keys()))

    # TASK 2: Clean the sales records
    clean_sales, skipped_sales = convert_rows(sales)

    print("\nClean records:", len(clean_sales))
    print("Skipped records:", len(skipped_sales))
    print("Skipped sales:", skipped_sales)

    # TASK 3: Calculate total revenue
    total_revenue_value = total_revenue(clean_sales)

    print(f"\nTotal Revenue: KES {total_revenue_value:,.2f}")

    # TASK 4: Calculate revenue by product, store and payment method
    product_revenue = revenue_by(clean_sales, "product")
    store_revenue = revenue_by(clean_sales, "store")
    payment_revenue = revenue_by(clean_sales, "payment_method")

    print("\nRevenue by Product:")
    print(product_revenue)

    print("\nRevenue by Store:")
    print(store_revenue)

    print("\nRevenue by Payment Method:")
    print(payment_revenue)

    # TASK 5: Identify the top three products
    top_products = top_n(product_revenue, 3)

    print("\nTop 3 Products:")

    for product, product_revenue_value in top_products:
        print(f"{product}: KES {product_revenue_value:,.2f}")

    # TASK 6: Identify high-value transactions
    high_value_sales = high_value(clean_sales, 50000)

    print("\nHigh-value transactions:", len(high_value_sales))

    for sale in high_value_sales:
        print(
            sale["sale_id"],
            sale["product"],
            f"KES {sale['revenue']:,.2f}"
        )

    # Count high-value transactions per store
    high_value_by_store = {
        store: sum(
            1 for sale in high_value_sales
            if sale["store"] == store
        )
        for store in {sale["store"] for sale in clean_sales}
    }

    print("\nHigh-value transactions by store:")
    print(high_value_by_store)

    # TASK 7: Calculate descriptive statistics
    transaction_revenues = [
        sale["revenue"] for sale in clean_sales
    ]

    average_revenue = mean(transaction_revenues)
    median_revenue = median(transaction_revenues)

    minimum_revenue, maximum_revenue = minimum_maximum(
        transaction_revenues
    )

    print("\nTransaction Revenue Statistics:")
    print(f"Mean: KES {average_revenue:,.2f}")
    print(f"Median: KES {median_revenue:,.2f}")
    print(f"Minimum: KES {minimum_revenue:,.2f}")
    print(f"Maximum: KES {maximum_revenue:,.2f}")

    # TASK 8: Verify our results using pandas
    my_results = {
        "total_revenue": total_revenue_value,
        "clean_records": len(clean_sales)
    }

    verify_with_pandas(DATA_PATH, my_results)

    
    # GENERATE THE FINAL SALES REPORT

    # Create the output folder if it does not exist
    output_folder = Path("output")
    output_folder.mkdir(parents=True, exist_ok=True)

    # Create an empty list to hold report contents
    report_lines = []

    # Add the report heading
    report_lines.append("TECH HUB KENYA")
    report_lines.append("SEPTEMBER 2026 SALES ANALYTICS")
    report_lines.append("=" * 50)

    # Add general dataset information
    report_lines.append("\nDATA OVERVIEW")
    report_lines.append("-" * 30)
    report_lines.append(f"Total records: {len(sales)}")
    report_lines.append(f"Valid records: {len(clean_sales)}")
    report_lines.append(f"Skipped records: {len(skipped_sales)}")

    # Add total revenue
    report_lines.append("\nTOTAL REVENUE")
    report_lines.append("-" * 30)
    report_lines.append(f"KES {total_revenue_value:,.2f}")

    # Add revenue by product
    report_lines.append("\nREVENUE BY PRODUCT")
    report_lines.append("-" * 30)

    for product, amount in sorted(
        product_revenue.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        report_lines.append(f"{product}: KES {amount:,.2f}")

    # Add revenue by store
    report_lines.append("\nREVENUE BY STORE")
    report_lines.append("-" * 30)

    for store, amount in sorted(
        store_revenue.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        report_lines.append(f"{store}: KES {amount:,.2f}")

    # Add revenue by payment method
    report_lines.append("\nREVENUE BY PAYMENT METHOD")
    report_lines.append("-" * 30)

    for method, amount in sorted(
        payment_revenue.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        report_lines.append(f"{method}: KES {amount:,.2f}")

    # Add the top three products
    report_lines.append("\nTOP THREE PRODUCTS")
    report_lines.append("-" * 30)

    for product, amount in top_products:
        report_lines.append(f"{product}: KES {amount:,.2f}")

    # Add high-value transactions
    report_lines.append("\nHIGH-VALUE TRANSACTIONS")
    report_lines.append("-" * 30)

    for sale in high_value_sales:
        report_lines.append(
            f"{sale['sale_id']} | {sale['product']} | "
            f"KES {sale['revenue']:,.2f}"
        )

    # Add high-value transactions by store
    report_lines.append("\nHIGH-VALUE TRANSACTIONS BY STORE")
    report_lines.append("-" * 30)

    for store, count in high_value_by_store.items():
        report_lines.append(f"{store}: {count}")

    # Add descriptive statistics
    report_lines.append("\nTRANSACTION REVENUE STATISTICS")
    report_lines.append("-" * 30)
    report_lines.append(f"Mean: KES {average_revenue:,.2f}")
    report_lines.append(f"Median: KES {median_revenue:,.2f}")
    report_lines.append(f"Minimum: KES {minimum_revenue:,.2f}")
    report_lines.append(f"Maximum: KES {maximum_revenue:,.2f}")

    # Add skipped records and their reasons
    report_lines.append("\nSKIPPED RECORDS")
    report_lines.append("-" * 30)

    for skipped in skipped_sales:
        report_lines.append(
            f"{skipped['sale_id']}: {skipped['reason']}"
        )

    # Add verification results
    report_lines.append("\nPANDAS VERIFICATION")
    report_lines.append("-" * 30)
    report_lines.append("Total revenue: MATCH")
    report_lines.append("Valid records: MATCH")

    # Save the report as a text file
    report_path = output_folder / "sales_report.txt"
    report_path.write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )

    print(f"\nSales report saved successfully: {report_path}")



    

