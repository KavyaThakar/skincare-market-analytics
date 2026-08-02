# Skincare & Cosmetics Market Analytics

Data analytics project answering one question using a 1,472-product Sephora catalog: **does price actually predict product quality?**

## Overview

End-to-end pipeline: raw data → Python cleaning → SQL analysis → Python visualizations → Power BI dashboard.

- **Dataset**: 1,472 Sephora skincare products — brand, price, rating, full ingredient list, skin-type suitability, across 6 categories and 116 brands
- **Tools**: Python (pandas), SQLite/SQL, Matplotlib/Seaborn, Power BI
- **Type**: Personal portfolio project, built to practice the full analyst workflow end to end

## Key findings

1. **Price barely moves rating.** Average rating stays in a tight 4.0–4.2 band from budget (<$25) to luxury ($100+) products, despite an 11x price difference.
2. **Eye cream underperforms.** It's priced mid-pack but rated lowest of all six categories — worth flagging for further investigation.
3. **Formula complexity doesn't buy a better rating** — products with 50+ ingredients rate about the same as products with under 15.
4. **Data quality catch**: several products had `Rating = 0`, which turned out to mean "not yet rated" rather than a real zero-star score. These were identified and excluded from all rating-based analysis to avoid skewing category and brand averages.

## Project structure
skincare-market-analytics/
├── cosmetics_raw.csv raw source data
├── cosmetics_clean.csv cleaned data (output of 01)
├── ingredients_long.csv one row per product-ingredient pair (output of 01)
├── skincare.db SQLite database (output of 02)
├── 01_clean_data.py cleaning + data quality checks
├── 02_load_sql.py loads cleaned data into SQLite
├── 03_run_queries.py runs SQL analysis, prints insights
├── 04_visualize.py generates charts
├── queries.sql reference SQL (window functions, CTEs)
├── charts/ PNG chart outputs
└── skincare-market-analysis.pbix Power BI dashboard
## How to run
pip install pandas matplotlib seaborn
python 01_clean_data.py
python 02_load_sql.py
python 03_run_queries.py
python 04_visualize.py

Open `skincare-market-analysis.pbix` in Power BI Desktop for the interactive dashboard.

## SQL techniques used

See `queries.sql` for the full set. Includes:
- Window functions: `RANK()`, `DENSE_RANK()` partitioned by category
- CTEs for multi-step logic
- `GROUP BY` / `HAVING` with derived metrics

## Dashboard

Built in Power BI — two pages (Overview, Ingredients & Pricing), with category/brand/price-tier breakdowns, a price-vs-rating scatter plot, and interactive slicers.