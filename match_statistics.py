import requests
from datetime import datetime

def fetch_match_statistics(match_id):
    """Fetch match details and statistics from SofaScore using the correct API endpoint."""
    url = f"https://www.sofascore.com/api/v1/event/{match_id}/statistics"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Fetch additional match information such as date, teams, and league
        match_info_url = f"https://www.sofascore.com/api/v1/event/{match_id}"
        match_info_response = requests.get(match_info_url)
        match_info_response.raise_for_status()
        match_info_data = match_info_response.json()

        # Extract league name properly from the match_info_data
        league = match_info_data.get('event', {}).get('tournament', {}).get('name')
        if not league:
            league = "Unknown League"

        # Convert the Unix timestamp to a date
        match_timestamp = match_info_data.get('event', {}).get('startTimestamp')
        if match_timestamp:
            match_date = datetime.utcfromtimestamp(match_timestamp).date()
        else:
            return None

        home_team = match_info_data.get('event', {}).get('homeTeam', {}).get('name')
        away_team = match_info_data.get('event', {}).get('awayTeam', {}).get('name')

        if not home_team or not away_team:
            return None

        # Extract relevant statistics
        statistics = extract_statistics(data)

        return {
            "date": match_date,
            "home_team": home_team,
            "away_team": away_team,
            "league": league,
            "statistics": statistics
        }

    except requests.RequestException as e:
        return None
    except Exception as e:
        return None

def extract_statistics(data):
    """Extracts statistics from the API response."""
    statistics = {}
    try:
        # Check if the expected structure exists
        if 'statistics' in data and len(data['statistics']) > 0:
            groups = data['statistics'][0].get('groups', [])

            for group in groups:
                group_name = group.get('groupName', '').lower()
                
                for stat in group.get('statisticsItems', []):
                    stat_name = stat['name'].lower()
                    statistics[f"{stat_name}_home"] = str(stat.get('home', 'N/A'))
                    statistics[f"{stat_name}_away"] = str(stat.get('away', 'N/A'))
    except (KeyError, IndexError, TypeError):
        pass

    return statistics
