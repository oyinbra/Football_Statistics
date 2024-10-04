import csv
import os

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
def export_match_statistics_to_csv(match_ids, file_title, csv_file, match_details_func, match_statistics_func, prepare_statistics_func):
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

            match_date, home_team, away_team, league = match_details_func(match_id)
            statistics = match_statistics_func(match_id)

            if not statistics:
                print(f"Failed to retrieve statistics for Match ID {match_id}. Skipping...")
                continue

            # Prepare statistics row
            stats_row = prepare_statistics_func(statistics, home_team, away_team)
            match_info = f"{home_team} vs {away_team}"

            # Write match data into CSV
            writer.writerow([
                match_id, match_date, league, match_info, stats_row["ball_possession"], stats_row["expected_goals"], 
                stats_row["big_chances"], stats_row["total_shots"], stats_row["shots_on_target"], stats_row["shots_off_target"],
                stats_row["blocked_shots"], stats_row["goalkeeper_saves"], stats_row["corner_kicks"], stats_row["fouls"], 
                stats_row["passes"], stats_row["tackles"], stats_row["free_kicks"], stats_row["yellow_cards"], 
                stats_row["red_cards"], stats_row["hit_woodwork"], stats_row["shots_inside_box"], 
                stats_row["shots_outside_box"], stats_row["big_chances_scored"], stats_row["big_chances_missed"], 
                stats_row["through_balls"], stats_row["touches_in_box"], stats_row["fouled_in_third"], 
                stats_row["offsides"], stats_row["accurate_passes"], stats_row["throw_ins"], stats_row["final_third_entries"], 
                stats_row["accurate_long_balls"], stats_row["accurate_crosses"], stats_row["duels"], 
                stats_row["dispossessed"], stats_row["ground_duels"], stats_row["aerial_duels"], 
                stats_row["dribbles"], stats_row["tackles_won"], stats_row["interceptions"], 
                stats_row["recoveries"], stats_row["clearances"], stats_row["goals_prevented"], 
                stats_row["high_claims"], stats_row["goal_kicks"]
            ])
            
            print(f"Statistics exported for {home_team} vs {away_team} (Match ID: {match_id}).")
