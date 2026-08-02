import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110

df = pd.read_csv("cosmetics_clean.csv")
ing = pd.read_csv("ingredients_long.csv")

os.makedirs("charts", exist_ok=True)

# 1. Average price and rating by category
cat_summary = df.groupby("Category").agg(
    avg_price=("Price", "mean"), avg_rating=("Rating", "mean")
).reset_index().sort_values("avg_price", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.barplot(data=cat_summary, x="Category", y="avg_price", ax=axes[0], color="#9C3D52")
axes[0].set_title("Average price by category ($)")
axes[0].tick_params(axis='x', rotation=30)

sns.barplot(data=cat_summary, x="Category", y="avg_rating", ax=axes[1], color="#5F7A63")
axes[1].set_title("Average rating by category")
axes[1].set_ylim(3.5, 4.5)
axes[1].tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.savefig("charts/01_category_price_rating.png")
plt.show()

# 2. Rating by price tier — the "does price buy quality" chart
tier_order = ["Budget (<$25)", "Mid ($25-50)", "Premium ($50-100)", "Luxury ($100+)"]
tier_summary = df.groupby("Price_Tier", observed=True)["Rating"].mean().reindex(tier_order)

plt.figure(figsize=(7, 5))
sns.barplot(x=tier_summary.index, y=tier_summary.values, color="#9C3D52")
plt.title("Average rating by price tier")
plt.ylim(3.8, 4.3)
plt.ylabel("Average rating")
plt.xlabel("")
plt.tight_layout()
plt.savefig("charts/02_price_tier_rating.png")
plt.show()

# 3. Top 10 brands by product count
top_brands = df["Brand"].value_counts().head(10)

plt.figure(figsize=(8, 6))
sns.barplot(x=top_brands.values, y=top_brands.index, color="#B8934F")
plt.title("Top 10 brands by product count")
plt.xlabel("Number of products")
plt.tight_layout()
plt.savefig("charts/03_top_brands.png")
plt.show()

# 4. Top 15 most common ingredients
top_ing = ing["Ingredient"].value_counts().head(15)

plt.figure(figsize=(8, 7))
sns.barplot(x=top_ing.values, y=top_ing.index, color="#5F7A63")
plt.title("Top 15 most common ingredients")
plt.xlabel("Number of products containing it")
plt.tight_layout()
plt.savefig("charts/04_top_ingredients.png")
plt.show()

# 5. Price vs rating scatter, colored by category — shows there's no clean trend
plt.figure(figsize=(9, 6))
sns.scatterplot(data=df, x="Price", y="Rating", hue="Category", alpha=0.6, s=40)
plt.title("Price vs rating (every product, colored by category)")
plt.tight_layout()
plt.savefig("charts/05_price_vs_rating.png")
plt.show()

print("Saved 5 charts to the 'charts' folder.")