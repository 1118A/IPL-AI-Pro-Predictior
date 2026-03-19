import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.data.fetch_data import sync_data_pipeline
from src.data.processor import engineer_features
from src.model.train import train_win_predictor

def run_daily_update():
    print("=========================================")
    print("Starting IPL AI Automation Daily Pipeline")
    print("=========================================")
    
    print("\n[1/3] Syncing Real-Time Matches & Squads from API into SQLite...")
    try:
        sync_data_pipeline()
    except Exception as e:
        print(f"Error during Data Sync: {e}")
        
    print("\n[2/3] Processing advanced features (Player micro-stats & Match Context)...")
    try:
        engineer_features()
    except Exception as e:
        print(f"Error during Feature Engineering: {e}")
        
    print("\n[3/3] Training Win Probability ML Model & Promo Strategy Engine...")
    try:
        train_win_predictor()
    except Exception as e:
        print(f"Error during Model Training: {e}")
    
    print("\n=========================================")
    print("Daily Update and Automation Complete!")
    print("AI Agent is ready for latest predictions.")
    print("=========================================")

if __name__ == "__main__":
    run_daily_update()
