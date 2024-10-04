import requests
import os
from datetime import datetime, timezone
import re

# Function to extract match ID from SofaScore URL
def extract_match_id(url):
    match = re.search(r'id:(\d+)', url)
    if match:
        return match.group(1)
    else:
        print("Invalid URL format. Couldn't extract match ID.")
        return None

# Function to fetch match details (date, home team, away team, and league)
def fetch_match_details(match_id):
    url = f"https://www.sofascore.com/api/v1/event/{match_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        match_timestamp = data['event']['startTimestamp']
        match_date = datetime.fromtimestamp(match_timestamp, timezone.utc).strftime('%Y-%m-%d')
        home_team = data['event']['homeTeam']['name']
        away_team = data['event']['awayTeam']['name']
        league = data['event']['tournament']['name']  # Fetch league/tournament name
        return match_date, home_team, away_team, league
    else:
        print(f"Failed to retrieve match details. Status code: {response.status_code}")
        return None, None, None, None

# Function to fetch match scores directly from match details API
def fetch_match_scores(match_id):
    url = f"https://www.sofascore.com/api/v1/event/{match_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        home_score = data['event']['homeScore']['current']
        away_score = data['event']['awayScore']['current']
        return home_score, away_score
    else:
        print(f"Failed to retrieve match scores. Status code: {response.status_code}")
        return None, None

# Function to fetch match incidents from the incidents API
def fetch_match_incidents(match_id):
    url = f"https://www.sofascore.com/api/v1/event/{match_id}/incidents"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        incidents = []

        for incident in data['incidents']:
            incident_data = {}
            if 'incidentType' in incident:
                incident_data['time'] = incident.get('time', 'N/A')

                if incident['incidentType'] == 'goal' and 'player' in incident:
                    incident_data['type'] = 'Goal'
                    incident_data['player'] = incident['player'].get('name', 'Unknown')
                    if 'assist1' in incident:
                        incident_data['assist'] = incident['assist1'].get('name', 'No Assist')

                elif incident['incidentType'] == 'card' and 'player' in incident:
                    incident_data['type'] = incident['incidentClass'].capitalize() + ' Card'
                    incident_data['player'] = incident['player'].get('name', 'Unknown')
                    incident_data['reason'] = incident.get('reason', 'No Reason')

                elif incident['incidentType'] == 'substitution' and 'playerIn' in incident and 'playerOut' in incident:
                    incident_data['type'] = 'Substitution'
                    incident_data['playerIn'] = incident['playerIn'].get('name', 'Unknown')
                    incident_data['playerOut'] = incident['playerOut'].get('name', 'Unknown')

                # Append the incident if relevant data exists
                if incident_data:
                    incidents.append(incident_data)

        return incidents
    else:
        print(f"Failed to retrieve match incidents. Status code: {response.status_code}")
        return []

# Function to export match statistics and incidents to a markdown file
def export_match_statistics_to_markdown(match_id, file_title, file_path):
    match_date, home_team, away_team, league = fetch_match_details(match_id)
    home_score, away_score = fetch_match_scores(match_id)
    
    if home_score is None or away_score is None:
        print("Failed to retrieve match scores.")
        return
    
    url = f"https://www.sofascore.com/api/v1/event/{match_id}/statistics"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        statistics = []

        groups = data['statistics'][0]['groups']

        for group in groups:
            group_name = group['groupName']
            for stat in group['statisticsItems']:
                stat_name = stat['name']
                home_stat = stat['home']
                away_stat = stat['away']
                statistics.append(f"- **{stat_name}**: {home_team}: {home_stat}, {away_team}: {away_stat}")

        incidents = fetch_match_incidents(match_id)

        with open(file_path, "a") as file:
            file.write(f"\n## {home_team} vs {away_team}\n")
            file.write(f"- **Match Date**: {match_date}\n")
            file.write(f"- **League**: {league}\n")
            file.write(f"- **Score**: {home_team} {home_score} - {away_score} {away_team}\n")

            file.write(f"\n### Match Statistics\n")
            for stat in statistics:
                file.write(f"{stat}\n")

            file.write(f"\n### Match Incidents\n")
            if incidents:
                for incident in incidents:
                    time = incident.get('time', 'N/A')
                    event_type = incident.get('type', 'Unknown Event')
                    if event_type == 'Goal':
                        file.write(f"- {time}': {event_type} by {incident.get('player', 'Unknown')}")
                        if 'assist' in incident:
                            file.write(f", assisted by {incident.get('assist')}")
                        file.write("\n")
                    elif event_type == 'Substitution':
                        file.write(f"- {time}': {event_type}, {incident.get('playerOut', 'Unknown')} out, {incident.get('playerIn', 'Unknown')} in\n")
                    elif 'reason' in incident:
                        file.write(f"- {time}': {event_type} for {incident.get('player', 'Unknown')} ({incident.get('reason', 'No reason provided')})\n")
            else:
                file.write("No significant incidents were recorded.\n")

        print(f"Statistics and incidents appended for {home_team} vs {away_team}.")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

# Main code to handle user input for multiple games
if __name__ == "__main__":
    while True:
        match_urls = input("Enter the SofaScore match URLs (comma separated): ").split(',')

        match_ids = [extract_match_id(url.strip()) for url in match_urls]
        match_ids = [mid for mid in match_ids if mid]

        if not match_ids:
            print("No valid match IDs found. Exiting.")
            break

        match_date, home_team, away_team, league = fetch_match_details(match_ids[0])

        print(f"Select the title for the file:\n1. {home_team}\n2. {away_team}\n3. Enter a custom title")
        team_choice = input("Enter 1 for home team, 2 for away team, or 3 for custom title: ")

        if team_choice == "1":
            file_title = home_team
        elif team_choice == "2":
            file_title = away_team
        elif team_choice == "3":
            file_title = input("Enter the custom title: ").strip()
        else:
            print("Invalid choice. Exiting.")
            break

        directory = os.path.expanduser('~/Apex/Brainiac/Home/Statistics/FootballMatchStatistic/')
        if not os.path.exists(directory):
            os.makedirs(directory)

        markdown_file = os.path.join(directory, f"{file_title}.md")

        for match_id in match_ids:
            export_match_statistics_to_markdown(match_id, file_title, markdown_file)

        another_game = input("Do you want to process another set of games? (yes/no): ").strip().lower()

        if another_game in ['n', 'no']:
            print("Exiting program.")
            break
        elif another_game not in ['y', 'yes']:
            print("Invalid input. Exiting program.")
            break
