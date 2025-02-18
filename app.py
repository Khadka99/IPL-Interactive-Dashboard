import streamlit as st
import pandas as pd
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px


#analysis_type = st.sidebar.radio("Select Analysis Type", ["Player Analysis", "Team Analysis", "Overall Analysis"])
st.set_page_config(layout='wide')

db = DB()

st.sidebar.title("IPL Analysis")
analysis_type = st.sidebar.radio("Select Analysis Type", ["About Dashboard","Over-All", "Player Analysis", "Team Analysis"])

if analysis_type == "Over-All":
    st.title("Over All Analysis")

    over_all_analysis = st.sidebar.radio("Select Top 10", ["Player Of Match","Win Type Distribution","Batter", "Bowler","Fielder"])

    if over_all_analysis == "Player Of Match":
        #st.subheader("Top 10 Player Of The Match")

        if st.sidebar.button('Search'):
            # Fetch the top 10 players of the match
            player_of_match_data = db.player_of_match()

            # Convert the data into a pandas DataFrame
            df = pd.DataFrame(player_of_match_data, columns=["Player", "Total Awards"])

            # Display the top 10 players
            st.write("### Top 10 Players with Most 'Player of the Match' Awards")
            st.dataframe(df.head(10))

            # Create a bar chart using Plotly Express
            st.write("### Bar Chart: Top 10 Players of the Match")
            fig = px.bar(
                df.head(10),  # Use the top 10 players
                x="Player",  # Player names on the x-axis
                y="Total Awards",  # Total awards on the y-axis
                title="Top 10 Players of the Match",
                labels={"Player": "Player", "Total Awards": "Total Awards"},
                text="Total Awards",  # Display the total awards on top of the bars
                color="Total Awards",  # Color bars based on total awards
                color_continuous_scale=px.colors.sequential.Viridis  # Use a color scale
            )

            # Update layout for better readability
            fig.update_traces(textposition='outside')  # Position text outside the bars
            fig.update_layout(
                xaxis_title="Player",
                yaxis_title="Total Awards",
                showlegend=False,  # Hide the legend
                template="plotly_white", # Use a clean template
                width=800,  # Set the width of the figure
                height=500  # Set the height of the figure
            )

            # Remove gridlines
            fig.update_xaxes(showgrid=False)  # Remove x-axis gridlines
            fig.update_yaxes(showgrid=False)  # Remove y-axis gridlines
            # Display the chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)

    elif over_all_analysis == "Win Type Distribution":
        st.write("### Win Type")

        if st.sidebar.button('Search'):
            # Fetch the top 10 players of the match
            win_type = db.win_type_distribution()
            df = pd.DataFrame(win_type, columns=["Result", "Runs", "Wickets", "Tie", "No_Result"])
            df_melted = pd.melt(df, id_vars=["Result"], value_vars=["Runs", "Wickets", "Tie", "No_Result"],
                                var_name="Win Type", value_name="Count")

            # Define a dictionary to map Win Types to colors (or a list)
            color_map = {  # Or use a list: colors = ["red", "green", "blue", "purple"]
                "Runs": "blue",
                "Wickets": "green",
                "Tie": "orange",
                "No_Result": "gray"
            }

            fig = px.pie(
                df_melted,
                names="Win Type",
                values="Count",
                #title="Win Type Distribution",
                color="Win Type",  # Color based on Win Type
                color_discrete_map=color_map  # Or color_discrete_sequence=colors
            )

            fig.update_layout(
                template="plotly_white",
                width=800,
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)  # Only the pie chart is displayed

        else:
            st.write("No data found for win type distribution.")



    elif over_all_analysis == "Batter":

        if st.sidebar.button('Search'):
            # Fetch the top 10 batters
            top_batters_data = db.top_batter()

            # Convert the data into a pandas DataFrame
            df = pd.DataFrame(top_batters_data, columns=["Batter", "Total Runs"])

            # Display the top 10 batters
            st.write("### Top 10 Batters by Total Runs")
            st.dataframe(df)

            # Create a bar chart using Plotly Express
            st.write("### Bar Chart: Top 10 Batters")
            fig = px.bar(
                df,  # Use the top 10 batters data
                x="Batter",  # Batter names on the x-axis
                y="Total Runs",  # Total runs on the y-axis
                title="Top 10 Batters by Total Runs",
                labels={"Batter": "Batter", "Total Runs": "Total Runs"},
                text="Total Runs",  # Display the total runs on top of the bars
                color="Total Runs",  # Color bars based on total runs
                color_continuous_scale=px.colors.sequential.Viridis  # Use a color scale
            )

            # Update layout for better readability
            fig.update_traces(textposition='outside')  # Position text outside the bars
            fig.update_layout(
                xaxis_title="Batter",
                yaxis_title="Total Runs",
                showlegend=False,  # Hide the legend
                template="plotly_white",  # Use a clean template
                width = 800,  # Set the width of the figure
                height = 500  # Set the height of the figure
            )

            # Remove gridlines
            fig.update_xaxes(showgrid=False)  # Remove x-axis gridlines
            fig.update_yaxes(showgrid=False)  # Remove y-axis gridlines
            # Display the chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)

    elif over_all_analysis == "Bowler":
        # Fetch the top 10 bowlers
        top_bowlers_data = db.top_bowler()

        # Convert the data into a pandas DataFrame
        df = pd.DataFrame(top_bowlers_data, columns=["Bowler", "Total Wickets"])

        # Display the top 10 bowlers
        st.write("### Top 10 Bowlers by Total Wickets")
        st.dataframe(df)

        # Create a bar chart using Plotly Express
        st.write("### Bar Chart: Top 10 Bowlers")
        fig = px.bar(
            df,  # Use the top 10 bowlers data
            x="Bowler",  # Bowler names on the x-axis
            y="Total Wickets",  # Total wickets on the y-axis
            title="Top 10 Bowlers by Total Wickets",
            labels={"Bowler": "Bowler", "Total Wickets": "Total Wickets"},
            text="Total Wickets",  # Display the total wickets on top of the bars
            color="Total Wickets",  # Color bars based on total wickets
            color_continuous_scale=px.colors.sequential.Viridis  # Use a color scale
        )

        # Update layout for better readability and remove gridlines
        fig.update_traces(textposition='outside')  # Position text outside the bars
        fig.update_layout(
            xaxis_title="Bowler",
            yaxis_title="Total Wickets",
            showlegend=False,  # Hide the legend
            template="plotly_white",  # Use a clean template
            width=800,  # Set the width of the figure
            height=500  # Set the height of the figure
        )

        # Remove gridlines
        fig.update_xaxes(showgrid=False)  # Remove x-axis gridlines
        fig.update_yaxes(showgrid=False)  # Remove y-axis gridlines

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    elif over_all_analysis == "Fielder":

        if st.sidebar.button('Search'):
            # Fetch the top 10 fielders
            top_fielders_data = db.top_fielder()

            # Convert the data into a pandas DataFrame
            df = pd.DataFrame(top_fielders_data, columns=["Fielder", "Total Wickets"])

            # Display the top 10 fielders
            st.write("### Top 10 Fielders by Total Wickets")
            st.dataframe(df)

            # Create a bar chart using Plotly Express
            st.write("### Bar Chart: Top 10 Fielders")
            fig = px.bar(
                df,  # Use the top 10 fielders data
                x="Fielder",  # Fielder names on the x-axis
                y="Total Wickets",  # Total wickets on the y-axis
                title="Top 10 Fielders by Total Wickets",
                labels={"Fielder": "Fielder", "Total Wickets": "Total Wickets"},
                text="Total Wickets",  # Display the total wickets on top of the bars
                color="Total Wickets",  # Color bars based on total wickets
                color_continuous_scale=px.colors.sequential.Viridis  # Use a color scale
            )

            # Update layout for better readability and remove gridlines
            fig.update_traces(textposition='outside')  # Position text outside the bars
            fig.update_layout(
                xaxis_title="Fielder",
                yaxis_title="Total Wickets",
                showlegend=False,  # Hide the legend
                template="plotly_white",  # Use a clean template
                width=800,  # Set the width of the figure
                height=500  # Set the height of the figure
            )

            # Remove gridlines
            fig.update_xaxes(showgrid=False)  # Remove x-axis gridlines
            fig.update_yaxes(showgrid=False)  # Remove y-axis gridlines

            # Display the chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)



