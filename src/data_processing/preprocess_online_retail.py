
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "online+retail" / "Online Retail.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOAD ORIGINAL DATA
# --------------------------------------------------

df = pd.read_excel(DATA_PATH)
original_record_count = len(df)

print("Original dataset:", df.shape)

# Remove exact duplicate records
df = df.drop_duplicates().copy()

print("After removing exact duplicates:", df.shape)


# --------------------------------------------------
# 3. STANDARDISE DATA TYPES
# --------------------------------------------------

df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()
df["StockCode"] = df["StockCode"].astype(str).str.strip()

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce"
)

df["Quantity"] = pd.to_numeric(
    df["Quantity"],
    errors="coerce"
)

df["UnitPrice"] = pd.to_numeric(
    df["UnitPrice"],
    errors="coerce"
)


# --------------------------------------------------
# 4. SEPARATE CANCELLATIONS
# --------------------------------------------------

cancelled_mask = df["InvoiceNo"].str.startswith("C")

cancellations = df[cancelled_mask].copy()
sales = df[~cancelled_mask].copy()

print("Cancellation records:", len(cancellations))


# --------------------------------------------------
# 5. IDENTIFY POTENTIALLY FULLY REVERSED SALES
# --------------------------------------------------

# Cancellation invoice numbers do not necessarily match
# original invoice numbers.
#
# Therefore, use conservative one-to-one matching based on:
# CustomerID, StockCode, UnitPrice, transaction date,
# and exact absolute quantity.
#
# This is a heuristic, not a guaranteed invoice-level link.
# Only customers with known IDs are included.

sales = sales.copy()
cancellations = cancellations.copy()

sales["_sale_row_id"] = range(len(sales))
cancellations["_cancel_row_id"] = range(len(cancellations))

sales["TransactionDate"] = sales["InvoiceDate"].dt.date

cancellations["TransactionDate"] = (
    cancellations["InvoiceDate"].dt.date
)

positive_sales = sales[
    (sales["Quantity"] > 0)
    & sales["CustomerID"].notna()
].copy()

customer_cancellations = cancellations[
    (cancellations["Quantity"] < 0)
    & cancellations["CustomerID"].notna()
].copy()

# Use absolute quantities for matching
positive_sales["MatchQuantity"] = positive_sales["Quantity"]

customer_cancellations["MatchQuantity"] = (
    customer_cancellations["Quantity"].abs()
)

match_keys = [
    "CustomerID",
    "StockCode",
    "UnitPrice",
    "TransactionDate",
    "MatchQuantity"
]

# Assign occurrence numbers to identical transaction groups.
# This allows each sale and cancellation row to be paired once.

positive_sales["_match_occurrence"] = (
    positive_sales
    .groupby(match_keys, dropna=False)
    .cumcount()
)

customer_cancellations["_match_occurrence"] = (
    customer_cancellations
    .groupby(match_keys, dropna=False)
    .cumcount()
)

pair_keys = match_keys + ["_match_occurrence"]

# One-to-one matching prevents many-to-many duplication.
matched_pairs = positive_sales[
    pair_keys + ["_sale_row_id"]
].merge(
    customer_cancellations[
        pair_keys + ["_cancel_row_id"]
    ],
    on=pair_keys,
    how="inner",
    validate="one_to_one"
)

reversed_sale_ids = matched_pairs["_sale_row_id"].tolist()
reversed_cancel_ids = matched_pairs["_cancel_row_id"].tolist()

# Preserve matched original sales
fully_reversed_originals = sales[
    sales["_sale_row_id"].isin(reversed_sale_ids)
].copy()

# Preserve their matched cancellation records
fully_reversed_cancellations = cancellations[
    cancellations["_cancel_row_id"].isin(reversed_cancel_ids)
].copy()

fully_reversed_originals["RecordType"] = "Original invoice"
fully_reversed_cancellations["RecordType"] = "Cancellation"

fully_reversed_audit = pd.concat(
    [
        fully_reversed_originals,
        fully_reversed_cancellations
    ],
    ignore_index=True
)

# Remove only individually matched original sales
sales = sales[
    ~sales["_sale_row_id"].isin(reversed_sale_ids)
].copy()

