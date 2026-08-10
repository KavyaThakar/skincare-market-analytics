# Skincare Intelligence | AI/ML Analytics & Recommendation System 

A comprehensive data analytics and AI/ML system built on a 1,472-product Sephora skincare dataset. Features an **AI-powered Content-based Recommender**, **Random Forest Price Value Regressor**, **Formula Safety Scanner**, and **Interactive Streamlit Web Application**.

## 🚀 Live Project

🔗 **[View Live Project](https://kavyathakar-skincare-market-analytics-app-jba1bb.streamlit.app/)**

---

## 🌟 Key Features

1. **AI Product Matcher & Recommendation Engine**
   - Content-based vector similarity matching using TF-IDF and Cosine Similarity on product ingredients.
   - Filters products by category, max budget, skin type compatibility (Dry, Oily, Sensitive, Combination, Normal), liked ingredients, and avoided sensitivities (Fragrance, Alcohol, Parabens).

2. **ML Formula Price & Value Estimator**
   - Trained `RandomForestRegressor` predicting fair market prices based on product category, ingredient complexity, and skin type suitability.
   - Evaluates product value ("Outstanding Bargain", "Fair Price", "Premium Luxury Price").

3. **AI Ingredient Safety & Formula Scanner**
   - Deep-scans product formulation strings to identify active dermatological compounds (Niacinamide, Hyaluronic Acid, Salicylic Acid, Retinol) and flags common skin irritants/allergens.

4. **Live Market Analytics Dashboard**
   - Interactive Plotly charts analyzing price vs. rating distributions, category price benchmarks, and top brand catalog distributions.

---

## 🚀 How to Run Locally

### Prerequisites
Make sure Python 3.9+ is installed. Install required packages:

```bash
pip install -r requirements.txt
```

### 1. Data Cleaning & Model Setup
Run the processing scripts:

```bash
py 01_clean_data.py
py ml_pipeline.py
```

### 2. Launch the Streamlit Web Application

```bash
py -m streamlit run app.py
```

The web app will open automatically in your browser at `http://localhost:8501`.

---

## ☁️ Cloud Deployment Guide (How to Make it Live)

### Option A: Streamlit Community Cloud (Recommended — Free & 1-Click)

1. **Push Code to GitHub**:
   ```bash
   git add .
   git commit -m "Add AI/ML pipeline, Streamlit app, and deployment files"
   git push origin main
   ```
2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
   - Click **New App**.
   - Select your repository (`skincare-market-analytics`), branch (`main`), and set Main file path to `app.py`.
   - Click **Deploy**! Your app will be live with a shareable URL in under 2 minutes.

---

### Option B: Hugging Face Spaces (Free Cloud Hosting)

1. Create a new Space on [Hugging Face Spaces](https://huggingface.co/spaces).
2. Select **Streamlit** as the Space SDK.
3. Push or upload your repository files (`app.py`, `ml_pipeline.py`, `cosmetics_clean.csv`, `requirements.txt`, `.streamlit/config.toml`).
4. Hugging Face will automatically build and host your live interactive AI web app.

---

### Option C: Docker Cloud Hosting (Render / GCP / AWS)

Use the included `Dockerfile` to build and deploy to any container platform:

```bash
docker build -t skincare-ai-app .
docker run -p 8501:8501 skincare-ai-app
```

---

## 📁 Repository Structure

```
├── app.py                      # Main Streamlit Web Application
├── ml_pipeline.py              # ML Engine (Recommender, Regressor, Scanner)
├── 01_clean_data.py            # Data cleaning pipeline
├── 02_load_sql.py              # Loads clean data into SQLite database
├── 03_run_queries.py           # Executes SQL analytical queries
├── 04_visualize.py             # Generates static Matplotlib/Seaborn charts
├── cosmetics_clean.csv         # Cleaned dataset (1,472 products)
├── ingredients_long.csv        # Exploded ingredient-product relational table
├── requirements.txt            # Python dependencies for app & ML
├── Dockerfile                  # Container deployment configuration
└── .streamlit/
    └── config.toml             # Streamlit custom theme configuration
```
