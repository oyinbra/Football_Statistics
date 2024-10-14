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

# Function to prepare statistics for XLSX row
def prepare_statistics_row(statistics, home_team, away_team):
    def get_stat_value(stat_name, home_or_away):
        return statistics.get(stat_name, {}).get(home_or_away, 'N/A')

    return {
        "ball_possession": f"{home_team} {get_stat_value('Ball possession', 'home')}% - {get_stat_value('Ball possession', 'away')}% {away_team}",
        "expected_goals": f"{home_team} {get_stat_value('Expected goals', 'home')} - {get_stat_value('Expected goals', 'away')} {away_team}",
        "big_chances": f"{home_team} {get_stat_value('Big chances', 'home')} - {get_stat_value('Big chances', 'away')} {away_team}",
        "total_shots": f"{home_team} {get_stat_value('Total shots', 'home')} - {get_stat_value('Total shots', 'away')} {away_team}",
        "shots_on_target": f"{home_team} {get_stat_value('Shots on target', 'home')} - {get_stat_value('Shots on target', 'away')} {away_team}",
        "shots_off_target": f"{home_team} {get_stat_value('Shots off target', 'home')} - {get_stat_value('Shots off target', 'away')} {away_team}",
        "blocked_shots": f"{home_team} {get_stat_value('Blocked shots', 'home')} - {get_stat_value('Blocked shots', 'away')} {away_team}",
        "goalkeeper_saves": f"{home_team} {get_stat_value('Goalkeeper saves', 'home')} - {get_stat_value('Goalkeeper saves', 'away')} {away_team}",
        "corner_kicks": f"{home_team} {get_stat_value('Corner kicks', 'home')} - {get_stat_value('Corner kicks', 'away')} {away_team}",
        "fouls": f"{home_team} {get_stat_value('Fouls', 'home')} - {get_stat_value('Fouls', 'away')} {away_team}",
        "passes": f"{home_team} {get_stat_value('Passes', 'home')} - {get_stat_value('Passes', 'away')} {away_team}",
        "tackles": f"{home_team} {get_stat_value('Total tackles', 'home')} - {get_stat_value('Total tackles', 'away')} {away_team}",
        "free_kicks": f"{home_team} {get_stat_value('Free kicks', 'home')} - {get_stat_value('Free kicks', 'away')} {away_team}",
        "yellow_cards": f"{home_team} {get_stat_value('Yellow cards', 'home')} - {get_stat_value('Yellow cards', 'away')} {away_team}",
        "red_cards": f"{home_team} {get_stat_value('Red cards', 'home')} - {get_stat_value('Red cards', 'away')} {away_team}",
        "hit_woodwork": f"{home_team} {get_stat_value('Hit woodwork', 'home')} - {get_stat_value('Hit woodwork', 'away')} {away_team}",
        "shots_inside_box": f"{home_team} {get_stat_value('Shots inside box', 'home')} - {get_stat_value('Shots inside box', 'away')} {away_team}",
        "shots_outside_box": f"{home_team} {get_stat_value('Shots outside box', 'home')} - {get_stat_value('Shots outside box', 'away')} {away_team}",
        "big_chances_scored": f"{home_team} {get_stat_value('Big chances scored', 'home')} - {get_stat_value('Big chances scored', 'away')} {away_team}",
        "big_chances_missed": f"{home_team} {get_stat_value('Big chances missed', 'home')} - {get_stat_value('Big chances missed', 'away')} {away_team}",
        "through_balls": f"{home_team} {get_stat_value('Through balls', 'home')} - {get_stat_value('Through balls', 'away')} {away_team}",
        "touches_in_box": f"{home_team} {get_stat_value('Touches in penalty area', 'home')} - {get_stat_value('Touches in penalty area', 'away')} {away_team}",
        "fouled_in_third": f"{home_team} {get_stat_value('Fouled in final third', 'home')} - {get_stat_value('Fouled in final third', 'away')} {away_team}",
        "offsides": f"{home_team} {get_stat_value('Offsides', 'home')} - {get_stat_value('Offsides', 'away')} {away_team}",
        "accurate_passes": f"{home_team} {get_stat_value('Accurate passes', 'home')} - {get_stat_value('Accurate passes', 'away')} {away_team}",
        "throw_ins": f"{home_team} {get_stat_value('Throw-ins', 'home')} - {get_stat_value('Throw-ins', 'away')} {away_team}",
        "final_third_entries": f"{home_team} {get_stat_value('Final third entries', 'home')} - {get_stat_value('Final third entries', 'away')} {away_team}",
        "accurate_long_balls": f"{home_team} {get_stat_value('Long balls', 'home')} - {get_stat_value('Long balls', 'away')} {away_team}",
        "accurate_crosses": f"{home_team} {get_stat_value('Crosses', 'home')} - {get_stat_value('Crosses', 'away')} {away_team}",
        "duels": f"{home_team} {get_stat_value('Duels', 'home')} - {get_stat_value('Duels', 'away')} {away_team}",
        "dispossessed": f"{home_team} {get_stat_value('Dispossessed', 'home')} - {get_stat_value('Dispossessed', 'away')} {away_team}",
        "ground_duels": f"{home_team} {get_stat_value('Ground duels', 'home')} - {get_stat_value('Ground duels', 'away')} {away_team}",
        "aerial_duels": f"{home_team} {get_stat_value('Aerial duels', 'home')} - {get_stat_value('Aerial duels', 'away')} {away_team}",
        "dribbles": f"{home_team} {get_stat_value('Dribbles', 'home')} - {get_stat_value('Dribbles', 'away')} {away_team}",
        "tackles_won": f"{home_team} {get_stat_value('Tackles won', 'home')} - {get_stat_value('Tackles won', 'away')} {away_team}",
        "interceptions": f"{home_team} {get_stat_value('Interceptions', 'home')} - {get_stat_value('Interceptions', 'away')} {away_team}",
        "recoveries": f"{home_team} {get_stat_value('Recoveries', 'home')} - {get_stat_value('Recoveries', 'away')} {away_team}",
        "clearances": f"{home_team} {get_stat_value('Clearances', 'home')} - {get_stat_value('Clearances', 'away')} {away_team}",
        "goals_prevented": f"{home_team} {get_stat_value('Goals prevented', 'home')} - {get_stat_value('Goals prevented', 'away')} {away_team}",
        "high_claims": f"{home_team} {get_stat_value('High claims', 'home')} - {get_stat_value('High claims', 'away')} {away_team}",
        "goal_kicks": f"{home_team} {get_stat_value('Goal kicks', 'home')} - {get_stat_value('Goal kicks', 'away')} {away_team}"
    }
