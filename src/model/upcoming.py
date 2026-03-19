import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.data.cricket_api import fetch_upcoming_matches
from src.data.weather_api import get_weather
from src.model.predictor import MatchPredictor

def get_proactive_predictions():
    """
    Fetches the next upcoming scheduled matches, finds their venue, 
    pulls the weather forecast for that venue's city, and generates
    the AI Strategy recommendation immediately.
    """
    try:
        predictor = MatchPredictor()
    except Exception:
        print("Failed to initialize MatchPredictor. Ensure models are trained.")
        return []

    upcoming_matches = fetch_upcoming_matches()
    predictions = []
    
    # We map specific generic venue size based on name to match the ML engine
    venue_size_map = {
        'Wankhede': 'Small',
        'Eden Gardens': 'Medium',
        'Chinnaswamy': 'Small',
        'Chepauk': 'Large',
        'Narendra Modi Stadium': 'Large',
        'Rajiv Gandhi Stadium': 'Medium',
        'Arun Jaitley Stadium': 'Small'
    }
    
    for match in upcoming_matches:
        teamA = match['team1']
        teamB = match['team2']
        venue = match['venue']
        date = match['date']
        pitch = match['pitch_type']
        
        # In a real scheduling match, toss winner isn't known. 
        # We process both scenarios or assume Home Team toss win for baseline proactive logic.
        # For simplicity, we assume TeamA wins toss randomly or use Home advantage.
        toss_winner = teamA
        
        weather_info = get_weather(venue)
        weather_cond = weather_info.get('condition', 'Clear')
        venue_size = venue_size_map.get(venue, 'Medium')
        
        # Predict using AI
        pred_result = predictor.predict(
            teamA, teamB, toss_winner, pitch, weather_cond, venue_size
        )
        
        predictions.append({
            "date": date,
            "venue": venue,
            "weather": weather_info,
            "prediction": pred_result
        })
        
    return predictions

if __name__ == '__main__':
    res = get_proactive_predictions()
    import pprint
    pprint.pprint(res)
