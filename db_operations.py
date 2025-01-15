import re
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def clean_stat_value(value):
    """Clean and format statistic values for database insertion."""
    # If the value is in the form of '41/57 (72%)', extract the percentage part.
    match = re.search(r'\((\d+)%\)', value)
    if match:
        return match.group(1) + "%"  # Extract the percentage value.
    
    # Remove any non-numeric characters for values that should be numeric.
    if isinstance(value, str) and '/' in value:
        return value.split('/')[0]  # Return the first part before the slash.
    
    # For all other values, return as is.
    return value

def get_or_create_league_id(cursor, league_name):
    """Gets or creates a league ID."""
    cursor.execute("SELECT league_id FROM leagues WHERE league_name = %s", (league_name,))
    league_id = cursor.fetchone()
    if not league_id:
        cursor.execute("INSERT INTO leagues (league_name) VALUES (%s) RETURNING league_id", (league_name,))
        league_id = cursor.fetchone()[0]
    else:
        league_id = league_id[0]
    return league_id

def get_or_create_team_id(cursor, team_name):
    """Gets or creates a team ID."""
    cursor.execute("SELECT team_id FROM teams WHERE team_name = %s", (team_name,))
    team_id = cursor.fetchone()
    if not team_id:
        cursor.execute("INSERT INTO teams (team_name) VALUES (%s) RETURNING team_id", (team_name,))
        team_id = cursor.fetchone()[0]
    else:
        team_id = team_id[0]
    return team_id

