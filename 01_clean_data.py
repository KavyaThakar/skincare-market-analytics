import pandas as pd

df = pd.read_csv("cosmetics_raw.csv", encoding="utf-8-sig")

print("RAW SHAPE:", df.shape)
print(df.isnull().sum())
print("Duplicates:", df.duplicated().sum())

# Rename confusing columns
df.columns = [c.strip() for c in df.columns]
df = df.rename(columns={"Label": "Category", "Rank": "Rating"})

# Remove duplicate products
df = df.drop_duplicates(subset=["Brand", "Name", "Category"]).reset_index(drop=True)

# Clean text fields
for col in ["Category", "Brand", "Name"]:
    df[col] = df[col].astype(str).str.strip()

# Enforce numeric types
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

# Rating = 0 means "not yet rated" in this dataset, not a real 0-star score.
# Drop those rows so they don't drag down category/brand averages.
zero_rating_count = (df["Rating"] == 0).sum()
print(f"Dropping {zero_rating_count} rows with placeholder Rating = 0 (unrated products, not real 0-star ratings)")

df = df[(df["Price"] > 0) & (df["Rating"] > 0) & (df["Rating"] <= 5)]

# Turn the ingredients string into a real list + count
def parse_ingredients(text):
    if not isinstance(text, str) or text.strip() == "":
        return []
    return [p.strip() for p in text.rstrip(".").split(",") if p.strip()]

df["Ingredient_List"] = df["Ingredients"].apply(parse_ingredients)
df["Ingredient_Count"] = df["Ingredient_List"].apply(len)
df = df[df["Ingredient_Count"] > 0].reset_index(drop=True)

# How many skin types each product claims to suit
skin_cols = ["Combination", "Dry", "Normal", "Oily", "Sensitive"]
df["Skin_Types_Suited"] = df[skin_cols].sum(axis=1)

# Price tier buckets
df["Price_Tier"] = pd.cut(
    df["Price"], bins=[0, 25, 50, 100, 1000],
    labels=["Budget (<$25)", "Mid ($25-50)", "Premium ($50-100)", "Luxury ($100+)"]
)

print("\nCLEANED SHAPE:", df.shape)
df.to_csv("cosmetics_clean.csv", index=False)

# Long-format table: one row per (product, ingredient) — needed for ingredient frequency analysis
rows = []
for _, r in df.iterrows():
    for ing in r["Ingredient_List"]:
        rows.append((r["Brand"], r["Name"], r["Category"], ing))
pd.DataFrame(rows, columns=["Brand", "Name", "Category", "Ingredient"]).to_csv("ingredients_long.csv", index=False)

print("Saved cosmetics_clean.csv and ingredients_long.csv")