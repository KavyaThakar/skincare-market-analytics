# 🌐 Netlify Deployment Guide

This project is configured to run on **Netlify** using **Stlite** (Streamlit in Pyodide/WebAssembly). This allows the entire Streamlit app, Scikit-Learn ML pipeline, Pandas data processor, and Plotly charts to run 100% serverless in the client's browser with **zero backend server maintenance or cost**.

---

## 🚀 Deployment Methods

### Method 1: Git Integration (Recommended — Automated CI/CD)

1. **Commit and Push to GitHub**:
   ```bash
   git add index.html netlify.toml NETLIFY_DEPLOYMENT.md README.md
   git commit -m "Add Netlify deployment configuration powered by Stlite"
   git push origin main
   ```

2. **Connect to Netlify**:
   - Log in to your [Netlify Dashboard](https://app.netlify.com/).
   - Click **Add new site** → **Import an existing project**.
   - Choose **GitHub** and select your repository (`skincare-market-analytics`).

3. **Configure Build Settings**:
   - **Build command**: *(Leave blank — static site)*
   - **Publish directory**: `.` (or `./`)
   - Click **Deploy skincare-market-analytics**!

   Your site will be live at `https://<site-name>.netlify.app` within seconds! Every `git push` to `main` will automatically trigger a production deploy.

---

### Method 2: Netlify CLI Deployment (Direct from Command Line)

If you have Node.js installed, you can deploy directly from your terminal:

```bash
# 1. Install Netlify CLI globally or use npx
npx netlify-cli login

# 2. Initialize project (first time only)
npx netlify-cli init

# 3. Deploy to production
npx netlify-cli deploy --prod --dir=.
```

---

### Method 3: Drag-and-Drop (Netlify Drop — 30 Seconds)

1. Go to [app.netlify.com/drop](https://app.netlify.com/drop).
2. Drag and drop your project folder (`skincare-market-analytics`) into the upload area.
3. Netlify will instantly process `index.html`, `app.py`, `ml_pipeline.py`, `cosmetics_clean.csv`, and `netlify.toml` and issue a live URL!

---

## ⚡ How It Works Under the Hood

- `index.html` loads `@stlite/browser` from CDN.
- `stlite` downloads Pyodide (Python WebAssembly engine) into the user's browser.
- It automatically installs requirements: `pandas`, `numpy`, `scikit-learn`, `plotly`.
- It executes `app.py` and `ml_pipeline.py` using `cosmetics_clean.csv` directly in browser memory.
- `netlify.toml` sets appropriate HTTP headers and caching strategies for `.wasm` and `.csv` assets.
