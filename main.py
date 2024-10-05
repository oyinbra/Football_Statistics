import os
import re
from match_details import fetch_match_details
from match_statistics import fetch_match_statistics, prepare_statistics_row
from xlsx_operations import export_match_statistics_to_xlsx

# Function to extract match ID from SofaScore URL
def extract_match_id(url):
    match = re.search(r'id:(\d+)', url)
    if match:
        return match.group(1)
    else:
        print("Invalid URL format. Couldn't extract match ID.")
        return None

if __name__ == "__main__":
    while True:
        match_urls = input("Enter the SofaScore match URLs (comma separated): ").split(',')

        match_ids = [extract_match_id(url.strip()) for url in match_urls]
        match_ids = [mid for mid in match_ids if mid]

        if not match_ids:
            print("No valid match IDs found. Exiting.")
            break

        match_date, home_team, away_team, league = fetch_match_details(match_ids[0])

        print(f"Select the title for the file:\n1. {home_team}\n2. {away_team}\n3. {home_team} vs {away_team} H2H\n4. Enter a custom title")
        team_choice = input("Enter 1 for home team, 2 for away team, 3 for H2H, or 4 for custom title: ")

        if team_choice == "1":
            file_title = home_team
        elif team_choice == "2":
            file_title = away_team
        elif team_choice == "3":
            file_title = f"{home_team} vs {away_team} H2H"
        elif team_choice == "4":
            file_title = input("Enter the custom title: ").strip()
        else:
            print("Invalid choice. Exiting.")
            break

        directory = os.path.expanduser('~/Apex/Brainiac/Home/Statistics/FootballMatchStatistic/')
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 
        xlsx_file = os.path.join(directory, f"{file_title}.xlsx")

        # Export match statistics to XLSX
        export_match_statistics_to_xlsx(match_ids, file_title, xlsx_file, fetch_match_details, fetch_match_statistics, prepare_statistics_row)

        another_game = input("Do you want to process another set of games? (yes/no): ").strip().lower()

        if another_game in ['n', 'no']:
            print("Exiting program.")
            break
        elif another_game not in ['y', 'yes']:
            print("Invalid input. Exiting program.")
            break
