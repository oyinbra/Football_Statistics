import requests

# Function to fetch match statistics from the SofaScore API
def fetch_match_statistics(match_id):
    url = f"https://www.sofascore.com/api/v1/event/{match_id}/statistics"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        statistics = {}
        groups = data['statistics'][0]['groups']
        for group in groups:
            for stat in group['statisticsItems']:
                stat_name = stat['name']
                home_stat = stat['home']
                away_stat = stat['away']
                statistics[stat_name] = {
                    'home': home_stat,
                    'away': away_stat
                }
        return statistics
    else:
        print(f"Failed to retrieve match statistics. Status code: {response.status_code}")
        return None

# Function to prepare statistics for CSV row
def prepare_statistics_row(statistics, home_team, away_team):
    def get_stat_value(stat_name, home_or_away):
        return statistics.get(stat_name, {}).get(home_or_away, 'N/A')

    return {
        "ball_possession": f"{home_team}: {get_stat_value('Ball possession', 'home')}%, {away_team}: {get_stat_value('Ball possession', 'away')}%",
        "expected_goals": f"{home_team}: {get_stat_value('Expected goals', 'home')}, {away_team}: {get_stat_value('Expected goals', 'away')}",
        "big_chances": f"{home_team}: {get_stat_value('Big chances', 'home')}, {away_team}: {get_stat_value('Big chances', 'away')}",
        "total_shots": f"{home_team}: {get_stat_value('Total shots', 'home')}, {away_team}: {get_stat_value('Total shots', 'away')}",
        "shots_on_target": f"{home_team}: {get_stat_value('Shots on target', 'home')}, {away_team}: {get_stat_value('Shots on target', 'away')}",
        "shots_off_target": f"{home_team}: {get_stat_value('Shots off target', 'home')}, {away_team}: {get_stat_value('Shots off target', 'away')}",
        "blocked_shots": f"{home_team}: {get_stat_value('Blocked shots', 'home')}, {away_team}: {get_stat_value('Blocked shots', 'away')}",
        "goalkeeper_saves": f"{home_team}: {get_stat_value('Goalkeeper saves', 'home')}, {away_team}: {get_stat_value('Goalkeeper saves', 'away')}",
        "corner_kicks": f"{home_team}: {get_stat_value('Corner kicks', 'home')}, {away_team}: {get_stat_value('Corner kicks', 'away')}",
        "fouls": f"{home_team}: {get_stat_value('Fouls', 'home')}, {away_team}: {get_stat_value('Fouls', 'away')}",
        "passes": f"{home_team}: {get_stat_value('Passes', 'home')}, {away_team}: {get_stat_value('Passes', 'away')}",
        "tackles": f"{home_team}: {get_stat_value('Total tackles', 'home')}, {away_team}: {get_stat_value('Total tackles', 'away')}",
        "free_kicks": f"{home_team}: {get_stat_value('Free kicks', 'home')}, {away_team}: {get_stat_value('Free kicks', 'away')}",
        "yellow_cards": f"{home_team}: {get_stat_value('Yellow cards', 'home')}, {away_team}: {get_stat_value('Yellow cards', 'away')}",
        "red_cards": f"{home_team}: {get_stat_value('Red cards', 'home')}, {away_team}: {get_stat_value('Red cards', 'away')}",
        "hit_woodwork": f"{home_team}: {get_stat_value('Hit woodwork', 'home')}, {away_team}: {get_stat_value('Hit woodwork', 'away')}",
        "shots_inside_box": f"{home_team}: {get_stat_value('Shots inside box', 'home')}, {away_team}: {get_stat_value('Shots inside box', 'away')}",
        "shots_outside_box": f"{home_team}: {get_stat_value('Shots outside box', 'home')}, {away_team}: {get_stat_value('Shots outside box', 'away')}",
        "big_chances_scored": f"{home_team}: {get_stat_value('Big chances scored', 'home')}, {away_team}: {get_stat_value('Big chances scored', 'away')}",
        "big_chances_missed": f"{home_team}: {get_stat_value('Big chances missed', 'home')}, {away_team}: {get_stat_value('Big chances missed', 'away')}",
        "through_balls": f"{home_team}: {get_stat_value('Through balls', 'home')}, {away_team}: {get_stat_value('Through balls', 'away')}",
        "touches_in_box": f"{home_team}: {get_stat_value('Touches in penalty area', 'home')}, {away_team}: {get_stat_value('Touches in penalty area', 'away')}",
        "fouled_in_third": f"{home_team}: {get_stat_value('Fouled in final third', 'home')}, {away_team}: {get_stat_value('Fouled in final third', 'away')}",
        "offsides": f"{home_team}: {get_stat_value('Offsides', 'home')}, {away_team}: {get_stat_value('Offsides', 'away')}",
        "accurate_passes": f"{home_team}: {get_stat_value('Accurate passes', 'home')}, {away_team}: {get_stat_value('Accurate passes', 'away')}",
        "throw_ins": f"{home_team}: {get_stat_value('Throw-ins', 'home')}, {away_team}: {get_stat_value('Throw-ins', 'away')}",
        "final_third_entries": f"{home_team}: {get_stat_value('Final third entries', 'home')}, {away_team}: {get_stat_value('Final third entries', 'away')}",
        "accurate_long_balls": f"{home_team}: {get_stat_value('Long balls', 'home')}, {away_team}: {get_stat_value('Long balls', 'away')}",
        "accurate_crosses": f"{home_team}: {get_stat_value('Crosses', 'home')}, {away_team}: {get_stat_value('Crosses', 'away')}",
        "duels": f"{home_team}: {get_stat_value('Duels', 'home')}, {away_team}: {get_stat_value('Duels', 'away')}",
        "dispossessed": f"{home_team}: {get_stat_value('Dispossessed', 'home')}, {away_team}: {get_stat_value('Dispossessed', 'away')}",
        "ground_duels": f"{home_team}: {get_stat_value('Ground duels', 'home')}, {away_team}: {get_stat_value('Ground duels', 'away')}",
        "aerial_duels": f"{home_team}: {get_stat_value('Aerial duels', 'home')}, {away_team}: {get_stat_value('Aerial duels', 'away')}",
        "dribbles": f"{home_team}: {get_stat_value('Dribbles', 'home')}, {away_team}: {get_stat_value('Dribbles', 'away')}",
        "tackles_won": f"{home_team}: {get_stat_value('Tackles won', 'home')}, {away_team}: {get_stat_value('Tackles won', 'away')}",
        "interceptions": f"{home_team}: {get_stat_value('Interceptions', 'home')}, {away_team}: {get_stat_value('Interceptions', 'away')}",
        "recoveries": f"{home_team}: {get_stat_value('Recoveries', 'home')}, {away_team}: {get_stat_value('Recoveries', 'away')}",
        "clearances": f"{home_team}: {get_stat_value('Clearances', 'home')}, {away_team}: {get_stat_value('Clearances', 'away')}",
        "goals_prevented": f"{home_team}: {get_stat_value('Goals prevented', 'home')}, {away_team}: {get_stat_value('Goals prevented', 'away')}",
        "high_claims": f"{home_team}: {get_stat_value('High claims', 'home')}, {away_team}: {get_stat_value('High claims', 'away')}",
        "goal_kicks": f"{home_team}: {get_stat_value('Goal kicks', 'home')}, {away_team}: {get_stat_value('Goal kicks', 'away')}"
    }
