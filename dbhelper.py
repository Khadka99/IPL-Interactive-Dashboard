import mysql.connector
import os
import pandas as pd

#ipl = pd.read_csv("ipl.csv")

class DB:

    def __init__(self):

        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='adhya',
                database='revision'
                )
            self.mycursor = self.conn.cursor()
            print('Connection established')
        except:
            print('connection error')


    def fetch_player_name(self):

        players = []
        self.mycursor.execute("""
                    SELECT DISTINCT batter 
                    FROM ipl
                    UNION
                    SELECT DISTINCT bowler
                    FROM ipl
                    ORDER BY batter
                    """)

        data = self.mycursor.fetchall()

        for items in data:
            players.append(items[0])
        return players

    def fetch_bowler_name(self):

        bowlers = []
        self.mycursor.execute("""
                    SELECT DISTINCT batter 
                    FROM ipl
                    UNION
                    SELECT DISTINCT bowler
                    FROM ipl
                    ORDER BY batter
                    """)

        data = self.mycursor.fetchall()

        for items in data:
            bowlers.append(items[0])
        return bowlers


    def batsman_details(self,players):
        self.mycursor.execute("""
             SELECT bowling_team AS 'Against', SUM(batsman_runs) AS 'Run_scored'
             ,ROUND(SUM(batsman_runs) / COUNT(DISTINCT id),2)  AS 'Average'
            ,COUNT(DISTINCT id) AS 'Match_played',COUNT(ball) AS 'Ball_played'
            , ROUND(SUM(batsman_runs) * 100 / COUNT(ball),2) as 'Sr'
            ,COUNT(4s) AS 'Fours',COUNT(6s) AS 'Sixs'
            FROM ipl
            WHERE batter = '{}'
            GROUP BY bowling_team  
            """.format(players))
        data = self.mycursor.fetchall()
        return data

    def bowler_details(self,bowlers):
        self.mycursor.execute("""
            SELECT 
                batting_team AS 'Opponent',
                COUNT(DISTINCT id) AS 'Match Played',
                SUM(wickets_per_match) AS 'Total Wicket',
                SUM(overs_per_match) AS 'Total Overs',  
                ROUND(SUM(maiden_balls) / 6) AS 'Maiden', 
                SUM(total_runs_per_match) AS 'Runs Conceded',
                ROUND(SUM(total_runs_per_match)/SUM(overs_per_match),2) AS 'Economy'
            FROM (
                SELECT 
                    batting_team,
                    id,
                    COUNT(bowler_wicket) AS wickets_per_match,
                    COUNT(DISTINCT `over`) AS overs_per_match,  -- Overs per match
                    COUNT(maiden) AS maiden_balls,  -- Total balls in maiden overs
                    SUM(total_runs) AS total_runs_per_match
                FROM ipl
                WHERE bowler = '{}'
                GROUP BY batting_team, id
            ) AS match_stats
            GROUP BY batting_team
                    """.format(bowlers))
        data = self.mycursor.fetchall()
        return data

    def fetch_team(self):
        teams = []
        self.mycursor.execute("""
        SELECT DISTINCT batting_team FROM ipl
        """)

        data = self.mycursor.fetchall()
        for items in data:
            teams.append(items[0])
        return teams

    def fetch_toss_decision(self):
        toss = []

        self.mycursor.execute("""
        SELECT DISTINCT toss_decision FROM ipl
        """)

        data = self.mycursor.fetchall()

        for items in data:
            toss.append(items[0])
        return toss

    def head_to_head_compare(self, toss_decision, batting_team, bowling_team, toss_winner):
        query = """
            SELECT toss_winner AS 'Toss Winner',
                   toss_decision AS 'Toss Decision',
                   winner AS 'Winner',
                   COUNT(DISTINCT id) AS 'Total Wins',
                   SUM(COUNT(DISTINCT id)) OVER(PARTITION BY toss_winner) AS 'Total Game'
            FROM ipl
            WHERE toss_decision = '{}' AND batting_team = '{}' AND bowling_team = '{}' AND toss_winner = '{}'
            GROUP BY batting_team, bowling_team, winner, toss_decision, toss_winner
        """.format(toss_decision, batting_team, bowling_team, toss_winner)

        self.mycursor.execute(query)
        data = self.mycursor.fetchall()
        return data


    def team_against_all(self, bowling_team, winner):
        query = """
            SELECT t.winner AS 'Winner', t.oponent AS 'Opponent', COUNT(*) AS 'Total Win'
            FROM (
                SELECT DISTINCT id, bowling_team, batting_team AS oponent, winner
                FROM ipl
                WHERE bowling_team = %s AND winner = %s
                ORDER BY bowling_team, winner, batting_team
            ) t
            GROUP BY t.bowling_team, t.oponent, t.winner
        """
        params = (bowling_team, winner)
        self.mycursor.execute(query, params)
        data = self.mycursor.fetchall()
        return data
