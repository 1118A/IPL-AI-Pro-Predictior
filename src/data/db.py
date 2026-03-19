import sqlite3
import os
import pandas as pd
import sys

# Ensure it works when run directly or imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import DB_PATH

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Matches Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id TEXT PRIMARY KEY,
            date TEXT,
            venue TEXT,
            team1 TEXT,
            team2 TEXT,
            toss_winner TEXT,
            winner TEXT,
            pitch_type TEXT
        )
    ''')
    
    # Players Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_id TEXT PRIMARY KEY,
            name TEXT,
            team TEXT,
            role TEXT,
            matches_played INTEGER,
            form_score REAL,
            pp_strike_rate REAL,
            boundary_percentage REAL,
            impact_score REAL
        )
    ''')
    
    conn.commit()
    conn.close()

def save_matches_to_db(df):
    conn = get_connection()
    df.to_sql('matches', conn, if_exists='replace', index=False)
    conn.close()

def save_players_to_db(df):
    conn = get_connection()
    df.to_sql('players', conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
