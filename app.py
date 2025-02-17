import streamlit as st
import pandas as pd
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px

#analysis_type = st.sidebar.radio("Select Analysis Type", ["Player Analysis", "Team Analysis", "Overall Analysis"])
st.set_page_config(layout='wide')

db = DB()

st.sidebar.title("IPL Analysis")
analysis_type = st.sidebar.radio("Select Analysis Type", ["Player Analysis", "Team Analysis"])

if analysis_type == "Player Analysis":
    st.title('Player Analysis')

    # Player type selection
    player_type = st.sidebar.radio("Select Player Type", ["Batter", "Bowler"])

    if player_type == 'Batter':
        st.header('Batter Analysis')

        # Fetch player names from the database
        players = db.fetch_player_name()

        # Dropdown to select a player
        selected_player = st.sidebar.selectbox('Select Batter', sorted(players))

       # Button to search for player details
        if st.sidebar.button('Search'):
            st.write(f'Selected Batter: {selected_player}')

            # Fetch player details from the database
            result = db.batsman_details(selected_player)

            # Define column names for the DataFrame
            columns = ["Against", "Runs Scored", "Matches Played","Average", "Balls Played", "Strike Rate", "Fours", "Sixes"]

            if result:
                # Create a DataFrame and display it
                df = pd.DataFrame(result, columns=columns)
                st.dataframe(df)
            else:
                st.write("No details found for the selected batter.")

    elif player_type == 'Bowler':
        st.title('Bowler Analysis')
        #st.write("Bowler analysis functionality will be added here.")

        bowlers = db.fetch_bowler_name()

        # Dropdown to select a player
        selected_bowler = st.sidebar.selectbox('Select Bowler', sorted(bowlers))

        # Button to search for player details
        if st.sidebar.button('Search'):
            st.write(f'Selected bowler: {selected_bowler}')

            # Fetch player details from the database
            results = db.bowler_details(selected_bowler)

            # Define column names for the DataFrame
            columns = ["Opponent", "Match Played", "Total Wicket", "Total Overs", "Maiden", "Runs Conceded", "Economy"]

            if results:
                # Create a DataFrame and display it
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)
            else:
                st.write("No details found for the selected bowler.")


else:
    st.title("Team Analysis")

    # Add a sub-selection for the type of team analysis
    team_analysis_choice = st.sidebar.radio("Select Team Analysis", ["Team Against All", "Head To Head"])
    teams = db.fetch_team()
    toss = db.fetch_toss_decision()  # For head-to-head analysis


    if team_analysis_choice == "Team Against All":
        select_team = st.selectbox("Select Team", sorted(teams))

        if st.button('Search Team Against All'):
            result = db.team_against_all(select_team, select_team)
            columns = ['Winner', 'Opponent', 'Total Win']
            if result:
                df = pd.DataFrame(result, columns=columns)
                st.dataframe(df)
            else:
                st.write("No Data Found.")

    elif team_analysis_choice == "Head To Head":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            toss_decision = st.selectbox("Select Toss Decision", sorted(toss))
        with col2:
            team1 = st.selectbox("Select Team 1", sorted(teams))
        with col3:
            team2 = st.selectbox("Select Team 2", sorted(teams))
        with col4:
            toss_winner = st.selectbox("Select Toss Winner", sorted(teams))

        if st.button('Search Head-to-Head'):
            result = db.head_to_head_compare(toss_decision, team1, team2, toss_winner)
            columns = ['Toss Winner', 'Toss Decision', 'Winner', 'Total Wins', 'Total Game']
            if result:
                df = pd.DataFrame(result, columns=columns)
                st.dataframe(df)
            else:
                st.write("No Data Found.")
