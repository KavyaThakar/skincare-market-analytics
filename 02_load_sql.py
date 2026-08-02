import pandas as pd
import sqlite3

df = pd.read_csv("cosmetics_clean.csv")
ing = pd.read_csv("ingredients_long.csv")

df_sql = df.drop(columns=["Ingredient_List", "Ingredients"])

conn = sqlite3.connect("skincare.db")
df_sql.to_sql("products", conn, if_exists="replace", index=False)
ing.to_sql("ingredients", conn, if_exists="replace", index=False)

cur = conn.cursor()
cur.execute("CREATE INDEX idx_products_category ON products(Category);")
cur.execute("CREATE INDEX idx_ingredients_name ON ingredients(Ingredient);")
conn.commit()

for t in ["products", "ingredients"]:
    n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t}: {n} rows")

conn.close()