import re
from db_operations import insert_match
from match_statistics import fetch_match_statistics

# Function to extract match ID from SofaScore URL
def extract_match_id(url):
    match = re.search(r'id:(\d+)', url)
    if match:
        return int(match.group(1))
    else:
        print("Invalid URL format. Couldn't extract match ID.")
        return None

if __name__ == "__main__":
    while True:
        match_urls = input("Enter SofaScore match URLs (comma separated) or 'q' to quit: ").strip()

        # Check if the user wants to quit
        if match_urls.lower() == 'q':
            print("Exiting the program.")
            break

        # Process each URL
        match_ids = [extract_match_id(url.strip()) for url in match_urls.split(',')]
        match_ids = [mid for mid in match_ids if mid]

        if not match_ids:
            print("No valid match IDs found. Please try again.")
            continue

        for match_id in match_ids:
            # Fetch match details and statistics using the provided match ID
            match_details = fetch_match_statistics(match_id)
            if not match_details:
                print(f"Could not fetch details for match ID {match_id}. Skipping.")
                continue

            match_date = match_details.get('date')
            home_team = match_details.get('home_team')
            away_team = match_details.get('away_team')
            league = match_details.get('league')
            statistics = match_details.get('statistics')

            # Insert the match into the database
            insert_match(match_id, match_date, home_team, away_team, league, statistics)

        print("Processing complete. You can add more match IDs or type 'q' to quit.")
