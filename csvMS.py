import requests
import csv
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

# Function to check if a match ID already exists in the CSV
def check_existing_match_ids(csv_file):
    existing_match_ids = set()

    if os.path.exists(csv_file):
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            for row in reader:
                if row:  # Only process non-empty rows
                    existing_match_ids.add(row[0])  # Match ID is in the first column

    return existing_match_ids

# Function to export match data to CSV
def export_match_statistics_to_csv(match_ids, file_title, csv_file):
    # Get the list of existing Match IDs
    existing_match_ids = check_existing_match_ids(csv_file)
    
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Add headers if the file does not already exist
        if not os.path.exists(csv_file) or os.stat(csv_file).st_size == 0:
            writer.writerow([
                "MATCH ID", "DATE", "LEAGUE", "Match", "Ball Possession", "Expected Goals", "Big Chances", 
                "Total Shots", "Shots on Target", "Shots off Target", "Blocked Shots", "Goalkeeper Saves", 
                "Corner Kicks", "Fouls", "Passes", "Tackles", "Free Kicks", "Yellow Cards", "Red Cards", 
                "Hit Woodwork", "Shots inside Box", "Shots outside Box", "Big Chances Scored", 
                "Big Chances Missed", "Through Balls", "Touches in Penalty Area", "Fouled in Final Third", 
                "Offsides", "Accurate Passes", "Throw-ins", "Final Third Entries", "Accurate Long Balls", 
                "Accurate Crosses", "Duels", "Dispossessed", "Ground Duels", "Aerial Duels", 
                "Dribbles", "Tackles Won", "Interceptions", "Recoveries", "Clearances", "Goals Prevented", 
                "High Claims", "Goal Kicks"
            ])

        # Process each match
        for match_id in match_ids:
            if match_id in existing_match_ids:
                print(f"Match ID {match_id} already exists in the CSV file. Skipping...")
                continue

            match_date, home_team, away_team, league = fetch_match_details(match_id)
            statistics = fetch_match_statistics(match_id)

            if not statistics:
                print(f"Failed to retrieve statistics for Match ID {match_id}. Skipping...")
                continue

            # Prepare statistics row
            def get_stat_value(stat_name, home_or_away):
                return statistics.get(stat_name, {}).get(home_or_away, 'N/A')

            ball_possession = f"{home_team}: {get_stat_value('Ball possession', 'home')}%, {away_team}: {get_stat_value('Ball possession', 'away')}%"
            expected_goals = f"{home_team}: {get_stat_value('Expected goals', 'home')}, {away_team}: {get_stat_value('Expected goals', 'away')}"
            big_chances = f"{home_team}: {get_stat_value('Big chances', 'home')}, {away_team}: {get_stat_value('Big chances', 'away')}"
            total_shots = f"{home_team}: {get_stat_value('Total shots', 'home')}, {away_team}: {get_stat_value('Total shots', 'away')}"
            shots_on_target = f"{home_team}: {get_stat_value('Shots on target', 'home')}, {away_team}: {get_stat_value('Shots on target', 'away')}"
            shots_off_target = f"{home_team}: {get_stat_value('Shots off target', 'home')}, {away_team}: {get_stat_value('Shots off target', 'away')}"
            blocked_shots = f"{home_team}: {get_stat_value('Blocked shots', 'home')}, {away_team}: {get_stat_value('Blocked shots', 'away')}"
            goalkeeper_saves = f"{home_team}: {get_stat_value('Goalkeeper saves', 'home')}, {away_team}: {get_stat_value('Goalkeeper saves', 'away')}"
            corner_kicks = f"{home_team}: {get_stat_value('Corner kicks', 'home')}, {away_team}: {get_stat_value('Corner kicks', 'away')}"
            fouls = f"{home_team}: {get_stat_value('Fouls', 'home')}, {away_team}: {get_stat_value('Fouls', 'away')}"
            passes = f"{home_team}: {get_stat_value('Passes', 'home')}, {away_team}: {get_stat_value('Passes', 'away')}"
            tackles = f"{home_team}: {get_stat_value('Total tackles', 'home')}, {away_team}: {get_stat_value('Total tackles', 'away')}"
            free_kicks = f"{home_team}: {get_stat_value('Free kicks', 'home')}, {away_team}: {get_stat_value('Free kicks', 'away')}"
            yellow_cards = f"{home_team}: {get_stat_value('Yellow cards', 'home')}, {away_team}: {get_stat_value('Yellow cards', 'away')}"
            red_cards = f"{home_team}: {get_stat_value('Red cards', 'home')}, {away_team}: {get_stat_value('Red cards', 'away')}"
            hit_woodwork = f"{home_team}: {get_stat_value('Hit woodwork', 'home')}, {away_team}: {get_stat_value('Hit woodwork', 'away')}"
            shots_inside_box = f"{home_team}: {get_stat_value('Shots inside box', 'home')}, {away_team}: {get_stat_value('Shots inside box', 'away')}"
            shots_outside_box = f"{home_team}: {get_stat_value('Shots outside box', 'home')}, {away_team}: {get_stat_value('Shots outside box', 'away')}"
            big_chances_scored = f"{home_team}: {get_stat_value('Big chances scored', 'home')}, {away_team}: {get_stat_value('Big chances scored', 'away')}"
            big_chances_missed = f"{home_team}: {get_stat_value('Big chances missed', 'home')}, {away_team}: {get_stat_value('Big chances missed', 'away')}"
            through_balls = f"{home_team}: {get_stat_value('Through balls', 'home')}, {away_team}: {get_stat_value('Through balls', 'away')}"
            touches_in_box = f"{home_team}: {get_stat_value('Touches in penalty area', 'home')}, {away_team}: {get_stat_value('Touches in penalty area', 'away')}"
            fouled_in_third = f"{home_team}: {get_stat_value('Fouled in final third', 'home')}, {away_team}: {get_stat_value('Fouled in final third', 'away')}"
            offsides = f"{home_team}: {get_stat_value('Offsides', 'home')}, {away_team}: {get_stat_value('Offsides', 'away')}"
            accurate_passes = f"{home_team}: {get_stat_value('Accurate passes', 'home')}, {away_team}: {get_stat_value('Accurate passes', 'away')}"
            throw_ins = f"{home_team}: {get_stat_value('Throw-ins', 'home')}, {away_team}: {get_stat_value('Throw-ins', 'away')}"
            final_third_entries = f"{home_team}: {get_stat_value('Final third entries', 'home')}, {away_team}: {get_stat_value('Final third entries', 'away')}"
            accurate_long_balls = f"{home_team}: {get_stat_value('Long balls', 'home')}, {away_team}: {get_stat_value('Long balls', 'away')}"
            accurate_crosses = f"{home_team}: {get_stat_value('Crosses', 'home')}, {away_team}: {get_stat_value('Crosses', 'away')}"
            duels = f"{home_team}: {get_stat_value('Duels', 'home')}, {away_team}: {get_stat_value('Duels', 'away')}"
            dispossessed = f"{home_team}: {get_stat_value('Dispossessed', 'home')}, {away_team}: {get_stat_value('Dispossessed', 'away')}"
            ground_duels = f"{home_team}: {get_stat_value('Ground duels', 'home')}, {away_team}: {get_stat_value('Ground duels', 'away')}"
            aerial_duels = f"{home_team}: {get_stat_value('Aerial duels', 'home')}, {away_team}: {get_stat_value('Aerial duels', 'away')}"
            dribbles = f"{home_team}: {get_stat_value('Dribbles', 'home')}, {away_team}: {get_stat_value('Dribbles', 'away')}"
            tackles_won = f"{home_team}: {get_stat_value('Tackles won', 'home')}, {away_team}: {get_stat_value('Tackles won', 'away')}"
            interceptions = f"{home_team}: {get_stat_value('Interceptions', 'home')}, {away_team}: {get_stat_value('Interceptions', 'away')}"
            recoveries = f"{home_team}: {get_stat_value('Recoveries', 'home')}, {away_team}: {get_stat_value('Recoveries', 'away')}"
            clearances = f"{home_team}: {get_stat_value('Clearances', 'home')}, {away_team}: {get_stat_value('Clearances', 'away')}"
            goals_prevented = f"{home_team}: {get_stat_value('Goals prevented', 'home')}, {away_team}: {get_stat_value('Goals prevented', 'away')}"
            high_claims = f"{home_team}: {get_stat_value('High claims', 'home')}, {away_team}: {get_stat_value('High claims', 'away')}"
            goal_kicks = f"{home_team}: {get_stat_value('Goal kicks', 'home')}, {away_team}: {get_stat_value('Goal kicks', 'away')}"

            match_info = f"{home_team} vs {away_team}"

            # Write match data into CSV
            writer.writerow([
                match_id, match_date, league, match_info, ball_possession, expected_goals, big_chances, total_shots, 
                shots_on_target, shots_off_target, blocked_shots, goalkeeper_saves, corner_kicks, fouls, passes, tackles, 
                free_kicks, yellow_cards, red_cards, hit_woodwork, shots_inside_box, shots_outside_box, big_chances_scored, 
                big_chances_missed, through_balls, touches_in_box, fouled_in_third, offsides, accurate_passes, throw_ins, 
                final_third_entries, accurate_long_balls, accurate_crosses, duels, dispossessed, ground_duels, aerial_duels, 
                dribbles, tackles_won, interceptions, recoveries, clearances, goals_prevented, high_claims, goal_kicks
            ])
            
            print(f"Statistics exported for {home_team} vs {away_team} (Match ID: {match_id}).")

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

        print(f"Select the title for the file:\n1. {home_team}\n2. {away_team}\n3. {home_team} vs {away_team} Head-to-Head\n4. Enter a custom title")
        team_choice = input("Enter 1 for home team, 2 for away team, 3 for Head-to-Head, or 4 for custom title: ")

        if team_choice == "1":
            file_title = home_team
        elif team_choice == "2":
            file_title = away_team
        elif team_choice == "3":
            file_title = f"{home_team} vs {away_team} Head-to-Head"
        elif team_choice == "4":
            file_title = input("Enter the custom title: ").strip()
        else:
            print("Invalid choice. Exiting.")
            break

        directory = os.path.expanduser('~/Apex/Brainiac/Home/Statistics/FootballMatchStatistic/')
        if not os.path.exists(directory):
            os.makedirs(directory)

        csv_file = os.path.join(directory, f"{file_title}.csv")

        export_match_statistics_to_csv(match_ids, file_title, csv_file)

        another_game = input("Do you want to process another set of games? (yes/no): ").strip().lower()

        if another_game in ['n', 'no']:
            print("Exiting program.")
            break
        elif another_game not in ['y', 'yes']:
            print("Invalid input. Exiting program.")
            break
