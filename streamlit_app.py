import streamlit as st
import pandas as pd
from mplsoccer import Sbopen
from functions_plot import assists,player, defensive_actions,mistake, pressure_heatmap, transition, pass_cross, shot, passe, passnetwork

parser = Sbopen()
matches = parser.match(competition_id = 1267, season_id = 107)
matches['match'] = matches['home_team_name'] +' vs '+ matches.away_team_name

teams = list(matches.home_team_name.unique())
teams_choice = st.selectbox('Select a Team', teams)

def load_data(teams_choice):
    mask = (matches.home_team_name == teams_choice) | (matches.away_team_name == teams_choice)
    games_selected = matches.loc[mask,['match','match_date','kick_off','home_score','away_score','stadium_name']]

    return games_selected


if teams_choice:
    st.title('Matches Information')
    st.write('This table presents details of the matches played by the Selected Team.')
    games_selected = load_data(teams_choice)
    st.write(games_selected)
else:
    st.write('Please select a team to view match information')


mask_game = (matches.home_team_name == teams_choice) | (matches.away_team_name == teams_choice)
matches = matches[mask_game]
match_list = list(matches['match'])
match_choice = st.sidebar.selectbox('Match',match_list)

plot_options = ['Passing Network','Passes', 'Pressure Heatmap', 'Shots','Crosses','Deffensive Actions','Assists','Player Performance','Mistakes']

selected_plot = st.sidebar.selectbox('Select Plot', plot_options)

if match_choice:
    matchh = matches[matches.match == match_choice]
    match_id = matchh.match_id.unique()
    def event_data(match_choice):
        matchh = matches[matches.match == match_choice]
        match_id = matchh.match_id.unique()
        events = pd.DataFrame()
        for i in matchh['match_id']:
            events = parser.event(i)[0]
        return events

    df = event_data(match_choice)
    df_team_selected = df[df.team_name == teams_choice]

    if selected_plot == 'Assists':
        st.subheader('Assists')
        st.write('This plot shows the assists made by the selected team in the selected match.')
        assists(df_team_selected, teams_choice)

    elif selected_plot == 'Player Performance':
        st.subheader('Player Performance')
        player(df_team_selected)

    elif selected_plot == 'Deffensive Actions':
        st.subheader('Player Performance')
        defensive_actions(df_team_selected)

    elif selected_plot == 'Passing Network':
        st.subheader('Passing Network')
        passnetwork(match_id, teams_choice)

    elif selected_plot == 'Passes':
        st.subheader('Passes')
        passe(df_team_selected, teams_choice)

    elif selected_plot == 'Pressure Heatmap':
        st.subheader('Pressure Map')
        pressure_heatmap(df, teams_choice)

    elif selected_plot == 'Shots':
        st.subheader('Shots')
        shot(df_team_selected)  

    elif selected_plot == 'Crosses':
        st.subheader('Crosses')
        pass_cross(df_team_selected)

    elif selected_plot == 'Mistakes':
        st.subheader('Mistakes')
        mistake(df_team_selected)       



else:
    st.write('Please select a match from Match')