elif analysis_type == "About Dashboard":
    st.title("About Dashboard")
    st.write("""
        ### Welcome to the IPL Interactive Dashboard!
        This dashboard provides in-depth analysis of IPL matches, players, and teams. 
        You can explore:
        - **Player Statistics**: Batting and bowling performance of individual players.
        - **Team Statistics**: Performance of teams, including head-to-head comparisons.
        - **Toss Analysis**: Impact of toss decisions on match outcomes.

        Use the sidebar to navigate between different sections and customize your analysis.
        """)


elif analysis_type == "Player Analysis":
    st.title('Player Analysis')

    # Player type selection
    player_type = st.sidebar.radio("Select Player Type", ["Batter", "Bowler"])

    if player_type == 'Batter':
        st.header('Batter Analysis')

        batter_analysis = st.sidebar.radio("Select Analysis Type",["Batter","Most Fours","Most Sixes"])

        if batter_analysis == "Batter":
            st.subheader(" Over All Batter Analysis")

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


        elif batter_analysis == "Most Fours":

            if st.sidebar.button("Search"):
                top_hitters_data = db.top_4_hitter()  # Assuming 'db' is your database object

                if top_hitters_data:
                    df = pd.DataFrame(top_hitters_data, columns=["Batter", "Total"])  # Corrected column name

                    st.write("### Top 10 Four Hitters")
                    st.dataframe(df)

                    fig = px.bar(
                        df,
                        x="Batter",
                        y="Total",
                        title="Bar Chart: Top 10 Four Hitters",
                        labels={"Batter": "Batter", "Four Count": "Number of Fours"},
                        color="Total",  # Color bars based on the count
                        color_continuous_scale=px.colors.sequential.Viridis,
                        text="Total"  # Display count on bars
                    )

                    fig.update_traces(textposition='outside')
                    fig.update_layout(
                        xaxis_title="Batter",
                        yaxis_title="Number of Fours",
                        showlegend=False,
                        template="plotly_white",
                        width=800,
                        height=500
                    )

                    fig.update_xaxes(showgrid=False)
                    fig.update_yaxes(showgrid=False)

                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.write("No data found for top 4 hitters.")

        else :
            if st.sidebar.button("Search"):
                top_hitters_data = db.top_6_hitter()

                if top_hitters_data:
                    df = pd.DataFrame(top_hitters_data, columns=["Batter", "Total"])  # Column names must match the query

                    st.write("### Top 10 Six Hitters")
                    st.dataframe(df)

                    fig = px.bar(
                        df,
                        x="Batter",
                        y="Total",
                        title="Top 10 Six Hitters",
                        labels={"Batter": "Batter", "Total": "Total"},  # More descriptive label
                        color="Total",
                        color_continuous_scale=px.colors.sequential.Plasma,  # Different color scale example
                        text="Total"
                    )

                    fig.update_traces(textposition='outside')
                    fig.update_layout(
                        xaxis_title="Batter",
                        yaxis_title="Number of Sixes",
                        showlegend=False,
                        template="plotly_white",
                        width=800,
                        height=500
                    )

                    fig.update_xaxes(showgrid=False)
                    fig.update_yaxes(showgrid=False)

                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.write("No data found for top 6 hitters.")











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
    team_analysis_choice = st.sidebar.radio("Select Team Analysis", ["Season Winner" ,"Total Run By Teams" ,"Team Against All", "Head To Head"])
    teams = db.fetch_team()
    toss = db.fetch_toss_decision()  # For head-to-head analysis

    if team_analysis_choice == "Season Winner":

        if st.sidebar.button("Search"):
            season_winner = db.season_winners()

            if season_winner:
                df = pd.DataFrame(season_winner,columns=['Seasons','Winner'])

                st.write('### Season Winners')
                st.dataframe(df)

    elif team_analysis_choice == "Total Run By Teams":

        if st.sidebar.button('Search'):
            total_runs_data = db.total_run_by_teams()

            if total_runs_data:  # Check if data is returned from the database
                df = pd.DataFrame(total_runs_data, columns=["Team", "Total Runs"])

                st.write("### Total Runs Scored by Teams")
                st.dataframe(df)

                st.write("### Bar Chart: Total Runs by Teams")
                fig = px.bar(
                    df,
                    x="Team",
                    y="Total Runs",
                    title="Total Runs Scored by Teams",
                    labels={"Team": "Team", "Total Runs": "Total Runs"},
                    text="Total Runs",
                    color="Total Runs",
                    color_continuous_scale=px.colors.sequential.Viridis
                )

                fig.update_traces(textposition='outside')
                fig.update_layout(
                    xaxis_title="Team",
                    yaxis_title="Total Runs",
                    showlegend=False,
                    template="plotly_white",
                    width=800,
                    height=500
                )

                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data found for Total Runs by Teams.")  # Handle empty data case



    elif team_analysis_choice == "Team Against All":
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
