import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.data.cricket_api import fetch_recent_matches, fetch_squads
from src.data.scraper import scrape_player_microstats
from src.data.db import save_matches_to_db, save_players_to_db, init_db

def sync_data_pipeline():
    """
    Orchestrates the fetching of matches and players from APIs
    and saves them into the SQLite database.
    """
    print("Initialize Database if not exists...")
    init_db()

    print("Fetching IPL Match Data (Past 2 Years)...")
    matches_data = fetch_recent_matches()
    df_matches = pd.DataFrame(matches_data)
    
    print("Fetching IPL Squads Data...")
    players_data = fetch_squads()
    
    # Optional enhancement: We can intertwine the scraper to enhance players missing boundary_%
    # E.g., for key players, we could call scrape_player_microstats(player['name'])
    print("Scraping advanced micro-stats for players...")
    for idx, p in enumerate(players_data):
        if idx % 20 == 0:
            print(f"  Scraping stats for {p['name']} ({idx}/{len(players_data)})")
        stats = scrape_player_microstats(p['name'])
        # If the API returned empty placeholders for these, overwrite them with Scraper
        p['pp_strike_rate'] = stats.get('pp_strike_rate', p.get('pp_strike_rate', 0.0))
        p['boundary_percentage'] = stats.get('boundary_percentage', p.get('boundary_percentage', 0.0))
    
    df_players = pd.DataFrame(players_data)
    
    print("Saving Data to SQLite Database...")
    save_matches_to_db(df_matches)
    save_players_to_db(df_players)
    
    print("Data synchronization complete!")

if __name__ == "__main__":
    sync_data_pipeline()
