import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle
import os

# Dictionary of active ingredient benefits & potential sensitivities
BENEFICIAL_INGREDIENTS = {
    "hyaluronic acid": "Hydration & Moisture retention",
    "sodium hyaluronate": "Deep skin hydration",
    "niacinamide": "Brightening, pore control & barrier repair",
    "salicylic acid": "BHA exfoliation & acne clearing",
    "glycolic acid": "AHA exfoliation & skin smoothing",
    "lactic acid": "Gentle AHA exfoliation",
    "retinol": "Anti-aging & cell turnover",
    "vitamin c": "Antioxidant & collagen synthesis",
    "ascorbic acid": "Pure Vitamin C brightening",
    "ceramide": "Skin barrier restoration",
    "centella asiatica": "Soothing & anti-redness",
    "squalane": "Non-greasy moisture nourishment",
    "tocopherol": "Vitamin E antioxidant protection",
    "panthenol": "Pro-vitamin B5 skin calming",
    "peptide": "Firming & elasticity support",
    "tea tree": "Anti-bacterial acne treatment",
    "green tea": "Antioxidant soothing",
    "aloe": "Soothing hydration"
}

SENSITIVITY_FLAGS = {
    "fragrance": "Added fragrance — potential allergen for sensitive skin",
    "parfum": "Perfume/Fragrance component",
    "alcohol denat": "Drying alcohol",
    "denatured alcohol": "Drying alcohol",
    "essential oil": "Concentrated aromatic oil — potential reactive trigger",
    "limonene": "Fragrance allergen component",
    "linalool": "Fragrance allergen component",
    "citronellol": "Fragrance allergen component",
    "sodium lauryl sulfate": "Harsh surfactant (SLS)",
    "paraben": "Preservative"
}

class SkincareMLPipeline:
    def __init__(self, data_path="cosmetics_clean.csv"):
        self.data_path = data_path
        self.df = None
        self.tfidf = None
        self.tfidf_matrix = None
        self.price_model = None
        self.load_data()
        self.build_recommender()
        self.build_price_model()

    def load_data(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"{self.data_path} not found. Run 01_clean_data.py first.")
        self.df = pd.read_csv(self.data_path)
        # Ensure ingredients string is clean
        self.df["Ingredients"] = self.df["Ingredients"].fillna("").astype(str)

    def build_recommender(self):
        # Build TF-IDF matrix on raw ingredient text
        self.tfidf = TfidfVectorizer(max_features=1000, stop_words="english", token_pattern=r"(?u)\b[\w-]+\b")
        self.tfidf_matrix = self.tfidf.fit_transform(self.df["Ingredients"])

    def recommend(self, category=None, skin_types=None, max_price=None, min_rating=0.0, 
                  include_ingredients=None, avoid_ingredients=None, top_n=10):
        """
        Content-based recommendation engine incorporating ingredient similarity,
        skin-type suitability weights, price/rating constraints, and preference keywords.
        """
        filtered_df = self.df.copy()
        
        # Category Filter
        if category and category != "All":
            filtered_df = filtered_df[filtered_df["Category"] == category]
            
        # Price Filter
        if max_price is not None:
            filtered_df = filtered_df[filtered_df["Price"] <= max_price]
            
        # Rating Filter
        if min_rating > 0:
            filtered_df = filtered_df[filtered_df["Rating"] >= min_rating]

        # Skin Type Compatibility Filtering
        if skin_types:
            for st in skin_types:
                if st in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df[st] == 1]

        # Ingredient Exclusion Filter
        if avoid_ingredients:
            avoid_list = [ing.strip().lower() for ing in avoid_ingredients.split(",") if ing.strip()]
            for avoid in avoid_list:
                filtered_df = filtered_df[~filtered_df["Ingredients"].str.lower().str.contains(avoid, regex=False)]

        if filtered_df.empty:
            return pd.DataFrame()

        # Build query profile vector
        query_text = ""
        if include_ingredients:
            query_text += " " + include_ingredients
        if category and category != "All":
            query_text += " " + category

        indices = filtered_df.index
        sub_tfidf = self.tfidf_matrix[indices]

        if query_text.strip():
            query_vec = self.tfidf.transform([query_text])
            sim_scores = cosine_similarity(query_vec, sub_tfidf).flatten()
        else:
            # Default weighting: high ratings get slight boost
            sim_scores = sub_tfidf.mean(axis=1).A1 + (filtered_df["Rating"].values / 5.0) * 0.2

        filtered_df = filtered_df.copy()
        # Scale score between 0 and 100%
        if sim_scores.max() > sim_scores.min():
            norm_scores = (sim_scores - sim_scores.min()) / (sim_scores.max() - sim_scores.min() + 1e-6)
        else:
            norm_scores = np.ones_like(sim_scores)
            
        # Add skin suitability boost if multiple matched
        if skin_types:
            skin_boost = filtered_df[skin_types].sum(axis=1).values / len(skin_types)
            final_scores = 0.7 * norm_scores + 0.3 * skin_boost
        else:
            final_scores = norm_scores

        filtered_df["Match_Score"] = (final_scores * 100).round(1)
        results = filtered_df.sort_values(by=["Match_Score", "Rating", "Price"], ascending=[False, False, True])
        return results.head(top_n)

    def build_price_model(self):
        """Trains a Random Forest Regressor to predict estimated price based on formula features."""
        X = self.df[["Category", "Ingredient_Count", "Combination", "Dry", "Normal", "Oily", "Sensitive", "Skin_Types_Suited"]]
        y = self.df["Price"]

        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore"), ["Category"])
            ],
            remainder="passthrough"
        )

        self.price_model = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
        ])

        self.price_model.fit(X, y)

    def predict_price_and_value(self, category, ingredient_count, combination, dry, normal, oily, sensitive, actual_price=None):
        skin_types_suited = sum([combination, dry, normal, oily, sensitive])
        input_data = pd.DataFrame([{
            "Category": category,
            "Ingredient_Count": ingredient_count,
            "Combination": combination,
            "Dry": dry,
            "Normal": normal,
            "Oily": oily,
            "Sensitive": sensitive,
            "Skin_Types_Suited": skin_types_suited
        }])

        pred_price = float(self.price_model.predict(input_data)[0])

        value_rating = "Fair Market Price"
        if actual_price is not None:
            diff = actual_price - pred_price
            if diff < -15:
                value_rating = "💎 Outstanding Bargain (Underpriced)"
            elif diff < -5:
                value_rating = "👍 Great Value"
            elif diff > 20:
                value_rating = "👑 Premium Luxury Price (Overpriced)"
            elif diff > 5:
                value_rating = "💵 Above Average Price"

        return round(pred_price, 2), value_rating

    def analyze_ingredients(self, ingredient_text):
        """Scans ingredients string for key beneficial actives and sensitivity flags."""
        text_lower = ingredient_text.lower()
        found_benefits = []
        found_sensitivities = []

        for key, desc in BENEFICIAL_INGREDIENTS.items():
            if key in text_lower:
                found_benefits.append({"ingredient": key.title(), "benefit": desc})

        for key, desc in SENSITIVITY_FLAGS.items():
            if key in text_lower:
                found_sensitivities.append({"ingredient": key.title(), "flag": desc})

        return found_benefits, found_sensitivities

if __name__ == "__main__":
    pipeline = SkincareMLPipeline()
    print("[SUCCESS] ML Pipeline loaded successfully!")
    recs = pipeline.recommend(category="Moisturizer", skin_types=["Dry", "Sensitive"], top_n=3)
    print("\nSample Recommendations:")
    print(recs[["Name", "Brand", "Price", "Rating", "Match_Score"]])
