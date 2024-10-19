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

def insert_match(match_id, match_date, home_team, away_team, league, home_score, away_score):
    """Inserts match data into the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get or create league ID
        league_id = get_or_create_league_id(cursor, league)
        
        # Get or create team IDs
        home_team_id = get_or_create_team_id(cursor, home_team)
        away_team_id = get_or_create_team_id(cursor, away_team)

        # Insert the match data
        cursor.execute("""
            INSERT INTO matches (match_id, date, league_id, home_team_id, away_team_id, home_score, away_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (match_id) DO NOTHING
        """, (
            match_id,
            match_date,
            league_id,
            home_team_id,
            away_team_id,
            home_score,
            away_score
        ))

        conn.commit()
        print(f"Match {match_id} inserted successfully.")

    except Exception as e:
        print(f"Error inserting match {match_id}: {e}")

    finally:
        cursor.close()
        conn.close()