# Remove temporary matching columns
sales = sales.drop(
    columns=["_sale_row_id", "TransactionDate"]
)

cancellations = cancellations.drop(
    columns=["_cancel_row_id", "TransactionDate"]
)

fully_reversed_audit = fully_reversed_audit.drop(
    columns=[
        "_sale_row_id",
        "_cancel_row_id"
    ],
    errors="ignore"
)

print(
    "Potentially fully reversed original sales:",
    len(fully_reversed_originals)
)

print(
    "Matched cancellation records:",
    len(fully_reversed_cancellations)
)


# --------------------------------------------------
# 6. SEPARATE RETURNS
# --------------------------------------------------

returns_mask = sales["Quantity"] < 0

returns = sales[returns_mask].copy()
sales = sales[~returns_mask].copy()


# --------------------------------------------------
# 7. REMOVE INVALID SALES RECORDS
# --------------------------------------------------

invalid_mask = (
    sales["UnitPrice"].isna()
    | (sales["UnitPrice"] <= 0)
    | sales["Quantity"].isna()
    | (sales["Quantity"] <= 0)
    | sales["InvoiceDate"].isna()
)

excluded = sales[invalid_mask].copy()
cleaned = sales[~invalid_mask].copy()


# --------------------------------------------------
# 8. HANDLE MISSING DESCRIPTIONS
# --------------------------------------------------

cleaned["Description"] = (
    cleaned["Description"].fillna("Unknown")
)


# --------------------------------------------------
# 9. CALCULATE REVENUE
# --------------------------------------------------

cleaned["Revenue"] = (
    cleaned["Quantity"] * cleaned["UnitPrice"]
)


# --------------------------------------------------
# 10. SEPARATE PRODUCT SALES FROM NON-PRODUCT CHARGES
# --------------------------------------------------

non_product_codes = {
    "POST",
    "DOT",
    "M",
    "m",
    "C2",
    "23444",
    "23574",
    "BANK CHARGES",
    "AMAZONFEE",
    "B"
}

non_product_mask = cleaned["StockCode"].isin(non_product_codes)

non_product_audit = cleaned[non_product_mask].copy()
product_sales = cleaned[~non_product_mask].copy()


# --------------------------------------------------
# 11. SAVE PROCESSED DATASETS
# --------------------------------------------------

cleaned.to_csv(
    OUTPUT_DIR / "online_retail_cleaned.csv",
    index=False
)

product_sales.to_csv(
    OUTPUT_DIR / "online_retail_product_sales.csv",
    index=False
)

non_product_audit.to_csv(
    OUTPUT_DIR / "online_retail_non_product_audit.csv",
    index=False
)

# Preserve cancellation and return records together
returns_and_cancellations = pd.concat(
    [cancellations, returns],
    ignore_index=True
)

returns_and_cancellations.to_csv(
    OUTPUT_DIR / "online_retail_returns_cancellations.csv",
    index=False
)

excluded.to_csv(
    OUTPUT_DIR / "online_retail_excluded.csv",
    index=False
)

fully_reversed_audit.to_csv(
    OUTPUT_DIR / "online_retail_fully_reversed_audit.csv",
    index=False
)


# --------------------------------------------------
# 12. FINAL PREPROCESSING REPORT
# --------------------------------------------------

print("\n========== PREPROCESSING REPORT ==========")

print("Original records:", original_record_count)
print("Records after duplicate removal:", len(df))

print("Clean sales records:", len(cleaned))
print("Product sales records:", len(product_sales))
print("Non-product records separated:", len(non_product_audit))

print("Cancellation records:", len(cancellations))
print("Return records:", len(returns))
print("Invalid sales excluded:", len(excluded))

print(
    "Potentially fully reversed records preserved in audit:",
    len(fully_reversed_audit)
)

print(
    "Potentially fully reversed original sales removed:",
    len(fully_reversed_originals)
)

print(
    "Missing CustomerID:",
    cleaned["CustomerID"].isna().sum()
)

print(
    "Missing descriptions:",
    cleaned["Description"].isna().sum()
)

print("Final cleaned dataset shape:", cleaned.shape)

print("\nOutput folder:", OUTPUT_DIR)

print("\nPreprocessing completed.")
