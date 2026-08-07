import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from ml_pipeline import SkincareMLPipeline

# Page Configuration
st.set_page_config(
    page_title="Skincare Intelligence | AI/ML Market Analytics & Recommender",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Sleek Dark Glassmorphism Styling
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f1117 0%, #171b26 50%, #0f1117 100%);
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Styling */
    .main-title {
        background: linear-gradient(90deg, #f472b6, #c084fc, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 1.8rem;
    }

    /* Card Styling */
    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        margin-bottom: 15px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .glass-card:hover {
        border-color: rgba(244, 114, 182, 0.4);
    }

    /* Metric Badges */
    .badge-match {
        background: linear-gradient(135deg, #ec4899, #8b5cf6);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        display: inline-block;
    }
    .badge-tag {
        background: rgba(51, 65, 85, 0.7);
        color: #cbd5e1;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        margin-right: 6px;
        display: inline-block;
    }

    /* Benefit & Sensitivity Badges */
    .benefit-item {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #6ee7b7;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 6px;
    }
    .sensitivity-item {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: #fca5a5;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize ML Pipeline with caching
@st.cache_resource
def get_pipeline():
    return SkincareMLPipeline()

try:
    pipeline = get_pipeline()
    df = pipeline.df
except Exception as e:
    st.error(f"Error loading data pipeline: {e}")
    st.stop()

# Header Section
st.markdown('<div class="main-title">Skincare Intelligence AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-Powered Recommendation Engine, Formula Safety Scanner & Market Value Predictor</div>', unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.image("https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&q=80", use_container_width=True)
st.sidebar.title("🎛️ App Controls")
st.sidebar.info("Dataset: 1,472 Sephora Products | 116 Top Brands | 6 Categories")

# Main Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🌟 AI Matcher & Recommender", 
    "💰 ML Price & Value Predictor", 
    "🧪 Ingredient Scanner", 
    "📊 Market Analytics Dashboard"
])

# ----------------------------------------------------
# TAB 1: AI RECOMMENDER
# ----------------------------------------------------
with tab1:
    st.subheader("Find Your Perfect Skincare Match")
    st.write("Our content-based recommendation model analyzes formula compositions, ingredient similarity, and skin-type suitability.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Skin Profile & Preferences")
        
        category = st.selectbox("Category", ["All"] + sorted(list(df["Category"].unique())))
        
        st.write("**Skin Type Compatibility:**")
        skin_types = []
        c_combo = st.checkbox("Combination Skin", value=True)
        c_dry = st.checkbox("Dry Skin", value=False)
        c_norm = st.checkbox("Normal Skin", value=False)
        c_oily = st.checkbox("Oily Skin", value=False)
        c_sens = st.checkbox("Sensitive Skin", value=True)
        
        if c_combo: skin_types.append("Combination")
        if c_dry: skin_types.append("Dry")
        if c_norm: skin_types.append("Normal")
        if c_oily: skin_types.append("Oily")
        if c_sens: skin_types.append("Sensitive")
        
        max_price = st.slider("Max Budget ($)", min_value=10, max_value=300, value=75, step=5)
        min_rating = st.slider("Minimum Rating", min_value=1.0, max_value=5.0, value=4.0, step=0.1)
        
        inc_ing = st.text_input("Preferred Key Ingredients (e.g. Niacinamide, Hyaluronic Acid)", "")
        exc_ing = st.text_input("Ingredients to Avoid (e.g. Fragrance, Alcohol, Parabens)", "")
        
        num_results = st.number_input("Number of Recommendations", min_value=3, max_value=20, value=6)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        recs = pipeline.recommend(
            category=category,
            skin_types=skin_types,
            max_price=max_price,
            min_rating=min_rating,
            include_ingredients=inc_ing,
            avoid_ingredients=exc_ing,
            top_n=num_results
        )
        
        if recs.empty:
            st.warning("No products matched your exact filter criteria. Try relaxing your budget or ingredient exclusions.")
        else:
            st.success(f"Found {len(recs)} Top Matched Products")
            
            for _, item in recs.iterrows():
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span class="badge-tag">{item['Brand']}</span>
                            <span class="badge-tag">{item['Category']}</span>
                            <h3 style="margin: 6px 0; font-size:1.2rem;">{item['Name']}</h3>
                        </div>
                        <div>
                            <span class="badge-match">{item['Match_Score']}% Match</span>
                        </div>
                    </div>
                    <div style="margin-top:10px; display:flex; gap:15px; color:#cbd5e1; font-size:0.95rem;">
                        <span>💰 Price: <b>${item['Price']:.2f}</b></span>
                        <span>⭐ Rating: <b>{item['Rating']:.1f} / 5.0</b></span>
                        <span>🧪 Ingredients Count: <b>{item['Ingredient_Count']}</b></span>
                    </div>
                    <div style="margin-top:10px; font-size:0.85rem; color:#94a3b8; line-height:1.4;">
                        <b>Ingredients preview:</b> {item['Ingredients'][:140]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ----------------------------------------------------
# TAB 2: ML PRICE & VALUE PREDICTOR
# ----------------------------------------------------
with tab2:
    st.subheader("ML Formula Value Estimator")
    st.write("Predict expected market price and evaluate formula value using our trained Random Forest Regressor.")
    
    val_col1, val_col2 = st.columns([1, 1])
    
    with val_col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Product Parameters")
        
        v_cat = st.selectbox("Product Category", sorted(list(df["Category"].unique())), key="v_cat")
        v_ing_count = st.number_input("Formula Ingredient Count", min_value=1, max_value=120, value=30)
        
        st.write("Suitable Skin Types:")
        v_combo = st.checkbox("Combination", value=True, key="v1")
        v_dry = st.checkbox("Dry", value=True, key="v2")
        v_norm = st.checkbox("Normal", value=True, key="v3")
        v_oily = st.checkbox("Oily", value=False, key="v4")
        v_sens = st.checkbox("Sensitive", value=False, key="v5")
        
        v_actual_price = st.number_input("Actual Retail Price ($) [Optional]", min_value=0.0, max_value=500.0, value=45.0)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with val_col2:
        pred_price, value_rating = pipeline.predict_price_and_value(
            category=v_cat,
            ingredient_count=v_ing_count,
            combination=int(v_combo),
            dry=int(v_dry),
            normal=int(v_norm),
            oily=int(v_oily),
            sensitive=int(v_sens),
            actual_price=v_actual_price
        )
        
        st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("### 🤖 ML Valuation Result")
        st.metric(label="Predicted Fair Market Price", value=f"${pred_price:.2f}", delta=f"${v_actual_price - pred_price:.2f} difference" if v_actual_price else None)
        
        st.markdown(f"#### Value Status: **{value_rating}**")
        st.write(f"Based on **{v_cat}** formula with **{v_ing_count} ingredients** across **{sum([v_combo, v_dry, v_norm, v_oily, v_sens])} skin types**.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Gauge Chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = pred_price,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Predicted Fair Price ($)", 'font': {'size': 18, 'color': '#e2e8f0'}},
            gauge = {
                'axis': {'range': [None, 150], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
                'bar': {'color': "#ec4899"},
                'bgcolor': "rgba(30, 41, 59, 0.5)",
                'bordercolor': "#475569",
                'steps': [
                    {'range': [0, 25], 'color': '#065f46'},
                    {'range': [25, 60], 'color': '#1e3a8a'},
                    {'range': [60, 150], 'color': '#701a75'}
                ]
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#e2e8f0"}, height=280)
        st.plotly_chart(fig_gauge, use_container_width=True)

# ----------------------------------------------------
# TAB 3: INGREDIENT SCANNER
# ----------------------------------------------------
with tab3:
    st.subheader("AI Ingredient Safety & Formula Scanner")
    st.write("Scan product formulations for active dermatological benefits and potential reactive irritants.")
    
    scan_option = st.radio("Scanner Mode", ["Select Existing Product", "Custom Formula Input"])
    
    if scan_option == "Select Existing Product":
        selected_prod = st.selectbox("Choose Product", df["Brand"] + " - " + df["Name"])
        idx = (df["Brand"] + " - " + df["Name"]) == selected_prod
        prod_row = df[idx].iloc[0]
        ing_text = prod_row["Ingredients"]
        st.info(f"**Category:** {prod_row['Category']} | **Price:** ${prod_row['Price']} | **Rating:** {prod_row['Rating']} ⭐")
    else:
        ing_text = st.text_area("Paste Ingredient List", "Water, Glycerin, Niacinamide, Hyaluronic Acid, Salicylic Acid, Fragrance, Alcohol Denat, Phenoxyethanol")
        
    benefits, sensitivities = pipeline.analyze_ingredients(ing_text)
    
    b_col, s_col = st.columns(2)
    
    with b_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"### ✨ Key Beneficial Actives ({len(benefits)})")
        if benefits:
            for b in benefits:
                st.markdown(f'<div class="benefit-item"><b>{b["ingredient"]}:</b> {b["benefit"]}</div>', unsafe_allow_html=True)
        else:
            st.write("No major key active compounds detected.")
        st.markdown('</div>', unsafe_allow_html=True)

    with s_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"### ⚠️ Sensitivity & Irritant Flags ({len(sensitivities)})")
        if sensitivities:
            for s in sensitivities:
                st.markdown(f'<div class="sensitivity-item"><b>{s["ingredient"]}:</b> {s["flag"]}</div>', unsafe_allow_html=True)
        else:
            st.success("Clean formula! No common fragrance/alcohol sensitivity flags detected.")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------
# TAB 4: MARKET ANALYTICS DASHBOARD
# ----------------------------------------------------
with tab4:
    st.subheader("Skincare Market Analytics Dashboard")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Products", f"{len(df):,}")
    kpi2.metric("Total Brands", f"{df['Brand'].nunique():,}")
    kpi3.metric("Average Price", f"${df['Price'].mean():.2f}")
    kpi4.metric("Average Rating", f"{df['Rating'].mean():.2f} ⭐")
    
    m_col1, m_col2 = st.columns(2)
    
    with m_col1:
        # Scatter Plot: Price vs Rating
        fig_scatter = px.scatter(
            df, x="Price", y="Rating", color="Category", 
            hover_data=["Brand", "Name"],
            title="Price vs. Rating Distribution (by Category)",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with m_col2:
        # Category Price vs Rating
        cat_agg = df.groupby("Category").agg({"Price": "mean", "Rating": "mean"}).reset_index()
        fig_bar = px.bar(
            cat_agg, x="Category", y="Price", color="Rating",
            title="Average Price ($) and Rating by Category",
            template="plotly_dark",
            color_continuous_scale="Viridis"
        )
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

    # Top Brands
    top_b = df["Brand"].value_counts().head(10).reset_index()
    top_b.columns = ["Brand", "Product Count"]
    fig_brand = px.bar(
        top_b, x="Product Count", y="Brand", orientation="h",
        title="Top 10 Brands by Catalog Volume",
        template="plotly_dark",
        color="Product Count",
        color_continuous_scale="Purples"
    )
    fig_brand.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_brand, use_container_width=True)
