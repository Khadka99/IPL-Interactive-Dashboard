import sqlite3
import pandas as pd

class DB:
    def __init__(self):
        try:
            # Load the local dataset (CSV file)
            self.ipl = pd.read_csv("ipl.csv")

            # Create an in-memory SQLite database
            self.conn = sqlite3.connect(":memory:")
            self.mycursor = self.conn.cursor()

            # Load the dataset into the SQLite database
            self.ipl.to_sql("ipl", self.conn, index=False, if_exists="replace")
            print('Local dataset loaded into SQLite in-memory database')
        except Exception as e:
            print(f'Error: {e}')

    def fetch_player_name(self):
        """Fetch all unique players (batters and bowlers) from the dataset."""
        query = """
            SELECT DISTINCT batter AS player 
            FROM ipl
            UNION
            SELECT DISTINCT bowler
            FROM ipl
            ORDER BY player
        """
        self.mycursor.execute(query)
        return [row[0] for row in self.mycursor.fetchall()]

    def fetch_bowler_name(self):
        """Fetch all unique bowlers from the dataset."""
        query = """
            SELECT DISTINCT bowler 
            FROM ipl
            ORDER BY bowler
        """
        self.mycursor.execute(query)
        return [row[0] for row in self.mycursor.fetchall()]

    def batsman_details(self, player):
        """Fetch batting details for a specific player."""
        query = """
            SELECT 
                bowling_team AS 'Against', 
                SUM(batsman_runs) AS 'Run_scored',
                ROUND(SUM(batsman_runs) * 1.0 / COUNT(DISTINCT id), 2) AS 'Average',
                COUNT(DISTINCT id) AS 'Match_played',
                COUNT(ball) AS 'Ball_played',
                ROUND(SUM(batsman_runs) * 100.0 / COUNT(ball), 2) AS 'Sr',
                SUM(CASE WHEN batsman_runs = 4 THEN 1 ELSE 0 END) AS 'Fours',
                SUM(CASE WHEN batsman_runs = 6 THEN 1 ELSE 0 END) AS 'Sixs'
            FROM ipl
            WHERE batter = ?
            GROUP BY bowling_team
        """
        self.mycursor.execute(query, (player,))
        return self.mycursor.fetchall()

    def bowler_details(self, bowler):
        """Fetch bowling details for a specific bowler."""
        query = """
            SELECT 
                batting_team AS 'Opponent',
                COUNT(DISTINCT id) AS 'Match_Played',
                SUM(wickets_per_match) AS 'Total_Wicket',
                SUM(overs_per_match) AS 'Total_Overs',
                ROUND(SUM(maiden_balls) / 6.0) AS 'Maiden',
                SUM(total_runs_per_match) AS 'Runs_Conceded',
                ROUND(SUM(total_runs_per_match) * 1.0 / SUM(overs_per_match), 2) AS 'Economy'
            FROM (
                SELECT 
                    batting_team,
                    id,
                    COUNT(bowler_wicket) AS wickets_per_match,
                    COUNT(DISTINCT `over`) AS overs_per_match,
                    SUM(maiden) AS maiden_balls,
                    SUM(total_runs) AS total_runs_per_match
                FROM ipl
                WHERE bowler = ?
                GROUP BY batting_team, id
            ) AS match_stats
            GROUP BY batting_team
        """
        self.mycursor.execute(query, (bowler,))
        return self.mycursor.fetchall()

    def fetch_team(self):
        """Fetch all unique teams from the dataset."""
        query = """
            SELECT DISTINCT batting_team 
            FROM ipl
        """
        self.mycursor.execute(query)
        return [row[0] for row in self.mycursor.fetchall()]

    def fetch_toss_decision(self):
        """Fetch all unique toss decisions from the dataset."""
        query = """
            SELECT DISTINCT toss_decision 
            FROM ipl
        """
        self.mycursor.execute(query)
        return [row[0] for row in self.mycursor.fetchall()]

    def head_to_head_compare(self, toss_decision, batting_team, bowling_team, toss_winner):
        """Compare head-to-head stats based on toss decision, teams, and toss winner."""
        query = """
            SELECT 
                toss_winner AS 'Toss Winner',
                toss_decision AS 'Toss Decision',
                winner AS 'Winner',
                COUNT(DISTINCT id) AS 'Total Wins',
                SUM(COUNT(DISTINCT id)) OVER(PARTITION BY toss_winner) AS 'Total Game'
            FROM ipl
            WHERE toss_decision = ? 
                AND batting_team = ? 
                AND bowling_team = ? 
                AND toss_winner = ?
            GROUP BY toss_winner, toss_decision, winner
        """
        params = (toss_decision, batting_team, bowling_team, toss_winner)
        self.mycursor.execute(query, params)
        return self.mycursor.fetchall()

    def team_against_all(self, bowling_team, winner):
        """Fetch team performance against all opponents."""
        query = """
            SELECT 
                t.winner AS 'Winner', 
                t.oponent AS 'Opponent', 
                COUNT(*) AS 'Total Win'
            FROM (
                SELECT DISTINCT id, bowling_team, batting_team AS oponent, winner
                FROM ipl
                WHERE bowling_team = ? AND winner = ?
                ORDER BY bowling_team, winner, batting_team
            ) t
            GROUP BY t.bowling_team, t.oponent, t.winner
        """
        params = (bowling_team, winner)
        self.mycursor.execute(query, params)
        return self.mycursor.fetchall()

    def player_of_match(self):
        query = """
        SELECT 
            player_of_match AS 'Name', 
            COUNT(*) AS 'Total'
        FROM (
            SELECT DISTINCT id, player_of_match
            FROM ipl
        ) AS match_player
        GROUP BY player_of_match
        ORDER BY COUNT(*) DESC
        """
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def top_batter(self):
        query = """
                SELECT batter,sum(batsman_runs) AS 'Total Run' 
                FROM ipl
                GROUP BY batter
                ORDER BY `Total Run` DESC
                limit 10
        """
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def top_bowler(self):
        query = """
                SELECT bowler, sum(is_wicket) AS 'total_wicket'
                 FROM ipl
                 WHERE dismissal_kind = 'cought' OR dismissal_kind = 'bowled' OR 
                 dismissal_kind = 'run_out' OR dismissal_kind = 'lbw' OR 
                 dismissal_kind = 'stumped' OR dismissal_kind = 'caught and bowled' OR
                 dismissal_kind = 'hit wicket'
                GROUP BY bowler
                ORDER BY total_wicket DESC
                LIMIT 10;
        """
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def top_fielder(self):
        query = """
                SELECT fielder,count(*) AS 'Total Wicket'
                FROM ipl
                WHERE dismissal_kind = 'caught' OR  dismissal_kind = 'run out' AND fielder IS NOT NULL
                GROUP BY fielder
                ORDER BY count(dismissal_kind) DESC
                LIMIT 10
        """
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def total_run_by_teams(self):
        query = """
        SELECT batting_team AS 'Teams', SUM(total_runs) AS 'Total Runs'
        FROM ipl
        GROUP BY batting_team
        ORDER BY SUM(total_runs) DESC
        """
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def top_4_hitter(self):
        query = """
                SELECT batter AS 'Batter',count(*) AS 'Total' 
                FROM ipl
                WHERE batsman_runs = 4
                GROUP BY batter
                ORDER BY count(*) DESC
                LIMIT 10
        """
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def top_6_hitter(self):
        query = """
                SELECT batter AS 'Batter',count(*) AS 'Total' 
                FROM ipl
                WHERE batsman_runs = 6
                GROUP BY batter
                ORDER BY count(*) DESC
                LIMIT 10
        """
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def season_winners(self):
        query = """
                SELECT DISTINCT season AS 'Seasons', season_winner AS 'Winner' 
                FROM ipl
        """
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def win_type_distribution(self):
        query = """
                SELECT result AS 'Result',
                    SUM(CASE WHEN result = 'runs' THEN 1 ELSE 0 END) AS 'Runs',  
                    SUM(CASE WHEN result = 'wickets' THEN 1 ELSE 0 END) AS 'Wickets',
                    SUM(CASE WHEN result = 'tie' THEN 1 ELSE 0 END) AS 'Tie',
                    SUM(CASE WHEN result = 'no result' THEN 1 ELSE 0 END) AS 'No_Resuls'
                    FROM (
                        SELECT DISTINCT id, result
                        FROM ipl
                    ) AS results
                GROUP BY result
        """
        self.mycursor.execute(query)
        return self.mycursor.fetchall()



