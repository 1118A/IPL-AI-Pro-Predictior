import joblib
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.model.promo_engine import PromoEngine

class MatchPredictor:
    def __init__(self):
        try:
            saved_data = joblib.load('models/saved_models/win_model.pkl')
            self.model = saved_data['model']
            self.feature_names = saved_data['features']
            self.is_loaded = True
        except FileNotFoundError:
            self.is_loaded = False
            print("Warning: ML Win Model not found. Will return 50-50 chances.")
        
        self.promo = PromoEngine()

    def get_team_stats(self, team1, team2):
        try:
            df = pd.read_csv('data/processed/model_data.csv')
            
            # Simple average retrieval logic since processor already grouped it
            t1_form = df[df['team1'] == team1]['team1_form'].mean() if not df[df['team1'] == team1].empty else 50.0
            t2_form = df[df['team2'] == team2]['team2_form'].mean() if not df[df['team2'] == team2].empty else 50.0
            
            t1_pp_sr = df[df['team1'] == team1]['team1_pp_sr'].mean() if not df[df['team1'] == team1].empty else 130.0
            t2_pp_sr = df[df['team2'] == team2]['team2_pp_sr'].mean() if not df[df['team2'] == team2].empty else 130.0
            
            t1_b_pct = df[df['team1'] == team1]['team1_boundary_pct'].mean() if not df[df['team1'] == team1].empty else 35.0
            t2_b_pct = df[df['team2'] == team2]['team2_boundary_pct'].mean() if not df[df['team2'] == team2].empty else 35.0
            
            t1_imp = df[df['team1'] == team1]['team1_impact'].mean() if not df[df['team1'] == team1].empty else 5.0
            t2_imp = df[df['team2'] == team2]['team2_impact'].mean() if not df[df['team2'] == team2].empty else 5.0
            
            t1_win_rate = df[df['team1'] == team1]['team1_win_rate'].mean() if not df[df['team1'] == team1].empty else 0.5
            t2_win_rate = df[df['team2'] == team2]['team2_win_rate'].mean() if not df[df['team2'] == team2].empty else 0.5
            
            t1_v_win = df[df['team1'] == team1]['team1_venue_win_rate'].mean() if not df[df['team1'] == team1].empty else 0.5
            t2_v_win = df[df['team2'] == team2]['team2_venue_win_rate'].mean() if not df[df['team2'] == team2].empty else 0.5
            
            return {
                'team1_form': t1_form, 'team2_form': t2_form,
                'team1_pp_sr': t1_pp_sr, 'team2_pp_sr': t2_pp_sr,
                'team1_boundary_pct': t1_b_pct, 'team2_boundary_pct': t2_b_pct,
                'team1_impact': t1_imp, 'team2_impact': t2_imp,
                'team1_win_rate': t1_win_rate, 'team2_win_rate': t2_win_rate,
                'team1_venue_win_rate': t1_v_win, 'team2_venue_win_rate': t2_v_win
            }
        except:
            return None

    def predict(self, teamA, teamB, toss_winner, pitch_type, weather_cond='Clear', venue_size='Medium'):
        stats = self.get_team_stats(teamA, teamB)
        
        if stats and self.is_loaded:
            features = stats.copy()
            features['toss_advantage'] = 1 if toss_winner == teamA else 0
            
            input_df = pd.DataFrame([features])
            
            for col in self.feature_names:
                if col not in input_df.columns:
                    # check logic for specific dummy prefix
                    if col == f'pitch_{pitch_type}' or col == f'weather_{weather_cond}' or col == f'venue_{venue_size}':
                        input_df[col] = 1
                    else:
                        input_df[col] = 0

            input_df = input_df[self.feature_names]
            
            proba = self.model.predict_proba(input_df)[0]
            team1_prob = proba[1] * 100
            team2_prob = proba[0] * 100
        else:
            team1_prob, team2_prob = 50.0, 50.0
            
        # Post-Process with Promo Engine
        foa_A, foa_B = self.promo.eval_first_over_aggression(teamA, teamB, pitch_type)
        safe_pick, val_pick, promo_pick = self.promo.generate_picks(teamA, teamB, team1_prob, team2_prob, foa_A, foa_B)
        key_players = self.promo.find_key_players(teamA, teamB)

        prob_diff = abs(team1_prob - team2_prob)
        if prob_diff > 25:
            risk = "Low"
        elif prob_diff > 10:
            risk = "Medium"
        else:
            risk = "High"

        return {
            "match": f"{teamA} vs {teamB}",
            "probabilities": {
                teamA: round(team1_prob, 2),
                teamB: round(team2_prob, 2)
            },
            "first_over_aggression": {
                teamA: foa_A,
                teamB: foa_B
            },
            "picks": {
                "safe": safe_pick,
                "value": val_pick,
                "promo": promo_pick
            },
            "key_players": key_players,
            "risk_level": risk
        }

if __name__ == '__main__':
    predictor = MatchPredictor()
    res = predictor.predict("CSK", "MI", "CSK", "Batting Friendly", "Clear", "Small")
    import pprint
    pprint.pprint(res)
