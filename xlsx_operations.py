import pandas as pd
import os
from openpyxl import load_workbook

# Function to check if a match ID already exists in the XLSX
def check_existing_match_ids(xlsx_file):
    existing_match_ids = set()

    if os.path.exists(xlsx_file):
        df = pd.read_excel(xlsx_file)
        if "MATCH ID" in df.columns:
            existing_match_ids = set(df["MATCH ID"].astype(str))

    return existing_match_ids

# Function to export match data to XLSX and auto-adjust column widths
def export_match_statistics_to_xlsx(match_ids, file_title, xlsx_file, match_details_func, match_statistics_func, prepare_statistics_func):
    # Get the list of existing Match IDs
    existing_match_ids = check_existing_match_ids(xlsx_file)

    if os.path.exists(xlsx_file):
        df = pd.read_excel(xlsx_file)
    else:
        # Create an empty DataFrame with the correct headers
        columns = [
            "MATCH ID", "DATE", "LEAGUE", "Match", "Ball Possession", "Expected Goals", "Big Chances", 
            "Total Shots", "Shots on Target", "Shots off Target", "Blocked Shots", "Goalkeeper Saves", 
            "Corner Kicks", "Fouls", "Passes", "Tackles", "Free Kicks", "Yellow Cards", "Red Cards", 
            "Hit Woodwork", "Shots inside Box", "Shots outside Box", "Big Chances Scored", 
            "Big Chances Missed", "Through Balls", "Touches in Penalty Area", "Fouled in Final Third", 
            "Offsides", "Accurate Passes", "Throw-ins", "Final Third Entries", "Accurate Long Balls", 
            "Accurate Crosses", "Duels", "Dispossessed", "Ground Duels", "Aerial Duels", 
            "Dribbles", "Tackles Won", "Interceptions", "Recoveries", "Clearances", "Goals Prevented", 
            "High Claims", "Goal Kicks"
        ]
        df = pd.DataFrame(columns=columns)

    for match_id in match_ids:
        if match_id in existing_match_ids:
            print(f"Match ID {match_id} already exists in the file. Skipping...")
            continue

        # Retrieve match details and statistics
        match_date, home_team, away_team, league = match_details_func(match_id)
        statistics = match_statistics_func(match_id)

        if not statistics:
            print(f"Failed to retrieve statistics for Match ID {match_id}. Skipping...")
            continue

        # Prepare statistics row
        stats_row = prepare_statistics_func(statistics, home_team, away_team)
        match_info = f"{home_team} vs {away_team}"

        # Append match data to the DataFrame
        new_row = {
            "MATCH ID": match_id, "DATE": match_date, "LEAGUE": league, "Match": match_info,
            "Ball Possession": stats_row["ball_possession"], "Expected Goals": stats_row["expected_goals"], 
            "Big Chances": stats_row["big_chances"], "Total Shots": stats_row["total_shots"], 
            "Shots on Target": stats_row["shots_on_target"], "Shots off Target": stats_row["shots_off_target"],
            "Blocked Shots": stats_row["blocked_shots"], "Goalkeeper Saves": stats_row["goalkeeper_saves"], 
            "Corner Kicks": stats_row["corner_kicks"], "Fouls": stats_row["fouls"], "Passes": stats_row["passes"], 
            "Tackles": stats_row["tackles"], "Free Kicks": stats_row["free_kicks"], 
            "Yellow Cards": stats_row["yellow_cards"], "Red Cards": stats_row["red_cards"], 
            "Hit Woodwork": stats_row["hit_woodwork"], "Shots inside Box": stats_row["shots_inside_box"], 
            "Shots outside Box": stats_row["shots_outside_box"], "Big Chances Scored": stats_row["big_chances_scored"], 
            "Big Chances Missed": stats_row["big_chances_missed"], "Through Balls": stats_row["through_balls"], 
            "Touches in Penalty Area": stats_row["touches_in_box"], "Fouled in Final Third": stats_row["fouled_in_third"], 
            "Offsides": stats_row["offsides"], "Accurate Passes": stats_row["accurate_passes"], 
            "Throw-ins": stats_row["throw_ins"], "Final Third Entries": stats_row["final_third_entries"], 
            "Accurate Long Balls": stats_row["accurate_long_balls"], "Accurate Crosses": stats_row["accurate_crosses"], 
            "Duels": stats_row["duels"], "Dispossessed": stats_row["dispossessed"], "Ground Duels": stats_row["ground_duels"], 
            "Aerial Duels": stats_row["aerial_duels"], "Dribbles": stats_row["dribbles"], 
            "Tackles Won": stats_row["tackles_won"], "Interceptions": stats_row["interceptions"], 
            "Recoveries": stats_row["recoveries"], "Clearances": stats_row["clearances"], 
            "Goals Prevented": stats_row["goals_prevented"], "High Claims": stats_row["high_claims"], 
            "Goal Kicks": stats_row["goal_kicks"]
        }
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        print(f"Statistics exported for {home_team} vs {away_team} (Match ID: {match_id}).")

    # Save DataFrame to XLSX
    df.to_excel(xlsx_file, index=False)

    # Adjust column width
    workbook = load_workbook(xlsx_file)
    worksheet = workbook.active

    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter  # Get the column letter
        for cell in column:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = (max_length + 2)
        worksheet.column_dimensions[column_letter].width = adjusted_width

    workbook.save(xlsx_file)
    print(f"Data successfully exported to {xlsx_file} with adjusted column widths.")
