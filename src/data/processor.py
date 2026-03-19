import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.data.db import get_connection
from src.data.weather_api import get_weather

def engine_match_context(matches):
    """
    Simulates bringing in weather and venue size for Match Context Engine.
    """
    venue_sizes = {
        'Wankhede': 'Small',
        'Eden Gardens': 'Medium',
        'Chinnaswamy': 'Small',
        'Chepauk': 'Large',
        'Narendra Modi Stadium': 'Large'
    }
    
    matches['venue_size'] = matches['venue'].map(venue_sizes).fillna('Medium')
    matches['toss_advantage'] = (matches['toss_winner'] == matches['team1']).astype(int)
    
    # We will simulate weather for historical matches based on random probability for demo purposes
    # In live scenario, this would use get_weather(venue) on match day
    np.random.seed(42)
    matches['weather_condition'] = np.random.choice(['Clear', 'Cloudy', 'Rain Probable'], len(matches), p=[0.7, 0.2, 0.1])
    
    return matches

def calculate_team_venue_win_rate(matches):
    """
    Calculates historical win rate of a team at a specific venue.
    """
    # Simply grouping by venue and counting wins
    venue_wins = matches.groupby(['venue', 'winner']).size().unstack(fill_value=0)
    
    def get_venue_win_rate(venue, team):
        if venue in venue_wins.index and team in venue_wins.columns:
            team_wins = venue_wins.loc[venue, team]
            total_matches = matches[matches['venue'] == venue].shape[0]
            return team_wins / total_matches if total_matches > 0 else 0.0
        return 0.0
        
    matches['team1_venue_win_rate'] = matches.apply(lambda x: get_venue_win_rate(x['venue'], x['team1']), axis=1)
    matches['team2_venue_win_rate'] = matches.apply(lambda x: get_venue_win_rate(x['venue'], x['team2']), axis=1)
    return matches

def encode_categorical_features(matches):
    """
    Encodes pitch, venue size, and weather.
    """
    dummies = pd.get_dummies(matches[['pitch_type', 'venue_size', 'weather_condition']], prefix=['pitch', 'venue', 'weather'])
    return pd.concat([matches, dummies], axis=1), list(dummies.columns)

def engineer_features():
    print("Connecting to DB and loading data...")
    conn = get_connection()
    matches = pd.read_sql_query("SELECT * FROM matches", conn)
    players = pd.read_sql_query("SELECT * FROM players", conn)
    conn.close()

    print("Performing Player Analysis...")
    # Calculate team aggregates based on player micro-stats
    team_stats = players.groupby('team').agg({
        'form_score': 'mean',
        'pp_strike_rate': 'mean',
        'boundary_percentage': 'mean',
        'impact_score': 'sum'
    }).reset_index()
    
    matches = matches.merge(team_stats, left_on='team1', right_on='team', how='left').rename(columns={
        'form_score': 'team1_form',
        'pp_strike_rate': 'team1_pp_sr',
        'boundary_percentage': 'team1_boundary_pct',
        'impact_score': 'team1_impact'
    }).drop('team', axis=1)
    
    matches = matches.merge(team_stats, left_on='team2', right_on='team', how='left').rename(columns={
        'form_score': 'team2_form',
        'pp_strike_rate': 'team2_pp_sr',
        'boundary_percentage': 'team2_boundary_pct',
        'impact_score': 'team2_impact'
    }).drop('team', axis=1)

    print("Performing Match Context Analysis...")
    matches = engine_match_context(matches)
    matches = calculate_team_venue_win_rate(matches)
    
    # Base overall win rate
    team_wins = matches['winner'].value_counts().to_dict()
    team_total_matches = matches['team1'].value_counts().add(matches['team2'].value_counts(), fill_value=0).to_dict()
    team_overall_win_rate = {team: team_wins.get(team, 0) / team_total_matches.get(team, 1) for team in team_total_matches}
    
    matches['team1_win_rate'] = matches['team1'].map(team_overall_win_rate)
    matches['team2_win_rate'] = matches['team2'].map(team_overall_win_rate)
    
    # Target Variable: 1 if team1 wins, 0 if team2 wins
    matches['target'] = (matches['winner'] == matches['team1']).astype(int)
    
    print("Encoding features...")
    matches, dummy_cols = encode_categorical_features(matches)
    
    features = [
        'team1_win_rate', 'team2_win_rate', 
        'team1_form', 'team2_form',
        'team1_pp_sr', 'team2_pp_sr',
        'team1_boundary_pct', 'team2_boundary_pct',
        'team1_impact', 'team2_impact',
        'team1_venue_win_rate', 'team2_venue_win_rate',
        'toss_advantage'
    ] + dummy_cols
    
    df_processed = matches[features + ['target', 'team1', 'team2', 'venue']]
    df_processed = df_processed.fillna(0)
    
    os.makedirs('data/processed', exist_ok=True)
    df_processed.to_csv('data/processed/model_data.csv', index=False)
    
    # Save a copy of team aggregated player stats for real-time inference
    team_stats.to_csv('data/processed/team_stats_aggregated.csv', index=False)
    
    print(f"Feature engineering complete. {df_processed.shape[1]} features created.")
    print("Data saved to data/processed/model_data.csv")

if __name__ == '__main__':
    engineer_features()
