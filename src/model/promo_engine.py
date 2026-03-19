import pandas as pd
import numpy as np

class PromoEngine:
    def __init__(self):
        try:
            self.team_stats = pd.read_csv('data/processed/team_stats_aggregated.csv')
            self.is_loaded = True
        except Exception as e:
            self.is_loaded = False
            self.team_stats = None
            print(f"Warning: Team stats missing for Promo Engine: {e}")

    def get_team_stats(self, team):
        if self.is_loaded and team in self.team_stats['team'].values:
            return self.team_stats[self.team_stats['team'] == team].iloc[0]
        else:
            return pd.Series({
                'team': team,
                'form_score': 50.0,
                'pp_strike_rate': 130.0,
                'boundary_percentage': 35.0,
                'impact_score': 5.0
            })

    def eval_first_over_aggression(self, teamA, teamB, pitch_type):
        """
        Predicts probability of an aggressive start / first over six
        based on PP Strike Rate & Pitch conditions.
        """
        stats_A = self.get_team_stats(teamA)
        stats_B = self.get_team_stats(teamB)
        
        # Base multiplier out of max ~180 SR
        base_A = min(stats_A['pp_strike_rate'] / 180.0, 1.0) * 100
        base_B = min(stats_B['pp_strike_rate'] / 180.0, 1.0) * 100
        
        # Adjust for pitch
        if pitch_type == 'Batting Friendly':
            base_A = min(base_A * 1.15, 95.0)
            base_B = min(base_B * 1.15, 95.0)
        elif pitch_type in ['Bowling Friendly', 'Spin Friendly']:
            base_A *= 0.85
            base_B *= 0.85

        return round(base_A, 2), round(base_B, 2)

    def generate_picks(self, teamA, teamB, probA, probB, foa_A, foa_B):
        """
        Determines the Safe Pick, Value Pick, and Promo Pick.
        """
        # Safe Pick: The one with highest probability
        safe_pick = teamA if probA >= probB else teamB
        
        # Value Pick: The underdog if they have close probability (e.g. > 35%) and good form, 
        # else just the underdog.
        value_pick = teamA if probA < probB else teamB
        
        # Promo Pick: High first over aggression
        promo_pick = teamA if foa_A >= foa_B else teamB
        
        return safe_pick, value_pick, promo_pick
        
    def find_key_players(self, teamA, teamB):
        """
        Finds highest impact score players from the SQLite DB.
        """
        import sqlite3
        import os
        from src.config import DB_PATH
        
        try:
            conn = sqlite3.connect(DB_PATH)
            # Find top 2 highest impact players among these two teams
            query = f'''
                SELECT name, impact_score 
                FROM players 
                WHERE team IN ("{teamA}", "{teamB}")
                ORDER BY impact_score DESC 
                LIMIT 2
            '''
            top_players = pd.read_sql_query(query, conn)
            conn.close()
            
            key_players = [
                {"name": row["name"], "impact_score": round(row["impact_score"], 2)} 
                for _, row in top_players.iterrows()
            ]
            return key_players
        except Exception:
            # Fallback mock
            return [
                {"name": f"Top Player {teamA}", "impact_score": 8.5},
                {"name": f"Top Player {teamB}", "impact_score": 8.2}
            ]
