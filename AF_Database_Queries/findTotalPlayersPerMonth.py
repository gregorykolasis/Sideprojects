try:
    import pymysql
except Exception as e:
    import os
    os.system("pip install pymysql")
from datetime import datetime

# Example of database configuration
db_config = {
    'host'     : 'localhost',
    'db'       : 'agent_factory',  
    'user'     : 'python_user',     # root , python_user
    'password' : 'Mindtr@p123'      #      , Mindtr@p123
}

def tryConnection():
    # Create a connection to the MySQL database using PyMySQL
    connection = pymysql.connect(
        host=db_config['host'],
        db=db_config['db'],  # Use 'db' instead of 'database'
        user=db_config['user'],
        password=db_config['password'],
        cursorclass=pymysql.cursors.DictCursor  # Optional for dictionary-like results
    )
    return connection

def get_players_for_month(db_config, month, year):
    try:
        if connection.open:
            # Create a cursor to execute the query
            cursor = connection.cursor()

            # Convert month and year into start and end dates
            start_date = f'{year}-{month:02d}-01'
            end_date = f'{year}-{month:02d}-{(datetime(year, month, 1).replace(month=month+1) - datetime(year, month, 1)).days}'

            # SQL query with dynamic date range
            query = f"""
            SELECT DISTINCT p.id, p.name, p.username, p.email
            FROM player p
            JOIN roster_player rp ON p.id = rp.player_id
            JOIN roster r ON rp.roster_id = r.id
            JOIN team t ON r.team_id = t.id
            JOIN game g ON t.id = g.team_id
            WHERE g.created BETWEEN '{start_date}' AND '{end_date}'
              AND g.game_status IN ('WIN', 'LOSE')
              AND t.last_register_attempt_time BETWEEN '{start_date}' AND '{end_date}'
              AND LOWER(t.name) NOT LIKE '%test%'
              AND t.total_points > 0
              AND (p.created BETWEEN '{start_date}' AND '{end_date}' 
                   OR p.updated BETWEEN '{start_date}' AND '{end_date}')
            GROUP BY p.id, p.name, p.username, p.email
            HAVING COUNT(g.id) > 5;
            """

            # Execute the query to fetch the players
            cursor.execute(query)
            result = cursor.fetchall()

            # Print the total number of players found
            total_players = len(result)
            print(f"\nTotal Players Found: {total_players} for Month {month} on Year {year}\n")

            # Ask if the user wants more details
            if total_players > 0:
                show_details = input("Do you want to see more details for each player? (Y/N): ").strip().upper()
                if show_details == 'Y':
                    print("\nPlayer Details:")
                    for row in result:
                        print(f"ID: {row['id']}, Name: {row['name']}, Username: {row['username']}, Email: {row['email']}")
                else:
                    print("No detailed information will be shown.")

    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")

    finally:
        if connection and connection.open:
            cursor.close()
            connection.close()
            #print("MySQL connection closed")

try:
    connection = None
    connection = tryConnection()
    # Wait for user input for month and year
    month = int(input("Enter the month (1-12): "))
    year = int(input("Enter the year (e.g., 2024): "))
    # Run the query for the user-specified month and year
    get_players_for_month(db_config, month, year)
except Exception as e:
    print(e)
    while True:
        x=0