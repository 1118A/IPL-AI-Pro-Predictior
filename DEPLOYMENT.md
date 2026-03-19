# Deploying IPL AI Strategy Engine to Streamlit Community Cloud

Streamlit Community Cloud is the best way to host this IPL Predictor completely for free. Since your app relies on pre-trained ML models and a built SQLite database, you need to ensure these files are uploaded to GitHub correctly.

Follow these exact steps:

### Step 1: Prepare Your Git Repository
Before deploying, you must push your local code, database, and machine learning models to a **public GitHub repository**. 
*(Note: Streamlit Community Cloud allows free private repos if you only deploy 1 app, but public is easiest).*

Run these commands in your terminal (`d:\Code\ipl_predictor`):
```bash
git init
git add .
git commit -m "Initial commit of V3 IPL Predictor with ML tools"
git branch -M main
# Create a Github repo online, then paste your remote URL here:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```
**CRITICAL:** Ensure the `data/predictor.db`, `data/processed/*.csv`, and `models/saved_models/win_model.pkl` files are properly pushed! Your cloud dashboard will crash if the pre-trained data isn't uploaded.

### Step 2: Connect Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **"New app"**.
3. Fill in the deployment form:
   - **Repository:** `YOUR_USERNAME/YOUR_REPO_NAME`
   - **Branch:** `main`
   - **Main file path:** `src/app/dashboard.py`
4. **DO NOT CLICK DEPLOY YET!** Proceed to Step 3.

### Step 3: Secure Your API Keys (Advanced Settings)
Since your GitHub repository might be public, **do not** ever push your raw API keys in code (we use placeholders locally). Streamlit handles this via **Secrets**.

1. Before clicking deploy, click on **"Advanced settings..."** (the blue gear icon).
2. Look for the **Secrets** text box.
3. Paste your live API keys exactly like this:
```toml
CRIC_API_KEY = "a6177fed-ecff-44e0-8e3a-2c1af4efad0c"
WEATHER_API_KEY = "dummy_weather_api_key"
```
4. Click **Save**, and then click **Deploy**!

### Success!
Your app will spin up a server, install `requirements.txt`, and launch your premium Glassmorphism Interface to the global internet! 

**Handling Daily Updates in the Cloud:**
Streamlit Community Cloud spins down when no one is using it. Since you cannot run cron-jobs directly on their frontend server, to update the prediction model every day, you should run `python src/automation/updater.py` **locally** on your computer each morning, and then simply run `git commit -am "Daily update" && git push`. Streamlit Cloud will automatically refresh the app with the new database limits instantly!
