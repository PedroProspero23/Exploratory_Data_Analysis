# Libraries
import pandas as pd

# Path to the exported CSV file from UN Comtrade
file_path = "C:/Users/pedro/OneDrive/Área de Trabalho/Códigos/Exploratory_Data_Analysis/TradeData_5_29_2025_9_6_47.csv"

# Initial data load
df = pd.read_csv(file_path)

# View the first few rows
print(df.head())

# Check column names
print(df.columns)

# Check data types
print(df.dtypes)

# Select relevant columns for analysis
useful_columns = [
    "refPeriodId",     # Reference year
    "reporterCode",    # Exporting country code
    "partnerCode",     # Importing country code
    "flowCode",        # Flow type code (probably 2 = Export)
    "cmdCode",         # Commodity code (e.g., 1201 for soybeans)
    "qtyUnitAbbr",     # Quantity unit
    "fobvalue",        # FOB value
    "cifvalue"         # CIF value
]

# Create reduced DataFrame
df_reduced = df[useful_columns].copy()

# Rename columns for clarity
df_reduced.rename(columns={
    "refPeriodId": "Year",
    "reporterCode": "Exporting_Country",
    "partnerCode": "Importing_Country",
    "flowCode": "Flow",
    "cmdCode": "Commodity_Code",
    "qtyUnitAbbr": "Unit",
    "fobvalue": "FOB_Value_USD",
    "cifvalue": "CIF_Value_USD"
}, inplace=True)

# Verify result
print(df_reduced.head())

# Ensure 'Year' is an integer
df_reduced["Year"] = df_reduced["Year"].astype(int)

# Check for missing values
print(df_reduced.isnull().sum())

# 📌 Detailed diagnostics of zero values

# Total records with Unit == 0
total_zeros = (df_reduced["Unit"] == 0).sum()
print(f"🔴 Total records with Unit = 0: {total_zeros}\n")

# Breakdown by exporting country
print("📍 Records with Unit = 0 by exporting country:")
print(df_reduced[df_reduced["Unit"] == 0]["Exporting_Country"].value_counts(), "\n")

# Breakdown by year
print("📍 Records with Unit = 0 by year:")
print(df_reduced[df_reduced["Unit"] == 0]["Year"].value_counts(), "\n")

# Cross tab by country and year
print("📍 Cross tab: Exporting country x Year with Unit = 0")
print(df_reduced[df_reduced["Unit"] == 0].groupby(["Exporting_Country", "Year"]).size())

# 📊 Check proportion of zero values in "Unit"
zeros_unit = (df_reduced["Unit"] == 0).sum()
total = len(df_reduced)
percentage = (zeros_unit / total) * 100

print(f"\n🔎 Found {zeros_unit} records with 'Unit' equal to 0 ({percentage:.2f}%).")

# ✅ Fix if proportion is < 20%
if percentage < 20:
    print("✅ Replacing 'Unit' values based on the mean per exporting country...")

    # Create a copy column
    df_reduced["Unit_adjusted"] = df_reduced["Unit"]

    # Compute mean per country excluding zeros
    country_means = df_reduced[df_reduced["Unit"] > 0].groupby("Exporting_Country")["Unit"].mean()

    # Replacement function
    def replace_zero(row):
        if row["Unit_adjusted"] == 0:
            return country_means[row["Exporting_Country"]]
        return row["Unit_adjusted"]

    # Apply replacement
    df_reduced["Unit_adjusted"] = df_reduced.apply(replace_zero, axis=1)
    print("✅ Replacement completed.")
else:
    print("⚠️ Proportion of zeros in 'Unit' is above the limit. No replacement applied.")

# Check for duplicate rows
duplicates = df_reduced.duplicated().sum()
print(f"🔍 Total duplicate rows: {duplicates}")

# Display duplicates before removal
print(df_reduced[df_reduced.duplicated()])

# Drop duplicates keeping the first occurrence
df_cleaned = df_reduced.drop_duplicates()
print("✅ Duplicates successfully removed!")

# Save cleaned DataFrame to CSV
df_cleaned.to_csv("C:/Users/pedro/OneDrive/Área de Trabalho/Códigos/Exploratory_Data_Analysis/clean_data_soyUNComtrade.csv", index=False)
print("✅ File saved successfully!")