def insert_match(match_id, match_date, home_team, away_team, league, statistics):
    """Inserts or updates match data into the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get or create league ID
        league_id = get_or_create_league_id(cursor, league)
        
        # Get or create team IDs
        home_team_id = get_or_create_team_id(cursor, home_team)
        away_team_id = get_or_create_team_id(cursor, away_team)

        # Clean up all the statistics before inserting.
        cleaned_statistics = {key: clean_stat_value(value) for key, value in statistics.items()}

        # Check if the match ID already exists
        cursor.execute("SELECT match_id FROM match_statistics WHERE match_id = %s", (match_id,))
        existing_match = cursor.fetchone()

        if existing_match:
            # Update the existing match details
            cursor.execute("""
                UPDATE match_statistics
                SET date = %s, league_id = %s, home_team_id = %s, away_team_id = %s,
                    ball_possession_home = %s, ball_possession_away = %s,
                    expected_goals_home = %s, expected_goals_away = %s,
                    big_chances_home = %s, big_chances_away = %s,
                    total_shots_home = %s, total_shots_away = %s,
                    shots_on_target_home = %s, shots_on_target_away = %s,
                    shots_off_target_home = %s, shots_off_target_away = %s,
                    blocked_shots_home = %s, blocked_shots_away = %s,
                    goalkeeper_saves_home = %s, goalkeeper_saves_away = %s,
                    corner_kicks_home = %s, corner_kicks_away = %s,
                    fouls_home = %s, fouls_away = %s,
                    passes_home = %s, passes_away = %s,
                    tackles_home = %s, tackles_away = %s,
                    free_kicks_home = %s, free_kicks_away = %s,
                    yellow_cards_home = %s, yellow_cards_away = %s,
                    red_cards_home = %s, red_cards_away = %s,
                    hit_woodwork_home = %s, hit_woodwork_away = %s,
                    shots_inside_box_home = %s, shots_inside_box_away = %s,
                    shots_outside_box_home = %s, shots_outside_box_away = %s,
                    big_chances_scored_home = %s, big_chances_scored_away = %s,
                    big_chances_missed_home = %s, big_chances_missed_away = %s,
                    through_balls_home = %s, through_balls_away = %s,
                    touches_in_penalty_area_home = %s, touches_in_penalty_area_away = %s,
                    fouled_in_final_third_home = %s, fouled_in_final_third_away = %s,
                    offsides_home = %s, offsides_away = %s,
                    accurate_passes_home = %s, accurate_passes_away = %s,
                    throw_ins_home = %s, throw_ins_away = %s,
                    final_third_entries_home = %s, final_third_entries_away = %s,
                    accurate_long_balls_home = %s, accurate_long_balls_away = %s,
                    accurate_crosses_home = %s, accurate_crosses_away = %s,
                    duels_home = %s, duels_away = %s,
                    dispossessed_home = %s, dispossessed_away = %s,
                    ground_duels_home = %s, ground_duels_away = %s,
                    aerial_duels_home = %s, aerial_duels_away = %s,
                    dribbles_home = %s, dribbles_away = %s,
                    tackles_won_home = %s, tackles_won_away = %s,
                    interceptions_home = %s, interceptions_away = %s,
                    recoveries_home = %s, recoveries_away = %s,
                    clearances_home = %s, clearances_away = %s,
                    goals_prevented_home = %s, goals_prevented_away = %s,
                    high_claims_home = %s, high_claims_away = %s,
                    goal_kicks_home = %s, goal_kicks_away = %s
                WHERE match_id = %s
            """, (
                match_date, league_id, home_team_id, away_team_id,
                cleaned_statistics.get("ball possession_home", 'N/A'),
                cleaned_statistics.get("ball possession_away", 'N/A'),
                cleaned_statistics.get("expected goals_home", 'N/A'),
                cleaned_statistics.get("expected goals_away", 'N/A'),
                cleaned_statistics.get("big chances_home", 'N/A'),
                cleaned_statistics.get("big chances_away", 'N/A'),
                cleaned_statistics.get("total shots_home", 'N/A'),
                cleaned_statistics.get("total shots_away", 'N/A'),
                cleaned_statistics.get("shots on target_home", 'N/A'),
                cleaned_statistics.get("shots on target_away", 'N/A'),
                cleaned_statistics.get("shots off target_home", 'N/A'),
                cleaned_statistics.get("shots off target_away", 'N/A'),
                cleaned_statistics.get("blocked shots_home", 'N/A'),
                cleaned_statistics.get("blocked shots_away", 'N/A'),
                cleaned_statistics.get("goalkeeper saves_home", 'N/A'),
                cleaned_statistics.get("goalkeeper saves_away", 'N/A'),
                cleaned_statistics.get("corner kicks_home", 'N/A'),
                cleaned_statistics.get("corner kicks_away", 'N/A'),
                cleaned_statistics.get("fouls_home", 'N/A'),
                cleaned_statistics.get("fouls_away", 'N/A'),
                cleaned_statistics.get("passes_home", 'N/A'),
                cleaned_statistics.get("passes_away", 'N/A'),
                cleaned_statistics.get("tackles_home", 'N/A'),
                cleaned_statistics.get("tackles_away", 'N/A'),
                cleaned_statistics.get("free kicks_home", 'N/A'),
                cleaned_statistics.get("free kicks_away", 'N/A'),
                cleaned_statistics.get("yellow cards_home", 'N/A'),
                cleaned_statistics.get("yellow cards_away", 'N/A'),
                cleaned_statistics.get("red cards_home", 'N/A'),
                cleaned_statistics.get("red cards_away", 'N/A'),
                cleaned_statistics.get("hit woodwork_home", 'N/A'),
                cleaned_statistics.get("hit woodwork_away", 'N/A'),
                cleaned_statistics.get("shots inside box_home", 'N/A'),
                cleaned_statistics.get("shots inside box_away", 'N/A'),
                cleaned_statistics.get("shots outside box_home", 'N/A'),
                cleaned_statistics.get("shots outside box_away", 'N/A'),
                cleaned_statistics.get("big chances scored_home", 'N/A'),
                cleaned_statistics.get("big chances scored_away", 'N/A'),
                cleaned_statistics.get("big chances missed_home", 'N/A'),
                cleaned_statistics.get("big chances missed_away", 'N/A'),
                cleaned_statistics.get("through balls_home", 'N/A'),
                cleaned_statistics.get("through balls_away", 'N/A'),
                cleaned_statistics.get("touches in penalty area_home", 'N/A'),
                cleaned_statistics.get("touches in penalty area_away", 'N/A'),
                cleaned_statistics.get("fouled in final third_home", 'N/A'),
                cleaned_statistics.get("fouled in final third_away", 'N/A'),
                cleaned_statistics.get("offsides_home", 'N/A'),
                cleaned_statistics.get("offsides_away", 'N/A'),
                cleaned_statistics.get("accurate passes_home", 'N/A'),
                cleaned_statistics.get("accurate passes_away", 'N/A'),
                cleaned_statistics.get("throw-ins_home", 'N/A'),
                cleaned_statistics.get("throw-ins_away", 'N/A'),
                cleaned_statistics.get("final third entries_home", 'N/A'),
                cleaned_statistics.get("final third entries_away", 'N/A'),
                cleaned_statistics.get("accurate long balls_home", 'N/A'),
                cleaned_statistics.get("accurate long balls_away", 'N/A'),
                cleaned_statistics.get("accurate crosses_home", 'N/A'),
                cleaned_statistics.get("accurate crosses_away", 'N/A'),
                cleaned_statistics.get("duels_home", 'N/A'),
                cleaned_statistics.get("duels_away", 'N/A'),
                cleaned_statistics.get("dispossessed_home", 'N/A'),
                cleaned_statistics.get("dispossessed_away", 'N/A'),
                cleaned_statistics.get("ground duels_home", 'N/A'),
                cleaned_statistics.get("ground duels_away", 'N/A'),
                cleaned_statistics.get("aerial duels_home", 'N/A'),
                cleaned_statistics.get("aerial duels_away", 'N/A'),
                cleaned_statistics.get("dribbles_home", 'N/A'),
                cleaned_statistics.get("dribbles_away", 'N/A'),
                cleaned_statistics.get("tackles won_home", 'N/A'),
                cleaned_statistics.get("tackles won_away", 'N/A'),
                cleaned_statistics.get("interceptions_home", 'N/A'),
                cleaned_statistics.get("interceptions_away", 'N/A'),
                cleaned_statistics.get("recoveries_home", 'N/A'),
                cleaned_statistics.get("recoveries_away", 'N/A'),
                cleaned_statistics.get("clearances_home", 'N/A'),
                cleaned_statistics.get("clearances_away", 'N/A'),
                cleaned_statistics.get("goals prevented_home", 'N/A'),
                cleaned_statistics.get("goals prevented_away", 'N/A'),
                cleaned_statistics.get("high claims_home", 'N/A'),
                cleaned_statistics.get("high claims_away", 'N/A'),
                cleaned_statistics.get("goal kicks_home", 'N/A'),
                cleaned_statistics.get("goal kicks_away", 'N/A'),
                match_id
            ))
            conn.commit()
            print(f"UPDATED Match {match_id} successfully.")
        else:
            # Insert new match if it does not exist
            cursor.execute("""
                INSERT INTO match_statistics (
                    match_id, date, league_id, home_team_id, away_team_id,
                    ball_possession_home, ball_possession_away, expected_goals_home, expected_goals_away,
                    big_chances_home, big_chances_away, total_shots_home, total_shots_away,
                    shots_on_target_home, shots_on_target_away, shots_off_target_home, shots_off_target_away,
                    blocked_shots_home, blocked_shots_away, goalkeeper_saves_home, goalkeeper_saves_away,
                    corner_kicks_home, corner_kicks_away, fouls_home, fouls_away,
                    passes_home, passes_away, tackles_home, tackles_away, free_kicks_home, free_kicks_away,
                    yellow_cards_home, yellow_cards_away, red_cards_home, red_cards_away, hit_woodwork_home,
                    hit_woodwork_away, shots_inside_box_home, shots_inside_box_away, shots_outside_box_home,
                    shots_outside_box_away, big_chances_scored_home, big_chances_scored_away,
                    big_chances_missed_home, big_chances_missed_away, through_balls_home, through_balls_away,
                    touches_in_penalty_area_home, touches_in_penalty_area_away, fouled_in_final_third_home,
                    fouled_in_final_third_away, offsides_home, offsides_away, accurate_passes_home,
                    accurate_passes_away, throw_ins_home, throw_ins_away, final_third_entries_home,
                    final_third_entries_away, accurate_long_balls_home, accurate_long_balls_away,
                    accurate_crosses_home, accurate_crosses_away, duels_home, duels_away, dispossessed_home,
                    dispossessed_away, ground_duels_home, ground_duels_away, aerial_duels_home, aerial_duels_away,
                    dribbles_home, dribbles_away, tackles_won_home, tackles_won_away, interceptions_home,
                    interceptions_away, recoveries_home, recoveries_away, clearances_home, clearances_away,
                    goals_prevented_home, goals_prevented_away, high_claims_home, high_claims_away,
                    goal_kicks_home, goal_kicks_away
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                match_id, match_date, league_id, home_team_id, away_team_id,
                cleaned_statistics.get("ball possession_home", 'N/A'),
                cleaned_statistics.get("ball possession_away", 'N/A'),
                cleaned_statistics.get("expected goals_home", 'N/A'),
                cleaned_statistics.get("expected goals_away", 'N/A'),
                cleaned_statistics.get("big chances_home", 'N/A'),
                cleaned_statistics.get("big chances_away", 'N/A'),
                cleaned_statistics.get("total shots_home", 'N/A'),
                cleaned_statistics.get("total shots_away", 'N/A'),
                cleaned_statistics.get("shots on target_home", 'N/A'),
                cleaned_statistics.get("shots on target_away", 'N/A'),
                cleaned_statistics.get("shots off target_home", 'N/A'),
                cleaned_statistics.get("shots off target_away", 'N/A'),
                cleaned_statistics.get("blocked shots_home", 'N/A'),
                cleaned_statistics.get("blocked shots_away", 'N/A'),
                cleaned_statistics.get("goalkeeper saves_home", 'N/A'),
                cleaned_statistics.get("goalkeeper saves_away", 'N/A'),
                cleaned_statistics.get("corner kicks_home", 'N/A'),
                cleaned_statistics.get("corner kicks_away", 'N/A'),
                cleaned_statistics.get("fouls_home", 'N/A'),
                cleaned_statistics.get("fouls_away", 'N/A'),
                cleaned_statistics.get("passes_home", 'N/A'),
                cleaned_statistics.get("passes_away", 'N/A'),
                cleaned_statistics.get("tackles_home", 'N/A'),
                cleaned_statistics.get("tackles_away", 'N/A'),
                cleaned_statistics.get("free kicks_home", 'N/A'),
                cleaned_statistics.get("free kicks_away", 'N/A'),
                cleaned_statistics.get("yellow cards_home", 'N/A'),
                cleaned_statistics.get("yellow cards_away", 'N/A'),
                cleaned_statistics.get("red cards_home", 'N/A'),
                cleaned_statistics.get("red cards_away", 'N/A'),
                cleaned_statistics.get("hit woodwork_home", 'N/A'),
                cleaned_statistics.get("hit woodwork_away", 'N/A'),
                cleaned_statistics.get("shots inside box_home", 'N/A'),
                cleaned_statistics.get("shots inside box_away", 'N/A'),
                cleaned_statistics.get("shots outside box_home", 'N/A'),
                cleaned_statistics.get("shots outside box_away", 'N/A'),
                cleaned_statistics.get("big chances scored_home", 'N/A'),
                cleaned_statistics.get("big chances scored_away", 'N/A'),
                cleaned_statistics.get("big chances missed_home", 'N/A'),
                cleaned_statistics.get("big chances missed_away", 'N/A'),
                cleaned_statistics.get("through balls_home", 'N/A'),
                cleaned_statistics.get("through balls_away", 'N/A'),
                cleaned_statistics.get("touches in penalty area_home", 'N/A'),
                cleaned_statistics.get("touches in penalty area_away", 'N/A'),
                cleaned_statistics.get("fouled in final third_home", 'N/A'),
                cleaned_statistics.get("fouled in final third_away", 'N/A'),
                cleaned_statistics.get("offsides_home", 'N/A'),
                cleaned_statistics.get("offsides_away", 'N/A'),
                cleaned_statistics.get("accurate passes_home", 'N/A'),
                cleaned_statistics.get("accurate passes_away", 'N/A'),
                cleaned_statistics.get("throw-ins_home", 'N/A'),
                cleaned_statistics.get("throw-ins_away", 'N/A'),
                cleaned_statistics.get("final third entries_home", 'N/A'),
                cleaned_statistics.get("final third entries_away", 'N/A'),
                cleaned_statistics.get("accurate long balls_home", 'N/A'),
                cleaned_statistics.get("accurate long balls_away", 'N/A'),
                cleaned_statistics.get("accurate crosses_home", 'N/A'),
                cleaned_statistics.get("accurate crosses_away", 'N/A'),
                cleaned_statistics.get("duels_home", 'N/A'),
                cleaned_statistics.get("duels_away", 'N/A'),
                cleaned_statistics.get("dispossessed_home", 'N/A'),
                cleaned_statistics.get("dispossessed_away", 'N/A'),
                cleaned_statistics.get("ground duels_home", 'N/A'),
                cleaned_statistics.get("ground duels_away", 'N/A'),
                cleaned_statistics.get("aerial duels_home", 'N/A'),
                cleaned_statistics.get("aerial duels_away", 'N/A'),
                cleaned_statistics.get("dribbles_home", 'N/A'),
                cleaned_statistics.get("dribbles_away", 'N/A'),
                cleaned_statistics.get("tackles won_home", 'N/A'),
                cleaned_statistics.get("tackles won_away", 'N/A'),
                cleaned_statistics.get("interceptions_home", 'N/A'),
                cleaned_statistics.get("interceptions_away", 'N/A'),
                cleaned_statistics.get("recoveries_home", 'N/A'),
                cleaned_statistics.get("recoveries_away", 'N/A'),
                cleaned_statistics.get("clearances_home", 'N/A'),
                cleaned_statistics.get("clearances_away", 'N/A'),
                cleaned_statistics.get("goals prevented_home", 'N/A'),
                cleaned_statistics.get("goals prevented_away", 'N/A'),
                cleaned_statistics.get("high claims_home", 'N/A'),
                cleaned_statistics.get("high claims_away", 'N/A'),
                cleaned_statistics.get("goal kicks_home", 'N/A'),
                cleaned_statistics.get("goal kicks_away", 'N/A')
            ))
            conn.commit()
            print(f"▄▖▖▖▄▖▄▖▄▖▄▖▄▖▄▖▖▖▖ ▖ ▖▖")
            print(f"▚ ▌▌▌ ▌ ▙▖▚ ▚ ▙▖▌▌▌ ▌ ▌▌")
            print( "▄▌▙▌▙▖▙▖▙▖▄▌▄▌▌ ▙▌▙▖▙▖▐ Inserted Match {match_id}.")

    except Exception as e:
        print(f"ERROR Inserting Match {match_id}: {e}")

    finally:
        cursor.close()
        conn.close()
