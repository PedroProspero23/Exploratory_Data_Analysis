# 📦 Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 📥 Load the dataset
file_path = "C:/Users/pedro/OneDrive/Área de Trabalho/Códigos/Funcionários/salary_dataset_cleaning.csv"
df = pd.read_csv(file_path)

# 📊 Step 1 - Basic overview of the dataset
print("Shape of dataset:", df.shape)
print("\nMissing values per column:\n", df.isna().sum())
print("\nSummary statistics:\n", df.describe(include='all'))

# 📌 Step 2 - Handling missing values
# Fill missing Salary values using the average by Education level
df["Salary (R$)"] = df.groupby("Education")["Salary (R$)"].transform(
    lambda x: x.fillna(x.mean())
)

# Optional alternative (by Department)
# df["Salary (R$)"] = df.groupby("Department")["Salary (R$)"].transform(
#     lambda x: x.fillna(x.mean())
# )

# ✅ Verify missing values handled
print("\nMissing values after treatment:\n", df.isna().sum())

# 🚨 Step 3 - Detecting and treating outliers using IQR (Interquartile Range)
Q1 = df["Salary (R$)"].quantile(0.25)
Q3 = df["Salary (R$)"].quantile(0.75)
IQR = Q3 - Q1

# Define bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identify outliers
outliers = df[(df["Salary (R$)"] < lower_bound) | (df["Salary (R$)"] > upper_bound)]
print(f"\nNumber of outliers detected: {outliers.shape[0]}")

# Visualize boxplot
plt.figure(figsize=(8, 4))
sns.boxplot(x=df["Salary (R$)"])
plt.title("Salary Distribution with Outliers")
plt.show()

# ✂️ Remove outliers
df_cleaned = df[(df["Salary (R$)"] >= lower_bound) & (df["Salary (R$)"] <= upper_bound)]

# ✅ Summary of cleaned dataset
print("\nShape after removing outliers:", df_cleaned.shape)

# 📤 Save cleaned dataset
cleaned_path = "C:/Users/pedro/OneDrive/Área de Trabalho/Códigos/Funcionários/salary_dataset_cleaned_final.csv"
df_cleaned.to_csv(cleaned_path, index=False)
print("\nCleaned dataset saved at:", cleaned_path)
