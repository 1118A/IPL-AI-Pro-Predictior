import requests
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import CRIC_API_KEY

def fetch_recent_matches():
    """
    Fetches the last 2 years of IPL matches from CricAPI.
    Uses mock data if the API key is not set.
    """
    if not CRIC_API_KEY or CRIC_API_KEY == "dummy_cric_api_key":
        print("[Cricket API] Using mock match data (No API Key provided)")
        # Generating a sample set of matches resembling past 2 years
        return _generate_mock_matches()
        
    # Example logic for a real API call (CricAPI/RapidAPI structure)
    url = f"https://api.cricapi.com/v1/matches?apikey={CRIC_API_KEY}&offset=0"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            print(f"[Cricket API] Warning: returned {response.status_code}. Using mock fallback.")
            return _generate_mock_matches()
    except Exception as e:
        print(f"[Cricket API] Connection Error: {e}")
        return _generate_mock_matches()

def _generate_mock_matches():
    import random
    from datetime import datetime, timedelta
    teams = ['CSK', 'MI', 'RCB', 'KKR', 'DC', 'RR', 'PBKS', 'SRH', 'GT', 'LSG']
    venues = ['Wankhede', 'Eden Gardens', 'Chinnaswamy', 'Chepauk', 'Narendra Modi Stadium']
    pitch_types = ['Batting Friendly', 'Bowling Friendly', 'Balanced', 'Spin Friendly']
    
    matches = []
    base_date = datetime.now() - timedelta(days=700) # Past 2 years approx
    
    for i in range(120): # Mocking 120 matches
        t1, t2 = random.sample(teams, 2)
        match = {
            "id": f"M_mock_{i}",
            "date": (base_date + timedelta(days=i*3)).strftime("%Y-%m-%d"),
            "venue": random.choice(venues),
            "team1": t1,
            "team2": t2,
            "toss_winner": random.choice([t1, t2]),
            "winner": t1 if random.random() > 0.5 else t2,
            "pitch_type": random.choice(pitch_types)
        }
        matches.append(match)
        
    return matches

def _normalize_api_match(raw_match):
    """
    Normalizes a raw match dict from CricAPI to a consistent internal format
    with guaranteed keys: team1, team2, venue, date, pitch_type.
    """
    # CricAPI v1 uses a 'teams' list or 'teamInfo' list for team names
    teams = raw_match.get('teams', [])
    team_info = raw_match.get('teamInfo', [])

    if len(teams) >= 2:
        team1, team2 = teams[0], teams[1]
    elif len(team_info) >= 2:
        team1 = team_info[0].get('name', 'TBD')
        team2 = team_info[1].get('name', 'TBD')
    else:
        team1 = raw_match.get('team1', raw_match.get('team-1', 'TBD'))
        team2 = raw_match.get('team2', raw_match.get('team-2', 'TBD'))

    venue = ''
    venue_info = raw_match.get('venue', {})
    if isinstance(venue_info, dict):
        venue = venue_info.get('name', '')
    elif isinstance(venue_info, str):
        venue = venue_info

    return {
        'id': raw_match.get('id', ''),
        'date': raw_match.get('date', ''),
        'venue': venue,
        'team1': team1,
        'team2': team2,
        'pitch_type': raw_match.get('pitch_type', 'Balanced'),
    }


def fetch_upcoming_matches():
    """
    Fetches the schedule of upcoming matches.
    Uses mock data if API key is not set.
    Always returns a list of dicts with keys: team1, team2, venue, date, pitch_type.
    """
    if not CRIC_API_KEY or CRIC_API_KEY == "dummy_cric_api_key":
        print("[Cricket API] Using mock upcoming schedule (No API Key)")
        return _generate_upcoming_mock_matches()

    url = f"https://api.cricapi.com/v1/matches?apikey={CRIC_API_KEY}&offset=0"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json().get('data', [])
            from datetime import datetime
            today_str = datetime.now().strftime("%Y-%m-%d")
            upcoming_raw = [m for m in data if m.get('date', '2000-01-01') > today_str]
            # Normalize each match to the expected internal format
            return [_normalize_api_match(m) for m in upcoming_raw[:5]]
        else:
            return _generate_upcoming_mock_matches()
    except Exception:
        return _generate_upcoming_mock_matches()

def _generate_upcoming_mock_matches():
    from datetime import datetime, timedelta
    
    upcoming = []
    tomorrow = datetime.now() + timedelta(days=1)
    
    # Hardcode a realistic set of upcoming matches for the mock demo
    matches = [
        {"team1": "CSK", "team2": "RCB", "venue": "Chepauk", "pitch_type": "Spin Friendly"},
        {"team1": "MI", "team2": "GT", "venue": "Narendra Modi Stadium", "pitch_type": "Batting Friendly"},
        {"team1": "KKR", "team2": "SRH", "venue": "Eden Gardens", "pitch_type": "Balanced"}
    ]
    
    for i, m in enumerate(matches):
        match = {
            "id": f"M_mock_upcoming_{i}",
            "date": (tomorrow + timedelta(days=i)).strftime("%Y-%m-%d"),
            "venue": m["venue"],
            "team1": m["team1"],
            "team2": m["team2"],
            "pitch_type": m["pitch_type"]
        }
        upcoming.append(match)
    return upcoming

def fetch_squads():
    """
    Fetches squads for the current IPL season. 
    """
    if not CRIC_API_KEY or CRIC_API_KEY == "dummy_cric_api_key":
        return _generate_mock_players()
        
    print("[Cricket API] Fetching real squad data is not fully implemented without a valid key. Using mock data.")
    return _generate_mock_players()

def _generate_mock_players():
    import random
    import uuid
    import numpy as np
    teams = ['CSK', 'MI', 'RCB', 'KKR', 'DC', 'RR', 'PBKS', 'SRH', 'GT', 'LSG']
    roles = ['Batsman', 'Bowler', 'All-Rounder', 'Wicketkeeper']
    players = []
    
    for team in teams:
        for p in range(15):
            role_choice = random.choice(roles)
            
            # Create more statistically realistic distributions
            is_star_player = random.random() > 0.85
            form_base = np.random.normal(85, 5) if is_star_player else np.random.normal(50, 15)
            form_score = min(max(form_base, 10.0), 99.0)
            
            sr_base = np.random.normal(160, 15) if (role_choice == 'Batsman' and is_star_player) else np.random.normal(125, 20)
            pp_strike_rate = min(max(sr_base, 80.0), 200.0)
            
            boundary_base = np.random.normal(60, 10) if (role_choice == 'Batsman' and is_star_player) else np.random.normal(30, 15)
            boundary_pct = min(max(boundary_base, 5.0), 85.0)
            
            impact = min(max((form_score/100)*4 + (pp_strike_rate/200)*4 + (boundary_pct/100)*2, 1.0), 10.0)
            
            players.append({
                "player_id": f"P_mock_{uuid.uuid4().hex[:8]}",
                "name": f"Player_{team}_{p}",
                "team": team,
                "role": role_choice,
                "matches_played": random.randint(5, 150),
                "form_score": round(form_score, 2),
                "pp_strike_rate": round(pp_strike_rate, 2),
                "boundary_percentage": round(boundary_pct, 2),
                "impact_score": round(impact, 2)
            })
    return players

if __name__ == "__main__":
    matches = fetch_recent_matches()
    print(f"Fetched {len(matches)} matches.")
